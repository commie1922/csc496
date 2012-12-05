import math
import random 
import pygame
from pygame.locals import *
pygame.init()

###########################################  Entity  ##########################################
### Governing Class
class Entity(object):

    def __init__(self, *args):        
        self.x          = args[1][0]    #Coordinate X
        self.y          = args[1][1]    #Coordinate Y
        self.health     = args[2]       #Health
        self.maxHealth  = args[2]       #Maxhealth
        self.rotation   = args[3]       #Degree of rotation
        self.width      = args[4][0]    #Width of object
        self.height     = args[4][1]    #Height of object
        self.mana       = args[5]       #Mana pool
        self.maxMana    = args[5]       #Max mana pool
        self.weapon     = args[7]
        ###*********kind of hacky, maybe we can improve later?*********
        if args[6] != None:
            self.move_speed_xy  = args[6] #Speed object moves along x and y axis 
            self.moveSpeedTemp  = args[6] #Special case where speed may temporarily change,
                                          #store original here.
            try:
                self.diagonal_speed = (self.move_speed_xy[0] / math.sqrt((self.move_speed_xy[0] * 1.7)**2) ) * \
                              self.move_speed_xy[0] * math.sqrt((self.move_speed_xy[0]**2) + (self.move_speed_xy[1]**2))#/1.01
            except Exception as e:
                pass
        else:
            self.move_speed_xy = 0
            self.moveSpeedTemp = 0
            self.diagonal_speed = 0
        ###************************************************************
            
        self.img        = self.setImg(args[0]) #Surface Image, must be initialized
                                               #after width and height are set

    def getAttributes(self):
        print "Location   : "   + str(self.x) + " " + str(self.y)
        print "Health     : "   + str(self.health)
        print "Max Health : "   + str(self.maxHealth)
        print "Mana       : "   + str(self.mana)
        print "Max Mana   : "   + str(self.maxMana)
        print "Rotation   : "   + str(self.rotation)
        print "W x H      : ("  + str(self.width) + ", " + str(self.height) + ")"
        print "Move Speed : "   + str(self.move_speed_xy)
        print "Diag Move  : "   + str(self.diagonal_speed)
        print "Surface    : "   + str(self.img)
        print "Rectangle  : "   + str(self.img.get_rect())
        print ""

    """
    handles the movement keys of the hero character
    params:
    keys_pressed;the pygame (or any) array retrieved with values
        of the keys wdwdwdwdwdstored in the array ex: [q, w, e, r, t, y, ...]
    """
    def move(self, keys_pressed, screen_size):
        hasNotMoved = True
        if(keys_pressed[119] == 1 and keys_pressed[97] == 1):   #w and a
            self.x -= self.diagonal_speed
            self.y -= self.diagonal_speed
            hasNotMoved = False
        elif(keys_pressed[119] == 1 and keys_pressed[100] == 1):  #w and d
            self.x += self.diagonal_speed
            self.y -= self.diagonal_speed
            hasNotMoved = False
        elif(keys_pressed[115] == 1 and keys_pressed[97] == 1):   #s and a  
            self.x -= self.diagonal_speed
            self.y += self.diagonal_speed 
            hasNotMoved = False     
        elif(keys_pressed[115] == 1 and keys_pressed[100] == 1):   #s and d
            self.x += self.diagonal_speed
            self.y += self.diagonal_speed
            hasNotMoved = False
        if hasNotMoved:
            if(keys_pressed[119] == 1):   #w
                self.y -= self.move_speed_xy[1]
            if(keys_pressed[115] == 1):   #s
                self.y += self.move_speed_xy[1]
            if(keys_pressed[97] == 1):    #a
                self.x -= self.move_speed_xy[0]
            if(keys_pressed[100] == 1):   #d
                self.x += self.move_speed_xy[0]
        return self.x, self.y

    def setImg(self, image):
        if isinstance(image, tuple):
            self.img = pygame.Surface((self.width, self.height))
            self.img.set_colorkey((255,255,255))
            self.img.fill((image), pygame.Rect((1,1), (self.width, self.height)))
        else:
            self.img = pygame.image.load(image).convert_alpha()
            surf = pygame.Surface((self.width, self.height), 0, self.img)
            self.img = pygame.transform.smoothscale(self.img, (self.width, self.height), surf) 
        return self.img

    def createImg(self, image, rect):
        if isinstance(image, tuple):
            img = pygame.Surface((rect.width, rect.height))
            img.set_colorkey((255,255,255))
            img.fill((image), rect)
        else:
            img = pygame.image.load(image).convert_alpha()
            surf = pygame.Surface((rect.width, rect.height), 0, img)
            img = pygame.transform.smoothscale(img, (rect.width, rect.height), surf) 
        return img
    
    def isAlive(self):
        if(self.health > 0):
            return True
        else:
            return False

    def takeDamage(self, dmg):        
        if self.health - dmg > 0:
            self.health = self.health - dmg
        else:
            self.health = 0

    def resize(self, screen_size, old_screen_size):
        if old_screen_size[0] != 0 or old_screen_size[1] != 0:
            x_ratio = round((self.x + (self.width/2)) / old_screen_size[0], 10)
            y_ratio = round((self.y + (self.height/2)) / old_screen_size[1], 10)
        else:
            x_ratio = round((float(screen_size[0])/float((screen_size[0]*2))), 1)
            y_ratio = round((float(screen_size[1])/float((screen_size[1]*2))), 1)
        self.width = screen_size[0]/32 + 10
        self.height = screen_size[0]/32 + 10  
        self.x = (screen_size[0] * x_ratio) - self.width/2
        self.y = (screen_size[1] * y_ratio) - self.height/2
        surf = pygame.Surface((self.width, self.height), 0, self.img)
        self.img = pygame.transform.smoothscale(self.img, (self.width, self.height), surf) 
        surf = pygame.Surface((self.width, self.height), 0, self.img)
        return self.img
    
    def size(self, screen_size, old_screen_size, ratio = 80):     
        self.width = screen_size[0]/ratio
        self.height = screen_size[0]/ratio
        surf = pygame.Surface((self.width, self.height), 0, self.img)
        self.img = pygame.transform.smoothscale(self.img, (self.width, self.height), surf) 
        surf = pygame.Surface((self.width, self.height), 0, self.img)
        return self.img
    """
    def inBounds(self, bound, amt_moved, greaterThan):
        if greaterThan:
            if amt_moved > bound:
                return False
        else:
            if amt_moved < bound:
                return False
        return True
    """    
    def inBounds(self, screen_size):
        if self.x > screen_size[0]or self.y < 0 or self.y < 0 or self.y > screen_size[1]:
            return False
        return True
    
    """
    logic for the hero character to face the mouse based the starting position
    of the hero characters img to start facing south (towards bottom of screen)
    params:
    SCREEN; the screen that the rotating hero character is being drawn on
    returns:
    rotated_Surf; surface of the image, this gets drawn to pos of rectangle
    rotated_Rect; destination of the surface image
    """
    def rotateTowardObject(self, obj):
        if isinstance(obj, tuple):
            posX, posY = obj
        else:
            posX, posY = obj.getPosition() #get mouse positions
        try:
            #self.rotation = math.atan2((self.y - posY), (posX - self.x))/math.pi*180.0
            #self.rotation += 90
            rads = math.atan2(-(self.y- posY), (self.x - posX))       
            rads %= (2 * math.pi) #get degrees from the angle radians
            self.rotation = math.degrees(rads) - 90
        except Exception as e:   
            print e #attempt to play it off as though nothing has happened
        oldCenter = (self.x , self.y)  #find center of the calling surface rectangle
        rotated_Surf = pygame.transform.rotate(self.img, self.rotation)  #rotate based on degrees
                                                                         #of the mouse and the character,
                                                                         #steps listed above
        rotated_Rect = rotated_Surf.get_rect()  #get the surfaces current rectangle
        rotated_Rect.center = oldCenter         #set that rectangles center to the original incoming rectangles
                                                #center, must be done or heros center stays in the corner
        return rotated_Surf, rotated_Rect       #returns the source and the destination of the source

    def rotate(self, degrees = None):  
        oldCenter = (self.x , self.y)  #find center of the calling surface rectangle
        if degrees == None:
            rotated_Surf = pygame.transform.rotate(self.img, self.rotation)  #rotate based on degrees
                                                                             #of self.rotation
        else:
            rotated_Surf = pygame.transform.rotate(self.img, degrees)  #rotate based on degrees
                                                                       #passed as argument
        rotated_Rect = rotated_Surf.get_rect()  #get the surfaces current rectangle
        rotated_Rect.center = oldCenter         #set that rectangles center to the original incoming rectangles
                                                #center, must be done or heros center stays
                                                #in the corner
        #self.rotation += degrees
        return rotated_Surf, rotated_Rect       #returns the source and the destination of the source
    
    def performRotation(self, degrees):
        self.rotation += degrees
        round_source, round_dest = self.move()
        round_source, round_dest = self.rotate(self.rotation)
        return round_source, round_dest
    
    def healthBar(self, screen, screen_size):   
        health_border_rect = pygame.draw.rect(screen, (255, 255, 255), (screen_size[1]/50-2, screen_size[1]/50-2, (screen_size[0]/800) * self.maxHealth*2 + 4, math.ceil(screen_size[0]/80.0)+4))
        health_back_rect = pygame.draw.rect(screen, (0, 0, 0), (screen_size[1]/50, screen_size[1]/50, (screen_size[0]/800) * self.maxHealth*2, math.ceil(screen_size[0]/80.0)))
        health_rect = pygame.draw.rect(screen, (255, 0, 0), (screen_size[1]/50, screen_size[1]/50, (screen_size[0]/800) * self.health*2, math.ceil(screen_size[0]/80.0)))
        return health_rect
    
    def manaBar(self, screen, mana_gained, screen_size):
        if(self.mana == 100):
            pass
        else:
            self.mana += mana_gained
        mana_border_rect = pygame.draw.rect(screen, (255, 255, 255), (screen_size[1]/50-2, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0) - 2, (screen_size[0]/800) * self.maxMana + 4, (math.ceil(screen_size[0]/80.0)/2.0)+4))
        mana_back_rect = pygame.draw.rect(screen, (0, 0, 0), (screen_size[1]/50, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0), (screen_size[0]/800) * self.maxMana, math.ceil(screen_size[0]/80.0)/2.0))
        mana_rect = pygame.draw.rect(screen, (0, 191, 255), (screen_size[1]/50, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0), (screen_size[0]/800) * self.mana, math.ceil((screen_size[0]/80.0)/2.0)))
        return mana_rect
    
    def ammoBar(self, screen, screen_size):
        ammo = self.weapon.currClip
        mana_border_rect = pygame.draw.rect(screen, (255, 255, 255), (screen_size[1]/50-2, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0) - 2, (screen_size[0]/800) * ((self.weapon.clipSize*100)/self.weapon.clipSize) + 4, (math.ceil(screen_size[0]/80.0)/2.0)+4))
        ammo_rect = pygame.Rect(screen_size[1]/50, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0), (screen_size[0]/800) * ((self.weapon.clipSize*100)/self.weapon.clipSize), math.ceil((screen_size[0]/80.0)/2.0))
        ammo_surf = self.createImg("images/ammobelt.jpg", ammo_rect)
        screen.blit(ammo_surf, ammo_rect)
        mana_back_rect = pygame.draw.rect(screen, (0, 0, 0), (screen_size[1]/50 + (screen_size[0]/800) * ((self.weapon.clipSize * 100)/self.weapon.clipSize), screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0), (screen_size[0]/800) * (((ammo - self.weapon.clipSize) * 100)/self.weapon.clipSize), math.ceil(screen_size[0]/80.0)/2.0))



        #try:
        #    mana_rect = pygame.draw.rect(screen, self.setImg("images/ammobelt.jpg"), (screen_size[1]/50, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0), (screen_size[0]/800) * ((ammo *100)/self.weapon.clipSize), math.ceil((screen_size[0]/80.0)/2.0)))
        #except Exception as e:
        #    mana_rect = pygame.draw.rect(screen, self.setImg("images/ammobelt.jpg"), (screen_size[1]/50, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0), (screen_size[0]/800) * 0, math.ceil((screen_size[0]/80.0)/2.0)))
        #return mana_rect
    
    def blink(self, mouse_x, mouse_y):
        if self.mana == 100:
            self.mana = 0
            self.x = float(mouse_x)
            self.y = float(mouse_y)
        else:
            pass
        
    def carry(self):
        if self.weapon != None:
            self.weapon.x = self.x
            self.weapon.y = self.y
    
    def getPosition(self):
        return (self.x, self.y)

    def setDiagSpeed(self, diagSpeed):
        self.diagonal_speed = diagSpeed
        
    def collidesWith(self, obj):
        return self.getRect().colliderect(obj.getRect())

    def getRect(self):
        return self.img.get_rect(x = self.x, y = self.y)    

    def drop(self, obj = None):
        if not obj == None:
            return obj
        else:
            randRange = random.randrange(0,100)
            if randRange <= 25:                
                return Handgun((self.x, self.y))
            elif randRange > 25 and randRange <= 50:
                return AssaultRifle((self.x, self.y))
            elif randRange > 50 and randRange <= 75:
                return Sawshot((self.x, self.y))
            elif randRange > 75 and randRange <= 100:
                return Flamethrower((self.x, self.y))
            elif randRange > 95:
                return Handgun((self.x, self.y))
