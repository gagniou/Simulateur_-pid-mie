import pygame
from random import *
from pygame.locals import *
from math import sqrt

timer=0
continuer=1

fps=30

nb_cycle=0

number=1000 #population
R=0.025 #taux de contagion
#le vrai R = number/64 (nb lieu) *recovery(temps de contagion) * R(taux de contagion)
D=0.0001#taux de décés
V=0.0005 #taux de vaccination
recovery=10 #temps avant guérison
imunity=20 #temps d'imunité aprés guérison en nb cycle ( -1 : infini )
vaccinate=70 #temps de vaccination en nbde cycle (-1 : infini )

Item_ID=0
moving=0
liste_Item=[]
liste_graphe=[]
###############################################################################################################################################

class Item():
    def __init__(self,x,y,taille,couleur,ID):
        self.id=ID
        self.centre_x=x
        self.centre_y=y
        
        self.taille=taille

        self.couleurRGB=couleur
    def change_color(r,g,b):
        self.couleurRGB=(r,g,b)
        
    def dist(self,other):
        return sqrt((self.centre_x-other.centre_x)*(self.centre_x-other.centre_x)+(self.centre_y-other.centre_y)*(self.centre_y-other.centre_y))
        
###############################################################################################################################################
        
class poid(Item):
    def __init__(self,ID,food):
        self.house=randint(0,63)
        housebloc=self.house//4

        x=100
        x+=(housebloc%4*150)
        y=100
        y+=(housebloc//4*150)

        houseplace=self.house%4
        houseplacex=houseplace%2
        houseplacey=houseplace//2

        x+=houseplacex*50
        y+=houseplacey*50
        
        x+=randint(-20,20)
        y+=randint(-20,20)

        self.vitesse_x=0
        self.vitesse_y=0

        self.target_x=0
        self.target_y=0
        
        self.direction=0
        
        self.energie=2000
        self.status=0 #0 healthy , 1 sick , 2 cured , 3 vaccinated, 4 dead
        self.time=0
        self.move=0
        self.step=0  #0start 1 door 2 street 3othet door 4 arrived
        
        self.target=0
        self.vitesse=8
        
        Item.__init__(self,x,y,8,(8,50,150),ID)
        

    def death(self):
        self.status=4
        self.couleurRGB=(0,0,0)
        
    def sick(self):
        self.status=1
        self.couleurRGB=(150,50,8)

    def vaccine(self):
        self.status=3
        self.couleurRGB=(8,150,8)
        
    def in_house(self):# dans une maison
        x=self.centre_x
        y=self.centre_y
        if x<675 and y<675:
            x-=75
            y-=75

            if x%150<100 and y%150<100:
                return 1
        
        return 0

    def action(self):
        if self.step==0:
            self.goto_door()
            if self.in_house()==0:
                self.step+=1
                if self.direction==1:
                    self.target_x=self.centre_x
                    self.target_y=self.centre_y+25
                else :
                    self.target_x=self.centre_x
                    self.target_y=self.centre_y-25

                    
        elif self.step==1:
            self.goto(self.target_x,self.target_y)
            if (self.target_x-2<self.centre_x<self.target_x+2):
                if (self.target_y-2<self.centre_y<self.target_y+2):
                    self.step+=1
                    self.vitesse_x=0
                    self.vitesse_y=0
                    houseplace=self.house%4
                    houseplacex=houseplace%2
                    if houseplacex==1:
                        self.target_x=self.centre_x+50
                    else:
                        self.target_x=self.centre_x-50

                        
        elif self.step==2:
            self.goto(self.target_x,self.target_y)
            if (self.target_x-2<self.centre_x<self.target_x+2):
                if (self.target_y-2<self.centre_y<self.target_y+2):
                    self.step+=1
                    self.vitesse_x=0
                    self.vitesse_y=0
                    y=50
                    housebloc=self.target//4
                    housebloc=housebloc//4
                    y+=housebloc*150

                    houseplace=self.target%4
                    houseplacey=houseplace//2
                    y+=houseplacey*150
                    
                    self.target_y=y
                    self.target_x=self.centre_x
        elif self.step==3:
            self.goto(self.target_x,self.target_y)
            if (self.target_x-5<self.centre_x<self.target_x+5):
                if (self.target_y-5<self.centre_y<self.target_y+5):
                    self.step+=1
                    self.vitesse_x=0
                    self.vitesse_y=0
                    x=50
                    housebloc=self.target//4
                    housebloc=housebloc%4
                    x+=housebloc*150

                    houseplace=self.target%4
                    houseplacex=houseplace%2
                    x+=houseplacex*150
                    
                    self.target_x=x
                    self.target_y=self.centre_y
        elif self.step==4:
            self.goto(self.target_x,self.target_y)
            if (self.target_x-5<self.centre_x<self.target_x+5):
                if (self.target_y-5<self.centre_y<self.target_y+5):
                    self.step+=1
                    self.vitesse_x=0
                    self.vitesse_y=0

                    houseplace=self.target%4
                    houseplacex=houseplace%2
                    if houseplacex==1:
                        self.target_x=self.centre_x-50
                    else:
                        self.target_x=self.centre_x+50
        elif self.step==5:
            self.goto(self.target_x,self.target_y)
            if (self.target_x-5<self.centre_x<self.target_x+5):
                if (self.target_y-5<self.centre_y<self.target_y+5):
                    self.step+=1
                    self.vitesse_x=0
                    self.vitesse_y=0

                    
                    houseplace=self.target%4
                    houseplacey=houseplace//2
                    if houseplacey==1:
                        self.target_y=self.centre_y-50
                    else:
                        self.target_y=self.centre_y+50

                    x=randint(-20,20)
                    y=randint(-20,20)

                    self.target_y+y
                    self.target_x+x

        elif self.step==6:
            self.goto(self.target_x,self.target_y)
            if (self.target_x-5<self.centre_x<self.target_x+5):
                if (self.target_y-5<self.centre_y<self.target_y+5):
                    self.step+=1
                    self.vitesse_x=0
                    self.vitesse_y=0

        else:
            self.house=self.target
        self.movement()

    def goto_door(self):
        housebloc=self.house//4

        x=100
        x+=(housebloc%4*150)
        y=100
        y+=(housebloc//4*150)

        houseplace=self.house%4
        houseplacex=houseplace%2
        houseplacey=houseplace//2

        if houseplacey==1:
            #bot
            y+=80
            self.direction=1
        else :
            #top
            y-=30
            self.direction=2
        if houseplacex==1:
            x+=50

        self.goto(x,y)
        
    def goto(self,x,y):
        x=self.centre_x-x
        y=self.centre_y-y
        if x!=0 or y!=0:
            if abs(x)+abs(y)>20:
                self.vitesse_x=abs(x)/(abs(x)+abs(y))*30
                self.vitesse_y=abs(y)/(abs(x)+abs(y))*30
            elif 20>abs(x)+abs(y)>8:
                self.vitesse_x=abs(x)/(abs(x)+abs(y))*16
                self.vitesse_y=abs(y)/(abs(x)+abs(y))*16
            elif 8>abs(x)+abs(y)>4 :
                self.vitesse_x=abs(x)/(abs(x)+abs(y))*6
                self.vitesse_y=abs(y)/(abs(x)+abs(y))*6
            elif 4>abs(x)+abs(y)>2 :
                self.vitesse_x=abs(x)/(abs(x)+abs(y))*3
                self.vitesse_y=abs(y)/(abs(x)+abs(y))*3
            else :
                self.vitesse_x=abs(x)/(abs(x)+abs(y))*1
                self.vitesse_y=abs(y)/(abs(x)+abs(y))*1
            if x>0:
                self.vitesse_x*=-1
            if y>0:
                self.vitesse_y*=-1
        else:
            self.vitesse_x=0
            self.vitesse_y=0

            
    def movement(self):
        self.centre_x+=self.vitesse_x
        self.centre_y+=self.vitesse_y
"""
    def meet(self,other):
        global R
        if self.house==other.house:
            if self.status==1:
                if other.status==1:
                    return
                elif other.status==0:
                    x=randint(0,100)/100
                    if x<R:
                        other.status=1
            elif other.status==1:
                if self.status==1:
                    return
                elif self.status==0:
                    x=randint(0,100)/100
                    if x<R:
                        self.status=1
"""
    
###############################################################################################################################################
def draw_blocs(fenetre):
    p1x=75
    p1y=75
    for i in range(4):
        for j in range(4):
            #house bloc
            pygame.draw.line(fenetre,(0,0,0),(p1x,p1y),(p1x+100,p1y),1)
            pygame.draw.line(fenetre,(0,0,0),(p1x,p1y),(p1x,p1y+100),1)
            pygame.draw.line(fenetre,(0,0,0),(p1x+100,p1y+100),(p1x+100,p1y),1)
            pygame.draw.line(fenetre,(0,0,0),(p1x+100,p1y+100),(p1x,p1y+100),1)
            
            pygame.draw.line(fenetre,(0,0,0),(p1x+50,p1y),(p1x+50,p1y+100),1)
            pygame.draw.line(fenetre,(0,0,0),(p1x,p1y+50),(p1x+100,p1y+50),1)

            #door_street
            pygame.draw.line(fenetre,(150,150,150),(p1x+25,p1y),(p1x+25,p1y-25),1)
            pygame.draw.line(fenetre,(150,150,150),(p1x+75,p1y),(p1x+75,p1y-25),1)
            pygame.draw.line(fenetre,(150,150,150),(p1x+25,p1y+100),(p1x+25,p1y+125),1)
            pygame.draw.line(fenetre,(150,150,150),(p1x+75,p1y+100),(p1x+75,p1y+125),1)
            p1x += 150
        p1y += 150
        p1x=75
        
    for i in range(5):
        pygame.draw.line(fenetre,(150,150,150),(50+i*150,50),(50+i*150,650),1)
        pygame.draw.line(fenetre,(150,150,150),(50,50+i*150),(650,50+i*150),1)
            

            
def init():
    global Item_ID,number
    for i in range(number):
        liste_Item.append(poid(Item_ID,1))
        Item_ID+=1
    for i in liste_Item:
         i.target=randint(0,63)
    liste_Item[int(number/2)].sick()
    liste_Item[int(number/2)+1].sick()

def cycle():
    global nb_cycle,action,recovery,imunity,Item_ID,number
    nb_cycle+=1

    for i in liste_Item:
        i.move=0
        i.step=0
        i.direction=0
        i.target=randint(0,63)
        
        if i.status==1:         #sick
            i.time+=1
            if i.time>=recovery:
                i.time=0
                i.status=2
                i.couleurRGB=(180,180,180)
            else:
                rand=random()
                if rand<D:
                    i.death()

                    
        if i.status==2:         #recover
            i.time+=1
            if i.time>=imunity:
                i.time=0
                i.status=0
                i.couleurRGB=(8,50,150)

                
        if i.status==0:         #healthy
            for j in liste_Item:
                if j.house==i.house:
                    if j.status==1:
                        rand=random()
                        if rand<R:
                            i.sick()
            if i.status==0:
                rand=random()
                if rand<V:
                    i.vaccine()

        if i.status==3:
            i.time+=1
            if i.time>=vaccinate:
                i.time=0
                i.status=0
                i.couleurRGB=(8,50,150)
    nb_sain=0
    nb_sick=0
    nb_recover=0
    nb_vaccine=0
    nb_dead=0

    for i in liste_Item:
        if i.status==0:
            nb_sain+=1
        elif i.status==1:
            nb_sick+=1
        elif i.status==3:
            nb_vaccine+=1
        elif i.status==4:
            nb_dead+=1
        else:
            nb_recover+=1
    if len(liste_graphe)>1:
        liste_graphe.append((nb_sain,nb_sick,nb_recover,nb_vaccine,liste_graphe[len(liste_graphe)-1][4]+nb_dead))
    else:
        liste_graphe.append((nb_sain,nb_sick,nb_recover,nb_vaccine,0))

        # birth ###############################################
    birth=randint(0,int((number-nb_dead)/100))
    number+=birth
    for i in range(birth):
        liste_Item.append(poid(Item_ID,1))
        Item_ID+=1
        liste_Item[len(liste_Item)-1].target=randint(0,63)


    #######################################################
        

def graphe(nb_cycle,nbitem,fenetre,font_s):

    sain=(8,50,150)
    sick=(150,50,8)
    recover=(180,180,180)
    dead=(0,0,0)
    vaccine=(8,150,8)
    
    x=751
    y=299
    taillel=600/nb_cycle
    tailleh=250/nbitem
    for i in liste_graphe :
        if i==liste_graphe[len(liste_graphe)-1]:
            tdead=font_s.render(str(liste_graphe[len(liste_graphe)-1][4]),1,(0,0,0),0)
            tsain=font_s.render(str(liste_graphe[len(liste_graphe)-1][0]),1,(8,50,150),0)
            tsick=font_s.render(str(liste_graphe[len(liste_graphe)-1][1]),1,(150,50,8),0)
            trecover=font_s.render(str(liste_graphe[len(liste_graphe)-1][2]),1,(150,150,150),0)
            tvaccin=font_s.render(str(liste_graphe[len(liste_graphe)-1][3]),1,(8,150,8),0)

            total=font_s.render(str(number),1,(0,0,0),0)
        else:
            tdead=font_s.render('',1,(0,0,0),0)
            tsain=font_s.render('',1,(8,50,150),0)
            tsick=font_s.render('',1,(150,50,8),0)
            trecover=font_s.render('',1,(150,150,150),0)
            tvaccin=font_s.render('',1,(8,150,8),0)

            total=font_s.render('',1,(0,0,0),0)
            
        
        fenetre.blit(total,(730,30))
        
        pygame.draw.rect(fenetre, dead, pygame.Rect(x,y,taillel+1,-i[4]*tailleh), 0)
        y-=i[4]*tailleh
        fenetre.blit(tdead,(1365,y))
        
        pygame.draw.rect(fenetre,sick,pygame.Rect(x,y,taillel+1,-i[1]*tailleh),0)
        y-=i[1]*tailleh
        fenetre.blit(tsick,(1365,y-5))
        
        pygame.draw.rect(fenetre, recover, pygame.Rect(x,y,taillel+1,-i[2]*tailleh), 0)
        y-=i[2]*tailleh
        fenetre.blit(trecover,(1365,y-10))
        
        pygame.draw.rect(fenetre, sain, pygame.Rect(x,y,taillel+1,-i[0]*tailleh), 0)
        y-=i[0]*tailleh
        fenetre.blit(tsain,(1365,y))
        
        pygame.draw.rect(fenetre,vaccine,pygame.Rect(x,y,taillel+1,-i[3]*tailleh), 0)
        y-=i[3]*tailleh
        fenetre.blit(tvaccin,(1365,y-10))
        
        x+=taillel
        y=299


###############################################################################################################################################
        
def main():
    global number,R,D,V,recovery,imunity,vaccinate
    pygame.init()
    fenetre = pygame.display.set_mode((1400, 700))
    pygame.display.set_caption("Simulateur")
    
    timer=0
    continuer=1
    pause=0

    
    nbcycle=0
    cycle_fin=1
    
    clock=pygame.time.Clock()

    font=pygame.font.SysFont("comicsansms",18,bold=False,italic=False)
    font_s=pygame.font.SysFont("comicsansms",12,bold=False,italic=False)
    font_xs=pygame.font.SysFont("comicsansms",8,bold=False,italic=False)
    #image
    pauseimg = pygame.image.load('../image/pause.png').convert()
    playimg = pygame.image.load('../image/play.png').convert()
    Di = pygame.image.load('../image/D.png').convert()
    Ri = pygame.image.load('../image/R.png').convert()
    Vi = pygame.image.load('../image/V.png').convert()
    I = pygame.image.load('../image/Imunity.png').convert()
    N = pygame.image.load('../image/Number.png').convert()
    Reco = pygame.image.load('../image/recovery.png').convert()
    Vacc = pygame.image.load('../image/Vaccin.png').convert()

    init()
    while continuer:
        #affichage image fond
        pygame.draw.rect(fenetre,(120,120,120),(0,0,700,700),0)
        pygame.draw.rect(fenetre,(50,50,50),(700,0,700,700),0)
        pygame.draw.line(fenetre,(0,0,0),(700,0),(700,700),2)

        #graphe
        pygame.draw.line(fenetre,(0,0,0),(750,300),(1350,300),2)
        pygame.draw.line(fenetre,(0,0,0),(750,50),(750,300),2)



        #dessin bloc et rue:
        draw_blocs(fenetre)

        
        
        if cycle_fin==1:
            cycle_fin=0
            nbcycle+=1
            cycle()
            
            
        for event in pygame.event.get():
            if event.type==QUIT:
                continuer=0
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    continuer=0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 330<event.pos[1]<350:
                        if 750<event.pos[0]<790:
                            pause+=1
                            pause=pause%2
                    elif 360<event.pos[1]<380:
                        if 850<event.pos[0]<950:
                            if 910<event.pos[0]<930: #+
                                liste_Item.append(poid(Item_ID,1))
                                Item_ID+=1
                                number+=1
                            elif 930<event.pos[0]:#-
                                x=randint(0,number)
                                liste_Item.remove(liste_Item[x])
                                number-=1
                                
                    elif 390<event.pos[1]<410:
                        if 750<event.pos[0]<850:
                            if 810<event.pos[0]<830:
                                recovery+=1
                            elif 830<event.pos[0]:
                                recovery-=1
                        if 950<event.pos[0]<1050:
                            if 1010<event.pos[0]<1030:
                                R+=0.001
                            elif 1030<event.pos[0]:
                                R-=0.001
                    elif 420<event.pos[1]<440:
                        if 750<event.pos[0]<850:
                            if 810<event.pos[0]<830:
                                imunity+=1
                            elif 830<event.pos[0]:
                                imunity-=1
                        if 950<event.pos[0]<1050:
                            if 1010<event.pos[0]<1030:
                                D+=0.0001
                            elif 1030<event.pos[0]:
                                D-=0.0001

                    elif 450<event.pos[1]<470:
                        if 750<event.pos[0]<850:
                            if 810<event.pos[0]<830:
                                vaccinate+=1
                            elif 830<event.pos[0]:
                                vaccinate-=1
                        if 950<event.pos[0]<1050:
                            if 1010<event.pos[0]<1030:
                                V+=0.0001
                            elif 1030<event.pos[0]:
                                V-=0.0001
                    
                        

        move=0
        if pause==0:
            for i in liste_Item:
                if i.status!=4:
                    if i.target!=i.house:
                        i.action()
                    else:
                        i.move=1
                        move+=1
                else:
                    i.move=1
                    move+=1
                    liste_Item.remove(i)
               
        for i in liste_Item:
            pygame.draw.rect(fenetre,i.couleurRGB,(i.centre_x-i.taille/2,i.centre_y-i.taille/2,i.taille,i.taille),0)

        if move==len(liste_Item):
            cycle_fin=1
        #affichage image 
        timer=timer+1
        text=font.render(str(timer),1,(255,255,0))
        fenetre.blit(text,(2,2))
        textnbcycle=font_s.render(str(nbcycle),1,(0,0,0))
        
        fenetre.blit(textnbcycle,(1345,305))
        
        graphe(nbcycle,number,fenetre,font_s)
        if pause==0:
            fenetre.blit(pauseimg,(750,330))
        else :
            fenetre.blit(playimg,(750,330))



        fenetre.blit(N,(850,360))
        Ntxt=font_s.render(str(number),1,(150,150,150),0)
        fenetre.blit(Ntxt,(950,360))
        
        fenetre.blit(Reco,(750,390))
        Recotxt=font_s.render(str(recovery),1,(150,150,150),0)
        fenetre.blit(Recotxt,(850,390))
        
        fenetre.blit(I,(750,420))
        Itxt=font_s.render(str(imunity),1,(150,150,150),0)
        fenetre.blit(Itxt,(850,420))
        
        fenetre.blit(Vacc,(750,450))
        Vacctxt=font_s.render(str(vaccinate),1,(150,150,150),0)
        fenetre.blit(Vacctxt,(850,450))

        
        fenetre.blit(Ri,(950,390))
        Rtxt=font_s.render(str(R),1,(150,150,150),0)
        fenetre.blit(Rtxt,(1050,390))
        
        fenetre.blit(Di,(950,420))
        Dtxt=font_s.render(str(D),1,(150,150,150),0)
        fenetre.blit(Dtxt,(1050,420))
        
        fenetre.blit(Vi,(950,450))
        Vtxt=font_s.render(str(V),1,(150,150,150),0)
        fenetre.blit(Vtxt,(1050,450))

        

        
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()



main()
