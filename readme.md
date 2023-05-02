### Simple Project Readme

-----

#### 개발 사양

- OS : Ubuntu 22.04 LTS
- CPU : vCPU 4
- Memory : 8G
- Disk : 250G
- docker engine version : Docker version 23.0.3, build 3e7cbfd
- docker-compose version : Docker Compose version v2.13.0

-----

#### 참고사항
- 원활한 테스트를 위해서 SECRET_KEY 및 암호들에 대한 참조 파일 및 설정 파일을 첨부했습니다.
- 구동 테스트 시 docker 및 docker-compose가 필요합니다.
----

#### 개발 프레임워크 및 DB

- Backend : Django 4.1.1 + ninja library
- Database : Mysql 5.7

-----

#### API Docs (Swagger)

- http://{url}/api/docs

----

#### Port Mapping

- 80 (django)  [ 개발 환경 : runserver | 프로덕션 환경 : Gunicorn ]
- 3306(mysql)

-----

#### 컨테이너 기동

```shell
# docker-compose.yml 파일이 있는 위치에서 해당 명령을 실행할 것

# 신규 이미지 생성을 하지 않고 빌드하는 경우
$ sudo docker-compose up --build -d

# 신규 이미지 생성 + 빌드하는 경우
$ sudo docker-compose up --build -d --force-recreate
```

#### 컨테이너 기동 중지 및 일시 정지

```shell
# docker-compose.yml에 명시된 모든 컨테이너의 기동을 중단 하는 경우
$ sudo docker-compose down

# 일정 컨테이너만을 일시 정지하는 경우
$ sudo docker-compose stop {container_name}
```

#### 컨테이너 로그 확인

```shell
# 로그 기록 모니터링
$ sudo docker logs {container_name}

# 지속적인 로그 기록 모니터링
$ sudo docker logs --tail 1000 -f {container_name}
```

#### 컨테이너 내부 접속

```shell
# django
$ sudo docker exec -it {container_name} /bin/bash

# mysql
$ sudo docker exec -it {container_name} /bin/bash
```

#### docker-compose 명세 보기

```shell
$ sudo docker-compose config
```

#### 컨테이너 자원 활용 모니터링ß

```shell
$ sudo docker stats
```

-----





- ninja 라이브러리란?
  - django 프레임워크에서 동작하는 서드파티 패키지, Fast API에 영향을 받았으며, Fast API와 같은 구문을 사용하는것이 특징

- DRF vs Django + ninja
  - RESTful API 구축을 위한 프레임워크라는 부분에서는 유사함
  - DRF에서 제공하는 유효성 검사보다 ninja에서 제공하는 pydanic 기반의 유효성 검사가 더 빠른 특성을 보여줌
  - DRF가 더욱 큰 커뮤니티를 보유하고 있기에 압도적인 사용량을 보여준다고 생각했으나, piptrends.com에서 검색해보면 ninja가 의외로 선전하는 모습을 보임

- DRF 대신 django + ninja 
  - ninja를 알게된 경로는 DRF가 아닌 django로 개발된 프로젝트에서 속도 개선 및 기존 ORM 활용을 통해 RESTful API를 개발하기 위해 리서칭 과정 중 알게된 라이브러리
  - ninja의 단점 중 꼽히는 기본 제공 기능 외에는 모든 기능을 개발해야하므로, 생산성에 떨어진다는 단점이 있다고 하지만, 필요한 기능을 개발하는 부분은 문제가 되지 않으므로 사용함
  - 과거 인공지능 추론 시스템을 활용한 보조 기능 개발 과정에서 Fast API의 경량화 및 기본 기능 제공에 대한 이점을 파악한 것이 선택하는 과정에 한몫함
  - 기본 Swagger 탑재 덕분에 빠르게 개발하는 과정에서 편리하는 장점들이 많았음

