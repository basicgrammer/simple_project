from django.db import models
from auth_app.models import *

class Product(models.Model) :

    p_pk_id = models.AutoField(primary_key = True, verbose_name = "기본키(자동 증가)")
    fk_key = models.ForeignKey(Profile, on_delete = models.CASCADE, verbose_name = "외래키 : 자동 할당 번호 (Profile)",db_column = "fk_key")

    ## 카테고리가 정해져있다는 가정하에 CHOCIES를 사용함
    CATEGORY_CHOICES = [
        ("A", "TYPE A"),
        ("B", "TYPE B"),
        ("C", "TYPE C"),
        ("D", "TYPE D")
    ]
    p_category = models.CharField(max_length = 10, choices= CATEGORY_CHOICES, default = CATEGORY_CHOICES[0][0], null=False, verbose_name = "상품 카테고리 종류")

    p_price = models.IntegerField(default = 0, null = False, verbose_name = "상품 가격")
    p_cost =  models.IntegerField(default = 0, null = False, verbose_name = "상품 원가")
    p_name = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")
    p_subscription = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")
    p_barcode = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")
    p_expire_date = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")

    SIZE_CHOICES = [
        ("S", "small"),
        ("L", "large")
    ]
    p_size = models.CharField(max_length = 16, choices=SIZE_CHOICES, default = SIZE_CHOICES[0][0], null = False, verbose_name = "상품 사이즈")
    p_delete_check = models.BooleanField(default = False, null = False, verbose_name = "상품 삭제 여부") # default = False  ( delete => True)
    p_regi_user = models.CharField(max_length = 128, default = '', null = False, verbose_name = "로그인 아이디")
    p_regi_date = models.DateTimeField(auto_now_add = True, null = False, verbose_name = "최초 가입 날짜")
    p_fix_date = models.DateTimeField(auto_now_add = True, null = False, verbose_name = "상품 정보 수정 날짜")
    p_keyword = models.CharField(max_length = 128, default = '', null = False, verbose_name = "상품 초성 키워드")
    # P_regi_username = IntegerField