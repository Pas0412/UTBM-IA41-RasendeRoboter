import itertools

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


Listobstacle=[['se', 'sw', 'se', 'swe', 'ew', 'swe', 'swe', 'swe', 'sw', 'se', 'swe', 'ew', 'swe', 'swe', 'swe', 'sw'],
['nse', 'swen', 'swen', 'swen', 'ovsw', 'nse', 'swen', 'swen', 'swen', 'swen', 'nsw', 'ores', 'swen', 'swen', 'swen', 'nw'], 
['nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'new', 'sw'], 
['ns', 'trne', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'swen', 'tvsw', 'ns'], 
['nse', 'swe', 'swen', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'cbnw', 'nse', 'swen', 'swen', 'swen', 'swen', 'nsw'], 
['ne', 'swen', 'swen', 'swen', 'nsw', 'cjes', 'swen', 'swen', 'swen', 'swe', 'swen', 'swen', 'swen', 'swen', 'swen', 'nsw'], 
['se', 'swen', 'swen', 'ibnw', 'nse', 'swen', 'swen', 'new', 'new', 'swen', 'swen', 'nsw', 'ijne', 'swen', 'swen', 'nsw'], 
['nse', 'swen', 'swen', 'swe', 'swen', 'swen', 'nsw', '0', '0', 'nse', 'swen', 'swen', 'swe', 'swen', 'swen', 'nsw'], 
['nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'nsw', '0', '0', 'nse', 'swen', 'swen', 'swen', 'swen', 'swen', 'nsw'], 
['nse', 'swen', 'swen', 'swen', 'nsw', 'cvne', 'swen', 'swe', 'swe', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'nsw'], 
['nse', 'obnw', 'nse', 'swen', 'swen', 'swe', 'swen', 'swen', 'swen', 'swen', 'nsw', 'ives', 'swen', 'swen', 'swen', 'nsw'], 
['nse', 'swe', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'swen', 'swen', 'new', 'swen', 'nsw', 'crne', 'swen', 'nw'], 
['ne', 'swen', 'new', 'swen', 'irsw', 'nse', 'swen', 'swen', 'swen', 'swen', 'tbsw', 'nse', 'swen', 'swe', 'swen', 'sw'], 
['se', 'swen', 'YYsw', 'nse', 'swen', 'swen', 'new', 'swen', 'swen', 'swen', 'swen', 'swen', 'ojnw', 'nse', 'swen', 'nsw'], 
['nse', 'swen', 'swen', 'swen', 'swen', 'nsw', 'tjes', 'swen', 'swen', 'swen', 'swen', 'swen', 'swe', 'swen', 'swen', 'nsw'], 
['ne', 'new', 'new', 'nw', 'ne', 'new', 'new', 'new', 'new', 'nw', 'ne', 'new', 'new', 'new', 'new', 'nw']]# liste de test 

Listobstacledym=L()
Listobstacledym.append([L])#a faire une fois au début
Listrobot=[(0,0,"b"),(5,0,"r"),(0,2,"j"),(5,2,"v")]
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
            """print(I)
            print(xtemp)
            print(ytemp)
            print("")"""
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


def getthemovtowin(listallmov,listalliamov):
    global netats
    te=listalliamov.ret()
    va=listalliamov.take(len(te)-1)
    n=va[5]
    listret=[]
    while(n!=0):
        val=listallmov.take(n-1)
        listret=[val]+listret
        n=val[4]
    listret=[listalliamov.take(0)]+listret    
    return listret



def BFS(et_debut,et_final, Listobstacle):
    Listobstacle = getthematrix(Listobstacle)
    Li=L()
    test2=L()
    test=[]
    Lt=L()
    Ba=L()
    Ba.append([et_debut])
    temp=et_debut
    temp=temp+[0,0]
    n=0
    test2.append(et_debut)
    Li.append([temp])
    a=0
    while(test2.isNot2(et_final)):
        a+=1
        if a%1000 == 0:print(a)
        temp=nextstates(temp, Listobstacle)
        Lt.append(temp)
        temp=Lt.take(n)
        test=[temp[0]]+[temp[1]]+[temp[2]]+[temp[3]]
        if(Ba.isIn2(test)):
            while(Ba.isIn2(test)):
                n=n+1
                temp=Lt.take(n)
                test=[temp[0]]+[temp[1]]+[temp[2]]+[temp[3]]
        else:
            n=n+1
        test2.new()
        test2.append(test)
        Ba.append([test])
        Li.append([temp])
        
    return (getthemovtowin(Lt,Li))

if __name__ == '__main__':
    pass
    BFS([(0,0,"b"),(15,15,"r"),(15,15,"j"),(15,15,"v")],(0,12,'b'), Listobstacle)
