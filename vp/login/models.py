from django.db import models

class Mem(models.Model):
    memno = models.CharField(primary_key=True, max_length=64, verbose_name='회원 번호, 네이버 api 식별자, 64자 이내로 구성된 BASE64 형식의 문자열')
    memid = models.CharField(max_length=30, verbose_name='이메일(아이디)')
    memname = models.CharField(max_length=30, verbose_name='성명, 10자 이내로 구성된 문자열')
    membirth = models.CharField(max_length=20, verbose_name='출생연도, 연(YYYY) 형태의 문자열')
    memdate = models.DateField(verbose_name='가입일')
    memgender = models.CharField(max_length=10, verbose_name='M/F (남성/여성) 으로 표현된 문자')

    class Meta:
        db_table = 'mem'
        verbose_name = '회원 정보 테이블'
        verbose_name_plural = '회원 정보 테이블'
