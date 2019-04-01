from projectq.ops import C, CNOT, X, H, Rz, Measure
from projectq import MainEngine
from projectq import backends
import pygame
import math
import colorsys
from random import *

pygame.init()

display_width = 800
display_height = 800
centerx = display_width/2
centery = display_height/2
center = (centerx, centery)
radius = 200
gametime = 30
highscore = 10000

buttonWidth = 140
buttonHeight = 70
button1 = pygame.Rect(display_width/4 - buttonWidth/2 + 20, 680 - buttonHeight/2,
                      buttonWidth, buttonHeight)
button2 = pygame.Rect(display_width*3/4 - buttonWidth/2 - 20, 680 - buttonHeight/2,
                      buttonWidth, buttonHeight)

black = (0,0,0)
white = (255,255,255)
lav = (159, 171, 206)

crashed = False

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Quantum Simon Says')
gameDisplay.fill(white)
pygame.display.update()

def initialize(qreg):
    #H | qreg[3]
    #H | qreg[2]
    #X | qreg[1]
    #CNOT | (qreg[2], qreg[1])
    #CNOT | (qreg[1], qreg[0])

    #for i in range(0,4):
    #    Rz(random()*2*math.pi) | qreg[i]

    for i in range(0,2):
        H | qreg[i]
    #for i in range(0,2):
    #    for j in range(0,2):
    #        if i != j:
    #            C(Rz(random()*2*math.pi)) | (qreg[i], qreg[j])
    #Rz(random()*2*math.pi) | qreg[0]
    #Rz(random()*2*math.pi) | qreg[1]
    '''H | qreg[1]
    CNOT | (qreg[0],qreg[1])
    H | qreg[1]
    X | qreg[1]
    X | qreg[0]
    H | qreg[1]
    CNOT | (qreg[0],qreg[1])
    H | qreg[1]
    X | qreg[1]
    X | qreg[0]'''




#only works for 2-qubit state vectors
def display(state, radius, goal):
    gameDisplay.fill(white)
    for i in range(0,4):
        if state[i].real == 0:
            if state[i].imag > 0:
                hue = 0.25
            else:
                hue = 0.75
        else:
            hue = math.atan(state[i].imag/state[i].real) / (2*math.pi)
        if state[i].real < 0:
            hue += 0.5
        if hue < 0:
            hue = 1 + hue
        saturation = state[i].real*state[i].real + state[i].imag*state[i].imag
        color = colorsys.hsv_to_rgb(hue, saturation, 1)
        color = (color[0] * 255, color[1] * 255, color[2] * 255)

        if i == 0:
            points = (center, (centerx - radius/2, centery - radius/2), (centerx, centery - radius),
                      (centerx + radius/2, centery - radius/2))
        if i == 1:
            points = (center, (centerx + radius/2, centery - radius/2), (centerx + radius, centery),
                      (centerx + radius/2, centery + radius/2))
        if i == 2:
            points = (center, (centerx - radius/2, centery + radius/2), (centerx - radius, centery),
                      (centerx - radius/2, centery - radius/2))

        if i == 3:
            points = (center, (centerx + radius/2, centery + radius/2), (centerx, centery + radius),
                      (centerx - radius/2, centery + radius/2))

        pygame.draw.polygon(gameDisplay, color, points)

    if goal == 0:
        points = (center, (centerx - radius/2, centery - radius/2), (centerx, centery - radius),
                  (centerx + radius/2, centery - radius/2))
    if goal == 1:
        points = (center, (centerx + radius/2, centery - radius/2), (centerx + radius, centery),
                  (centerx + radius/2, centery + radius/2))
    if goal == 2:
        points = (center, (centerx - radius/2, centery + radius/2), (centerx - radius, centery),
                  (centerx - radius/2, centery - radius/2))

    if goal == 3:
        points = (center, (centerx + radius/2, centery + radius/2), (centerx, centery + radius),
                  (centerx - radius/2, centery + radius/2))

    pygame.draw.polygon(gameDisplay, black, points, 4)

def text_objects(text, font, angle):
    textSurface = font.render(text, True, black)
    textSurface = pygame.transform.rotate(textSurface, angle)
    return textSurface, textSurface.get_rect()

def message_display(text, center, size, angle):
    futura = pygame.font.SysFont('arial', size)
    TextSurf, TextRect = text_objects(text, futura, angle)
    TextRect.center = center
    gameDisplay.blit(TextSurf, TextRect)

def button_display(text1, text2):
    pygame.draw.rect(gameDisplay, lav, button1, 0)
    message_display(text1, button1.center, 40, 0)
    pygame.draw.rect(gameDisplay, lav, button2, 0)
    message_display(text2, button2.center, 40, 0)

