from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def persnalcolor_result(request):
  return render(request, 'persnalcolor_result/persnalcolor_result.html')