import time
import pygame

# Checking if load in is succesfull
try:
    pygame.init()
except False:
    print("Fail")
else:
    print("Success")

# Basic Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Initializing Display and Clock
DisplayX = 400
DisplayY = 450
Display = pygame.display.set_mode((DisplayX, DisplayY))
Display.fill(white)
pygame.display.set_caption("CastleCrasher")
pygame.display.set_icon(pygame.image.load('Sprites/GameLogo.png'))
border = pygame.image.load('Sprites/GameEnvironments/Border.png')
clock = pygame.time.Clock()

# Initializing Character Sprites and States
CharacterUp = pygame.image.load('Sprites/Basic Movement/Up.png')
CharacterDown = pygame.image.load('Sprites/Basic Movement/Down.png')
CharacterCenter = pygame.image.load('Sprites/Basic Movement/Center.png')
CharacterRight = pygame.image.load('Sprites/Basic Movement/Right.png')
CharacterLeft = pygame.image.load('Sprites/Basic Movement/Left.png')
CharacterRightSword = pygame.image.load('Sprites/SwordStuff/SwordCharacterRight.png')
CharacterLeftSword = pygame.image.load('Sprites/SwordStuff/SwordCharacterLeft.png')

# Initializing Sprites for Sword Attack Animation
SwordAttackRight = [pygame.image.load('Sprites/SwordStuff/Animations/RightSwordAnimation/SwordRightFrame1.png'),
                    pygame.image.load('Sprites/SwordStuff/Animations/RightSwordAnimation/SwordRightFrame2.png'),
                    pygame.image.load('Sprites/SwordStuff/Animations/RightSwordAnimation/SwordRightFrame3.png'),
                    pygame.image.load('Sprites/SwordStuff/Animations/RightSwordAnimation/SwordRightFrame4.png'),
                    pygame.image.load('Sprites/SwordStuff/Animations/RightSwordAnimation/SwordRightFrame5.png'),
                    pygame.image.load('Sprites/SwordStuff/Animations/RightSwordAnimation/SwordRightFrame6.png')]
SwordAttackLeft = [pygame.image.load('Sprites/SwordStuff/Animations/LeftSwordAnimation/SwordLeftFrame1.png'),
                   pygame.image.load('Sprites/SwordStuff/Animations/LeftSwordAnimation/SwordLeftFrame2.png'),
                   pygame.image.load('Sprites/SwordStuff/Animations/LeftSwordAnimation/SwordLeftFrame3.png'),
                   pygame.image.load('Sprites/SwordStuff/Animations/LeftSwordAnimation/SwordLeftFrame4.png'),
                   pygame.image.load('Sprites/SwordStuff/Animations/LeftSwordAnimation/SwordLeftFrame5.png'),
                   pygame.image.load('Sprites/SwordStuff/Animations/LeftSwordAnimation/SwordLeftFrame6.png')]
AttackFrameCount = 0
AttackTicker = 0
# State Variables
CurrentItem = 'none'
IsAttacking = False

# Initializing Sprites for Health Potion Sprites
CharacterHealthPotionRight = pygame.image.load(
    'Sprites/Collectibles Character Animations/HealthPotion/CharacterHealthPotionRight.png')
CharacterHealthPotionLeft = pygame.image.load(
    'Sprites/Collectibles Character Animations/HealthPotion/CharacterHealthPotionLeft.png')

# Setting Up Inventory
inventoryFrame = pygame.image.load('Sprites/GameEnvironments/Inventory/InventoryFrame/InventoryFrame.png')
inventorySword = pygame.image.load('Sprites/GameEnvironments/Inventory/InventoryItems/InventorySword.png')
selectedItemFrame = pygame.image.load('Sprites/GameEnvironments/Inventory/InventoryFrame/SelectedItemSlot.png')

# Keeping track of current inventory item index
CurrentInvItemIndex = 0

# Inventory Items have to be 32x40
inventoryItems = [inventorySword]
inventoryCoords = [(10, 404), (60, 404), (110, 404), (160, 404), (210, 404), (260, 404), (310, 404), (360, 404),
                   (410, 404)]


# List for game objecsts
gameObjects = []
# Index number for removing collectibles on pickup
ColllectiblesIndex = 0