def controls_display():
    color = (230,230,230)
    width = 60
    arect = pygame.Rect(centerx - radius/2 - width - 50, centery - radius/2 - width + 20, width, width)
    wrect = pygame.Rect(centerx - radius/2 - width + 20, centery - radius/2 - width - 50, width, width)
    qrect = pygame.Rect(centerx + radius/2 - 20, centery - radius/2 - width - 50, width, width)
    srect = pygame.Rect(centerx + radius/2 + 50, centery - radius/2 - width + 20, width, width)

    pygame.draw.rect(gameDisplay, color, arect, 3)
    message_display("A", arect.center, 50, 0)
    pygame.draw.rect(gameDisplay, color, wrect, 3)
    message_display("W", wrect.center, 50, 0)
    pygame.draw.rect(gameDisplay, color, qrect, 3)
    message_display("Q", qrect.center, 50, 0)
    pygame.draw.rect(gameDisplay, color, srect, 3)
    message_display("S", srect.center, 50, 0)

def display_start():
    gameDisplay.fill(white)
    message_display("QUANTUM", ((display_width/2), 110), 120, 0)
    message_display("SIMON SAYS", ((display_width/2), 210), 120, 0)
    if highscore != 10000:
        message_display("BEST TIME: " + str(highscore), (display_width/2, 400), 60, 0)
    button_display("HELP", "PLAY")

def display_help():
    gameDisplay.fill(white)
    message_display("Visit", (display_width/2, 200), 55, 0)
    message_display("tnargmada.github.io/untangling-entanglement", (display_width/2, 250), 45, 0)
    message_display("for instructions", (display_width/2, 300), 55, 0)
    button_display("MENU", "PLAY")

def display_win(state, time, goal):
    global highscore
    display(state, radius, goal)

    for i in range(0,4):
        if state[i].real != 0 or state[i].imag != 0:
            if i == goal:
                message_display("YOU WIN", ((display_width/2), 90), 110, 0)
                message_display("YOUR TIME: " + str(time), (centerx - radius/2 - 20, centery + radius/2 + 20), 40, 315)
                if time < highscore:
                    highscore = time
            else:
                message_display("YOU LOST", ((display_width/2), 90), 110, 0)
    if highscore != 10000:
        message_display("BEST TIME: " + str(highscore), (centerx + radius/2 + 20, centery + radius/2 + 20), 40, 45)

    button_display("MENU", "PLAY")

def win(state, time, goal):
    global crashed
    display_win(state, time, goal)
    pygame.display.update()
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if x>button2.left and x<button2.right and y>button2.top and y<button2.bottom:
                    play()
                if x>button1.left and x<button1.right and y>button1.top and y<button1.bottom:
                    start()
    return

def tutorial():
    global crashed
    display_help()
    pygame.display.update()
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if x>button2.left and x<button2.right and y>button2.top and y<button2.bottom:
                    play()
                if x>button1.left and x<button1.right and y>button1.top and y<button1.bottom:
                    start()
    return

def start():
    global crashed
    display_start()
    pygame.display.update()
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if x>button2.left and x<button2.right and y>button2.top and y<button2.bottom:
                    play()
                if x>button1.left and x<button1.right and y>button1.top and y<button1.bottom:
                    tutorial()
    return

def run_game(goal):
    global crashed
    playing = True
    start_time = pygame.time.get_ticks()
    finish_time = 0

    eng = MainEngine(backends.Simulator())
    qreg = eng.allocate_qureg(2)
    initialize(qreg)
    eng.flush()
    state = eng.backend.cheat()[1]
    print(state)
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    Rz(0.3) | qreg[1]
                if event.key == pygame.K_q:
                    Rz(0.3) | qreg[0]
                if event.key == pygame.K_w:
                    H | qreg[1]
                if event.key == pygame.K_s:
                    H | qreg[0]
                if event.key == pygame.K_RETURN:
                    playing = False
            eng.flush()
            state = (eng.backend.cheat())[1]
        display(state, radius, goal)
        #controls_display()
        finish_time = round((pygame.time.get_ticks() - start_time)/1000, 1)
        message_display(str(finish_time), ((display_width/2), 90), 120, 0)
        pygame.display.update()

    for i in range(0,2):
        Measure | qreg[i]

    eng.flush()
    state = (eng.backend.cheat())[1]
    print(state)

    return(state, finish_time)

def play():
    goal = int(random()*4)
    finish = run_game(goal)
    win(finish[0], finish[1], goal)

start()

pygame.quit()
quit()
