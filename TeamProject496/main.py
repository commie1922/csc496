import screen
import thread
import time
import pygame
import sys
import math
import random
import os
from wpn import *
from pygame.locals import *
from image import *
from menu import *


os.environ['SDL_VIDEO_CENTERED'] = '1' # Center the game window.
pygame.init()#Need to work this out, main should not need to know about pygame.

window = screen.Window(800, 600, "TeamProject 496", (0,0,0)) # Create game window.
#window.set_font(((12, None), (24, None))) <- Another example of the two statements below
window.set_font(12, None) # index 0
window.set_font(24, None) # index 1

#Music - DaftPunk
pygame.mixer.init()
pygame.mixer.music.load("music/end.ogg")
pygame.mixer.music.play()


mif = "images/cursor.png"
pygame.mouse.set_visible(False)                  #hides the cursor so only the cross hair is seen
mouse_c = pygame.image.load(mif).convert_alpha()  #For converting images to types that are usable by python


def check_significant_keypresses(keys_pressed, window, player, items, fired, enemies):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if keys_pressed[114] == 1:
            player.weapon.reloadWeapon()
        elif keys_pressed[102] == 1:            
            pygame.key.set_repeat(0, 0)
            for item in items:
                if player.collidesWith(item):
                    items.remove(item)
                    pickedUp = player.pickUp(item)
                    if not pickedUp == None:
                        items.extend([pickedUp])   
        elif keys_pressed[112] == 1:
            return pauseMenu()
            window.set_background("images/field.jpg")
        pygame.key.set_repeat(1, 1)
    return True
            
"""
gets current position of the mouse
sets the mouse image position, the cursor is set to the center of theimage
copies the mouse image created earlier to the screen
"""
def setupCrossHairCursor():    
    X, Y = pygame.mouse.get_pos()    
    mouse_block = mouse_c.get_rect()
    mouse_block.center = (X - mouse_block[2]/2, Y - mouse_block[3]/2)
    X -= mouse_c.get_width()
    Y -= mouse_c.get_height()
    return mouse_block

def gameAndLogic():
    clock = pygame.time.Clock()
    m_sec = 0
    fired = []
    items = []
    z = []
    i = 0
    obj = []    
    MAXNUM = 1
    speedIn = .1
    isPaused = False
    player = Player((window.SCREEN_WIDTH/2, window.SCREEN_HEIGHT/2)) # Init the player.
    weapons = [AssaultRifle, Handgun, Flamethrower, Sawshot] # List of weapons we want in the game.
    window.set_background("images/field.jpg")
    continueGame = True
    quitGame = False    
    while player.isAlive() and continueGame:                    
        #***********************************************************************
        # Keep stable frame rate.
        m_sec = clock.tick(140)
        fps = round(clock.get_fps())#maybe good idea to make player speed fn of fps
        #***********************************************************************


        #***********************************************************************
        # Create more zombies when player kills them off.
        # Create randomly positioned walls when no zombies left.
        if len(z) == 0:
            while i < MAXNUM:
                z.append(Zombie((random.randrange(0,window.SCREEN_WIDTH),random.randrange(0,window.SCREEN_HEIGHT))))
                i += 1                
            if MAXNUM < 16:
                MAXNUM = MAXNUM * 2
            i = 0
            obj = []      
            while i < 4:
                obj.append(Object());
                i +=1
            i=0
            
            
            #Make the objects (walls)
            for o in obj:
                if player.collidesWith(o):
                    obj.remove(o)
        #***********************************************************************

        
        #***********************************************************************            
        keys_pressed = pygame.key.get_pressed() # Get the pressed keys for events
        continueGame = check_significant_keypresses (keys_pressed, window, player, items, fired, z)
        
        # Player movement, weapon carrying and drawing structures placed here.
        lastx = player.x # If player tries to move and collides with an enemy 
        lasty = player.y # revert him back to his previous spot
        player.move(keys_pressed, (window.SCREEN_WIDTH, window.SCREEN_HEIGHT))
        for enemy in z:
            if player.collidesWith(enemy):
                player.x = lastx
                player.y = lasty
        for o in obj:
            if player.collidesWith(o):
                player.x = lastx
                player.y = lasty
        hero_source, hero_destination = player.rotateTowardObject(pygame.mouse.get_pos())
        fired = player.weapon.shoot((window.SCREEN_WIDTH, window.SCREEN_HEIGHT), (window.OLD_SCREEN_WIDTH, window.OLD_SCREEN_HEIGHT))
        player.carry()
        w = player.weapon
        gun_source, gun_destination = w.rotateTowardObject(pygame.mouse.get_pos())
        #***********************************************************************

        
        #***********************************************************************
        # Movement       
        px = player.x - window.SCREEN_WIDTH/2
        py = player.y - window.SCREEN_HEIGHT/2
        for item in items:
            item.x -= px
            item.y -= py
        for enemy in z:
            enemy.x -= px
            enemy.y -= py
        for o in obj:
            o.x -= px
            o.y -= py
        player.x = window.SCREEN_WIDTH/2
        player.y = window.SCREEN_HEIGHT/2
        
        #***********************************************************************
        # Drawing functionality
        window.draw_background()                                                    # Draw background
        player.healthBar(window.SCREEN, (window.SCREEN_WIDTH, window.SCREEN_HEIGHT))# Draw health bar
        player.ammoBar(window.SCREEN, (window.SCREEN_WIDTH, window.SCREEN_HEIGHT))  # Draw ammo bar        

        try:# Make sure there are never more than 20 items on the game board.
            while len(items) > 20:   
                needsRemoved = items[0]
                items.remove(needsRemoved) 
        except Exception as e:
            pass
          
        try: # Draw dropped items that are on the map
            for item in items:
                if player.collidesWith(item):
                    if player.grab(item):
                        removeItem = item
                        items.remove(removeItem)
                item_source, item_destination = item.img, item.getPosition()
                window.draw(item_source, item_destination)                
        except Exception as e:
            pass
        
        try: # Check if zombie can see player, if so move zombie towards player.
            for enemy in z:
                if not enemy.collidesWith(player):
                    enemy.notAttacking()                    
                    moveZ = True
                    for o in obj:
                        if enemy.moveCheck(player.getPosition(), o.givePosition()):
                           moveZ = False
                           break
                    if moveZ:
                        for o in obj:
                            enemy.move(player.getPosition(), o.givePosition())
                            break 
                else:
                    player.takeDamage(enemy.attack())
                window.draw(enemy.rotateTowardObject(player))
        except Exception as e:
            pass
            
        try: # Draw bullets and check for their collision
            for bullet in fired:
                round_in_bound = bullet.inBounds((window.SCREEN_WIDTH, window.SCREEN_HEIGHT))
                if round_in_bound == True:
                    bullet.move()
                    round_source, round_dest = bullet.handleProjectile()
                    window.draw(round_source, round_dest)
                    for enemy in z:
                        if bullet.isDestroyed:
                            fired.remove(bullet)
                        elif bullet.collidesWith(enemy):
                            enemy.takeDamage(bullet.dmg)
                            if not bullet.isDestroyed:
                                fired.remove(bullet)
                            if enemy.isAlive() == False:
                                dropped = enemy.drop()
                                if not dropped == None:
                                    items.append(dropped)
                                z.remove(enemy)
                            break
                    for o in obj:
                        if bullet.collidesWith(o):
                            fired.remove(bullet)
                else:
                    fired.remove(bullet)
                player.weapon.activeRounds = fired
        except Exception as e:
            pass 

        try:
            window.draw(gun_source, gun_destination)    # Draw players gun
            window.draw(hero_source,hero_destination)   # Draw the player
            window.write("FPS: "+str(fps), (window.SCREEN_WIDTH * .04,\
                                            window.SCREEN_HEIGHT * .05), (255,255,255), 0) # Show player FPS
            window.draw(mouse_c, setupCrossHairCursor().center) # Draw mouse cross hair
        except Exception as e:
            pass       
        
        # Draw Wall
        for o in obj:
            window.draw(o.img, o.getPosition()) 
        window.update()
