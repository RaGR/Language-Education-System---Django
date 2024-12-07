from django.db import models
from django.contrib.auth.models import AbstractUser

class Course(models.Model):
    course_code = models.CharField(max_length=3, unique=True)
    course_level = models.CharField(max_length=10)

    class Meta:
        unique_together = ('course_code', 'course_level')

    def __str__(self):
        return f"{self.course_code} {self.course_level}"

class User(AbstractUser):
    # Additional fields for all user types
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)

    # National ID field for all user types
    national_id = models.CharField(max_length=20, unique=True)

    # User type field
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('supervisor', 'Supervisor')])

    # Specific fields for students
    courses = models.ManyToManyField('Course', related_name='students')  # Assuming you have a Course model

    # Specific fields for teachers
    courses_taught = models.ManyToManyField('Course', related_name='teachers')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'