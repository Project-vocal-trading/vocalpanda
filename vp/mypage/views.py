from django.shortcuts import render, redirect
from django.contrib.auth import logout
from requests import request
from vp.decorators import check_session

from persnalcolor_record.models import Voice

@check_session
def mypage(request):
    memno = request.session.get('memno')
    voices = Voice.objects.filter(memno=memno)
    return render(request, 'mypage/mypage.html', {'voices': voices})

def logout_view(request):
    logout(request)
    return redirect('mainpage')