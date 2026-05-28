from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


# Create your views here.
# def index(request):
#    return HttpResponse("Hello world!")

# View to see home page.
class HomeView(TemplateView):
    template_name = "attendance/home.html"
