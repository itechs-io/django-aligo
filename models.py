import json

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models


def is_debug():
    try:
        debug = settings.DJANGO_ALIGO_DEBUG
    except Exception as e:
        return True
    else:
        return debug


class Message(models.Model):
    class Meta:
        verbose_name = '발송기록'
        verbose_name_plural = verbose_name
        ordering = ('-registered_at',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aligo_client_id = settings.DJANGO_ALIGO_IDENTIFIER
        self.aligo_client_key = settings.DJANGO_ALIGO_KEY

    MSG_TYPE_CHOICES = (("SMS", "SMS"), ("LMS", "LMS"), ("MMS", "MMS"))

    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='요청일시')
    sender = models.CharField(max_length=16, null=False, blank=False, verbose_name='발신자 전화번호')
    receiver = models.CharField(max_length=16, null=False, blank=False, verbose_name='수신자 전화번호')
    msg = models.TextField(null=False, blank=False, verbose_name='메시지 내용')
    title = models.CharField(max_length=44, null=True, blank=True, verbose_name='메시지 제목')
    debug = models.BooleanField(default=is_debug, null=True, blank=True, verbose_name='테스트모드')
    #
    msg_type = models.CharField(max_length=3, choices=MSG_TYPE_CHOICES, null=True, blank=True, verbose_name='메시지 구분')
    result = models.NullBooleanField(default=None, verbose_name='발송결과')
    result_code = models.IntegerField(null=True, blank=True, verbose_name='결과코드')
    result_message = models.TextField(null=True, blank=True, verbose_name='결과 메세지')
    result_message_id = models.IntegerField(null=True, blank=True, verbose_name='메시지 고유 아이디')

    def __str__(self):
        return self.receiver

    @classmethod
    def send(cls, receiver: str, msg: str, title=None, sender=None):
        if sender:
            real_sender = sender
        else:
            if hasattr(settings, "DJANGO_ALIGO_SENDER"):
                real_sender = settings.DJANGO_ALIGO_SENDER
            else:
                raise ImproperlyConfigured("발신자가 지정되지 않았습니다.")
        message = Message.objects.create(sender=real_sender, receiver=receiver, msg=msg, title=title)
        message._send()
        return message

    def _send(self):
        url = "https://apis.aligo.in/send/"
        data = {
            "key": self.aligo_client_key,
            "user_id": self.aligo_client_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "msg": self.msg,
            "testmode_yn": "Y" if self.debug else "N"
        }
        if self.title:
            data['title'] = self.title
        response = requests.post(url=url, data=data)
        if response.status_code == 200:
            res_data = response.json()
            if res_data['result_code'] == "1":
                self.result = True
                self.result_message_id = res_data['msg_id']
                self.msg_type = res_data['msg_type']
            else:
                self.result = False
            self.result_code = int(res_data['result_code'])
            self.result_message = res_data['message']
        else:
            self.result = False
            self.result_message = '알리고 서버가 정상 응답하지 않습니다. status code : {}'.format(response.status_code)
            self.result_code = response.json()
        self.save()
        return self
