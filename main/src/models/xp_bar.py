class XpBarController:
    def __init__(self, full_pool_lenght: int, pull_lenght: int):
        self.full_pool_lenght = full_pool_lenght
        self.pull_lenght = pull_lenght
        self.left_empty = '<:LeftEmpty:1003042459560972319>'
        self.middle_empty = '<:MiddleEmpty:1003042466276065331>'
        self.right_empty = '<:RightEmpty:1003042956481151087>'
        self.left_green = '<:LeftGreen:1003072714644402267>'
        self.middle_green = '<:MiddleGreen:1003042465026158723>'
        self.right_green = '<:RightGreen:1003042832803696742>'

    def __str__(self):
        xp = ''
        if self.full_pool_lenght <= 0:
            xp = xp + self.left_empty
        else:
            xp = xp + self.left_green

        xp = xp + ((self.full_pool_lenght - 1) * self.middle_green)
        xp = xp + ((self.pull_lenght - self.full_pool_lenght) * self.middle_empty)

        if self.full_pool_lenght >= self.pull_lenght:
            xp = xp + self.right_green
        else:
            xp = xp + self.right_empty

        return xp

