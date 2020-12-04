from django.shortcuts import render

# Create your views here.
from django.views import View


class Index(View):
    template_name = 'landing.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass
