import os
import random
import webcolors
import librosa
import numpy as np
import json
import matplotlib.pyplot as plt
import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vp.decorators import check_session

from .models import Voice
from login.models import Mem
from .predictor import Predictor

@check_session
def persnalcolor_result(request):
    return render(request, 'persnalcolor_result/persnalcolor_result.html')

def closest_color(requested_color):
    min_colors = {}
    for hex, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

@csrf_exempt
@check_session
def result(request):
    if request.method == 'POST':
        audio_data = request.FILES['audio_data']
        filename = audio_data.name

        y, sr = librosa.load(filename)

        rms = librosa.feature.rms(y=y)[0]
        rms = (rms - np.min(rms)) / (np.max(rms) - np.min(rms))
        
        rms_json = json.dumps(rms.tolist())

        if 'M' in filename:
            gender = 'M'
        elif 'F' in filename:
            gender = 'F'
        else:
            gender = 'Unknown'

        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitches = pitches[magnitudes > np.median(magnitudes)]
        pitch = pitches[0] if len(pitches) > 0 else 0

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        intensity = np.sum(magnitudes)

        r = int((pitch / sr) * 10500)
        g = 255 - r
        b = int((intensity / (np.max(magnitudes) * 280)) * 255)

        if gender == 'F':
            r, g, b = r + random.randint(20, 150), g + random.randint(-40, 90) , b + random.randint(-90, 30)
        elif gender == 'M':
            r, g, b = r + random.randint(-50, 30), g + random.randint(-70, 30), b + random.randint(0, 120)

        r, g, b = max(min(r, 255), 0), max(min(g, 255), 0), max(min(b, 255), 0)

        color = (r, g, b)
        closest_name = closest_color(color)

        plt.figure(figsize=(2,2))
        plt.imshow([[color]])
        plt.axis('off')
        plt.savefig('color.png')  # 색상 이미지를 파일로 저장

        predictor = Predictor()
        emo_label = predictor.predict(filename)

        # Voice 인스턴스 생성
        voice = Voice()
        
        # voiceno는 1부터 1씩 증가하게 설정
        # 이를 위해 voice 테이블의 마지막 voiceno를 찾아 1을 더함
        last_voice = Voice.objects.order_by('-voiceno').first()
        if last_voice is None:
            voice.voiceno = 1
        else:
            voice.voiceno = last_voice.voiceno + 1
        
        # memno는 세션에서 가져옴
        voice.memno = request.session.get('memno')

        # vtextno는 이전 페이지로부터 전달 받음
        # 이 코드는 vtextno를 전달받는 방법에 따라 수정해야 함
        voice.vtextno = request.POST.get('vtextno')

        # birth는 mem 테이블의 memno와 같은 대상의 membirth를 넣음
        # mem 테이블에서 memno에 해당하는 회원을 찾아 birth에 할당
        mem = Mem.objects.get(memno=voice.memno)
        voice.birth = mem.membirth

        # gender는 mem 테이블의 memno와 같은 대상의 memgender를 넣음
        voice.gender = mem.memgender

        # emotion은 해당 페이지에서 감정 추정을 한 결과를 넣음
        voice.emotion = emo_label

        # intensity는 해당 페이지에서 강도 값 계산 함수를 실행한 결과를 넣음
        voice.intensity = intensity

        # voicename은 (현재 년도 - membirth)_gender_emotion.wav로 지정
        current_year = datetime.datetime.now().year
        voice.voicename = f"{current_year - int(voice.birth)}_{voice.gender}_{voice.emotion}.wav"

        # voice 인스턴스 저장
        voice.save()
        
        # 파일 이름 변경
        os.rename(filename, voice.voicename)

        return render(request, 'persnalcolor_result/persnalcolor_result.html', {'color': closest_name})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
