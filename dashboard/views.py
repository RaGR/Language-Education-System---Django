from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import DeleteView

from .forms import AssignmentForm, CourseForm, ExamForm, StudentForm, TeacherRegistrationForm
from .models import Assignment, Course, Exam, Schedule, Student, Teacher


class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Ensure the current user has a teacher profile."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        try:
            user.teacher
            return True
        except (Teacher.DoesNotExist, AttributeError):
            return False

    def handle_no_permission(self):
        user = self.request.user
        if user.is_authenticated:
            try:
                user.student_profile
                return redirect("dashboard:student_dashboard")
            except (Student.DoesNotExist, AttributeError):
                pass
            return redirect("home")
        return super().handle_no_permission()


class StudentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict access to authenticated users with a student profile."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        try:
            user.student_profile
            return True
        except (Student.DoesNotExist, AttributeError):
            return False

    def handle_no_permission(self):
        user = self.request.user
        if user.is_authenticated:
            try:
                user.teacher
                return redirect("dashboard:teacher_dashboard")
            except (Teacher.DoesNotExist, AttributeError):
                pass
            return redirect("home")
        return super().handle_no_permission()


class TeacherDashboardView(TeacherRequiredMixin, TemplateView):
    """Main dashboard for teachers with quick access to management features."""

    template_name = "dashboard/teacher_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher: Teacher = self.request.user.teacher
        context["students_managed"] = teacher.assigned_students.all()
        context["courses"] = Course.objects.all()
        context["assignments"] = Assignment.objects.filter(assigned_by=teacher).order_by("due_date")[:5]
        context["exams"] = Exam.objects.filter(assigned_by=teacher).order_by("date")[:5]
        context["schedules"] = Schedule.objects.filter(teacher=teacher).order_by("day", "start_time")
        return context


class StudentManagementView(TeacherRequiredMixin, ListView):
    """List students with ability to jump to edit view."""

    template_name = "dashboard/student_management.html"
    context_object_name = "students"
    model = Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()
        return context


class EditStudentView(TeacherRequiredMixin, UpdateView):
    """Allow teachers to edit student information."""

    model = Student
    form_class = StudentForm
    template_name = "dashboard/edit_student.html"
    success_url = reverse_lazy("dashboard:student_management")


class ExamsView(TeacherRequiredMixin, CreateView):
    """List and create exams."""

    form_class = ExamForm
    template_name = "dashboard/exams.html"
    success_url = reverse_lazy("dashboard:exams")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher: Teacher = self.request.user.teacher
        context["upcoming_exams"] = Exam.objects.filter(
            assigned_by=teacher,
            date__gte=date.today(),
        ).order_by("date")
        context["past_exams"] = Exam.objects.filter(
            assigned_by=teacher,
            date__lt=date.today(),
        ).order_by("-date")
        return context

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user.teacher
        response = super().form_valid(form)
        form.save_m2m()
        return response


class AssignmentsView(TeacherRequiredMixin, CreateView):
    """List and create assignments."""

    form_class = AssignmentForm
    template_name = "dashboard/assignments.html"
    success_url = reverse_lazy("dashboard:assignments")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher: Teacher = self.request.user.teacher
        context["assignments"] = Assignment.objects.filter(
            assigned_by=teacher,
        ).order_by("due_date")
        return context

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user.teacher
        response = super().form_valid(form)
        form.save_m2m()
        return response


class CoursesView(TeacherRequiredMixin, CreateView):
    """List and create courses."""

    form_class = CourseForm
    template_name = "dashboard/courses.html"
    success_url = reverse_lazy("dashboard:courses")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher: Teacher = self.request.user.teacher
        context["courses"] = Course.objects.filter(created_by=teacher).select_related("subject")
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user.teacher
        messages.success(self.request, "دوره با موفقیت ایجاد شد.")
        return super().form_valid(form)


class CourseUpdateView(TeacherRequiredMixin, UpdateView):
    """Edit an existing course."""

    model = Course
    form_class = CourseForm
    template_name = "dashboard/course_form.html"
    success_url = reverse_lazy("dashboard:courses")

    def get_queryset(self):
        teacher: Teacher = self.request.user.teacher
        return Course.objects.filter(created_by=teacher)

    def form_valid(self, form):
        messages.success(self.request, "دوره با موفقیت بروزرسانی شد.")
        return super().form_valid(form)


class CourseDeleteView(TeacherRequiredMixin, DeleteView):
    """Remove a course designed by the teacher."""

    model = Course
    template_name = "dashboard/course_confirm_delete.html"
    success_url = reverse_lazy("dashboard:courses")

    def get_queryset(self):
        teacher: Teacher = self.request.user.teacher
        return Course.objects.filter(created_by=teacher)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "دوره حذف شد.")
        return super().delete(request, *args, **kwargs)


class StudentDashboardView(StudentRequiredMixin, TemplateView):
    """Provide students with a personal dashboard."""

    template_name = "dashboard/student_dashboard.html"

    def get_student(self):
        if hasattr(self.request.user, "student_profile"):
            return self.request.user.student_profile
        return get_object_or_404(Student, email=self.request.user.email)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_student()
        context["student"] = student
        context["upcoming_exams"] = student.exams.filter(date__gte=date.today()).order_by("date")
        context["assignments"] = student.assignments.filter(due_date__gte=date.today()).order_by("due_date")
        context["schedules"] = Schedule.objects.filter(course__in=student.courses.all()).order_by("day", "start_time")
        context["average_gpa"] = student.gpa
        context["courses"] = student.courses.all()
        return context


class TeacherSignupView(CreateView):
    """Allow new teachers to register."""

    form_class = TeacherRegistrationForm
    template_name = "dashboard/teacher_signup.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                request.user.teacher
                return redirect("dashboard:teacher_dashboard")
            except (Teacher.DoesNotExist, AttributeError):
                try:
                    request.user.student_profile
                    return redirect("dashboard:student_dashboard")
                except (Student.DoesNotExist, AttributeError):
                    return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save_m2m()
        return response
