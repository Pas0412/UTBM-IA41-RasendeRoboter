import itertools
import time
import json

# Liste vide
class L:
    
    def __init__(self):
        self.List=[]
        
    def __repr__(self):
        return 'List: {} (Length: {})'.format(self.List,len(self.List))
    
    
    def append(self,e):
        self.List=self.List+e

    def append2(self,e):
        self.List=e+self.List

    def isIn(self,e):
        return e in self.List

    def isIn2(self,e):
        for i in self.List:
            if e==i:
                return True
        return False
    def isNot2(self,e):
        for i in self.List:
            if e==i:
                return False
        return True
    def take(self,n):
        return self.List[n]
    def new(self):
        self.List =[]

    def ret(self):
        return self.List



Listobstacledym=L()
Listobstacledym.append([L])#a faire une fois au début

global netats
netats=0
def getthematrix(Listobstacle):
    newlist=[]
    n=len(Listobstacle)
    for e in range(n):
        newlist=newlist+Listobstacle[e]
    Listobstacle=newlist
    return Listobstacle

def inc():
    global netats
    netats=netats+1
    return netats


def movement(coordinate,mov, Listobstacle):
    #global Listobstacle
    x=coordinate[0]
    j=coordinate[1]
    color=coordinate[2]
    if mov=='north':
        
        flag0=True
        xtemp=x
        ytemp=j
        while (flag0==True):
            I=xtemp+ytemp*16
            if not("n" in Listobstacle[I]):
                flag0=False
            else:
                ytemp=ytemp-1
                I=xtemp+ytemp*16
                if not("s" in Listobstacle[I]) or Listobstacledym.isIn2([xtemp,ytemp]):
                    ytemp=ytemp+1
                    flag0=False # si case d'après obstacle faut ajouter les autres obstacle

    if mov=='south':
        flag0=True
        xtemp=x
        ytemp=j
        while (flag0==True):
            I=xtemp+ytemp*16
            if not("s" in Listobstacle[I]):# si obstacle sur la case actuelle 
                flag0=False
            else:
                ytemp=ytemp+1
                I=xtemp+ytemp*16
                if( not("n" in Listobstacle[I]) or Listobstacledym.isIn2([xtemp,ytemp])):
                    ytemp=ytemp-1
                    flag0=False # si case d'après obstacle

    if mov=='west':
        flag0=True
        xtemp=x
        ytemp=j
        while (flag0==True):
            I=xtemp+ytemp*16
            if not("w" in Listobstacle[I]):# si obstacle sur la case actuelle 
                flag0=False
            else:
                xtemp=xtemp-1
                I=xtemp+ytemp*16
                if (not("e" in Listobstacle[I])or Listobstacledym.isIn2([xtemp,ytemp])):
                    xtemp=xtemp+1
                    flag0=False # si case d'après obstacle

    if mov=='east':
        flag0=True
        xtemp=x
        ytemp=j
        while (flag0==True):
            I=xtemp+ytemp*16
            if not("e" in Listobstacle[I]):
                flag0=False
            else:
                xtemp=xtemp+1
                I=xtemp+ytemp*16
                if (not("w" in Listobstacle[I])or Listobstacledym.isIn2([xtemp,ytemp])):
                    xtemp=xtemp-1
                    flag0=False # si case d'après obstacle
    return(xtemp,ytemp,color)

def getrobotpos(robotcolor,listposrobot):
        Listobstacledym.new()
        if robotcolor=="b":
            Listobstacledym.append([[listposrobot[1][0],listposrobot[1][1]],[listposrobot[2][0],listposrobot[2][1]],[listposrobot[3][0],listposrobot[3][1]]])
            return listposrobot[0]
        if robotcolor=="r" :
            Listobstacledym.append([[listposrobot[0][0],listposrobot[0][1]],[listposrobot[2][0],listposrobot[2][1]],[listposrobot[3][0],listposrobot[3][1]]])
            return listposrobot[1]
        if robotcolor=="j":
            Listobstacledym.append([[listposrobot[0][0],listposrobot[0][1]],[listposrobot[1][0],listposrobot[1][1]],[listposrobot[3][0],listposrobot[3][1]]])
            return listposrobot[2]
        if robotcolor=="v":
            Listobstacledym.append([[listposrobot[0][0],listposrobot[0][1]],[listposrobot[1][0],listposrobot[1][1]],[listposrobot[2][0],listposrobot[2][1]]])
            return listposrobot[3]

def changerobotpos(robotcolor,listposrobot,newpos,nbactu):
        global netats
        nbprevious=nbactu
        listnewpos=[]
        inc()
        if robotcolor=="b":
            newlist=([newpos])+[listposrobot[1]]+[listposrobot[2]]+[listposrobot[3]]+[nbprevious]+[netats]
        if robotcolor=="r" :
            newlist=[listposrobot[0]]+([newpos])+[listposrobot[2]]+[listposrobot[3]]+[nbprevious]+[netats]
        if robotcolor=="j":
            newlist=[listposrobot[0]]+[listposrobot[1]]+([newpos])+[listposrobot[3]]+[nbprevious]+[netats]
        if robotcolor=="v":
            newlist=[listposrobot[0]]+[listposrobot[1]]+[listposrobot[2]]+([newpos])+[nbprevious]+[netats]
        return newlist


def movementrobot(robotcolor,robotmov,listposrobot, Listobstacle):
    nbactu=listposrobot[5]
    pos=getrobotpos(robotcolor,listposrobot)
    newpos=movement(pos,robotmov, Listobstacle)
    return (changerobotpos(robotcolor,listposrobot,newpos,nbactu))

