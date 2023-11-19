from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def record(request):
  return render(request, 'persnalcolor_record/persnalcolor_record.html')