from json import dumps, loads
from random import random, randint

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import pytz

from datetime import date, datetime
from .models import Entry

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


mood_icons = {0: "fa-sad-cry", 1: "fa-frown", 2: "fa-smile", 3: "fa-laugh-beam"}

activity_icons = {
    "sleep": "fa-bed",
    "hobbies": "fa-guitar",
    "social": "fa-users",
    "health": "fa-medkit",
    "self-improvement": "fa-laugh-beam",
    "food": "fa-hamburger",
    "other": ""
}


class Dashboard(View):
    template_name = 'dashboard.html'

    last_seven = Entry.objects.filter().order_by('-id')[:7]

    weekly_mood = 0
    weekly_moods = []
    weekly_activities = []

    for i in last_seven:
        weekly_mood += i.mood
        weekly_moods += [i.mood]
        weekly_activities += loads(i.activity).keys()

    weekly_activity = max(set(weekly_activities), key=weekly_activities.count)
    weekly_mood = int(weekly_mood / 7)

    weekly_moods = weekly_moods[::-1]
    percentages = []

    for i in range(1, 5):
        percentages.append(weekly_moods.count(i))
    percentages = [int(i / 7 * 100) for i in percentages]

    print(percentages)

    context = {
        'entries': Entry.objects.count(),
        'entry_streak': 4,
        'mood': mood_icons[weekly_mood],
        'activity': weekly_activity,
        'activity_icon': activity_icons[weekly_activity],
        'weekly_moods': weekly_moods,
        'percentages': percentages
    }

    def get(self, request):
        return render(template_name=self.template_name, request=request, context=self.context)

    def post(self, request):
        pass


class Entries(View):
    template_name = 'entries.html'

    def get(self, request):
        return render(template_name=self.template_name, request=request)

    def post(self, request):
        activity_categories = {
            'sleep': ['sleep-early', 'good-sleep', 'medium-sleep', 'bad-sleep'],
            'hobbies': ['movies', 'reading', 'gaming', 'travel'],
            'social': ['family', 'friends', 'date', 'party'],
            'health': ['exercise', 'drink-water', 'walk'],
            'self-improvement': ['meditation', 'kindness', 'breathing-techniques'],
            'food': ['eat-healthy', 'home-made', 'fast-food']
        }

        activity = {}

        for i in request.POST.keys():
            for j in activity_categories.keys():
                if i in activity_categories[j]:
                    try:
                        activity[j] += i
                    except KeyError:
                        activity[j] = [i]

        print(activity)

        # query = Entry.objects.create(
        #     date_added=timezone.now(),                                      # DONE
        #     author=get_object_or_404(User, username=request.user),          # DONE
        #     mood=0,                                                         # TODO
        #     activity=dumps({'health': 'exercise', 'food': 'eat_healthy'}),  # DONE
        #     note="This is a test note"                                      # TODO
        # )

        return redirect('/entries')


class NewEntry(View):
    template_name = 'new_entry.html'

    def get(self, request):
        return render(template_name=self.template_name, request=request)

    def post(self, request):
        pass


def Logout(request):
    logout(request)
    return redirect('/')