###############################################################################################
        
##########################################  Weapon  ###########################################
class Weapon(Entity):
    
    def __init__(self, *args):
        pygame.init()
        super(Weapon, self).__init__(args[0],\
                                     args[1],\
                                     None,\
                                      0,\
                                     (32, 32),\
                                     None,\
                                     None,\
                                     None)
        self.ammo       = args[2]   #Ammo
        self.max_ammo   = args[2]   #Max ammo
        self.currClip   = args[3]   #Ammo in current clip
        self.clipSize   = args[3]   #Clip size (before reload)
        self.reloadTime = args[4]   #Reload time, seconds
        self.limiter    = 20
        self.rof        = args[5]   #Rate of fire
        self.projectile = args[6]   #Projectile
        self.activeRounds = []
        self.hasFired   = False

        
    def getAttributes(self):
        print "Weapon     : " + str(self)
        print "Ammo       : " + str(self.ammo)
        print "Max Ammo   : " + str(self.max_ammo)
        print "Curr Clip  : " + str(self.currClip)
        print "Clip Size  : " + str(self.clipSize)
        print "Reload Time: " + str(self.reloadTime)
        print "ROF        : " + str(self.rof)
        print "Projectile : " + str(self.projectile)
        print ""
        super(Weapon, self).getAttributes()
        
    def getActiveRounds(self):
        return self.activeRounds

    def setWeaponSecificDamage(self, dmg):
        self.projectile.dmg = dmg
        print self.projectile.dmg
        
    #Edit for Shell ************************
    def shoot(self, screen_size, old_screen_size):
        pressed = pygame.mouse.get_pressed()
        keys_pressed = pygame.key.get_pressed() # Get the pressed keys
        mouse_pos = pygame.mouse.get_pos()
        #make sound here!!!
        if (pressed[0] == 1 or keys_pressed[32] == 1) and self.currClip != 0 and self.limiter >= 20:            
            self.limiter = 0
            self.currClip -= 1
            self.activeRounds.append(self.projectile((self.x, self.y)))
            angle = math.atan2((self.y - mouse_pos[1]), (mouse_pos[0] - self.x)) / math.pi * 3.0
            self.activeRounds[0].rotation = math.degrees(angle)
            self.hasFired = True
        if self.hasFired and self.limiter < 20:
            self.limiter += 2 + self.rof / 3
        return self.activeRounds

    def reloadWeapon(self):
        clipRefillAmt = (self.clipSize - self.currClip)
        if self.ammo <= clipRefillAmt:
            self.currClip += self.ammo
            self.ammo = 0
        else:
            self.currClip += clipRefillAmt
            self.ammo -= clipRefillAmt            
        
    def getShells(self):
        return self.activeRounds
    #***************************************

