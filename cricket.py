class cric:
    def __init__(self, message):
        self.players = message.mentions
        print(self.players)
    
    def check(self):
        uni = []
        for player in self.players:
            idd = player.id
            if idd not in uni and player.bot==False:
                uni.append(idd)
            else:
                return False
        return True

    def ready(self):
        return 'undr progress'