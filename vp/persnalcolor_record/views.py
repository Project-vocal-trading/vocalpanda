from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vp.decorators import check_session  
from .models import Vtext  # 'Vtext'는 vtext 테이블의 모델 이름이라 가정
import random
import os

@check_session  
def record(request):
    return render(request, 'persnalcolor_record/persnalcolor_record.html')

@csrf_exempt
@check_session  
def save_recording(request):
    if request.method == 'POST':
        audio_data = request.FILES['audio_data']
        base_name = os.path.splitext(audio_data.name)[0]  # 확장자를 제거한 파일 이름
        audio_file = os.path.join('D:\\vp-logic\\record_file', f'{base_name}.wav')  # 확장자를 .wav로 변경

        with open(audio_file, 'wb+') as destination:
            for chunk in audio_data.chunks():
                destination.write(chunk)

        return JsonResponse({'message': 'Recording saved successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@check_session 
def get_random_script_for_recording(request):
    vtext_count = Vtext.objects.count()
    random_index = random.randint(0, vtext_count - 1)
    random_vtext = Vtext.objects.all()[random_index]
    return render(request, 'persnalcolor_record.html', { 'vtext': random_vtext }) 