#************************************************************************

#*********************************Main Menu Function***************************************
def mainMenu():
    state = 0
    prev_state = 1
    rect_list = []
    image1 = load_image('ammobelt.jpg', 'images')
    mainMenu = cMenu(50,50, 10,10, 'vertical', 10, window.SCREEN,
                 [('Play Game',         1, image1, (250,40)),
                  ('Leaderboards',      2, image1, (250,40)),
                  ('Controls',           3, image1, (250,40)),
                  ('Exit',              4, image1, (250,40))])    
    pygame.key.set_repeat(0, 0)
    window.set_background("images/field.jpg")
    window.draw_background()
    while True:
        if prev_state != state:        
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        l = pygame.event.wait()
        k = pygame.key.get_pressed()
        if k[pygame.K_DOWN] == 1 or k[pygame.K_UP] == 1 or \
           l.type == EVENT_CHANGE_STATE or k[pygame.K_RETURN] == 1:
            if state == 0: 
                rect_list, state = mainMenu.update(l, state)
            if state == 1:                
                pygame.key.set_repeat(1, 1)
                gameAndLogic()
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))       
                pygame.key.set_repeat(0, 0)
                window.set_background("images/field.jpg")
                window.draw_background()
                state = 0
            elif state == 2:                
                pass
                state = 0
            elif state == 3:
                pass
                state = 0
            elif state == 4:                    
                pygame.quit()
                exit()                
        if l.type == QUIT:
            pygame.quit()
            exit()                 
        window.update()

#*********************************Pause Menu Function***************************************
def pauseMenu():
    state = 0
    prev_state = 1
    rect_list = []
    paused = True
    image1 = load_image('ammobelt.jpg', 'images')
    pauseMenu = cMenu(50,50, 10,10, 'vertical', 10, window.SCREEN,
                 [('Resume',         1, image1, (250,40)),
                  ('Controls',       2, image1, (250,40)),
                  ('Fullscreen',     3, image1, (250,40)),
                  ('Quit Game',      4, image1, (250,40)),
                  ('Exit Game',      5, image1, (250,40))])
        
    pygame.key.set_repeat(0, 0)
    window.set_background((0,255,0))
    window.draw_background()
    while paused:
        if prev_state != state:        
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        l = pygame.event.wait()
        k = pygame.key.get_pressed()
        if k[pygame.K_DOWN] == 1 or k[pygame.K_UP] == 1 or \
           l.type == EVENT_CHANGE_STATE or k[pygame.K_RETURN] == 1:
            if state == 0:
                rect_list, state = pauseMenu.update(l, state)
            if state == 1:                
                paused = False
                state = 0
            elif state == 2:
                optionsMenu()
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                state = 0
            elif state == 3:
                if not window.isFullScreened:
                    window.full_screen()
                else:                    
                    window.exit_full_screen(800,600)
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                window.draw_background()
                state = 0
            elif state == 4:
                return False
                state = 0
            elif state == 5:                    
                pygame.quit()
                exit()
                
        if l.type == QUIT:
            pygame.quit()
            exit()
        window.update()
    pygame.key.set_repeat(1, 1)
    return True
    
def main(args):
    mainMenu()
main(None)


