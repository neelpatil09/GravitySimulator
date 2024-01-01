import random
import pygame
import math
g =0.5
dt = 0.008
tol = 50
s = 1000000
gameWidth = 1280
gameHeight = 800

screen = pygame.display.set_mode((gameWidth,gameHeight))

def gameLoop(masses):
    pygame.init()

    massBoxWidth = 200
    massBoxes= []
    massBoxColors=[]
    massBoxColor = (255,204,102)
    massBoxSelectedColor = (102, 153, 255)

    delete = pygame.Rect(gameWidth-massBoxWidth/5, 28, 20, 20)
    input_box = pygame.Rect(20, 20, 300, 40)

    startpos = 0
    newCount = 0
    selected= -1

    running = True
    notAdding = True
    enteringVX = False

    text=''
    textvx = ''
    startText = 'Set New Mass: '

    setVX = pygame.Rect(gameWidth-massBoxWidth+22,50+64,30,20)

    massFont = pygame.font.SysFont('Arial', 10)
    selectedMassFont = pygame.font.SysFont('Arial', 12)
    boxFont = pygame.font.SysFont('Arial',15)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                hitBox = False
                for index,massBox in enumerate(massBoxes):
                    if(massBox.collidepoint(event.pos)):
                        if(selected == index):
                            if setVX.collidepoint(event.pos):
                                enteringVX=True
                            elif(confirmV.collidepoint(event.pos)):
                                try:
                                    masses[selected].vx = int(textvx.split(',')[0])
                                    masses[selected].vy = int(textvx.split(',')[1])
                                    enteringVX = False
                                except Exception as e:
                                    enteringVX = False
                                textvx = ''
                            elif(delete.collidepoint(event.pos)):
                                masses.pop(selected)
                                massBoxColors.pop(selected)
                                massBoxes.pop(selected)
                                selected = -1
                            else:
                                textvx=''
                                enteringVX=False
                                massBoxColors = [massBoxColor for m in massBoxes]
                                selected = -1
                        else:
                            massBoxColors = [massBoxColor for m in massBoxes]
                            massBoxColors[index]=massBoxSelectedColor
                            selected = index
                        hitBox = True
                if not hitBox:
                    enteringVX = False
                    if notAdding:
                        startpos = pygame.mouse.get_pos()
                        notAdding = False
                        pygame.draw.rect(screen,(255,204,102), input_box)
                        pygame.draw.rect(screen, (255,255,255), input_box, 2)
                        txt_surface = boxFont.render(startText + text, True, pygame.Color('black'))
                        screen.blit(txt_surface, (input_box.x+2, input_box.y+2))
                    else:
                        notAdding = True
                        text=''
                    
            elif event.type == pygame.KEYDOWN:
                if not notAdding:
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE :
                        text = text[:-1]
                    elif event.key == pygame.K_RETURN:
                        newCount+=1
                        tempMass = Mass(int(text),startpos,[random.randint(-50,50),random.randint(-50,50)],"UserMass " + str(newCount) + "!")
                        masses.append(tempMass)
                        text=''
                        notAdding=True
                    else:
                        try:
                            isNum = int(event.unicode) >=0 and int(event.unicode) <= 9
                        except Exception as e:
                            isNum = False
                        if isNum:
                            text+=event.unicode
                        else:
                            text=''
                    txt_surface = boxFont.render(startText + text, True, pygame.Color('black'))
                    screen.blit(txt_surface, (input_box.x+2, input_box.y+2))
                if enteringVX:
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        textvx = textvx[:-1]
                    else:
                        try:
                            isNum = (int(event.unicode) >= 0 and int(event.unicode) <= 9) or event.unicode == '-' or event.unicode == ','
                        except Exception as e:
                            enteringVX = False
                        if isNum:
                            textvx+=event.unicode
                        else:
                            textvx = ''
        pygame.display.flip()

        if notAdding:
            screen.fill("black")
            massBoxes = []
            for index, mass in enumerate(masses):
                player_pos = pygame.Vector2(mass.x,mass.y)
                if (index == selected):
                    pygame.draw.circle(screen, mass.color, player_pos, mass.r*1.2)
                    nameText = selectedMassFont.render(mass.label, True, (255, 255, 255)) 
                    speedText = selectedMassFont.render(str(round(math.sqrt(mass.vx**2 + mass.vy**2)))+ " m/s",True,(255,255,255))    
                else:
                    pygame.draw.circle(screen, mass.color, player_pos, mass.r)
                    nameText = massFont.render(mass.label, True, (255, 255, 255)) 
                    speedText = massFont.render(str(round(math.sqrt(mass.vx**2 + mass.vy**2)))+ " m/s",True,(255,255,255))

                pygame.draw.line(screen, (0,255,0), (mass.x, mass.y), (mass.x+mass.vx/2,mass.y+mass.vy/2),2)
                pygame.draw.line(screen, (255,0,0), (mass.x, mass.y), (mass.x+mass.ax*2,mass.y+mass.ay*2),2)
                
                screen.blit(nameText, (mass.x-len(mass.label)*2.5, mass.y+mass.r+2))
                screen.blit(speedText, (mass.x-len(mass.label)*2.5, mass.y+mass.r+12))
                
                massBoxes.append(pygame.Rect(gameWidth-massBoxWidth-20, 20+80*index, massBoxWidth, 78))
                massBoxColors.append(massBoxColor)
                
                infoText = "Velocity: " + str(round(math.sqrt(mass.vx**2 + mass.vy**2))) + ". Acceleration: " + str(round(math.sqrt(mass.ax**2 + mass.ay**2)))
                descriptText = "Mass: " + str(mass.mass ) + ". Radius: " + str(round(mass.r,2))
                
                massBoxLabel = boxFont.render(mass.label,True,(0,0,0))
                massBoxInfo = massFont.render(infoText,True,(0,0,0))
                massBoxDesc = massFont.render(descriptText,True,(0,0,0))

                pygame.draw.rect(screen,massBoxColors[index], massBoxes[index])
                screen.blit(massBoxLabel, (gameWidth-massBoxWidth-18,22+80*index))
                screen.blit(massBoxInfo, (gameWidth-massBoxWidth-18,39+80*index))

                if(selected == index):
                    delete = pygame.Rect(gameWidth-massBoxWidth/4, 28+80*index, 20, 20)
                    confirmV = pygame.Rect(gameWidth-massBoxWidth/4,70+80*index,20,20)
                    newVX = massFont.render("New VX: ",True,(0,0,0))
                    enteredvx = massFont.render(textvx,True,(0,0,0))

                    screen.blit(massBoxDesc, (gameWidth-massBoxWidth-18,54+80*index))
                    screen.blit(newVX, (gameWidth-massBoxWidth-18,72+80*index))
                    screen.blit(enteredvx, (gameWidth-massBoxWidth+24,72+80*index))
                    setVX = pygame.Rect(gameWidth-massBoxWidth+24,70+80*index,30,20)

                    if enteringVX:
                        color = "green"
                    else: color = "yellow"

                    pygame.draw.rect(screen,color,setVX,1)
                    pygame.draw.rect(screen,"green",confirmV)
                    pygame.draw.rect(screen,"red", delete)


            pygame.display.flip()

            updatePos(masses,dt)
            updateVelocity(masses,dt)
            updateAcceleration(masses)
            resolveCollisions(masses)

    pygame.quit()

