from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User, Permission
from django.views.generic import UpdateView, CreateView
from wms.forms import UserForm


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', {'info': 'logowanie'})


class UserUpdateView(UpdateView):
    form_class = UserForm
    model = User
    template_name = "permission.html"

    def get_success_url(self):
        return reverse_lazy("permission", args=(self.object.id,))


class CreateUserView(CreateView):

    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "permission.html"


def index(request):
    return render(request, 'index.html')