from django.db import models

class Vtext(models.Model):
    vtextno = models.IntegerField(primary_key=True, verbose_name='스크립트 번호')
    vtextcon = models.CharField(max_length=2000, verbose_name='스크립트 내용')

    class Meta:
        db_table = 'vtext'
        verbose_name = '스크립트'
        verbose_name_plural = '스크립트'
        
class Voice(models.Model):
    voiceno = models.IntegerField(primary_key=True, verbose_name='음성 번호')
    memno = models.CharField(max_length=64, verbose_name='회원 번호')
    vtextno = models.ForeignKey(Vtext, on_delete=models.CASCADE, verbose_name='스크립트 번호')
    voicename = models.CharField(max_length=100, verbose_name='음성 저장 파일명')
    birth = models.CharField(max_length=20, verbose_name='출생연도')
    gender = models.CharField(max_length=10, verbose_name='성별')
    emotion = models.CharField(max_length=100, verbose_name='감정')
    intensity = models.CharField(max_length=100, verbose_name='프레임별 강도')

    class Meta:
        db_table = 'voice'
        verbose_name = '음성 정보'
        verbose_name_plural = '음성 정보'
