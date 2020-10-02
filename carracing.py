import pygame
import random
import threading
import time
import RPi.GPIO as GPIO
buttonleft=21
buttonright=20
relay=26
kickcoin=19
atick=13
stick=6
gar=16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relay,GPIO.OUT)
GPIO.setup(atick,GPIO.OUT)
GPIO.setup(stick,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(kickcoin,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(buttonleft,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(buttonright,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(gar,GPIO.IN,GPIO.PUD_UP)
GPIO.output(atick,False)
GPIO.output(relay,False)
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 50, True)
win = pygame.display.set_mode((1360,768))
pygame.display.set_caption("Car Racing")
khungready = pygame.image.load('/home/pi/newgame/khungok.png')
background = pygame.image.load('/home/pi/newgame/background.jpg')
#bg1 = pygame.image.load('/home/pi/newgame/bg1.png')
bgline = pygame.image.load('/home/pi/newgame/8.png')
car = pygame.image.load('/home/pi/newgame/car.png')
boom =pygame.mixer.Sound('/home/pi/newgame/ting.wav')
music = pygame.mixer.music.load('/home/pi/newgame/bgmusic.mp3')
insertcoin=pygame.mixer.Sound('/home/pi/newgame/insertcoin.wav')
readysound=pygame.mixer.Sound('/home/pi/newgame/readysound.wav')
garup=pygame.mixer.Sound('/home/pi/newgame/gar.wav')
g1 = pygame.image.load('/home/pi/newgame/g1.png')
g2 = pygame.image.load('/home/pi/newgame/g2.png')
g3 = pygame.image.load('/home/pi/newgame/g3.png')
g4 = pygame.image.load('/home/pi/newgame/g4.png')
g5 = pygame.image.load('/home/pi/newgame/g5.png')
e1 = pygame.image.load('/home/pi/newgame/e1.png')
e2 = pygame.image.load('/home/pi/newgame/e2.png')
e3 = pygame.image.load('/home/pi/newgame/e3.png')
e4 = pygame.image.load('/home/pi/newgame/e4.png')
e5 = pygame.image.load('/home/pi/newgame/e5.png')
pygame.mixer.music.play(-5)
score=0
showtic=''
global opengar
opengar=True
global heso
heso=3
global curtime
curtime=0
ticket=''
run=True
minticket=20
timeshowticket=5
curtimetic=0
timeshowready=5
curtimeready=0
sready=''
demomessage='Demo Play'
lsline=[]
gifts=[]
effects=[]
class myplayer(object):
    def __init__(self,pltime,ctime,stime,coin,startgame,showticket,allowmove,left,right,ready,ticket,demo):
        self.playtime=pltime
        self.counttime=ctime
        self.showtime=stime
        self.coin=coin
        self.startgame=startgame
        self.showticket=showticket
        self.allowmovecar=allowmove
        self.isleft=left
        self.isright=right
        self.ready=ready
        self.ticket=ticket
        self.demo=demo
class Gifclass(object):
    def __init__(self,x,y,width,height,img,vel,startp):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.img=img
        self.vel=vel
        self.startpos = startp
    def draw(self,win):
        win.blit(self.img,(self.x,self.y))
        
    def moveup(self):
        if(self.y<550):
            self.y+=self.vel
        else:
            self.y = self.startpos
class bgimage(object):
    def __init__(self,x,y,width,height,img,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.img=img
        self.vel=vel
       
    def draw(self,win):
        win.blit(self.img,(self.x,self.y))
    def moveup(self):
        if(self.y<600):
            self.y+=self.vel
        else:                         
            self.y=350
class playerinfo(object):
    def __init__(self):       
        self.returntick=0      
        self.tradiem=False
        self.readticket=0
        self.ticket=0
        
playinfo = playerinfo()
mplayer = myplayer(60,0,0,0,False,False,False,False,False,False,0,False)
mycar = bgimage(50,450,300,300,car,10)
mykhung = bgimage(565,330,300,300,khungready,1)  
myline = bgimage(400,350,553,208,bgline,15)
myg1 = Gifclass(500,150,100,100,g1,5,100)
myg2 = Gifclass(280,120,100,100,g2,4,120)
myg3 = Gifclass(550,110,100,100,g3,5,110)
myg4 = Gifclass(980,90,100,100,g4,4,90)
myg5 = Gifclass(1080,80,100,100,g5,5,80)
gifts.append(myg1)
gifts.append(myg2)
gifts.append(myg3)
gifts.append(myg4)
gifts.append(myg5)
mye1 = Gifclass(0,-100,110,110,e1,5,0)
mye2 = Gifclass(0,-100,110,110,e2,3,0)
mye3 = Gifclass(0,-100,110,110,e3,2,0)
mye4 = Gifclass(0,-100,110,110,e4,4,0)
mye5 = Gifclass(0,-100,110,110,e5,3,0)
effects.append(mye1)
effects.append(mye2)
effects.append(mye3)
effects.append(mye4)
effects.append(mye5)
lsline.append(myline)
rd=-1
mplayer.demo=True

def moveleftmycar():
    if mycar.x >100:
        mycar.x-=20        
        
def moverightmycar():
    if mycar.x <1000:
        mycar.x+=20        
        
def redrawGameWindow():
    win.blit(background,(0,0))    
    
    myline.draw(win)
    
    for g in gifts:
        g.draw(win)  
    
    for e in effects:
        e.draw(win)
        
    mycar.draw(win)   
    
    txtscore = font.render('Score: ' + str(mplayer.ticket), 1, (255,255,255))
    txtplaytime = font.render('Time: ' + str(mplayer.showtime), 1, (255,0,0))
    txtcoin = font.render('Coin: ' + str(mplayer.coin), 1, (255,255,255))
    txtticket = font.render(str(showtic), 1, (0,255,0))
    txtready = font.render(str(sready), 1, (255,0,0))
    txtdemo = font.render(str(demomessage),1,(255,0,0))
    mykhung.draw(win)  
  
    win.blit(txtdemo, (580, 350))
    win.blit(txtscore, (1120, 35))
    win.blit(txtplaytime,(85,35))
    win.blit(txtcoin,(90,650))
    win.blit(txtticket,(580,350))
    win.blit(txtready,(600,350))
    
    pygame.display.update()
def checkticket(num):   
    while True:
        if num<=0:
            if playinfo.readticket<1:
                playinfo.tradiem=False
                GPIO.output(atick,False)
            break    
        num-=1
        pygame.time.delay(1000)   
def returnticket(tk):
    playinfo.ticket=tk
    playinfo.readticket=0
    playinfo.tradiem=True
    GPIO.output(atick,True)
    threadcheckticket=threading.Thread(target=checkticket,name='checkticket',args=[5])
    threadcheckticket.start()
    while playinfo.tradiem:
        if playinfo.readticket>=playinfo.ticket:
            playinfo.tradiem=False
            GPIO.output(atick,False)
        if GPIO.input(stick)==False:
            pygame.time.delay(150)
            playinfo.readticket+=1
def tinhticket(tk):
    global heso
    global minticket
    myticket = tk/heso
    if myticket<minticket:
        myticket=minticket
    return round(myticket)
def Checkcoin():   
    if mplayer.startgame==False:
        global demomessage
        if(mplayer.coin>0):
            mplayer.coin-=1
            mplayer.ready=True
            mplayer.demo=False
            mplayer.ticket=0
            mycar.x=550
            demomessage=''
            readysound.play()
            if len(gifts)>0:
                Destroyallgift()
        
def Rundemo():
    if mplayer.demo: 
        Checkgift()
        MoveCarDemo()
        if mycar.x <=100:
            mplayer.isleft=False
            mplayer.isright=True
        elif mycar.x>=1000:
            mplayer.isleft=True
            mplayer.isright=False
        
def Rungame():
    global curtime
    if mplayer.startgame:
        if mplayer.counttime>0:            
            if pygame.time.get_ticks()-curtime >1000:
                curtime = pygame.time.get_ticks()
                mplayer.counttime-=1
                mplayer.showtime=round(mplayer.counttime)
        else:                      
            mplayer.showticket=True
            mplayer.allowmovecar=False
            mycar.x=1010
            GPIO.output(relay,False)           
            
def Destroyallgift():
    for g in gifts:
        gifts.pop(gifts.index(g))
def Movegift():    
        for g in gifts:
            g.moveup()
            if g.y>550:
                gifts.pop(gifts.index(g))

        if len(gifts)<4:
            rd = random.randrange(5)
            if rd==0:
                gifts.append(myg1)
            elif rd==1:
                gifts.append(myg2)
            elif rd==2:
                gifts.append(myg3)
            elif rd==3:
                gifts.append(myg4)           
            elif rd==4:
                gifts.append(myg5)  

def Checkgift():         
     for g in gifts:
         if g.y>400 and g.y <500:
             gifpos = g.x+ g.width/2
             carpos = mycar.x +mycar.width
             if gifpos>mycar.x and gifpos<carpos:
                 gindex = gifts.index(g)
                 gifts.pop(gindex) 
                 mplayer.ticket+=1
                 effects[gindex].y =350
                 effects[gindex].x = mycar.x + (mycar.width/4)
                 boom.play()
                 destroyef = threading.Thread(target=Refreshef)
                 destroyef.start()

def Refreshef():
    time.sleep(.3)
    for e in effects:
        if e.y>0:
            e.y=-100

def MoveCar():   
    if mplayer.allowmovecar:
        if mplayer.isleft:           
            moveleftmycar()
        if mplayer.isright:
            moverightmycar()
            
def MoveCarDemo(): 
    if mplayer.isleft:           
        if mycar.x >100:
            mycar.x-=10 
    if mplayer.isright:
        if mycar.x <1000:
            mycar.x+=10 
def Showreadytime():
    global timeshowready
    global curtimeready
    global curtime
    global sready
    if mplayer.ready:
        if pygame.time.get_ticks()-curtimeready>1000:
            curtimeready = pygame.time.get_ticks()
            timeshowready-=1
            sready = 'Ready ' + str(timeshowready)

        if timeshowready==0:
            sready=''
            curtime = pygame.time.get_ticks()
            mplayer.ready=False
            mplayer.counttime=mplayer.playtime
            mplayer.startgame=True
            mplayer.allowmovecar=True
            timeshowready=5
            mykhung.y=-100
            GPIO.output(relay,True)
            pygame.mixer.music.stop()
            music = pygame.mixer.music.load('/home/pi/newgame/playing.mp3')
            pygame.mixer.music.play(-10)                       
     
def Showticket():
    if mplayer.showticket:
        global showtic
        global timeshowticket
        global curtimetic
        global demomessage        
        Destroyallgift()
        if pygame.time.get_ticks()-curtimetic>1000:
            curtimetic=pygame.time.get_ticks()
            timeshowticket-=1
            
        if timeshowticket ==4:
            mykhung.y=330            
            custic= tinhticket(mplayer.ticket)
            showtic = 'Tickets ' + str(custic)
            returnticket(custic)
            # payout ticket
        if timeshowticket <=0:  
            mplayer.ticket=0
            timeshowticket=5
            mplayer.showticket=False
            showtic=''
            mplayer.demo=True
            demomessage='Demo Play'
            mplayer.startgame=False
            pygame.mixer.music.stop()
            music = pygame.mixer.music.load('/home/pi/newgame/bgmusic.mp3')
            pygame.mixer.music.play(-5)
def checkcointhread():
    while True:       
        if mplayer.startgame:  
            checkbutton()
        if GPIO.input(kickcoin)==False:
            pygame.mixer.music.stop()
            insertcoin.play()
            time.sleep(.3)
            mplayer.coin+=1
        time.sleep(.1)
def checkbutton():
    global opengar
    if GPIO.input(buttonleft)==False:
        mplayer.isleft=True       
    else:
        mplayer.isleft=False

    if GPIO.input(buttonright)==False:
        mplayer.isright=True       
    else:
        mplayer.isright=False
    if opengar:
        if GPIO.input(gar)==False:
            opengar=False            
            garup.play()
    if GPIO.input(gar)==True:
        opengar=True
        
cointhread=threading.Thread(target=checkcointhread,name="checkcoin")
cointhread.start()
while run:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT:
                    mplayer.isleft=True
                    mplayer.isright=False                
                if event.key ==pygame.K_RIGHT:
                    mplayer.isleft=False
                    mplayer.isright=True                
                    
        if event.type == pygame.KEYUP:
                if event.key ==pygame.K_x:
                    mplayer.coin+=1
                if event.key ==pygame.K_LEFT:
                    mplayer.isleft=False
                if event.key ==pygame.K_RIGHT:
                    mplayer.isright=False                

    if mplayer.startgame:
        if mplayer.allowmovecar:
            Checkgift()
            #checkbutton()
    #checkcointhread()
    myline.moveup()  
    Movegift()    
    Rundemo()
    Showreadytime()
    Checkcoin()
    Rungame()
    Showticket()
    MoveCar()
    redrawGameWindow()
    clock.tick(30)
    
pygame.quit()
