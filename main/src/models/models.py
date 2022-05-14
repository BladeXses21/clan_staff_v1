from mongoengine import *


class ClanStaffModel(Document):
    guild_id = IntField(min_value=0)  # ID сервера
    clan_staff_id = IntField(min_value=0)  # ID участника clan staff
    member_work_this_request = IntField()  # ID сообщения в которым работает clan staff
    sum_event_ends = IntField()  # суммарное количество проведенных ивентов
    wasting_time = IntField()  # суммарное потраченое время на все ивенты
    add_time = IntField()  # дата добавление участника выраженная в секундах unix time


class CrossGuildModel(Document):
    guild_id = IntField(min_value=0)  # ID сервера
    event_channel_id = IntField(min_value=0)  # ID текстового канала clan staff
    text_category_id = IntField(min_value=0)  # ID текстовой категории кланов
    voice_category_id = IntField(min_value=0)  # ID головой категории кланов
    clan_staff_role_id = IntField(min_value=0)  # ID роли clan staff
    auction_channel_id = IntField(min_value=0)  # ID текстового канала аукциона


class RequestModel(Document):
    guild_id = IntField(min_value=0)
    message_id = IntField(min_value=0)
    event_num = IntField(min_value=0)
    member_send_request = IntField(min_value=0)
    clan_name = StringField()
    comment = StringField()
    clan_staff_id = IntField(default=0)
    time_send_request = IntField(min_value=0)
    time_accept_request = IntField(min_value=0)


class CrossRequstModel(Document):
    guild_id = IntField(min_value=0)
    message_id = IntField(min_value=0)
    event_num = IntField(min_value=0)
    clan_send_request = StringField()
    clan_accept_request = StringField()
    clan_staff_id = IntField(min_value=0)
    time_send_request = IntField(min_value=0)
    time_accept_request = IntField(min_value=0)
