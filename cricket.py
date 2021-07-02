import random


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
        if len(self.players)==0:
            return 'you need more players to start'
        if len(self.players)%2!=0:
            return 'To divide into teams you need even number of players'
        for player in self.players:
            idd = player.id
            if player.bot==False:
                uni.append(idd)
            else:
                return 'Bot can\'t be mentioned!'
        return self.ready()

    def ready(self):
        self.players_count = int(len(self.players)/2)
        self.redteam, self.blueteam = self.players[:self.players_count], self.players[self.players_count:]
        st = 'RED TEAM\n'
        for i in self.redteam:
            st += i.name+'\n'
        st += '\nBLUE TEAM\n'
        for i in self.blueteam:
            st += i.name+'\n'
        st += '\nto continue the game everyone type ```hp start```'
        self.status = 'onyourmarks'
        self.cric_on = True
        self.start_lis = []
        return st

    def start(self, author):
        if author in self.players and author not in self.start_lis:
            self.start_lis.append(author)
            return '{} more to send'.format(len(self.players)-len(self.start_lis))
            if len(self.start_lis)==len(self.players):
                self.status = 'match'
                return 'Match is going to start. Everybody go to direct message.'

    def begin(self):
        self.status = 'play'
        self.inning = 0
        self.current = [-1, -1]
        if random.randint(0,1)==0:
            self.innings_det = [self.redteam, self.blueteam, [0, 0, 0], [0, 0, 0]]
        else:
            self.innings_det = [self.blueteam, self.redteam, [0, 0, 0], [0, 0, 0]]
        self.on_field = [self.innings_det[0][0], self.innings_det[1][0]]
        st = 'Match begins\n'
        st += '{} is batting first\n'.format(self.on_field[0].name)
        st += '{} is bowling first\n'.format(self.on_field[1].name)
        return st

    def play(self, sign, message):
        auth = message.author
        if auth in self.on_field:
            self.status = 'play'
            if auth == self.on_field[0]:
                self.current[0] = sign
            else:
                self.current[1] = sign


            if all([0<i<7 for i in self.current]):
                self.status = 'played'
                self.innings_det[2+self.inning][2]+=1
                over = int(self.innings_det[2+self.inning][2]/6)
                rem = self.innings_det[2+self.inning][2]-over*6
                st = '{} : {}\t{} : {}\n'.format(self.on_field[0].name,self.current[0],self.on_field[1].name,self.current[1])
                dic = {1:'It\'s a single.', 2:'It\'s a double.', 3:'It\'s a triples.', 4:'Boundary...!', 5:'Five runs...', 6:'Sixer!!!!'}
                if self.current[0]==self.current[1]:
                    self.innings_det[2+self.inning][1]+=1
                    st += 'WICKET!!\n({}/{})\tOvers:{}.{}\n'.format(self.innings_det[2+self.inning][0],self.innings_det[2+self.inning][1],over,rem)
                else:
                    self.innings_det[2+self.inning][0]+=self.current[0]
                    st += '{}\n({}/{})\tOvers:{}.{}\n'.format(dic[self.current[0]],self.innings_det[2+self.inning][0],self.innings_det[2+self.inning][1],over,rem)
                
                if self.inning == 1:
                    cha = self.innings_det[2][0] - self.innings_det[3][0]+1
                    if cha>0:
                        st += 'Need {} runs more\n'.format(cha)

                if self.inning==1 and (cha<1 or self.innings_det[3][1]==self.players_count):
                    if cha<1:
                        self.cric_on = False
                        if self.on_field[0] in self.blueteam:
                            st += 'BLUE TEAM won by {} wickets\n'.format(self.players_count-self.innings_det[3][1])
                        else:
                            st += 'RED TEAM won by {} wickets\n'.format(self.players_count-self.innings_det[3][1])
                    elif self.innings_det[3][1]==self.players_count:
                        self.cric_on = False
                        if self.on_field[1] in self.blueteam:
                            st += 'BLUE TEAM won by {} run\n'.format(cha)
                        else:
                            st += 'RED TEAM won by {} run\n'.format(cha)
                elif self.innings_det[2+self.inning][1]==self.players_count:
                    self.inning=1
                    st += 'Chase run:{}\n'.format(self.innings_det[2][0] - self.innings_det[3][0]+1)
                    self.on_field = [self.innings_det[1][0], self.innings_det[0][0]]
                    st += '{} is going to bat\n'.format(self.on_field[0].name)
                    st += '{} is going to bowl\n'.format(self.on_field[1].name)
                else:
                    if rem==0:
                        self.on_field[1]=self.innings_det[1-self.inning][over%self.players_count]
                        st += '{} is the next bowler'.format(self.on_field[1].name)
                    elif self.current[0]==self.current[1]:
                        self.on_field[0]=self.innings_det[self.inning][self.innings_det[2+self.inning][1]]
                        st += '{} is the next batsman'.format(self.on_field[0].name)
                self.current = [-1, -1]
                return st
                        