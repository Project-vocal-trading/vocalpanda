from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .models import Mem
from datetime import datetime
import requests
from urllib.parse import urlparse

def login(request):
    return render(request, 'login/login.html')

def naver_login(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    redirect_uri = request.build_absolute_uri()

    # 네이버에서 제공하는 access token 요청 URL
    token_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={vTKo54VTlSQklj7PQQcS}&client_secret={RN6GtHjNeU}&redirect_uri={redirect_uri}&code={code}&state={state}"

    # access token 요청
    result = requests.get(urlparse(token_url).geturl()).json()

    # access token을 이용하여 사용자 정보 요청
    profile_url = f"https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {result['access_token']}"}
    profile_result = requests.get(profile_url, headers=headers).json()

    # 사용자 정보 파싱
    memno = profile_result['response']['id']
    memid = profile_result['response']['email']
    memname = profile_result['response']['name']
    memgender = profile_result['response']['gender']
    membirth = profile_result['response']['birthyear']

    # 현재 시간 가져오기
    memdate = datetime.now()

    # Mem 테이블에 사용자 정보가 이미 있는지 확인
    if not Mem.objects.filter(memno=memno).exists():
        # 없다면 Mem 테이블에 사용자 정보 삽입
        user = User.objects.create_user(username=memno, email=memid)
        Mem.objects.create(user=user, memno=memno, memid=memid, memname=memname, memgender=memgender, membirth=membirth, memdate=memdate)

    # 사용자 세션 생성
    user = User.objects.get(username=memno)
    auth_login(request, user)

    return redirect('mypage')
