from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from dashboard.models import Student, Teacher


class RoleBasedLoginView(LoginView):
    """Redirect users to the appropriate dashboard after authentication."""

    template_name = "login/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def get_success_url(self):
        redirect_url = self.get_redirect_url()
        if redirect_url:
            return redirect_url

        user = self.request.user

        try:
            user.teacher
            return reverse_lazy("dashboard:teacher_dashboard")
        except (Teacher.DoesNotExist, AttributeError):
            pass

        try:
            user.student_profile
            return reverse_lazy("dashboard:student_dashboard")
        except (Student.DoesNotExist, AttributeError):
            pass

        return super().get_success_url()


def logout_view(request):
    """Terminate the user session then redirect home."""
    logout(request)
    return HttpResponseRedirect(reverse("home"))