```shell
# requirements.txt 
Django==4.1.1
django-ninja
gunicorn
mysqlclient
requests
bcrypt
orjson
jamo
django-ninja-jwt
six
```



#### 고려사항

- JWT 인증 처리 시 Exception Error에 대한 Message Custom --> 해당 문제에 대한 답을 찾지 못한 상황, 커스텀 작업이 필요할 것으로 생각됨
- Mysql 엔진 타입 선정
  - Mysql에서 지원하는 엔진 타입은 InnoDB와 MyISAM 2가지가 존재
  - InnoDB는 빈번한 쓰기, 수정, 삭제가 발생하는 경우에 유리하다고함
  - MyISAM은 주로 읽기 위주의 처리에 높은 성능을 발휘한다고 한다.
  - 카페 같은곳에서 활용되는 DB라면 평상시 장사를 하는 시간에는 읽기 위주의 처리에 좋은 MyISAM 엔진 타입을, 유지보수 같은 관리 작업을 진행하는 경우에는 InnoDB 엔진 타입을 스위칭하면서 사용하는것이 더 좋지 않을까 고민된다.
  - 현재는 개발이 진행되는 과정이며 읽기, 쓰기, 수정, 삭제 등 다양한 처리가 일어나기 때문에 InnoDB로 엔진을 사용하는 중

-----

#### PUT vs PATCH

- 과거 프로젝트에서는 HTTP Method를 용도에 맞지 않게 사용했었던적이 있었으나, 이번 기회에 확실하게 정의해서 사용하고 가려고 한다.

- PUT : 자원 전체의 교체 (자원의 모든 필드가 필요), 없는 경우 새롭게 생성
- PATCH : 자원의 부분 교체 (자원의 일부 필드가 필요)

- Update를 위해 PATCH를 선택하는 것이 자원을 아끼는 방식이라고 생각되어 수정에 관련된 API는 PATCH Method를 사용하고 있음

----

#### Testcase 사용

- 과거 프로젝트부터 Testcase 같은 테스트 방식을 주 방식으로 사용하지 않았었던 이유는, 컨테이너를 기반으로 테스트 및 개발을 진행했기 때문에 사용하는 목적 및 방법 터득이 난해했었다.

----

#### 키워드 검색 및 초성 검색 구현

- 키워드로 검색하는 경우 초성 검색을 할 수 없는 부분을 생각했을때, 검색할때마다 해당 테이블의 상품 이름을 초성으로 변환하는 과정은 매번 검색마다 작업이 수행되므로, 비효율적이라고 판단.
- 상품 등록 시 키워드를 초성으로 변환하여, 테이블에 저장하는 방식으로 초성 검색을 구현함

----

#### cursor based pagination 

- 생소한 페이지네이션 방식이었으나, 구현 원리가 어렵지 않기에 구현 처리를 완료

--------

#### 로깅 기능

- 프로젝트에서 로깅 기능을 넣었으면 더 좋았겠지만, 기능 구현에 할애된 시간때문에 여유가 된다면 로깅 기능을 넣어야한다.

----

#### JWT 토큰 검사

- 본인이 고려한 JWT 토큰 검사 방식 -> 데코레이터로 선언하여 JWT 토큰 유효성을 검사하는 방식,
- Django-ninja에서 지원하는 GlobalAuth를 활용하여 JWT 토큰 검사를 활용하는 방식이 더 깔끔하게 개발할 수 있어서 GlobalAuth로 JWT 기반으로 권한 제어를 수행함

------





#### API 관련 설명 및  호출 기능 예시

- BASE URL : /api
- auth_app URL : /autth
- platform_app URL : /plat

- 호출 경로 (auth_app인 경우) : /api/auth/...
- 호출 경로 (platform_app인 경우) : /api/plat/....

- API 테스트를 위해서는 Swagger (/api/docs)로 접근해서 테스트 할 수 있습니다.

- 등록된 Swagger을 활용하는 경우 = http://{url}/api/docs 

  

