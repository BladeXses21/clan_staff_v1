from mongoengine import Document, IntField, StringField


class ClanStaffModel(Document):
    guild_id = IntField(min_value=0)  # ID сервера
    clan_staff_id = IntField(min_value=0)  # ID участника clan staff
    member_work_this_request = IntField()  # ID сообщения в которым работает clan staff
    sum_event_ends = IntField()  # суммарное количество проведенных ивентов
    wasting_time = IntField()  # суммарное потраченое время на все ивенты
    butterfly = IntField()  # бабочки - валюта клан стафф
    fault = IntField()  # выговор - после третего выговора - улаояет с базы
    add_time = IntField()  # дата добавление участника выраженная в секундах unix time


class CrossGuildModel(Document):
    guild_id = IntField(min_value=0)  # ID сервера
    event_channel_id = IntField(min_value=0)  # ID текстового канала clan staff
    text_category_id = IntField(min_value=0)  # ID текстовой категории кланов
    voice_category_id = IntField(min_value=0)  # ID головой категории кланов
    clan_staff_role_id = IntField(min_value=0)  # ID роли clan staff
    auction_channel_id = IntField(min_value=0)  # ID текстового канала аукциона
    trash_channel_id = IntField(min_value=0)  # ID текстового канала корзины
    leader_role_id = IntField(min_value=0)  # ID роли лидера клана
    consliger_role_id = IntField(min_value=0)  # ID роли заместителя клана
    find_clan_channel_id = IntField(min_value=0)  # ID текстового канала поиск клана
    clan_info_channel_id = IntField(min_value=0)  # ID текстового канала клан инфо
    create_clan_url = StringField(min_length=0)  # ссылка формы создания клана
    verify_url = StringField(min_length=0)  # ссылка формы верификации клана
    clan_staff_url = StringField(min_length=0)  # ссылка формы набора на клан стафф
    team_lead_id = IntField(min_value=0)  # ID главного по кланам на сервере
    senior_lead_id = IntField(min_value=0)  # ID помощника по кланам


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


class CrossRequestModel(Document):
    guild_id = IntField(min_value=0)  # guild id
    message_id = IntField(min_value=0)  # response message id
    event_name = StringField()  # enum event dict
    clan_send_request = StringField()  # name clan which send close request
    clan_accept_request = StringField()  # name clan which accept close request
    clan_staff_id = IntField(min_value=0)  # id clan staff user which accept this close request
    time_send_request = IntField(min_value=0)  # time send request
    time_accept_request = IntField(min_value=0)  # time accept request


class SavedStatModel(Document):
    guild_id = IntField(min_value=0)  # guild_id - id сервера
    clan_staff_id = IntField(min_value=0)  # clan staff id - id челикса из клан стафф
    butterfly = IntField()  # бабочки - валюта клан стафф
    total_event_ends = IntField()
    total_time_events = IntField()
