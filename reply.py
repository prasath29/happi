import datetime
import random
import dialo

tt = ['Maths\nBEEE\nEVS\nEG\nData Structures\n',
 'EG\nEG\nBEEE\nData Structures\nDigital Electronics\n',
 'EVS\nData Structures\nMaths\nDigital Electronics\nBEEE\n',
 'Data Structures\nMaths\nDigital Electronics\nEG\nEG\n',
 'Digital Electronics\nEVS\nMaths\nData Structures Lab\nData Structures Lab\n',
 'BEEE\nMaths\nDigital Electronics\nPython\nPython\n',
 'It\'s sunday. Enjoy!']


def reply(msg, message, dat):
    #time table operation
    if msg.startswith('tt'):
        day = dat.weekday()
        msg = msg.split(' ')
        if len(msg)>1:
            di = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6, 'tmr':day+1, 'yst':day-1}
            if msg[1] in di:
                return tt[di[msg[1]]]
            else:
                return 'Invalid request\nTry \'hp tt mon\''
        else:
            return tt[day]
    #period operatoin
    elif msg.startswith('prd'):
        day = dat.weekday()
        msg = msg.split(' ')
        tim = dat.time()
        if day==7:
            return 'This is sunday.... funday... enjoy'
        else:
            pr = tt[day].split('\n')
            pr.pop()
            ti = [[9,0,10,0],[10,15,11,15],[11,30,12,30],[13,30,14,30],[14,45,15,45]]
            i=-0.5
            for j in range(5):
                if datetime.datetime.strptime(str(ti[j][0])+' '+str(ti[j][1]), '%H %M').time()<=tim:
                    i=j+0.5
                if i==j+0.5 and tim<=datetime.datetime.strptime(str(ti[j][2])+' '+str(ti[j][3]), '%H %M').time():
                    i=j
            if len(msg)>1:
                if msg[1]=='be' and i==-0.5:
                    return 'Class not yet started'
                elif msg[1]=='ne'and i==4.5:
                    return 'Class is over'
                di={'ne':int(i+1), 'be':int(i)}
                if msg[1] in di:
                    return pr[di[msg[1]]]
                else:
                    return 'Invalid request\nTry \'hp prd ne\''
            else:
                if i==-0.5:
                    return 'Class yet to begin'
                elif i==4.5:
                    return 'Class is over'
                elif i==int(i):
                    return pr[i]
                else:
                    return 'Break'
    #dialoga gpt replies
    else:
        return dialo.reply(msg, message)