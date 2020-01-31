===============
Django-Aligo
===============

Django-Aligo는 Django에서 알리고 SMS 서비스(https://smartsms.aligo.in)를 손쉽게 연동할 수 있도록 하는 app 입니다.

설치
-----


Quick Start
------------
1. "aligo_sms"를 settings.py의 INSTALLED_APPS에 추가합니다::

    INSTALLED_APPS = [
        ...
        'aligo_sms'
    ]
2. settings 파일에 아래 설정을 지정합니다::
    DJANGO_ALIGO_IDENTIFIER = `aligo identifer`

    DJANGO_ALIGO_KEY = `aligo key`

    DJANGO_ALIGO_DEBUG = False  # 테스트 모드 여부. 기본값 True.

    DJANGO_ALIGO_SENDER = None # 기본 발신자 번호. 기본값 None

3. `python manage.py migrate` 를 실행해 aligo_sms의 모델을 생성합니다.
