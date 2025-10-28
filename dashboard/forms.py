from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Assignment, Course, Exam, Student, Subject, Teacher


class BootstrapFormMixin:
    """Apply Bootstrap classes to form widgets."""

    def _init_bootstrap_widgets(self):
        for field in self.fields.values():
            widget = field.widget
            existing_classes = widget.attrs.get("class", "")
            if isinstance(widget, (forms.CheckboxSelectMultiple, forms.CheckboxInput)):
                widget.attrs["class"] = f"{existing_classes} form-check-input".strip()
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = f"{existing_classes} form-select".strip()
            else:
                widget.attrs["class"] = f"{existing_classes} form-control".strip()


class StudentForm(BootstrapFormMixin, forms.ModelForm):
    """Form for editing student details."""

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "age",
            "phone_number",
            "gender",
            "email",
            "gpa",
            "courses",
        ]
        widgets = {
            "courses": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_widgets()


class ExamForm(BootstrapFormMixin, forms.ModelForm):
    """Create or update exam instances."""

    class Meta:
        model = Exam
        fields = [
            "title",
            "subject",
            "date",
            "type",
            "course",
            "students",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "students": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_widgets()


class AssignmentForm(BootstrapFormMixin, forms.ModelForm):
    """Create or update assignment instances."""

    class Meta:
        model = Assignment
        fields = [
            "title",
            "description",
            "due_date",
            "course",
            "students",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "students": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_widgets()


class CourseForm(BootstrapFormMixin, forms.ModelForm):
    """Create or update course records."""

    class Meta:
        model = Course
        fields = [
            "name",
            "description",
            "subject",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_widgets()


class TeacherRegistrationForm(BootstrapFormMixin, UserCreationForm):
    """Registration form for teachers with additional profile data."""

    age = forms.IntegerField(min_value=0, required=False)
    gender = forms.ChoiceField(choices=Teacher.GENDER_CHOICES, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    gpa = forms.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False,
        min_value=0,
        max_value=4,
    )
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    assigned_students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = Teacher
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "age",
            "gender",
            "phone_number",
            "gpa",
            "subjects",
            "assigned_students",
        )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_widgets()
        self.field_order = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "age",
            "email",
            "gpa",
            "subjects",
            "assigned_students",
        ]