def updatePos(masses,dt):
    for mass in masses:
        mass.x += mass.vx * dt
        mass.y += mass.vy * dt

def updateVelocity(masses,dt):
    for mass in masses:
        mass.vx += mass.ax * dt
        mass.vy += mass.ay * dt      

def updateAcceleration(masses):
    for mainIndex,mass1 in enumerate(masses):
        ax = 0
        ay = 0
        for checkIndex, mass2 in enumerate(masses):
            if mainIndex != checkIndex:
                dx =abs(mass1.x - mass2.x)
                dy =abs(mass1.y-mass2.y)
                rsq = (dx)**2 + (dy)**2
                if rsq < tol:
                    rsq *= s
                force = (g * mass2.mass)/(rsq)
                if(mass2.x < mass1.x):
                    ax -= force * dx
                else:
                    ax += force * dx
                if mass2.y < mass1.y:
                    ay -= force * dy
                else:
                    ay += force * dy
        
        mass1.ax = ax
        mass1.ay = ay

def resolveCollisions(masses):
    collisions_x = [0 for m in masses]
    collisions_y = [0 for m in masses]
    for index,mass1 in enumerate(masses):
        for j,mass2 in enumerate(masses):
             if(j!= index):
                dist = math.sqrt((mass1.x-mass2.x)**2 + (mass1.y-mass2.y)**2)
                minDist = (mass1.r+mass2.r)
                if(dist <= minDist):
                    if(abs(mass1.vx + mass1.vy) < mass1.mass/2 and abs(mass2.vx + mass2.vy)<mass2.mass/2):
                        if(mass1.mass < mass2.mass):
                            mass2.mass+=mass1.mass
                            mass2.r+=mass1.r/10
                            masses.pop(index)
                        else:
                            mass1.mass+=mass2.mass
                            mass1.r+=mass2.r/10
                            masses.pop(j)
                        continue

                    normalizedCollisionAxis = [(mass1.x-mass2.x)/math.sqrt((mass1.x-mass2.x)**2 + (mass1.y-mass2.y)**2), (mass1.y-mass2.y)/math.sqrt((mass1.x-mass2.x)**2 + (mass1.y-mass2.y)**2)]
                    velocityDifference = [mass1.vx-mass2.vx,mass1.vy-mass2.vy]
                    f = (velocityDifference[0]*normalizedCollisionAxis[0] + velocityDifference[1]*normalizedCollisionAxis[1])/(normalizedCollisionAxis[0]**2 + normalizedCollisionAxis[1]**2)* (0.5*mass2.mass)/(mass1.mass + mass2.mass)

                    normalizedCollisionAxis[0]*=(f)
                    normalizedCollisionAxis[1]*=(f)

                    vx = mass1.vx - normalizedCollisionAxis[0]
                    vy = mass2.vy - normalizedCollisionAxis[1]

                    collisions_x[index]+=vx*mass2.mass/(mass1.mass+mass2.mass)
                    collisions_y[index]+=vy*mass2.mass/(mass1.mass+mass2.mass)
    for index,mass in enumerate(masses):
        if collisions_x[index] != 0 or collisions_y[index] != 0:
            mass.vx = collisions_x[index]
            mass.vy = collisions_y[index]