class Handgun(Weapon):

    def __init__(self, coordinates):
        super(Handgun, self).__init__("images/handgun.png",\
                                      coordinates,\
                                      60,\
                                      15,\
                                      0,\
                                      .1,\
                                      MagRound)
        super(Handgun, self).setWeaponSecificDamage(1000)
        self.isHeld = False
    
    def shoot(self, scr, old):
        pressed = pygame.mouse.get_pressed()
        if pressed[0] and not self.isHeld:
                self.isHeld = True
                return super(Handgun, self).shoot(scr, old)
        elif pressed[0] == 0:
            self.isHeld = False        
        if self.hasFired and self.limiter < 20:
            self.limiter += self.rof
        return super(Handgun, self).getActiveRounds()

class AssaultRifle(Weapon):

    def __init__(self, coordinates):
        super(AssaultRifle, self).__init__("images/assualtrifle.png",\
                                      coordinates,\
                                      120,\
                                      30,\
                                      0,\
                                      4,\
                                      Bullet)

class Flamethrower(Weapon):

    def __init__(self, coordinates):
        super(Flamethrower, self).__init__("images/flamethrower.png",\
                                      coordinates,\
                                      300,\
                                      100,\
                                      0,\
                                      14,\
                                      Fireball)
class Sawshot(Weapon):

    def __init__(self, coordinates):
        super(Sawshot, self).__init__("images/sawshot.png",\
                                      coordinates,\
                                      25,\
                                      4,\
                                      0,\
                                      2,\
                                      Sawblade)

