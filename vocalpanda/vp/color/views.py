from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def color(request):
  return render(request, 'color/persnalcolor.html')