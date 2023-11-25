import os
import random
import webcolors
import librosa
import numpy as np
import json
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .predictor import Predictor

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
def result(request):
    if request.method == 'POST':
        audio_data = request.FILES['audio_data']
        filename = audio_data.name
        audio_data.save(filename)  # 서버에 파일 저장

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

        os.remove(filename)

        return render(request, 'persnalcolor_result/persnalcolor_result.html', {'color': closest_name})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