class ZombieHands(Weapon):

    def __init__(self, coordinates):
        super(ZombieHands, self).__init__((255,0,0),\
                                      coordinates,\
                                      300,\
                                      100,\
                                      0,\
                                      14,\
                                      None)
        self.dmg = 5
###############################################################################################

##########################################  Projectile  #######################################
class Projectile(Entity):
    #Shoot in the direction the mouse is pointing.

    def __init__(self, img, coordinates = (0, 0), dmg = 0, aoe = 0, WxH = (10,10), moveSpeed = (5,5), timeOnField = 9999):
       mouse_pos = pygame.mouse.get_pos()
       try:
           theta = math.atan2((mouse_pos[1] - coordinates[1]), -(mouse_pos[0] - coordinates[0])) - (math.pi/2)
           degrees = math.degrees(theta)# = -(math.degrees(rads) + 90)
           dx = math.degrees(math.sin(theta) * moveSpeed[0])
           dy = math.degrees(-math.cos(theta) * moveSpeed[1])
           moveSpeed = dx, dy
       except Exception as e:
           print e + "Projectile creation"
       super(Projectile, self).__init__(img,\
                                         coordinates,\
                                         None,\
                                         0,\
                                         WxH,\
                                         None,\
                                         moveSpeed,\
                                         None,\
                                         timeOnField)
       self.aoe        = aoe  #Area of effect
       self.dmg        = dmg  #Damage        
       self.isDestroyed = False        
       self.timeOnField = timeOnField
       super(Projectile, self).rotateTowardObject(pygame.mouse.get_pos())
       
    def destroy(self):
        self.isDestroyed = True
        
    def inBounds(self, screen_size):
        if self.x > screen_size[0]or self.y < 0 or self.y < 0 or self.y > screen_size[1]:
            return False
        return True
    
    def handleProjectile(self, rotation = 0):
        self.move()
        self.timeOnField -= 1
        if self.timeOnField == 0:
            self.destroy()        
        self.rotation += rotation
        round_source, round_dest = self.rotate(self.rotation)
        return round_source, round_dest
    
    def move(self):
        self.x += self.move_speed_xy[0]
        self.y -= self.move_speed_xy[1]
        rect = self.img.get_rect()
        rect.center = (self.x, self.y)
        return self.img, rect

    def getAttributes(self):        
        print "Damage     : " + str(self.dmg)
        print "AOE        : " + str(self.aoe)
        super(Projectile, self).getAttributes()

    def setDamage(self, dmg):
        self.dmg = dmg
        
