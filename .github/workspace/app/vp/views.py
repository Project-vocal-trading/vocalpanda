from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

# Create your views here.
def mainpage(request):
  return render(request, 'mainpage/mainpage.html')

def error_404_view(request, exception):
  return HttpResponseNotFound(f'지금 페이지는 없는 페이지입니다.')