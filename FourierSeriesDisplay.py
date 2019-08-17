from FourierCircle import FourierCircle
from ImageTrace import ImageTrace
import math, random
from FourierCircle import FourierSeries
from PIL import Image
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    import pygame.gfxdraw

#create display width height 4 times larger because cells are 4 by 4 pixels
display_width = 1000
display_height = 1000

#initialize pygame environement
pygame.init()
systemDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Fourier Series')
s = pygame.Surface(systemDisplay.get_size(), pygame.SRCALPHA, 32)
mouse = pygame.mouse
clock = pygame.time.Clock()
BLACK = pygame.Color( 0 ,  0 ,  0 )
WHITE = pygame.Color(255, 255, 255)
BLUE = pygame.Color(0, 0, 255)
RED = pygame.Color(255, 0, 0)

#loading screen
font = pygame.font.Font('freesansbold.ttf',115)
systemDisplay.fill(WHITE)
text = font.render("Loading...", True, BLACK)
rect = text.get_rect()
rect.center=(display_width/2,display_height/2)
systemDisplay.blit(text,rect)
pygame.display.update()

#custom objects
series = FourierSeries(10)
tracedimage = ImageTrace(Image.open("title.png")).orderedPoints
series.loadOrderedSet(tracedimage)

#sets of points
trace = []
mouseTrace = []

#flags
horizontalTrace=False
crashed = False
restarted=True

#mouse flsg
mouseHold = False

#system loop
while not crashed:
    left_pressed, middle_pressed, right_pressed = mouse.get_pressed()
    
    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        
        #mouse event handling 
        elif left_pressed: #mouse being pressed/held
            if mouseHold == False: #initial press
                systemDisplay.fill(WHITE) 
                mouseTrace = []
                mouseHold=True
            mouseTrace.append(pygame.mouse.get_pos())
        elif mouseHold == True: #mouse released
            mouseHold = False
            trace=[]
            series.loadOrderedSet(mouseTrace)
            
    #very end of the fourier circles, used to draw trace
    trueTip = series.getTip()
    
    if horizontalTrace: #horizontal trace
        for i in range(len(trace)):
            trace[i]=(trace[i][0]+5,trace[i][1])
        trace.append((int(trueTip[0]),int(trueTip[1])))
    else: #full shape trace
        trace.append((int(trueTip[0]),int(trueTip[1])))
    
    #UPDATE DISPLAY - wipe screen
    systemDisplay.fill(WHITE) 
    
    #draw mouse trace
    for pos in mouseTrace:
        pygame.draw.circle(pygame.display.get_surface(), BLACK, (pos),1)      
    
    #draw fourier circles
    for ind in range(0,len(series.circles)):
        center = series.getCircle(ind).center
        tip = series.getCircle(ind).tip
        radius = int(series.getCircle(ind).radius)
        pygame.gfxdraw.circle(pygame.display.get_surface(), int(center[0]), int(center[1]), radius , (BLACK)) #circle
        pygame.draw.line(pygame.display.get_surface(), (RED), (int(center[0]),int(center[1])), (int(tip[0]),int(tip[1]))) #radius line
    
    #draw trace of the shape being drawin by the fourier circles
    for ind in range(1,len(trace)):
        pygame.draw.line(pygame.display.get_surface(), (BLUE), (trace[ind-1][0],trace[ind-1][1]), (trace[ind][0],trace[ind][1]),3)
    
    #update display and tick clocks
    pygame.display.update()
    series.tick(.01)
    clock.tick(100)    