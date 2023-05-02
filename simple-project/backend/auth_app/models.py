from django.db import models

# from django.contrib.auth.models import AbstractUser	# AbstractUser 불러오기

## 유저 등록시 휴대폰번호 + 비밀번호 입력을 통해 회원가입이 진행되므로 나머지 정보들은 모두 쓰지 않는다.
class Profile(models.Model) :

    profile_pk_id = models.AutoField(primary_key = True, verbose_name = "기본키(자동 증가)")
    user_id = models.CharField(max_length = 128, default = '', null = False, verbose_name = "유저 ID (휴대폰 번호 사용)")
    user_pw = models.CharField(max_length = 256, default = '', null = False, verbose_name = "유저 PW (암호화 저장 - 단방향 해시)")
    # user_nickname = models.CharField(max_length = 200, default = '', null = False, verbose_name = "유저 닉네임") ## 초기 닉네임은 user_id와 동일하게 구성
    phone_num = models.CharField(max_length = 30, default = '', null = False, verbose_name = "유저 휴대폰 번호 : 유저 ID와 동일하게 사용")
    ## refresh_token 정보가 없는 경우 해당 유저는 로그인 되지 않은것으로 판단하면 됨
    # refresh_token = models.CharField(max_length = 256, default = '', null = False, verbose_name = "유저에게 할당된 refresh_token")
    last_login = models.DateTimeField(null = True, verbose_name  = "마지막 로그인 날짜")
    regi_date = models.DateTimeField(auto_now_add = True, null = False, verbose_name = "최초 가입 날짜")


class Token(models.Model) :
    
    token_pk_id = models.AutoField(primary_key = True, verbose_name = "기본키(자동 증가)")
    relation_id = models.OneToOneField(Profile, on_delete = models.CASCADE, db_column = "relation_id")
    refresh_token = models.CharField(max_length = 256, default = '', null = False, verbose_name = "유저에게 발급된 rfresh_token 저장")
    


# class product(models.Model) :

#     p_pk_id = models.AutoField(primary_key = True, verbose_name = "기본키(자동 증가)")

#     ## 카테고리가 정해져있다는 가정하에 CHOCIES를 사용함
#     CATEGORY_CHOICES = [
#         ("A", "TYPE A"),
#         ("B", "TYPE B"),
#         ("C", "TYPE C"),
#         ("D", "TYPE D")
#     ]
#     p_category = models.CharField(max_length = 10, choices= CATEGORY_CHOICES, default = CATEGORY_CHOICES[0][0], verbose_name = "상품 카테고리 종류")

#     p_price = models.IntegerField(default = 0, null = False, verbose_name = "상품 가격")
#     p_cost =  models.IntegerField(default = 0, null = False, verbose_name = "상품 원가")
#     p_name = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")
#     p_subscription = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")
#     p_barcode = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")
#     p_expire_date = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")
#     p_size = models.CharField(max_length = 128, default = '',  null = False, verbose_name = "상품 이름")
#     p_delete_check = models.BooleanField(default = False, null = False, verbose_name = "상품 삭제 여부") # default = False  ( delete => True)
#     p_regi_user = models.CharField(max_length = 128, default = '', null = False, verbose_name = "로그인 아이디")
#     p_regi_date = models.DateTimeField(auto_now_add = True, null = False, verbose_name = "최초 가입 날짜")
#     p_fix_date = models.DateTimeField(auto_now_add = True, null = False, verbose_name = "상품 정보 수정 날짜")
    # P_regi_username = IntegerField


# class product_fix_history(models.Model) :

#     h_pk_id = models.AutoField(primary_key = True, verbose_name = "기본키 (자동 증가)")
#     fk_product = models.ForeignKey(product, on_delete = models.CASCADE, verbose_name = "외래키 (product table)", db_column = "fk_product")






# class Manuscript(models.Model): # 원고
#     title = models.CharField(max_length = 100) # 제목 ex) 나이트 소드 1
#     origin_name = models.CharField(max_length = 100, null = True) # 제목 나이트 소드 // 프로젝트 이름
#     # user_id = models.ForeignKey('UserProfile', null = True, on_delete=models.SET_NULL)
#     user_id = models.CharField(max_length = 100, null = True)
#     create_date = models.DateTimeField(null = True, auto_now_add = True)
#     content = models.JSONField(default = dict)
#     GENRE_CHOICES = [
#         ('NO', 'NO'),
#         ('FA', 'Fantasy'),
#         ('MA', 'Martial arts'),
#         ('RO', 'Romance'),
#     ]
#     genre = models.CharField(max_length = 10, choices = GENRE_CHOICES, default = GENRE_CHOICES[0][0])
#     pub = models.BooleanField(default = True)
#     order = models.IntegerField(default = 0) # 1편, 2편
#     cover_img = models.CharField(max_length = 100, null = True)

#     # def order_save(self, *args, **kwargs):
#     #     obj = Manuscript.objects.filter(origin_name = self.origin_name).order_by('-id')[0]
#     #     if obj: 
#     #         self.order = obj.order + 1

#     #     super().save()

# class File(models.Model):
#     file_name = models.CharField(max_length = 200)
#     file_path = models.CharField(max_length = 200)
#     file_type = models.CharField(max_length = 200)
    
# '''
#     임시용

#     1. router-link 클릭 -> 최근 작업 클릭시 툴로 이동
#     2. 툴로 이동하면 클릭한 정보 가져오기
#     3. 배치 수정
# '''