from django import template

from ..models import Student, Teacher

register = template.Library()


@register.filter
def is_teacher(user):
    """Return True if the authenticated user has a teacher profile."""
    if not getattr(user, "is_authenticated", False):
        return False
    try:
        user.teacher
        return True
    except (Teacher.DoesNotExist, AttributeError):
        return False


@register.filter
def is_student(user):
    """Return True if the authenticated user has a student profile."""
    if not getattr(user, "is_authenticated", False):
        return False
    try:
        user.student_profile
        return True
    except (Student.DoesNotExist, AttributeError):
        return False
