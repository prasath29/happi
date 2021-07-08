from os import sync
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
            self.colour = {'blue':552411, 'red':15142928}
            self.embed = {
                            "title": "Cricket - Score",
                            "description": "0/0\t(0.0)\n0/0\t(0.0)\n\nMatch Begins\n\n",
                            "color": 15142928,
                            "footer": {
                                "text": ""
                            }   
                        }
            print(self.players)
    
    def sync_embed(self, cus_msg='', cus_not='', refresh=True):
        if self.status=='played':
            dic = {1:'It\'s a single', 2:'It\'s a double', 3:'It\'s a triples', 4:'Boundary!', 5:'Five runs', 6:'Sixer!'}
            self.embed['color'] = self.colour[self.cur_bat_team]
            over1 = int(self.innings_det[2][2]/6)
            over2 = int(self.innings_det[3][2]/6)
            if cus_not=='':
                cus_not = '{}: {}'.format(dic[self.current[0]],self.current[0])
                if self.inning==1:
                    cus_not += '\n{} TEAM needs {} runs to win'.format(self.cur_bat_team.upper(),self.innings_det[2][0]-self.innings_det[3][0]+1)
            self.embed['description']='**{}/{}\t({}.{})\n{}/{}\t({}.{})**\n\n{}\n\n**{}** :{}\n**{}** :{}'.format(self.innings_det[2][0],self.innings_det[2][1],over1,self.innings_det[2][2]-over1*6,self.innings_det[3][0],self.innings_det[3][1],over2,self.innings_det[3][2]-over2*6,cus_not,self.bug_fix[0].name,self.current[0],self.bug_fix[1].name,self.current[1])
            self.embed['footer']['text'] = cus_msg
        else:
            self.embed['footer']['text'] = cus_msg
        return self.embed


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
            if len(self.start_lis)==len(self.players):
                self.status = 'match'
                return 'See my direct message.'
            else:
                return '{} more to send'.format(len(self.players)-len(self.start_lis))

    def begin(self):
        self.status = 'play'
        self.inning = 0
        self.current = [-1, -1]
        if random.randint(0,1)==0:
            self.innings_det = [self.redteam, self.blueteam, [0, 0, 0], [0, 0, 0], [0 for i in range(self.players_count)], [0 for i in range(self.players_count)], [0 for i in range(self.players_count)], [0 for i in range(self.players_count)]]
            self.cur_bat_team = 'red'
        else:
            self.innings_det = [self.blueteam, self.redteam, [0, 0, 0], [0, 0, 0], [0 for i in range(self.players_count)], [0 for i in range(self.players_count)], [0 for i in range(self.players_count)], [0 for i in range(self.players_count)]]
            self.cur_bat_team = 'blue'
        self.on_field = [self.innings_det[0][0], self.innings_det[1][0]]
        self.embed['color'] = self.colour[self.cur_bat_team]
        st = '{} is batting first\n'.format(self.on_field[0].name)
        st += '{} is bowling first\n'.format(self.on_field[1].name)
        self.embed['footer']['text'] = st
        return self.embed

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
                st_not = ''
                st_msg = ''
                self.bug_fix = self.on_field
                if self.current[0]==self.current[1]:
                    self.innings_det[2+self.inning][1] += 1
                    self.innings_det[6+self.inning][over%self.players_count] += 1
                    st_not += 'WICKET!'
                else:
                    self.innings_det[2+self.inning][0] += self.current[0]
                    self.innings_det[4+self.inning][self.innings_det[2+self.inning][1]] += self.current[0]
                
                if self.inning == 1:
                    cha = self.innings_det[2][0] - self.innings_det[3][0]+1

                if self.inning==1 and (cha<1 or self.innings_det[3][1]==self.players_count):
                    if cha<1:
                        self.cric_on = False
                        if self.on_field[0] in self.blueteam:
                            st_msg += 'BLUE TEAM won by {} wickets\n'.format(self.players_count-self.innings_det[3][1])
                        else:
                            st_msg += 'RED TEAM won by {} wickets\n'.format(self.players_count-self.innings_det[3][1])
                    elif self.innings_det[3][1]==self.players_count:
                        self.cric_on = False
                        if self.innings_det[2][0]==self.innings_det[3][0]:
                            st_msg += 'Draw\n'
                        elif self.on_field[1] in self.blueteam:
                            st_msg += 'BLUE TEAM won by {} run(s)\n'.format(cha-1)
                        else:
                            st_msg += 'RED TEAM won by {} run(s)\n'.format(cha-1)
                elif self.innings_det[2+self.inning][1]==self.players_count:
                    self.inning=1
                    if self.cur_bat_team=='red':
                        self.cur_bat_team = 'blue'
                    else:
                        self.cur_bat_team = 'red'
                    self.on_field = [self.innings_det[1][0], self.innings_det[0][0]]
                    st_msg += '{} is going to bat\n'.format(self.on_field[0].name)
                    st_msg += '{} is going to bowl\n'.format(self.on_field[1].name)
                else:
                    if rem==0:
                        self.on_field[1]=self.innings_det[1-self.inning][over%self.players_count]
                        st_msg += '{} is the next bowler'.format(self.on_field[1].name)
                    elif self.current[0]==self.current[1]:
                        self.on_field[0]=self.innings_det[self.inning][self.innings_det[2+self.inning][1]]
                        st_msg += '{} is the next batsman'.format(self.on_field[0].name)
                res = self.sync_embed(st_msg, st_not)
                self.res_msg = st_msg
                self.current = [-1, -1]
                return res

    def end(self):
        self.embed = {
                            "title": "",
                            "description": "",
                            "color": 15142928
                        }
        self.embed['title'] = self.res_msg
        if self.cur_bat_team=='red':
            i = 1
        else:
            i = 0
        over = int(self.innings_det[2+i][2]/6)
        self.embed['description'] = '**RED TEAM** : {} ({}.{})\n'.format(self.innings_det[2+i][0], over, self.innings_det[2+i][2]-over*6)
        for j in range(self.players_count):
            self.embed['description'] += '**{}**: run:{} wkt:{}\n'.format(self.redteam[j].name, self.innings_det[4+i][j], self.innings_det[6+i][j])
        self.embed['description'] += '\n'
        if self.cur_bat_team=='red':
            i = 0
        else:
            i = 1
        over = int(self.innings_det[2+i][2]/6)
        self.embed['description'] += '**BLUE TEAM** : {} ({}.{})\n'.format(self.innings_det[2+i][0], over, self.innings_det[2+i][2]-over*6)
        for j in range(self.players_count):
            self.embed['description'] += '**{}**: run:{} wkt:{}\n'.format(self.blueteam[j].name, self.innings_det[4+i][j], self.innings_det[6+i][j])
        if self.res_msg.startswith('Draw'):
            self.embed['color'] = 16777215
        else:
            self.embed['color'] = 3925776
        return self.embed