class Fireball(Projectile):

    def __init__(self, coordinates = (0, 0)):
        super(Fireball, self).__init__("images/fireball.png",\
                                    coordinates,\
                                    10,\
                                    10,\
                                    (30,30),\
                                    (.05, .05),\
                                    30)
        
    def handleProjectile(self):
        return super(Fireball, self).handleProjectile(5)
        
class Bullet(Projectile):

    def __init__(self, coordinates = (0, 0)):
        super(Bullet, self).__init__("images/bullet.png",\
                                    coordinates,\
                                    5,\
                                    0,\
                                    (5,5),\
                                    (.2,.2))

class MagRound(Projectile):

    def __init__(self, coordinates = (0, 0)):
        super(MagRound, self).__init__("images/bullet.png",\
                                    coordinates,\
                                    100,\
                                    0,\
                                    (5,5),\
                                    (.3,.3))
        
class Sawblade(Projectile):

    def __init__(self, coordinates = (0, 0)):
        super(Sawblade, self).__init__("images/sawblade.png",\
                                    coordinates,\
                                    50,\
                                    0,\
                                    (15,15),\
                                    (.09,.09))
        
    def handleProjectile(self):
        return super(Sawblade, self).handleProjectile(5)
        
###############################################################################################

        
##########################################  Character  ########################################
class Player(Entity):
                                         
    def __init__(self, coordinates):
        super(Player, self).__init__("images/player.png",\
                                     coordinates,\
                                     100,\
                                     0,\
                                     (32, 32),\
                                     100,\
                                     (1.37,1.37),\
                                     AssaultRifle(coordinates))#Handgun((coordinates)))
        self.maxMana = self.weapon.clipSize
        self.mana = self.weapon.currClip

    def pickUp(self, obj):
        classType = obj.__class__.__bases__[0].__name__
        if classType == 'Weapon':
            self.maxMana = obj.clipSize
            temp = self.weapon
            obj.activeRounds = self.weapon.activeRounds
            self.weapon = obj
            return temp
        else:
            return None
            
        
    def getAttributes(self):
        print "Weapon     : " + str(self.weapon)
        self.weapon.getAttributes()
