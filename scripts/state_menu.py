import graphics   as gfx 
import state_enum as states
import common
import button
import aabb
import apple
import highscores

import time
import random
import math

def getRandX():
    '''Gets a random X-Position not above the button bounds'''
    return random.randint(0, common.WINDOW_WIDTH)

def addApple(apples, window):
    '''Adds an apple to the background of the menus'''
    x = getRandX()
    y = random.randint(-common.WINDOW_HEIGHT, 0)
    r = random.randint(5, 20)
    apples.append(apple.makeApple(x, y, "red", r, window))
    apples[-1].setOutline("red")

def updateApples(apples, window):
    '''Updates the apples, such as moves them as removes them when they hit the bottom'''
    for app in apples[:]:
        app.move(0, app.getRadius() / 5)
        #app.move(math.sin(elapsed) * app.getRadius(), app.getRadius() / 5)
        if app.getCenter().getY() > common.WINDOW_HEIGHT + apple.DIAMETER:
            app.undraw()
            apples.remove(app)
            addApple(apples, window)

def createHowToPlayMenu(window):
    sprites = [
        common.createTitle("HOW TO PLAY")
        #common.createCenteredImage("how_to_play")
    ]
    common.drawList(sprites, window)

    guiY =  common.WINDOW_HEIGHT / 10 + 50

    ctrlBtn,   \
    ctrlTxt,   \
    ctrlBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Controls", window, "gray")
    guiY += button.HEIGHT * 2
    objBtn,   \
    objTxt,   \
    objBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Objective", window, "gray")
    guiY += button.HEIGHT * 2
    typeBtn,   \
    typeTxt,   \
    typeBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Apple Types", window, "gray")

    #This is a list of sprites that have no purpose but to be shown, hence stored in a list
    #for ease of undrawing.
    sprites += [ctrlBtn, ctrlTxt, 
                objBtn,  objTxt, 
                typeBtn, typeTxt]

    return sprites, ctrlBounds, objBounds, typeBounds

def createHowToControls(window):
    sprites = [
        common.createTitle("Controls")
        #common.createCenteredImage("how_to_play")
    ]
    common.drawList(sprites, window)
    return sprites

def createHowToObjectives(window):
    sprites = [
        common.createTitle("Objectives")
        #common.createCenteredImage("how_to_play")
    ]
    common.drawList(sprites, window)
    return sprites

def createHowToAppleTypes(window):
    sprites = [
        common.createTitle("Apple Types")
        #common.createCenteredImage("how_to_play")
    ]
    common.drawList(sprites, window)
    return sprites

def displayHowToPlayMenu(window, control, apples):
    sprites, ctrlButton, objButton, typeButton = createHowToPlayMenu(window)
    backButton,      \
    backButtonText,  \
    backButtonBounds = button.create(aabb.create(button.LEFT, common.WINDOW_HEIGHT - button.HEIGHT - 10, 
                                     button.WIDTH, button.HEIGHT), 
                                     "Back", window, "gray")

    def displayMenu(guiCreateFunction):
        common.undrawList(sprites + [backButton, backButtonText])
        showMenu(window, control, apples, guiCreateFunction)
        if window.closed:
            return True
        common.drawList(sprites + [backButton, backButtonText], window)
        return False

    while not window.closed:
        mouseClickPoint = window.checkMouse()
        updateApples(apples, window)
        if button.isButtonPressed(mouseClickPoint, backButtonBounds, window):
            break
        if button.isButtonPressed(mouseClickPoint, ctrlButton, window):
            if displayMenu(createHowToControls):
                break
        if button.isButtonPressed(mouseClickPoint, objButton, window):
            if displayMenu(createHowToObjectives):
                break
        if button.isButtonPressed(mouseClickPoint, typeButton, window):
            if displayMenu(createHowToAppleTypes):
                break
        common.redrawList(sprites, window)
        gfx.update(common.UPDATE_SPEED)
    common.undrawList(sprites + [backButton, backButtonText])

def showMenu(window, control, apples, guiCreateFunction):
    sprites = guiCreateFunction(window)
    backButton,      \
    backButtonText,  \
    backButtonBounds = button.create(aabb.create(button.LEFT, common.WINDOW_HEIGHT - button.HEIGHT - 10, 
                                     button.WIDTH, button.HEIGHT), 
                                     "Back", window, "gray")
    sprites += [backButton, backButtonText]
    while not window.closed:
        mouseClickPoint = window.checkMouse()
        updateApples(apples, window)
        if button.isButtonPressed(mouseClickPoint, backButtonBounds, window):
            break
        common.redrawList(sprites, window)
        gfx.update(common.UPDATE_SPEED)
    common.undrawList(sprites)

def createFrontMenuButtons(window):
    '''Creates the main buttons for the main menu'''
    guiY =  common.WINDOW_HEIGHT / 10 + 50

    playBtn,   \
    playTxt,   \
    playBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Play Game", window, "gray")
    guiY += button.HEIGHT * 2
    howToPlayBtn,   \
    howToPlayTxt,   \
    howToPlayBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                                    "How To Play", window, "gray")

    guiY += button.HEIGHT * 2
    highBtn,   \
    highTxt,   \
    highBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Highscores", window, "gray")

    guiY += button.HEIGHT * 2
    exitBtn,   \
    exitTxt,   \
    exitBounds = button.create(aabb.create(button.LEFT, guiY, button.WIDTH, button.HEIGHT), 
                               "Exit", window, "gray")

    #This is a list of sprites that have no purpose but to be shown, hence stored in a list
    #for ease of undrawing.
    sprites = [ playBtn,        playTxt, 
                howToPlayBtn,   howToPlayTxt, 
                highBtn,        highTxt,
                exitBtn,        exitTxt]

    return sprites, playBounds, howToPlayBounds, highBounds, exitBounds



def runMenuState(window, control):
    '''Says it on the tin'''
    title = "ANDROID APPLE DROP"
    titleText = common.createTitle(title, window)

    sprites,         \
    playButton,      \
    howToPlayButton, \
    highscoreButton, \
    exitButton       = createFrontMenuButtons(window)

    apples = []
    for i in range(100):
        addApple(apples, window)

    def displayMenu(guiCreateFunction = None):
        common.undrawList([titleText] + sprites)
        showMenu(window, control, apples, guiCreateFunction)
        if window.closed:
            return True
        common.drawList([titleText] + sprites, window)
        return False
    
    start = time.time()
    while control["state"] == states.STATE_MENU and not window.closed:
        key   = common.getKeyPress(window)
        point = window.checkMouse()
        elapsed = common.calculateTime(start)

        if button.isButtonPressed(point, playButton, window):
            common.switchState(window, control, states.STATE_PLAYING)
        elif button.isButtonPressed(point, howToPlayButton, window):
            common.undrawList([titleText] + sprites)
            displayHowToPlayMenu(window, control, apples)
            if window.closed:
                break
            common.drawList([titleText] + sprites, window)
        elif button.isButtonPressed(point, highscoreButton, window):
            if displayMenu(highscores.createHighscoresDisplay):
                break
        elif button.isButtonPressed(point, exitButton, window):
            common.switchState(window, control, states.EXIT)

        updateApples(apples, window)
        #make it so the title is ALWAYS on front
        common.redrawList([titleText] + sprites, window)
        gfx.update(common.UPDATE_SPEED)

    common.undrawList([titleText] + sprites + apples)