# discord bot token
# Token = 'ODY2MDUwNzkzMzAwMDMzNTk2.YPM6pw.ydkfdaQT_hMroG5vYEXFJUpF8qg'
# TOKEN = 'ODY2MDUwNzkzMzAwMDMzNTk2.YPM6pw.N5_r85zmSGDf45PrZHvvK7ATf5s'

TOKEN = 'OTcwNTA1MTc3NTQ5MzgxNzAz.GW2drs.mX52QICi6fo2kOApErqMdKgvxhkqxqsbV9IFxc'

# MongoDb token
# BladeXses DB
MONGO_TOKEN = 'mongodb+srv://DesireBot:kopanura200121@cluster0.c1j11.mongodb.net/DesireBot?retryWrites=true&w=majority'
# DzianTao DB
# MongoToken = 'mongodb+srv://DesireBot:PiLeJcaVFhesIe02@cluster0.e9eia.mongodb.net/DesireBotDB?retryWrites=true&w=majority'

# bot prefix
PREFIX = '!'

# secs in 24 hours
DAY_IN_SECONDS = 86400

# region OWNER PERMISSION IDS | MAIN OWNER | OWNER LIST
BLADEXSES_ID = 450361269128790026
LESS_ID = 709820533176270911
DA_TI_CHE_ID = 692472578102525973
MAYES = 270664753129455626
SOPHI = 764219880786362390
BogratiOne = 350057334690545664
CURATOR_DARKNESS = 695278293057798171

MAIN_OWNER = 450361269128790026

OWNER_IDS = [
    BLADEXSES_ID,
    LESS_ID,
    DA_TI_CHE_ID,
    MAYES,
    SOPHI,
    BogratiOne,
    CURATOR_DARKNESS
]
# endregion

# region GUILD IDS | GUILD ID LIST
TENDERLY_ID = 457902248660434944
META_ID = 822354240713261068
DARKNESS_ID = 934073000117026866
SWEETNESS_ID = 890304318643785769
YUKI_ID = 955126116589383800

SERVERS = [
    TENDERLY_ID,
    META_ID,
    DARKNESS_ID,
    SWEETNESS_ID
]
# endregion

# region PERMISSION ROLE ON YUKINE SERVER
TEAMLEAD_YUKI = 955169324384006195
SENIOR_LEAR_YUKI = 955570935518343208
CURATOR_ROLE_YUKI_T = 969186895630327810
CURATOR_ROLE_YUKI_M = 969186934893183038
CURATOR_ROLE_YUKI_D = 969186941486657556
CURATOR_ROLE_YUKI_S = 985577582202331176
DESIGN_ROLE_YUKI = 956853213729017886

CURATOR_ROLE_BY_SERVER_ID = {
    TENDERLY_ID: CURATOR_ROLE_YUKI_T,
    META_ID: CURATOR_ROLE_YUKI_M,
    DARKNESS_ID: CURATOR_ROLE_YUKI_D,
    SWEETNESS_ID: CURATOR_ROLE_YUKI_S
}

PERMISSION_ROLE = [
    DESIGN_ROLE_YUKI,
    CURATOR_ROLE_YUKI_S,
    CURATOR_ROLE_YUKI_D,
    CURATOR_ROLE_YUKI_M,
    CURATOR_ROLE_YUKI_T,
    SENIOR_LEAR_YUKI,
    TEAMLEAD_YUKI
]

# endregion

# region VERIFICATION CLAN COST
VERIFICATION_COST_BY_GUILD_ID = {
    TENDERLY_ID: "20000",
    META_ID: "20000",
    DARKNESS_ID: "15000",
    SWEETNESS_ID: "15000",
}
# endregion

# region CLAN ROLE | LEADER - CONSIGLIERE
LEADER_ROLE_TENDERLY_ID = 774059943870726205
LEADER_ROLE_META_ID = 959907350725132299
LEADER_ROLE_DARKNESS_ID = 968580059403268116
LEADER_ROLE_SWEETNESS_ID = 891260463659225138
CONSIGLIERE_ROLE_TENDERLY_ID = 879418323350196274
CONSIGLIERE_ROLE_META_ID = 959907357024997386
CONSIGLIERE_ROLE_DARKNESS_ID = 968579961059422279
CONSIGLIERE_ROLE_SWEETNESS_ID = 985559901579378719

CLAN_MEMBER_ACCESS_ROLE = [
    LEADER_ROLE_TENDERLY_ID,
    LEADER_ROLE_META_ID,
    LEADER_ROLE_DARKNESS_ID,
    LEADER_ROLE_SWEETNESS_ID,
    CONSIGLIERE_ROLE_TENDERLY_ID,
    CONSIGLIERE_ROLE_META_ID,
    CONSIGLIERE_ROLE_DARKNESS_ID,
    CONSIGLIERE_ROLE_SWEETNESS_ID
]
# endregion