def nextstates(actueletat, Listobstacle):
    newactueletat=[]
    l=[range(4),range(4)]
    for e in itertools.product(*l):
        if e[1]==0:robotcolor="b"
        if e[1]==1:robotcolor="r"
        if e[1]==2:robotcolor="j"
        if e[1]==3:robotcolor="v"

        if e[0]==0:robotmov="north"
        if e[0]==1:robotmov="south"
        if e[0]==2:robotmov="west"
        if e[0]==3:robotmov="east"
        newactueletat.append(movementrobot(robotcolor,robotmov,actueletat, Listobstacle))
    return newactueletat
        #faire ban list et la suite d'etat, là je fais que les transitions d'états et recherche d'état


def getthemovtowin(IAMoves):
    final = IAMoves.List[-1]
    moves = [final]
    prochain = final[4]
    for etat in reversed(IAMoves.List):
        if etat[5] == prochain:
            prochain = etat[4]
            moves.append(etat)
    return [i for i in reversed(moves)]
            


def BFS(et_debut,et_final, Listobstacle):
    Listobstacle = getthematrix(Listobstacle)
    distance_initiale, _ = mesure_distance(et_debut, et_final)
    Li=L()
    test2=L()
    test=[]
    Lt=L()
    Ba=L()
    tout_les_moves = L()
    Ba.append([et_debut])
    temp=et_debut
    temp=temp+[0,0]
    n=0
    test2.append(et_debut)
    Li.append([temp])
    a=0
    test_distance = True
    if "Y" in et_final:
        test_distance = False

    while et_final not in test2.List:
        a+=1
        #if a%1000 == 0:print(a)
        temp=nextstates(temp, Listobstacle)
        tout_les_moves.append(temp)
        new_list = []
        if test_distance:
            for i, e in enumerate(temp):
                distance, divis = mesure_distance(e, et_final)
                if (distance <= distance_initiale + 1 or divis >= distance or divis <= 4):
                    new_list.append(e)
        if new_list != []:
            temp = new_list

        Lt.append(temp)
        temp=Lt.List[n]
        test=temp[0:4]
        if test in Ba.List: #(Ba.isIn2(test)):
            while test in Ba.List: #(Ba.isIn2(test)):
                n+=1
                temp=Lt.List[n]
                test=temp[0:4]
        else:
            n+=1

        test2.new()
        test2.append(test)
        Ba.append([test])
        Li.append([temp])

    return getthemovtowin(Li)





def mesure_distance(etat, etat_final):
    # crée une distance moyenne avec un coefficient important sur la distance du robot concerné par la cible.
    tot=0
    divis = 0
    for i in etat[0:4]:
        distance = ((i[0] - etat_final[0])**2 + (i[1] - etat_final[1])**2)**0.5 # distance du robot par rapport a la cible
        if i[2] == etat_final[2]:
            divis = distance
        else:
            tot += distance

    return ((tot + divis * 10) / 13, divis)






if __name__ == '__main__':

    BOARD = [['se', 'sw', 'se', 'swe', 'ew', 'swe', 'swe', 'swe', 'sw', 'se', 'swe', 'ew', 'swe', 'swe', 'swe', 'sw'], ['nse', 'swen', 'swen', 'swen', 'ovsw', 'nse', 'swen', 'swen', 'swen', 'swen', 'nsw', 'ores', 'swen', 'swen', 'swen', 'nw'], ['nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'new', 'sw'], ['ns', 'trne', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'tvsw', 'ns'], ['nse', 'swe', 'swen', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'cbnw', 'nse', 'swen', 'swen', 'swen', 'swen', 'nsw'], ['ne', 'swen', 'swen', 'swen', 'nsw', 'cjes', 'swen', 'swen', 'swen', 'swe', 'swen', 'swen', 'swen', 'swen', 'swen', 'nsw'], ['se', 'swen', 'swen', 'ibnw', 'nse', 'swen', 'swen', 'new', 'new', 'swen', 'swen', 'nsw', 'ijne', 'swen', 'swen', 'nsw'], ['nse', 'swen', 'swen', 'swe', 'swen', 'swen', 'nsw', '0', '0', 'nse', 'swen', 'swen', 'swe', 'swen', 'swen', 'nsw'], ['nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'nsw', '0', '0', 'nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'nsw'], ['nse', 'swen', 'swen', 'swen', 'nsw', 'cvne', 'swen', 'swe', 'swe', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'nsw'], ['nse', 'obnw', 'nse', 'swen', 'swen', 'swe', 'swen', 'swen', 'swen', 'swen', 'nsw', 'ives', 'swen', 'swen', 'swen', 'nsw'], ['nse', 'swe', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'swen', 'swen', 'new', 'swen', 'nsw', 'crne', 'swen', 'nw'], ['ne', 'swen', 'new', 'swen', 'irsw', 'nse', 'swen', 'swen', 'swen', 'swen', 'tbsw', 'nse', 'swen', 'swe', 'swen', 'sw'], ['se', 'swen', 'YYsw', 'nse', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'swen', 'swen', 'ojnw', 'nse', 'swen', 'nsw'], ['nse', 'swen', 'swen', 'swen', 'swen', 'nsw', 'tjes', 'swen', 'swen', 'swen', 'swen', 'swen', 'swe', 'swen', 'swen', 'nsw'], ['ne', 'new', 'new', 'nw', 'ne', 'new', 'new', 'new', 'new', 'nw', 'ne', 'new', 'new', 'new', 'new', 'nw']]

    with open("transfert", "r") as f:
        fichier = f.read().replace("'", '"').replace("(", "[").replace(")", "]")
    
    robots = json.loads(str(fichier.split('||')[0]))
    target = json.loads(fichier.split('||')[1])
    res = BFS([tuple(i) for i in robots], tuple(target), BOARD)
    with open("reponse", "w") as f:
        f.write(str(res))




# regler le probleme du mauvais nombre de coups