# Functino for adding Normal or Collective Objects
def MakeGameObject(RepetitiveOrNot, Object, ObjectCoords):
    global gameObjects
    if RepetitiveOrNot == 'yes':
        gameObjects.append((Object, (ObjectCoords)))
        for i in range(0, len(gameObjects)):
            Display.blit(gameObjects[i][0], gameObjects[i][1])
            pygame.display.update()
        gameObjects.pop(len(gameObjects) - 1)
    else:
        gameObjects.append((Object, (ObjectCoords)))


# making Inventory bar
def MakeInventoryandObjects():
    global inventoryItems, inventoryCoords, CurrentInvItemIndex, gameObjects
    Display.blit(inventoryFrame, (0, 400))

    for i in range(0, len(gameObjects)):
        Display.blit(gameObjects[i][0], gameObjects[i][1])

    for i in range(0, len(inventoryItems)):
        Display.blit(inventoryItems[i], inventoryCoords[i])
    if CurrentItem == 'none':
        pass
    else:
        Display.blit(selectedItemFrame, (50 * CurrentInvItemIndex, 400))


# General Functions
currentCharacterCoord = [200, 200]
Display.blit(CharacterCenter, (200, 200))
Direction = 'center'


# resetting env
def resetEnvironment():
    Display.fill(white)
    Display.blit(border, (0, 0))
    MakeInventoryandObjects()


# moving character
def moveCharacter():
    global Direction
    if Direction == 'left':
        if CurrentItem == 'sword':
            if currentCharacterCoord[0] > 42:
                currentCharacterCoord[0] -= 10
        else:
            if currentCharacterCoord[0] > 20:
                currentCharacterCoord[0] -= 10


    elif Direction == 'right':
        if CurrentItem == 'sword':
            if currentCharacterCoord[0] + 20 < 350:
                currentCharacterCoord[0] += 10
        else:
            if currentCharacterCoord[0] + 20 < 370:
                currentCharacterCoord[0] += 10

    elif Direction == 'up':
        if currentCharacterCoord[1] > 20:
            currentCharacterCoord[1] -= 10

    elif Direction == 'down':
        if currentCharacterCoord[1] + 20 < 350:
            currentCharacterCoord[1] += 10


# making character
def makeCharacter():
    resetEnvironment()
    if CurrentItem == 'sword':
        if Direction == 'up':
            Display.blit(CharacterUp, currentCharacterCoord)
        elif Direction == 'down':
            Display.blit(CharacterDown, currentCharacterCoord)
        elif Direction == 'right':
            Display.blit(CharacterRightSword, currentCharacterCoord)
        elif Direction == 'left':
            Display.blit(CharacterLeftSword, (currentCharacterCoord[0] - 20, currentCharacterCoord[1]))
        else:
            Display.blit(CharacterCenter, currentCharacterCoord)
    elif CurrentItem == 'health potion':
        if Direction == 'up':
            Display.blit(CharacterUp, currentCharacterCoord)
        elif Direction == 'down':
            Display.blit(CharacterDown, currentCharacterCoord)
        elif Direction == 'right':
            Display.blit(CharacterHealthPotionRight, currentCharacterCoord)
        elif Direction == 'left':
            Display.blit(CharacterHealthPotionLeft, (currentCharacterCoord[0] - 20, currentCharacterCoord[1]))
    else:
        if Direction == 'up':
            Display.blit(CharacterUp, currentCharacterCoord)
        elif Direction == 'down':
            Display.blit(CharacterDown, currentCharacterCoord)
        elif Direction == 'right':
            Display.blit(CharacterRight, currentCharacterCoord)
        elif Direction == 'left':
            Display.blit(CharacterLeft, (currentCharacterCoord[0], currentCharacterCoord[1]))
        else:
            Display.blit(CharacterCenter, currentCharacterCoord)


