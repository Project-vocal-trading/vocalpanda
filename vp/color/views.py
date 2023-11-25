from django.shortcuts import render
from vp.decorators import check_session 

# Create your views here.
@check_session  # 데코레이터 적용
def color(request):
    return render(request, 'color/persnalcolor.html')
