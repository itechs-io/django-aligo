from django.contrib import admin, messages

from aligo_sms.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['registered_at', 'sender', 'receiver', 'msg_type', 'result', 'debug']
    list_filter = ['result', 'result_code', 'msg_type']
    search_fields = ['sender', 'receiver', 'msg', 'title']
    actions = ['send_message']

    def send_message(self, request, queryset):
        result_list = []
        for message in queryset:
            result = message._send()
            result_list.append(result.result)
        msg = "{}개의 메시지 중 {}개 요청 성공".format(len(result_list), result_list.count(True))
        messages.info(request, msg)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            _r = ['registered_at', 'sender', 'receiver', 'msg', 'title', 'debug', 'msg_type', 'result', 'result_code',
                  'result_message', 'result_message_id']
        else:
            _r = []
        return _r