# checking which key is pressed
def checkKey():
    global Direction, CurrentItem, IsAttacking, AttackTicker, CurrentInvItemIndex
    AttackTicker += 1
    for event in pygame.event.get():
        # Check if event is quit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Check if event is keypress
        elif event.type == pygame.KEYDOWN:
            # Check if event is movement
            if event.key == pygame.K_a:
                Direction = "left"
                moveCharacter()
            elif event.key == pygame.K_d:
                Direction = "right"
                moveCharacter()
            elif event.key == pygame.K_w:
                Direction = "up"
                moveCharacter()
            elif event.key == pygame.K_s:
                Direction = "down"
                moveCharacter()

            # Check if inventory number is pressed
            elif event.key == pygame.K_1:
                CurrentItem = "none"
            elif event.key == pygame.K_2:
                CurrentItem = "sword"
                CurrentInvItemIndex = 0
            elif event.key == pygame.K_3 and hasHealthPotion == True:
                CurrentItem = "health potion"
                CurrentInvItemIndex = 1
            elif event.key == pygame.K_4:
                CurrentItem = ""
                CurrentInvItemIndex = 2
            elif event.key == pygame.K_5:
                CurrentItem = ""
                CurrentInvItemIndex = 3
            elif event.key == pygame.K_6:
                CurrentItem = ""
                CurrentInvItemIndex = 4
            elif event.key == pygame.K_7:
                CurrentItem = ""
                CurrentInvItemIndex = 5
            elif event.key == pygame.K_8:
                CurrentItem = ""
                CurrentInvItemIndex = 6
            elif event.key == pygame.K_9:
                CurrentItem = ""
                CurrentInvItemIndex = 7

            # Check if attack is pressed
            elif event.key == pygame.K_SPACE and CurrentItem == 'sword' and AttackTicker >= 22:
                AttackTicker = 0
                SwordAttack()
                IsAttacking = False

            else:
                pass


# displaying attack animation
def SwordAttack():
    global Direction, AttackFrameCount, IsAttacking
    if IsAttacking == False:
        while True:
            IsAttacking = True
            if (AttackFrameCount + 1 >= 30):
                AttackFrameCount = 0
                break
            if Direction == 'right':
                Display.blit(SwordAttackRight[AttackFrameCount // 5],
                             (currentCharacterCoord[0] - (2 * (AttackFrameCount // 5)), currentCharacterCoord[1]))
                pygame.display.update()
                resetEnvironment()
                time.sleep(0.005)
                AttackFrameCount += 1
            elif Direction == 'left':
                Display.blit(SwordAttackLeft[AttackFrameCount // 5],
                             (currentCharacterCoord[0] - (6.5 * (AttackFrameCount // 5)), currentCharacterCoord[1]))
                pygame.display.update()
                resetEnvironment()
                time.sleep(0.005)
                AttackFrameCount += 1


# Levels

hasHealthPotion = False


def TestLevel():
    global gameObjects, inventoryItems, hasHealthPotion, CurrentItem, ColllectiblesIndex, CollectionPopOutOfListTemp
    # Setting up health potion
    HealthPotion = pygame.image.load('Sprites/GameEnvironments/Inventory/InventoryItems/HealthPotion.png')
    if hasHealthPotion == False:
        MakeGameObject('yes', HealthPotion, (300, 100))
    if 280 < currentCharacterCoord[0] < 320 and 150 > currentCharacterCoord[1] > 50 and hasHealthPotion != True:
        inventoryItems.append(HealthPotion)
        hasHealthPotion = True
        return True


hasHealthPotion1 = False


def Level1():
    global gameObjects, inventoryItems, hasHealthPotion1, CurrentItem, ColllectiblesIndex, CollectionPopOutOfListTemp
    # Setting up health potion
    HealthPotion = pygame.image.load('Sprites/GameEnvironments/Inventory/InventoryItems/HealthPotion.png')
    if hasHealthPotion1 == False:
        MakeGameObject('yes', HealthPotion, (100, 300))
    if 80 < currentCharacterCoord[0] < 120 and 350 > currentCharacterCoord[1] > 250 and hasHealthPotion1 != True:
        inventoryItems.append(HealthPotion)
        hasHealthPotion1 = True
        return True


# Variable for keeping track of level
CurrentLevel = 1
while True:
    # fps
    clock.tick(30)

    makeCharacter()
    checkKey()

    # Level Testing
    if CurrentLevel == 1:
        if TestLevel() == True:
            CurrentLevel += 1
    elif CurrentLevel == 2:
        Level1()

    pygame.display.update()

print("HI?")