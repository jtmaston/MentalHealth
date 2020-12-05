from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View


class Index(View):
    template_name = 'landing.html'
    success_url = '/dashboard'
    failure_url = '/#signup'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['addr']
        username = request.POST['usr']
        password = request.POST['pwd']
        if not email or not username or not password:
            return redirect(self.failure_url)
        if password != request.POST['pwd_r']:
            messages.error(request, 'Passwords do not match!')
            return redirect(self.failure_url)
        try:
            get_object_or_404(User, username=username)
        except Http404:
            try:
                get_object_or_404(User, email=email)
            except Http404:
                u = User.objects.create_user(username, email, password)
                u.save()
                login(request, u)
                return redirect(self.success_url)
            else:
                messages.error(request, "Email address is taken!")
                return redirect(self.failure_url)
        else:
            messages.error(request, "Username already exists!")
            return redirect(self.failure_url)


class Login(View):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/dashboard/'
    failure_url = '/login'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, template_name=self.template_name)
        else:
            messages.warning(request, 'You are already logged in!')
            return redirect(self.success_url)

    def post(self, request):
        username = request.POST['usr']
        password = request.POST['pwd']

        try:
            username = get_object_or_404(User, email=username)
        except Http404:
            pass

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(self.success_url)
        else:
            messages.error(request, 'Username or password incorrect!')
            return redirect(self.failure_url)


class Dashboard(View):

    template_name = 'dashboard.html'

    def get(self, request):
        return render(template_name=self.template_name, request=request)

    def post(self, request):
        pass

class Entries(View):

    template_name = 'entries.html'

    def get(self, request):
        return render(template_name=self.template_name, request=request)

    def post(self, request):
        pass

class New_entry(View):

    template_name = 'new_entry.html'

    def get(self, request):
        return render(template_name=self.template_name, request=request)

    def post(self, request):
        pass

def Logout(request):
    logout(request)
    return redirect('/')
