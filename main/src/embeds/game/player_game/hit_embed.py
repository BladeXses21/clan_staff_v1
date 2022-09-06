from discord import Colour

from embeds.game.player_game.battle_embed import BattleEmbed
from models.game_model.battle_types.battle import Battle
from models.game_model.lifeform_types.hero_type import Hero


class HitEmbed(BattleEmbed):
    def __init__(self, battle: Battle, hero: Hero):
        super().__init__(battle, hero.id)
        self.color = Colour(0x292b2f)
        self.set_image(
            url="https://cdn.discordapp.com/attachments/952010583388074044/960474136071798814/ezgif.com-gif-maker_1.gif")