# region CLAN STAFF ROLE IDS | CLAN STAFF ROLE LIST

CLAN_STAFF_TENDERLY = 774059907317497867
CLAN_STAFF_META = 911700891357306900
CLAN_STAFF_DARKNESS = 953752849366532097
CLAN_STAFF_SWEETNESS = 985561662868324415
TEST_ROLE = 948739416820711424
TEST_ROLE_2 = 955570935518343208

CLAN_STAFF = [
    CLAN_STAFF_TENDERLY,
    CLAN_STAFF_META,
    CLAN_STAFF_DARKNESS,
    CLAN_STAFF_SWEETNESS,
    TEST_ROLE,
    TEST_ROLE_2
]

# endregion

# region CLAN VOICE CATEGORY IDS
TENDERLY_CATEGORY = 774043288940314664
META_CATEGORY = 959474295120228482
DARKNESS_CATEGORY = 968575027110875196
SWEETNESS_CATEGORY = 985554992977051668
# endregion

# region CLAN VOICE CATEGORY NAMES
TENDERLY_CATEGORY_NAME = '⎯⎯⎯▾КЛАНЫ'
META_CATEGORY_NAME = '──▾・clan voice'
DARKNESS_CATEGORY_NAME = 'КЛАНОВЫЕ ВОЙСЫ'
SWEETNESS_CATEGORY_NAME = '──・КЛАН ВОЙСЫ'
# endregion

# logs chat
STATS_SERVER_CHAT = 971631022791868447
STATS_CLAN_CHAT = 998625623197102322

# region CATEGORY NAME FOR A GUILD IDS | DICT
GUILD_DICT = {
    TENDERLY_ID: TENDERLY_CATEGORY_NAME,
    META_ID: META_CATEGORY_NAME,
    DARKNESS_ID: DARKNESS_CATEGORY_NAME,
    SWEETNESS_ID: SWEETNESS_CATEGORY_NAME
}
# endregion

AUCTION_BET_LIMIT = 500
STOP_WORD = 'stop'

# region AUCTION IMAGE
AUCTION_TENDERLY_IMAGE = 'https://cdn.discordapp.com/attachments/969202370280038410/974886473138585610/animesher.com_auction-gon-the-phantom-rouge-583231.gif'
AUCTION_META_IMAGE = 'https://cdn.discordapp.com/attachments/969202370280038410/974886473138585610/animesher.com_auction-gon-the-phantom-rouge-583231.gif'
AUCTION_DARKNESS_IMAGE = 'https://cdn.discordapp.com/attachments/843535589093015563/974352865952936026/4e17123556e04db4777d216b28fbfc1cfe284b9cr1-500-281_hq.gif'
AUCTION_SWEETNESS_IMAGE = 'https://cdn.discordapp.com/attachments/969202370280038410/974886473138585610/animesher.com_auction-gon-the-phantom-rouge-583231.gif'
# endregion

# region EMOJI
NEXT_STEP_EMOJI = '<a:next_step:980111048185090048>'
NEXT_STEP_PINK_EMOJI = '<a:next_step_pink:980113385955934208>'
BARRETTE_BLUE_EMOJI = '<:barrette_blue:980112872736718908>'
BARRETTE_PINK_EMOJI = '<:barrette__pink:980112872690548756>'
UKI_EMOGI = '<a:uki2:959118514814324788>'
# endregion

# region CHANCE | LVL | XP | PAYMENT
CHANCE_FOR_ITEMS = {
    'common': 47,
    'rare': 21,
    'mythical': 14,
    'legendary': 12,
    'immortal': 6
}

LEVEL_MULTIPLIER = {
    1: 1,
    2: 1.5,
    3: 2,
    4: 3
}

XP_INCREMENT = {
    1: 250,
    2: 500,
    3: 950,
    4: 950
}

PAYMENT = {
    TENDERLY_ID: {
        'right_time': 300,
        'right_payment': 750,
        'overtime': 50,
        'bonus_payment': 50
    },
    META_ID: {
        'right_time': 180,
        'right_payment': 1500,
        'overtime': 120,
        'bonus_payment': 20
    },
    DARKNESS_ID: {
        'right_time': 300,
        'right_payment': 1000,
        'overtime': 50,
        'bonus_payment': 20
    },
    SWEETNESS_ID: {
        'right_time': 300,
        'right_payment': 1000,
        'overtime': 50,
        'bonus_payment': 20
    }
}
# endregion

