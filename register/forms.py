from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from dashboard.models import Student


class StudentRegistrationForm(forms.Form):
    """Collect student details and create linked User/Student records."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام کاربری"}),
    )
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "رمز عبور"}),
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "تکرار رمز عبور"}),
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام"}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام خانوادگی"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل"}),
    )
    age = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "سن"}),
    )
    gender = forms.ChoiceField(
        choices=Student.GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    phone_number = forms.CharField(
        label="شماره موبایل",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "شماره تماس"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری از قبل ثبت شده است.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل از قبل ثبت شده است.")
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("دانش‌آموزی با این ایمیل ثبت شده است.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "گذرواژه‌ها با هم یکسان نیستند.")
        return cleaned_data

    def save(self):
        User = get_user_model()
        with transaction.atomic():
            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password1"],
                email=self.cleaned_data["email"],
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
            )

            Student.objects.create(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                age=self.cleaned_data["age"],
                phone_number=self.cleaned_data["phone_number"],
                gender=self.cleaned_data["gender"],
                email=self.cleaned_data["email"],
                gpa=Decimal("0.00"),
            )
        return user
