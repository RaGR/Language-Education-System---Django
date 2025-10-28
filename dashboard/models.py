from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    """Academic subject offered by the academy."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    """Course entity that students can enrol in."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    """Student records stored in the dashboard."""
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    courses = models.ManyToManyField(Course, related_name="students", blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Teacher(User):
    """Teacher profile extending Django's built-in User."""
    subjects = models.ManyToManyField(Subject, related_name="teachers", blank=True)
    assigned_students = models.ManyToManyField(
        Student,
        related_name="assigned_teachers",
        blank=True,
    )

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self) -> str:
        return self.get_full_name() or self.username


class Exam(models.Model):
    """Exam scheduled for a course."""
    MIDTERM = "midterm"
    FINAL = "final"
    TYPE_CHOICES = [
        (MIDTERM, "Midterm"),
        (FINAL, "Final"),
    ]

    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    assigned_by = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="exams",
    )
    students = models.ManyToManyField(Student, related_name="exams", blank=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.course}"


class Assignment(models.Model):
    """Assignments linked to courses."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    assigned_by = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    students = models.ManyToManyField(Student, related_name="assignments", blank=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.course}"


class Schedule(models.Model):
    """Course schedule entries."""
    DAY_CHOICES = [
        ("saturday", "Saturday"),
        ("sunday", "Sunday"),
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="schedules",
    )

    def __str__(self) -> str:
        return f"{self.course} - {self.day}"