- 회원가입 : /api/auth/regi-user

  ```python
  # HTTP Method : POST
  ## Autherization = None
  
  ### Body(JSON)
  {
    "phone_num":"010-7330-2687", 
    "pw_check":"pw3327",	
    "pw_check2":"pw3327"
  }
  
  ```

  

- 로그인 : /api/auth/sign-in

  ```python
  # HTTP Method : POST
  ## Autherization = None
  
  ### Body(JSON)
  
  {
      "user_id": "010-7330-2687",
      "user_pw": "pw3327"
  }
  ```

  

- 로그아웃 : /api/auth/sign-out

  ```shell
  # HTTP Method : POST
  ## Autherization = Required (Bearer : Access Token)
  
  ## Body(JSON)
  {
      "user_id": "010-7330-2687"
  }
  ```

  

- 상품 등록 : /api/plat/regi-item

  ```python
  # HTTP Method : POST
  ## Autherization = Required (Bearer : Access Token)
  
  ## Body (JSON)
  
  {
      "user_id":"010-7330-2687",
      "p_category":"A",
      "p_price":20000,
      "p_cost":11000,
      "p_name":"상품31",
      "p_describe":"상품에 대한 설명입니다. \n K사에서 제조한 제품으로 ~~~ 이러한 특징이 있습니다.",
      "p_barcode":"2577452819",
      "p_expire_date":"2023-04-16",
      "p_size":"S"
  }
  
  ```

  

- 상품 수정 : /api/plat/fix-item

  ```python
  # HTTP Method : PATCH
  ## Autherization = Required (Bearer : Access Token)
  
  ### Body (JSON)
  
  {
      "user_id":"010-7330-2687",
      "p_name":"상품6",
      "p_category":"C",
      "p_price":25000,
      "p_cost":22000
      "p_describe":null, ## null로 표시되는 경우 데이터에서 빼도 상관 없도록 설계되어있음
      "p_barcode":null,
      "p_expire_date":null,
      "p_size":null
  }
  ```

  

- 상품 등록 리스트 호출 : /api/plat/list-item

  ```shell
  # HTTP Method : GET
  ## Autherization = Required (Bearer : Access Token)
  
  ### Parms 
  
  {
  	"user_id":"010-7330-2687",
  	"cursor": 1 ## 여기서 cursor은 cursor based pagnation을 위한 default값이 1로 설정되어있음
  }
  ```

  

- 등록 상품 삭제 : /api/plat/remove-item

  ```shell
  # HTTP Method : POST
  ## Autherization = Required (Bearer : Access Token)
  
  ### Body (JSON)
  
  {
  	"user_id":"010-7330-2687",
  	"p_name": "초코파이", ## 초성 검색 가능 ex) ㅊㅋㅍㅇ
  	"barcode"" "12889526"
  }
  ```

  

- 상품 검색 : /api/plat/search-item

  ```python
  # HTTP Method : GET
  ## Autherization = Required (Bearer : Access Token)
  
  ### Params
  
  {
    "user_id":"010-7330-2687",
    "product_name":"초코파이" 
  }
  ```

- Access Token 신규 발급 : /api/auth/get-new-token

  ```shell
  # HTTP Method : POST
  ## Autherization = None
  
  ### Body (JSON)
  
  {
      "user_id" : "010-7440-2687",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzEyMjM0OCwiaWF0IjoxNjgzMDM1OTQ4LCJqdGkiOiIzMmM2OGVjMDllMzA0Yzk4YmNmYTRiMTMyZDM0MmNlYSIsInVzZXJfaWQiOiIwMTAtNzQ0MC0yNjg3In0.j9cR7QWRyoPH2UJstijtdq-1fyny8xzgvCUA1_qiQdE"
  }
  ```

-----

#### 프로젝트 진행 시 아쉬웠던점

- refresh 토큰 기반의 access 토큰 발급
- 삭제 시 history 로직 부재
- 