###############################################################################################
        
###########################################  Zombie  ##########################################
class Zombie(Entity):
    def __init__(self, coordinates):
        super(Zombie, self).__init__("images/zombie.png",\
                                     coordinates,\
                                     100,\
                                     0,\
                                     (32, 32),\
                                     None,\
                                     (.1, .1),\
                                     None)
        self.weapon = ZombieHands((self.x, self.y))
        self.dmgMultiplier = 0
        self.attackTime = 60

    def notAttacking(self):
        self.attackTime = 60

    def attack(self):
        self.attackTime += 1
        if self.attackTime >= 60:
            self.attackTime = 0
            #print self.weapon.dmg + (self.weapon.dmg * self.dmgMultiplier)
            return self.weapon.dmg + (self.weapon.dmg * self.dmgMultiplier)
        else:
            return 0

    def moveCheck(self, playerPosition, objectPosition):
        if self.intersect(playerPosition, self.getPosition(),\
                          objectPosition[0], objectPosition[1]):
            return True
        else:
            return False



    def move(self, playerPosition, objectPosition):
        if self.intersect(playerPosition, self.getPosition(),\
                          objectPosition[0], objectPosition[1]):
            self.moveRandomAI()
        else:
            self.moveSmartAI(playerPosition)
    def moveRandomAI(self):
        i = random.randrange(0,100)
        if(i<=10):
            self.moveRight()
        if(i<=20):
            self.moveLeft()
        if(i<=30):
            self.moveUp()
        if(i<=40):
            self.moveDown()
            
    def moveSmartAI(self, playerPosition):
        
        self.moveRandomAI()
        randRange = random.randrange(0,100)
        if(randRange >= 97):
            self.becomeSpecial()
        if(randRange >= 99):
            self.becomeSpecial2()
        
        if(playerPosition[0]>self.x):
            self.moveRight()
        if(playerPosition[1]>self.y):
            self.moveDown()
        if(playerPosition[0]<self.x):
            self.moveLeft()
        if(playerPosition[1]<self.y):
            self.moveUp()
            
    def moveRight(self):
        self.x += self.move_speed_xy[0]
        
    def moveLeft(self):
        self.x -= self.move_speed_xy[0]
        
    def moveUp(self):
        self.y -= self.move_speed_xy[1]
        
    def moveDown(self):
        self.y += self.move_speed_xy[1]

    # Does not make case for where x and y speeds vary.
    def becomeSpecial(self):
        if(self.move_speed_xy[0] > self.moveSpeedTemp[0]):
            self.move_speed_xy = self.moveSpeedTemp
            self.dmgMultiplier = 0
        else:
            self.move_speed_xy = self.move_speed_xy[0] + .3,\
                                 self.move_speed_xy[1] + .3
            self.dmgMultiplier = .5
    # Does not make case for where x and y speeds vary.  
    def becomeSpecial2(self):
            self.move_speed_xy = self.move_speed_xy[0] + .7,\
                                 self.move_speed_xy[1] + .7
            self.dmgMultiplier = 1
            
    def counterClockwiseOrder(self, A, B, C):
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
    
    def intersect(self, A, B, C, D):
        return self.counterClockwiseOrder(A,C,D) != self.counterClockwiseOrder(B,C,D) and self.counterClockwiseOrder(A,B,C) != self.counterClockwiseOrder(A,B,D)
###############################################################################################


class Object():
    def __init__(self):
        self.x = random.randrange(50,500)
        self.y = random.randrange(50,500)
        self.w = 10
        self.h = 100
        self.color = 10,10,10
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 0)
        
    def givePosition(self):
        return ((self.x,self.y),(self.x+self.w, self.y+self.h))

    def getRect(self):
        return (self.x+15, self.y+15, self.w, self.h)

