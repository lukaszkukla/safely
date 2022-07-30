from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Hazard


class HazardList(ListView):
    model = Hazard