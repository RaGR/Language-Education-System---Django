from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import StudentRegistrationForm


def register(request):
    if request.user.is_authenticated:
        messages.info(request, "شما قبلاً وارد شده‌اید.")
        return redirect("home")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ثبت‌نام با موفقیت انجام شد. لطفا وارد شوید.")
            return redirect("login")
    else:
        form = StudentRegistrationForm()

    return render(request, "register.html", {"form": form})
