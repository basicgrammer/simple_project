### Simple Project Readme

-----

### 프로젝트 설명



### 프로젝트 사용 기술

- Lanugae 

  ![python](https://img.shields.io/badge/python-3.9-red)

- Framework

  ![Django-ninja](https://img.shields.io/badge/Django--ninja-Django%20%2B%20FastAPI-lightgrey)


- Dataase

  ![MySQL](https://img.shields.io/badge/MySQL-Database-yellow)


- Deploy

  ![On-Premise](https://img.shields.io/badge/On--Premise-Infra-blue)</br>
  ![Docker](https://img.shields.io/badge/Docker-Container-brightgreen)</br>
  ![docker-compose](https://img.shields.io/badge/docker--compose-Orchestra%20Tool-orange)</br>
  ![Gunicorn](https://img.shields.io/badge/Gunicorn-App%20Server-red)</br>


#### 개발 사양

- OS : Ubuntu 22.04 LTS (XenServer 가상화 기반 VM)
- CPU : vCPU 4
- Memory : 8G
- Disk : 250G
- docker engine version : Docker version 23.0.3, build 3e7cbfd
- docker-compose version : Docker Compose version v2.13.0

-----

#### 참고사항

- 원활한 테스트를 위해서 Django SECRET_KEY 및 각종 설정들에 대한 참조 파일을 함께 업로드했습니다..
- 구동 테스트 시 docker 및 docker-compose가 필요합니다. / OS 및 환경은 관계 없습니다.
----

#### 컨테이너 기동

```shell
# docker-compose.yml 명세를 활용할 수 있는 디렉토리 위치에서 아래 명령을 실행해주세요.

# 명세 기반 다중 컨테이너의 빌드 및 백그라운드 구동
$ sudo docker-compose up --build -d

# 명세 기반 다중 컨테이너의 이미지 신규 빌드 및 백그라운드 구동
$ sudo docker-compose up --build -d --force-recreate
```

#### 컨테이너 기동 중지 및 일시 정지

```shell
# 명세 기반 다중 컨테이너 정지
$ sudo docker-compose down

# 일부 컨테이너 일시 정지
$ sudo docker-compose stop {container_name}
```

#### 컨테이너 로그 확인

```shell
# 컨테이너 로그 모니터링
$ sudo docker logs {container_name}

# 컨테이너 지속적인 로그 모니터링
$ sudo docker logs --tail 1000 -f {container_name}
```

#### 컨테이너 환경 접속

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

#### 컨테이너 자원 활용 모니터링

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

  ```python
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

  ```python
  # HTTP Method : GET
  ## Autherization = Required (Bearer : Access Token)
  
  ### Parms 
  
  {
  	"user_id":"010-7330-2687",
  	"cursor": 1 ## 여기서 cursor은 cursor based pagnation을 위한 default값이 1로 설정되어있음
  }
  ```

  

- 등록 상품 삭제 : /api/plat/remove-item

  ```python
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

  ```python
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
  - 관련 사용법을 파악하지 못해서 급하게 기존 Refresh + Access Token 신규 발급하는 함수를 활용해서 임의로 구현함. 
  - 해당 기능은 현재 반쪽짜리 기능으로, 차후 스터디를 통해 Refresh 토큰 유효성 체크 및 신규 Access 토큰을 발급하는 과정을 직접 구현하거나, 제공되는 기능을 활용해서 구현해야함
  - JWT 발급 및 접근 권한 제어에는 현재 문제가 없기에, 시간을 두고 천천히 개선할 예정


- 중복 로그인 처리를 위한 방법
  - 타 프로젝트 진행 시 Session 기반 인증을 사용했으므로, 중복 로그인 방지에 대한 문제가 없었지만 JWT를 도입하게 되면서 마땅한 중복 로그인 처리 방법이 떠오르지 않음
  - 그래서 이러한 중복 로그인 처리를 위해 서버 영역에서 JWT + Session 방식으로 운영하는것이 더 좋다고 판단됨
  - 추후 시간이 된다면 JWT + Session 방식의 인증 구현 예정
  - Session이 삭제되면서 발생되는 이벤트로 저장되는 Refresh Token의 유효성을 검증하는 방식으로 운영하면 좋을 것 같다.


- 상품 삭제 시 history 관련 로직 및 테이블 부재
- try + except 사용 

- Swagger 활용 미숙
  - Swagger를 활용한 api docs 운영 시 POST, PATCH 등을 GET처럼 파라미티 인자를 받는 형식으로 운영하지 못하고 있음, 학습을 통해 이 부분에 대한 개선이 필요함

-----


### 2023.05.10 업데이트 내용

- Swagger의 입력값 예시를 보기 위한 파라미터 값 추가

- 코드 오류 수정

  - 서로 다른 API의 동일한 이름의 함수 매핑, 함수 이름 수정 완료 
  - 로그아웃 API의 권한 체크가 없던 문제 해결
  

### 2023.05.11 업데이트 내용

- 응답 메시지 개편 및 수정
- Platform App의 API 일부 응답 수정