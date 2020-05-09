from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..models import User


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if User.objects.get(username=request.user).is_teacher:
            return redirect('teachers:quiz_change_list')
        elif User.objects.get(username=request.user).is_student:
            return redirect('students:quiz_list')
        else:
            return redirect('admin:index')
    return render(request, 'main/home.html')


