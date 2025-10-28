from django.contrib import admin

from .models import Assignment, Course, Exam, Schedule, Student, Subject, Teacher


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "created_by")
    list_filter = ("subject", "created_by")
    search_fields = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "gender", "gpa")
    list_filter = ("gender", "courses")
    search_fields = ("first_name", "last_name", "email")
    filter_horizontal = ("courses",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "age", "gender", "gpa")
    list_filter = ("gender", "subjects")
    search_fields = ("username", "first_name", "last_name", "email")
    filter_horizontal = ("subjects", "assigned_students")


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "date", "type")
    list_filter = ("type", "course")
    search_fields = ("title", "subject")
    filter_horizontal = ("students",)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "due_date")
    list_filter = ("course",)
    search_fields = ("title",)
    filter_horizontal = ("students",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("course", "day", "start_time", "end_time", "teacher")
    list_filter = ("day", "teacher")