class Mass:
    def __init__(self, mass,position,velocity,label):
        self.mass = mass
        self.r = 50-math.exp(-((mass/200)-3.912023))
        self.x = position[0]
        self.y = position[1]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.color = [random.randint(10, 255),random.randint(10, 255),random.randint(10, 255)]
        self.label = label
        self.ax = 0
        self.ay = 0
    
    def setColor(self,color):
        self.color = color

    def displayInfo(self):
        print(self.position)

def main():
    moon1 =  Mass(0.1,[300,300],[-20,20],"Sample Moon 1")
    moon2 = Mass(20,[640,100],[-30,-30],"Sample Moon 2")
    moon3 = Mass(30,[900,400],[-20,-20],"Sample Moon 3")
    moon4 = Mass(60,[1100,200],[-20,-20],"Sample Moon 4")
    moon5 = Mass(20,[0,400],[-20,-20],"Sample Moon 5")
    planet1 = Mass(3000,[640,400],[0,0], "Sample Planet 1")
    masses = [moon1,moon2,moon3,moon4,moon5, planet1]

    #head1 = Mass(10,[300,300],[20,0],"Moon 1")
    #head2 = Mass(12,[500,300],[-20,0],"Moon 2")
    #head3 = Mass(10,[400,300],[0,0],"Moon 3")
    #masses = [head1,head2,head3]
    gameLoop(masses)

if __name__ == "__main__":
    main()