RIGHT_AMOUNT_PEOPLE = {
    'Dota 2 5x5': 5,
    'CS:GO 5x5': 5,
    'VALORANT 5x5': 5
}

SHOP_CHANNEL_ID = 977712132906942484

# region START PROFILE CLAN STAFF
STANDART_PROFILE_AVATAR = 'https://media.discordapp.net/attachments/869036410479444008/983066247535161374/Picsart_22-06-05_20-51-34-675.jpg?width=666&height=666'
STANDART_PROFILE_BACKGROUND = 'https://media.discordapp.net/attachments/869036410479444008/983066247090556988/Picsart_22-06-05_20-50-47-538.jpg?width=898&height=508'
STANDART_BIRTHDAY = 'never born'
# endregion

# region HEART EMOJI FOR SERVER - BUTTON
tenderly_heart_emoji = '<:tenderly_icon:990008413842976799>'
meta_heart_emoji = '<:meta_icon:990008420478382171>'
darkness_heart_emoji = '<:darkness_icon:990008419501101056>'
sweetness_heart_emoji = '<:sweetness_icon:990008412853129326>'
# endregion

right_arrow_emoji = '<:freeicon3dforwardarrow64844:960536938782285894>'
left_arrow_emoji = '<:freeicon3dforwardarrow64844remov:960538574250471424>'

# region BUTTON FOR CLAN STAFF PROFILE | FROM FAULT TO TIME
fault_emoji = '<:fault:992743581527851058>'
history_emoji = '<:history:992743471649660989>'
quest_emoji = '<:quest:992743468474568734>'
xp_emoji = '<:xp:992743579845939251>'
event_emoji = '<:event:992743474489208902>'
butterfly_emoji = '<:butterfly:992743466838794260>'
time_emoji = '<:time:992743470139723838>'
# endregion

# region HEART EMOJI FOR A GUILD IDS - DICT
SERVER_EMOGI = {
    TENDERLY_ID: tenderly_heart_emoji,
    META_ID: meta_heart_emoji,
    DARKNESS_ID: darkness_heart_emoji,
    SWEETNESS_ID: sweetness_heart_emoji
}
# endregion

REQUEST_STAFF_CHANNEL = {
    TENDERLY_ID: 991002263856242728,
    META_ID: 992514958107611176,
    DARKNESS_ID: 991258406839132200,
    SWEETNESS_ID: 996879897668624514
}

CLAN_CREATE_REQUEST_CHANNEL = 991274737403703356
CHANNEL_WITHOUT_CLAN = 1011029284988653639

# region PNG IMAGE FOR EMBEDS
png_strip_for_embed = 'https://cdn.discordapp.com/attachments/836056310641459250/987354207566848010/1112.png'
png_heart_icon = '<:png_heart_icon:990008416980320297>'
png_signal_icon = '<:signal:973732570971897856>'
png_butterfly_gif = 'https://images-ext-2.discordapp.net/external/ZtDftGSI1KwmT7ML9u9R23RJqJHQv8cx1TPHxsQY2q0/%3Fsize%3D80%26quality%3Dlossless/https/cdn.discordapp.com/emojis/936017706480717825.gif'
# endregion

# region BOSS GAME

NEW_HERO_START_HEALTH = 100
NEW_HERO_START_ATTACK = 1
HERO_RES_TIME = 12  # time in hours
HERO_REGEN = 60  # time in seconds to regen 1 hp
ITEM_RARITY_DENOMINATOR = 1000

HERO_CLASS_BY_INDEX = {
    1: 'Fighter',
    2: 'Archer',
    3: 'Barbarian',
    4: 'Druid',
    5: 'Ranger',
    6: 'Rogue',
    7: 'Wizard'
}

HERO_DMG_BY_CLASS = {
    'Fighter': 2,
    'Archer': 2,
    'Barbarian': 1,
    'Druid': 1,
    'Ranger': 2,
    'Rogue': 3,
    'Wizard': 3
}

CHANGE_HEALTH_BY_CLASS = {
    'Fighter': 0,
    'Archer': 0,
    'Barbarian': 20,
    'Druid': 20,
    'Ranger': 0,
    'Rogue': -20,
    'Wizard': -20
}

HERO_CLASS_ARRAY = [
    f'<:Fighter:1016886174008229959> : Fighter',
    f'<:Archer:1016886179293057024> : Archer',
    f'<:Barbarian:1016886177430781992> : Barbarian',
    f'<:Druid:1016887074730811464> : Druid',
    f'<:Ranger:1016886175513989130> : Ranger',
    f'<:Rogue:1016886181339869284> : Rogue',
    f'<:Wizard:1016886171932033024> : Wizard'
]

# endregion
