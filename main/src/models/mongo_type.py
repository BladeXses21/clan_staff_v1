import json
import time

from mongoengine import *

connect("clan_staff_base")


# region STAFF MODAL | MONGODB
class CrossStaffModel(Document):
    guild_id = IntField(min_value=0)  # ID сервера
    clan_staff_id = IntField(min_value=0)  # ID участника clan staff
    member_work_this_request = IntField(min_value=0)  # ID сообщения в которым работает clan staff
    sum_event_ends = IntField(min_value=0)  # суммарное количество проведенных ивентов
    wasting_time = IntField(min_value=0)  # суммарное потраченое время на все ивенты
    curator = IntField(min_value=0)  # id человека, который принял
    xp_counter = IntField(min_value=0)  # опыт полученый за выполение квестов
    minimum_limit = IntField(min_value=0)  # минимальное количество времени нужное ивентеру для выполения нормы
    avatar = StringField(min_length=1)
    background = StringField(min_length=1)
    birthday = StringField(min_length=1)
    add_time = IntField(min_value=0)  # дата добавление участника выраженная в секундах unix time
    color = IntField(min_value=0)
    lvl = IntField(min_value=1)


# endregion

# region GUILD MODAL | MONGODB
class CrossGuildModel(Document):
    guild_id = IntField(min_value=0)  # ID сервера
    event_channel_id = IntField(min_value=0)  # ID текстового канала clan staff
    text_category_id = IntField(min_value=0)  # ID текстовой категории кланов
    voice_category_id = IntField(min_value=0)  # ID головой категории кланов
    clan_staff_role_id = IntField(min_value=0)  # ID роли clan staff
    auction_channel_id = IntField(min_value=0)  # ID текстового канала аукциона
    trash_channel_id = IntField(min_value=0)  # ID текстового канала корзины
    leader_role_id = IntField(min_value=0)  # ID роли лидера клана
    consigliere_role_id = IntField(min_value=0)  # ID роли заместителя клана
    find_clan_channel_id = IntField(min_value=0)  # ID текстового канала поиск клана
    clan_info_channel_id = IntField(min_value=0)  # ID текстового канала клан инфо
    create_clan_url = StringField(min_length=0)  # ссылка формы создания клана
    verify_url = StringField(min_length=0)  # ссылка формы верификации клана
    clan_staff_url = StringField(min_length=0)  # ссылка формы набора на клан стафф
    team_lead_id = IntField(min_value=0)  # ID главного по кланам на сервере
    senior_lead_id = IntField(min_value=0)  # ID помощника по кланам


# endregion

# region REQUEST EVENT MODAL | MONGODB
class RequestEventModel(Document):
    guild_id = IntField(min_value=0)
    message_id = IntField(min_value=0)
    event_num = IntField(min_value=0)
    member_send_request = IntField(min_value=0)
    clan_name = StringField()
    comment = StringField()
    clan_staff_id = IntField(default=0)
    time_send_request = IntField(min_value=0)
    time_accept_request = IntField(min_value=0)


# endregion

# region REQUEST CLOSE MODAL | MONGODB
class RequestCloseModel(Document):
    guild_id = IntField(min_value=0)
    clan_staff_id = IntField(default=0)
    eventName = StringField(min_length=1)
    memberSendRequest_Id = IntField(min_value=0)
    teamTwoMsg_Id = IntField(min_value=0)
    closeMsg_Id = IntField(min_value=0)
    teamOne_Id = IntField(min_value=0)
    teamTwo_Id = IntField(min_value=0)
    comment = StringField()
    timeSendRequest = IntField(min_value=0)
    timeAcceptRequest = IntField(default=0)


# endregion

# region SAVED STAT STAFF MODAL | MONGODB
class SavedStatModel(Document):
    guild_id = IntField(min_value=0)  # guild_id - id сервера
    clan_staff_id = IntField(min_value=0)  # clan staff id - id челикса из клан стафф
    butterfly = IntField()  # бабочки - валюта клан стафф
    total_event_ends = IntField()
    total_time_events = IntField()


# endregion

# region FAULT MODAL STAFF | MONGODB
class FaultModel(Document):
    guild_id = IntField(min_value=0)
    clan_staff_id = IntField(unique=True, min_value=0)
    fault_list = ListField()

    def json(self):
        fault_dict = {
            "guild_id": self.guild_id,
            "clan_staff_id": self.clan_staff_id,
            "fault_list": self.fault_list
        }
        return json.dumps(fault_dict)


# endregion

# region QUEST MODAL STAFF | MONGODB
class QuestModel(Document):
    guild_id = IntField(min_value=0)
    clan_staff_id = IntField(unique=True, min_value=0)
    quest_list = ListField()

    def json(self):
        quest_dict = {
            "guild_id": self.guild_id,
            "clan_staff_id": self.clan_staff_id,
            "quest_list": self.quest_list
        }
        return json.dumps(quest_dict)


# endregion

class Number(EmbeddedDocument):
    sequential_value = SequenceField(required=True)


# region CLAN WARN MODAL | MONGODB
class ClanWarnModal(Document):
    guild_id = IntField(unique=True, min_value=1)
    clan_staff_id = IntField(min_value=1)
    clan_role_id = IntField(min_value=1)
    reason = StringField(min_length=1)
    warn_date = IntField(min_value=1)
    unwarn_date = IntField(min_value=1)
    warn_list = ListField()

    def json(self):
        warn_dict = {
            "guild_id": self.guild_id,
            "clan_staff_id": self.clan_staff_id,
            "clan_role_id": self.clan_role_id,
            "reason": self.reason,
            "warn_date": self.warn_date,
            "unwarn_date": self.unwarn_date,
            'warn_list': self.warn_list
        }

        return json.dumps(warn_dict)

# endregion
