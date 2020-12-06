from json import dumps, loads
from random import random, randint, choice

import re

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import pytz

from datetime import date, datetime

from lorem import paragraph

from .models import Entry

# Create your views here.
from django.views import View


def mobile(request):
    mobile_agent = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)

    if mobile_agent.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


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


mood_icons = {1: "fa-sad-cry", 2: "fa-frown", 3: "fa-smile", 4: "fa-laugh-beam"}

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

    def get(self, request):

        last_seven = Entry.objects.filter(author=get_object_or_404(User, username=request.user)).order_by('-id')[:7]

        if len(last_seven) != 0:

            weekly_mood = 0
            weekly_moods = []
            weekly_activities = []

            for i in last_seven:
                weekly_mood += i.mood
                weekly_moods += [i.mood]
                weekly_activities += loads(i.activity).keys()

            weekly_activity = max(set(weekly_activities), key=weekly_activities.count)

            weekly_moods = weekly_moods[::-1]
            percentages = []

            for i in range(1, 5):
                percentages.append(weekly_moods.count(i))
            percentages = [int(i / 7 * 100) for i in percentages]

            weekly_mood = percentages.index(max(percentages)) + 1

            context = {
                'entries': Entry.objects.count(),
                'entry_streak': 4,
                'mood': mood_icons[weekly_mood],
                'activity': weekly_activity,
                'activity_icon': activity_icons[weekly_activity.lower()],
                'weekly_moods': weekly_moods,
                'percentages': percentages
            }
        else:
            context = {
                'entries': 0,
                'entry_streak': 0,
                'mood': None,
                'activity': None,
                'activity_icon': None,
                'weekly_moods': [],
                'percentages': []
            }

        return render(template_name=self.template_name, request=request, context=context)


class Entries(View):
    template_name = ""

    def get(self, request):

        if mobile(request):
            self.template_name = 'entries-mobile.html'
        else:
            self.template_name = 'entries-desktop.html'

        all_entries = Entry.objects.filter(author=get_object_or_404(User, username=request.user)).order_by('-id')

        entries = []
        for i in all_entries:
            entries.append({
                'id': i.id,
                'mood': {1: 'very sad', 2: 'sad', 3: 'happy', 4: 'very happy'}[i.mood],
                'date': i.date_added.strftime("%-d %B %Y")
            })

        return render(template_name=self.template_name, request=request, context={'entries': entries})

    def post(self, request):
        activity_categories = [
            "Sleep", "Hobbies", "Social", "Health", "Self-improvement", "Food", "Other"
        ]
        activity = {}

        for i in request.POST.keys():
            if i in activity_categories:
                try:
                    activity += i
                except KeyError:
                    activity = [i]

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


class Radio(View):
    template_name = 'radio.html'
    songs = [

        "https://www.youtube.com/embed/neV3EPgvZ3g",
        "https://www.youtube.com/embed/2v5iWf2KDCw",
        "https://www.youtube.com/embed/2v5iWf2KDCw",
        "https://www.youtube.com/embed/qvUWA45GOMg",
        "https://www.youtube.com/embed/rJlY1uKL87k",
        "https://www.youtube.com/embed/GdzrrWA8e7A",
    ]

    def get(self, request):

        weekly_mood = 0
        last_seven = Entry.objects.filter(author=get_object_or_404(User, username=request.user)).order_by('-id')[:7]

        for i in last_seven:
            weekly_mood += i.mood

        weekly_mood = int(weekly_mood / 7)

        if weekly_mood >= 2:
            with open("static/text/happy.txt", 'r') as f:
                quote_list = f.readlines()
        else:
            with open("static/text/sad.txt", 'r') as f:
                quote_list = f.readline()

        return render(template_name=self.template_name, request=request, context={
            'music_link': choice(self.songs),
            'motivational_text': choice(quote_list),
            'mobile': mobile(request)
        })


class Replier(View):

    def get(self, request, reply_id):
        categories = ""
        entry = Entry.objects.filter(id=reply_id)[0]

        for i in loads(entry.activity).keys():
            categories = categories + i + " "

        response = f'''<div class="box message-preview">
                            <div class="top">
                                <div class="avatar"><i class="fas {mood_icons[entry.mood]} fa-3x"></i></div>
                                <div class="address">
                                    <div class="name">{entry.date_added.strftime("%-d %B %Y")}</div>
                                    <div class="email">{categories}</div>
                                </div>
                                <hr>
                                <div class="content"><p>
                                    {entry.note}
                                </p></div>
                            </div>
                        </div>'''
        return HttpResponse(response)


class Fill_DB(View):
    def get(selfs, request):
        days = [
            date.fromisoformat("2020-12-01"),
            date.fromisoformat("2020-12-02"),
            date.fromisoformat("2020-12-03"),
            date.fromisoformat("2020-12-04"),
            date.fromisoformat("2020-12-05"),
            date.fromisoformat("2020-12-06"),
            date.fromisoformat("2020-12-07"),
        ]

        activity_categories = [
            "Sleep", "Hobbies", "Social", "Health", "Self-improvement", "Food", "Other"
        ]

        for index, date_elem in enumerate(days):
            query = Entry.objects.create(
                date_added=datetime(year=date_elem.year, month=date_elem.month, day=date_elem.day),
                author=get_object_or_404(User, username=request.user),
                mood=randint(2, 4),
                activity=dumps({f'{choice(activity_categories)}': 'a', f'{choice(activity_categories)}': 'a'}),
                note=f"{paragraph()} \n \n {paragraph()}"
            )
        query.save()

        return redirect("/dashboard")


def Logout(request):
    logout(request)
    return redirect('/')
