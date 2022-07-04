from discord import Colour, Embed


class BaseEmbed(Embed):
    def __init__(self, description, **kwargs):
        kwargs['description'] = description
        super().__init__(**kwargs)
        self.color = 3092790


class ErrorEmbed(BaseEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = Colour(0x292b2f)
