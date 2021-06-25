from discord import player


class cric:
    def __init__(self, message):
        if message == 0:
            self.cric_on = False
        else:
            self.players = message.mentions
            self.start_time = message.created_at
            self.status = 'initiation'
            self.channel = message.channel
            self.cric_on = False
            print(self.players)
    
    def check(self):
        uni = []
        if len(self.players)%2!=0:
            print('this happens')
            return 'To divide into teams you need even number of players'
        for player in self.players:
            idd = player.id
            if player.bot==False:
                uni.append(idd)
            else:
                return 'Bot can\'t be mentioned!'
        return self.ready()

    def ready(self):
        self.players_cout = int(len(self.players)/2)
        self.redteam, self.blueteam = self.players[:self.players_cout], self.players[self.players_cout:]
        st = 'RED TEAM\n'
        for i in self.redteam:
            st += i.name+'\n'
        st += '\nBLUE TEAM\n'
        for i in self.blueteam:
            st += i.name+'\n'
        st += '\nto continue the game everyone type ```hp start```'
        self.status = 'onyourmarks'
        self.cric_on = True
        return st