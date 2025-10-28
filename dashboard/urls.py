from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("signup/", views.TeacherSignupView.as_view(), name="teacher_signup"),
    path("teacher/dashboard/", views.TeacherDashboardView.as_view(), name="teacher_dashboard"),
    path("teacher/students/", views.StudentManagementView.as_view(), name="student_management"),
    path("teacher/students/<int:pk>/edit/", views.EditStudentView.as_view(), name="edit_student"),
    path("teacher/assignments/", views.AssignmentsView.as_view(), name="assignments"),
    path("teacher/exams/", views.ExamsView.as_view(), name="exams"),
    path("teacher/courses/", views.CoursesView.as_view(), name="courses"),
    path("teacher/courses/<int:pk>/edit/", views.CourseUpdateView.as_view(), name="course_edit"),
    path("teacher/courses/<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),
    path("student/dashboard/", views.StudentDashboardView.as_view(), name="student_dashboard"),
]
