#################################################
# FINAL TPPPP!!!!
#
# Version 14:
# What I've done: final touches
# Next step(in the future if I have time): circle view dots, or powerups
# 
# Your name: Audi Lin
# Your andrew id: audil
#################################################

import math, copy, random, time, decimal

# from the cmu 15-112 class notes
from cmu_112_graphics import *

#################################################
def dist(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# adapted from CMU 15-112 course notes: https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

# from CMU 15-112 course
def roundHalfUp(d):  # helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# adapted from my solution hw1 question 10: https://www.cs.cmu.edu/~112/notes/hw1.html 
def colorBlender(rgb1, rgb2, midpoints):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    colors = []
    
    rinc = (r2 - r1) / (midpoints + 1)  # increment of change for red
    ginc = (g2 - g1) / (midpoints + 1)  # increment of change for green
    binc = (b2 - b1) / (midpoints + 1)  # increment of change for blue
    for n in range(midpoints + 2):
        rn = roundHalfUp(r1 + n * rinc)
        gn = roundHalfUp(g1 + n * ginc)
        bn = roundHalfUp(b1 + n * binc)
        rgbn = (rn, gn, bn)
        colors.append(rgbString(rgbn))  
    return colors

def appStarted(app):
    app.player = Player(app, app.height / 20)
    color = (181, 51, 184) # starting color : purple
    app.mainColor = "black"
    app.backgroundColors = colorBlender(color, (0, 0, 0), 50)
    app.backgroundColorIndex = 0
    app.gameOver = False
    app.spikeWidth = app.width / 30
    app.spikeOffset = app.width * 0.7 # change spike offset instead of the individual spike x values
    app.minSpikeHeight = app.height / 20
    app.maxSpikeHeight = app.height * 0.6
    app.spikeMargin = app.height / 13
    app.spikes = makeSpikes(app, 100, 0, app.height)
    app.paused = False
    app.speed = app.width // 120 # 5
    app.timer = 0
    app.bestScore = 0
    app.spikeTimer = 0
    app.screen = "homeScreen"
    app.currentMap = "random map"
    app.message = ""

    app.buttons = [Button(app, "INSTRUCTIONS(i)", "instructionScreen", 0),
                    Button(app, "SAVED MAPS(m)", "mapScreen", 1),
                    Button(app, "ABOUT(a)", "aboutScreen", 2)]
    app.instructions = [
        "INSTRUCTIONS!!!",
        "",
        "to fly higher, the player can",
        "press (SPACE) or click the screen",
        "",
        "If the player touches the cave spikes,",
        "then the player will die :(",
        "",
        "Don't worry, you can always revive",
        "and try again with a new map",
        "",
        "Make it as far as you can and keep on trying!",
        "",
        "to start playing, press (SPACE)!",
        "to pause while playing, press (p)",
        "to go back to the home screen, press (h)"
    ]
    app.savedMaps = {}
    app.about = [
        "Hi! I'm Audi Lin, the marvelous creator",
        "and I'm so glad you're playing my game!",
        "",
        "This game was made the week of 8/9/2021",
        "for my CMU 15-112 term project",
        "",
        "I spent countless hours working on it,",
        "and I hope you enjoy playing it :)",
        "",
        "This game is a replication of a game on my phone",
        "by the same name, so I didn't come up with the concept,",
        "but I added some my own fun features I hope you like.",
        "",
        "to go back to the home screen, press (h)"
    ]
    
    # for the bat that flaps on the home screen
    app.homeScreenBat = Player(app, app.height / 5)
    app.homeScreenBat.x = app.width / 2
    app.homeScreenBat.y = app.height * 0.35
    app.homeScreenBat.color = None
    app.homeScreenTimer = 0

    app.lastKeyPressed = ""

def resetScreen(app):
    app.player = Player(app, app.height / 20)
    app.gameOver = False
    app.backgroundColorIndex = 0
    app.spikeWidth = app.width / 30
    app.spikeOffset = app.width * 0.7 # change spike offset instead of the individual spike x values
    app.minSpikeHeight = app.height / 20
    app.maxSpikeHeight = app.height * 0.6
    app.spikeMargin = app.height / 13
    app.paused = False
    app.spikes = makeSpikes(app, 100, 0, app.height)
    app.currentMap = "random map"
    app.speed = app.width // 120 # 5
    app.timer = 0
    app.spikeTimer = 0
    app.buttons = [Button(app, "INSTRUCTIONS(i)", "instructionScreen", 0),
                    Button(app, "SAVED MAPS(m)", "mapScreen", 1),
                    Button(app, "ABOUT(a)", "aboutScreen", 2)]
    app.homeScreenBat = Player(app, app.height / 5)
    app.homeScreenBat.x = app.width / 2
    app.homeScreenBat.y = app.height * 0.35
    app.homeScreenBat.color = None
    app.homeScreenTimer = 0

def sizeChanged(app):
    resetScreen(app)
    app.screen = "homeScreen"
    app.savedMaps = {} # because otherwise the sizing will be off

class Button(object): # specifically for buttons on the home screen
    def __init__(self, app, displayText, screen, index):
        self.app = app
        self.displayText = displayText
        self.screen = screen
        self.index = index
        self.y = app.height * 0.55 + index * (app.height / 7) # top of box
        self.height = app.height / 10
    
    def checkClicked(self, x, y):
        x0, y0, x1, y1 = self.app.width * 0.3, self.y, self.app.width * 0.7, self.y + self.height
        if x >= x0 and x <= x1 and y >= y0 and y <= y1:
            self.app.screen = self.screen

    def draw(self, canvas):
        canvas.create_rectangle(self.app.width * 0.3, self.y,
                            self.app.width * 0.7, self.y + self.height,
                            fill = "white")
        canvas.create_text(self.app.width / 2, self.y + self.height,
                        text = self.displayText, anchor = 's',
                        font = f"Arial {self.app.height // 20}")

class Player(object):
    def __init__(self, app, r):
        self.app = app
        self.x = app.width * 0.4
        self.y = app.height / 2
        self.r = r # 15 before
        self.yV = 0  # velocity
        self.yA = app.height / 400  # acceleration
        self.color = "hot pink"

        # adapted from 15-112 course notes: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
        self.spriteIndex = 0
        spritestrip = app.loadImage('batspritesheet.png')
        spritestrip = app.scaleImage(spritestrip, self.r / 200)
        self.sprites = [ ]
        imageWidth, imageHeight = spritestrip.size
        for i in range(2):
            sprite = spritestrip.crop(((imageWidth / 2)*i, 0, (imageWidth / 2)*(i+ 1), imageHeight))
            self.sprites.append(sprite)
    
    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r,
                        self.x + self.r, self.y + self.r,
                        fill = self.color, width = 0)
        sprite = self.sprites[self.spriteIndex]
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite))
        
class Spike(object):
    def __init__(self, app, index, leftY, rightY, pointingDown):
        self.app = app
        self.width = self.app.spikeWidth
        self.index = index
        self.x = index * self.width + self.app.spikeOffset # dependent on index and offset
        self.color = app.mainColor
        self.leftY = leftY # left y-value
        self.rightY = rightY # right y-value
        self.length = dist(0, leftY, self.width, rightY)
        self.slope = (self.rightY - self.leftY) / self.width
        self.cosalpha = (self.rightY - self.leftY) / self.length
        self.intersectionX = 0
        self.pointingDown = pointingDown # bool
        self.touchingPlayer = False

    def updateX(self):
        self.x = self.index * self.width + self.app.spikeOffset

    def touching(self, player): # checks if the spike is touching the player
        halfWidth = self.width / 2
        yOffset = self.length * (player.r / self.width) - 0.01 # using triangle similarity
        # point-slope formula : y - y1 = m * (x - x1)
        # y1 = leftHeight +/- yOffset, x1 = middleX - halfWidth
        self.touchingPlayer = False

        if self.pointingDown: # check if intersects top "spikes"
            leftside = player.y - (self.leftY + yOffset)
            rightside = self.slope * (player.x - (self.x - halfWidth))
            if leftside < rightside:
                self.intersectionX = player.x + player.r * self.cosalpha
                if ((self.x - halfWidth <= self.intersectionX <= self.x + halfWidth) or # intersection is tangent as expected
                        (dist(self.x + halfWidth, self.rightY, player.x, player.y) < player.r) or # right corner inside circle
                        (dist(self.x - halfWidth, self.leftY, player.x, player.y) < player.r)): #left corner inside circle
                    self.touchingPlayer = True
        else: # check if intersects bottom "spikes"
            leftside = player.y - (self.leftY - yOffset)
            rightside = self.slope * (player.x - (self.x - halfWidth))
            if leftside > rightside:
                self.intersectionX = player.x - player.r * self.cosalpha
                if ((self.x - halfWidth <= self.intersectionX <= self.x + halfWidth) or # intersection is tangent as expected   
                        (dist(self.x + halfWidth, self.rightY, player.x, player.y) < player.r) or # right corner inside circle
                        (dist(self.x - halfWidth, self.leftY, player.x, player.y) < player.r)): #left corner inside circle
                    self.touchingPlayer = True
        
        if self.touchingPlayer:
            self.color = "red"
            self.app.gameOver = True
            self.app.backgroundColorIndex = 0
        else:
            self.intersectionX = 0
            self.color = self.app.mainColor

    def draw(self, canvas):
        halfWidth = self.width / 2
        if self.pointingDown:
            canvas.create_polygon(self.x - halfWidth, 0,
                            self.x + halfWidth, 0,
                            self.x + halfWidth, self.rightY,
                            self.x - halfWidth, self.leftY,
                            fill = self.color, outline = self.color)
        else:
            canvas.create_polygon(self.x - halfWidth, self.app.height,
                            self.x + halfWidth, self.app.height,
                            self.x + halfWidth, self.rightY,
                            self.x - halfWidth, self.leftY,
                            fill = self.color, outline = self.color)

def makeSpikes(app, n, topStartY, bottomStartY, indexOffset = 0): # returns a list of n up & n down Spike objects
    spikes = []
    oldYs = topStartY, bottomStartY
    generalDirection = 1
    for i in range(n):
        topOldY, bottomOldY = oldYs
        minInc = app.height // 20 # 20
        maxInc = app.height // 8 # 50
        smallerMinInc = app.height // 40 # 10
        smallerMaxInc = app.height // 13 # 30

        # choose new y-values for the top spikes
        if topOldY < app.minSpikeHeight + app.spikeMargin:
            topNewY = topOldY + random.choice(range(minInc, maxInc))
            generalDirection = 1
        elif topOldY > app.maxSpikeHeight - app.spikeMargin:
            topNewY = topOldY + random.choice(range(-1 * maxInc, -1 * minInc))
            generalDirection = -1
        else:
            topNewY = topOldY + generalDirection * random.choice(range(-1 * smallerMinInc, smallerMaxInc))

        # choose new y-values for the bottom spikes
        if bottomOldY > app.height - (app.minSpikeHeight + app.spikeMargin):
            bottomNewY = bottomOldY + random.choice(range(-1 * maxInc, -1 * minInc))
            generalDirection = -1
        elif bottomOldY < app.height - (app.maxSpikeHeight - app.spikeMargin):
            bottomNewY = bottomOldY + random.choice(range(minInc, maxInc))
            generalDirection = 1
        else:
            bottomNewY = bottomOldY + generalDirection * random.choice(range(-1 * smallerMinInc, smallerMaxInc))
        
        # check if spikes are too close
        if abs(topNewY - bottomNewY) < app.player.r * 5:
            topNewY -= app.player.r * 0.5
            bottomNewY += app.player.r * 1.5
        
        # add spikes to list
        downSpike = Spike(app, i + indexOffset, topOldY, topNewY, True)
        upSpike = Spike(app, i + indexOffset, bottomOldY, bottomNewY, False)
        spikes.append(downSpike)
        spikes.append(upSpike)
        oldYs = topNewY, bottomNewY
    return spikes

def keyPressed(app, event):
    if event.key == "Space":
        app.screen = "gameScreen"
        app.player.yV = -1 * app.height // 70 # 6
    elif event.key == "h":
        resetScreen(app)
        app.screen = "homeScreen"
    elif event.key == "i":
        resetScreen(app)
        app.screen = "instructionScreen"
    elif event.key == "m":
        resetScreen(app)
        app.screen = "mapScreen"
    elif event.key == "a":
        resetScreen(app)
        app.screen = "aboutScreen"
    
    if app.screen == "gameScreen":
        if event.key == 'r':
            resetScreen(app)
            app.screen = "gameScreen"
        elif event.key == 'p':
            app.paused = not app.paused
        
        elif event.key == "s": # save map
            if 0 <= len(app.savedMaps) < 10 and app.gameOver and app.currentMap == "random map":
                name = f"Map {len(app.savedMaps) + 1}"
                app.currentMap = name
                app.savedMaps[name] = [app.timer / 1000, app.spikes] # keeps track of score too
                app.message = f"Map was saved as {name}\npress (m) to see saved maps"
            elif len(app.savedMaps) >= 10:
                app.message = f"You cannot save more than 9 maps"
        
        if app.paused:
            if event.key == "Up":
                app.player.y -= 1
            elif event.key == "Down":
                app.player.y += 1
            elif event.key == "Left":
                app.spikeOffset += app.speed
                for spike in app.spikes:
                    spike.updateX()
            elif event.key == "Right":
                app.spikeOffset -= app.speed
                for spike in app.spikes:
                    spike.updateX()
            
            for spike in app.spikes: # update what spikes the player is touching
                spike.touching(app.player)
    
    elif app.screen == "mapScreen":
        if event.key in "123456789":
            name = "Map " + event.key
            if name in app.savedMaps:
                resetScreen(app)
                app.currentMap = name
                app.spikes = app.savedMaps[name][1]
                app.screen = "gameScreen"
            else:
                print("Pick a valid map")
            
    app.lastKeyPressed = event.key

def mousePressed(app, event):
    if app.screen == "homeScreen":
        for button in app.buttons:
            button.checkClicked(event.x, event.y)
    elif app.screen == "gameScreen":
        app.player.yV = -1 * app.height // 70 # go up

def timerFired(app):
    if app.screen == "homeScreen":
        app.homeScreenTimer += app.timerDelay
        while app.homeScreenTimer > 500: # flap the wings of the home screen bat
            app.homeScreenBat.spriteIndex = (app.homeScreenBat.spriteIndex + 1) % 2
            app.homeScreenTimer -= 500
    
    elif app.screen == "gameScreen":
        if not app.gameOver and not app.paused:
            if app.currentMap == "random map":
                app.bestScore = 0
            else:
                app.bestScore = app.savedMaps[app.currentMap][0]
            
            app.timer += app.timerDelay
            app.spikeTimer += app.timerDelay

            app.player.y += app.player.yV
            app.player.yV += app.player.yA
            if app.player.yV > -1: # going down
                app.player.spriteIndex = 0
            else: # going up
                app.player.spriteIndex = 1

            # change background color
            if app.backgroundColorIndex < len(app.backgroundColors) - 1:
                app.backgroundColorIndex += 1

            # move spikes
            app.spikeOffset -= app.speed
            for spike in app.spikes:
                if spike.touching(app.player):
                    break
                spike.updateX()
        
        # if player goes out of bounds
        if app.player.y + app.player.r > app.height or app.player.y - app.player.r < 0:
            app.gameOver = True

        # add a new group of 100 spikes
        x = (app.spikeWidth / app.speed) * app.timerDelay # amount of time it takes for 1 spike to pass
        if app.spikeTimer > (x):
            app.spikeTimer -= (100 * x)
            if app.currentMap == "random map":
                size = len(app.spikes)
                lastTopSpike = app.spikes[size - 2]
                lastBottomSpike = app.spikes[size - 1]

                topStartY = lastTopSpike.rightY
                bottomStartY = lastBottomSpike.rightY
                indexOffset = size //  2
                app.spikes += makeSpikes(app, 100, topStartY, bottomStartY, indexOffset)
            app.speed += (app.width // 200)

        # changing app.message / best score once player dies
        if app.gameOver:
            if app.timer / 1000 > app.bestScore: # new high score
                app.bestScore = app.timer / 1000
                if app.currentMap != "random map":
                    app.savedMaps[app.currentMap][0] = app.bestScore
            if app.lastKeyPressed == "s": # map already saved
                pass
            else:
                if app.bestScore == app.timer / 1000:
                    app.message = "  NEW HIGH SCORE!!!"
                else:
                    app.message = "         Game Over!"
                app.message += f"\n You lasted {app.timer / 1000} seconds\n   Press (s) to save the\n         current map\n     Press (r) to restart\n      with a new map\nOr press (h) to return to\n      the home screen"
        elif app.paused:
            app.message = "PAUSED"
        else:
            app.message = ""

def drawSpikes(app, canvas):
    for spike in app.spikes:
        spike.draw(canvas)

def drawCircle(app, canvas): # the circle around the player
    radius = app.player.r * 6
    canvas.create_oval(app.player.x - radius, app.player.y - radius,
                        app.player.x + radius, app.player.y + radius,
                        fill = "white", width = 0)

def drawPlayer(app, canvas):
    app.player.draw(canvas)

def drawMessageAndTimer(app, canvas):
    canvas.create_text(5, 5, text = f"{app.timer / 1000} seconds", anchor = "nw",
                        fill = "white")
    canvas.create_text(5, 20, text = f"Best Score: {app.bestScore} seconds", anchor = "nw",
                        fill = "white")
    canvas.create_text(app.width / 2, 5, text = app.currentMap, anchor = "n",
                        fill = "white")
    
    if app.message == "":
        return False
    
    # draws the message, as well as a box behind the message
    textId = canvas.create_text(app.width  * 0.7, app.height / 2,
                        text = app.message,
                        fill = "hot pink", font = f"Arial {app.height // 30}")
    x0, y0, x1, y1 = canvas.bbox(textId)
    canvas.create_rectangle(x0 - 5, y0 - 5, x1 + 5, y1 + 5, outline = "hot pink", fill = "black", width = 3)
    canvas.create_text(app.width * 0.7, app.height / 2,
                        text = app.message,
                        fill = "white", font = f"Arial {app.height // 30}")

def drawHomeScreen(app, canvas):
    # draws the heading, as well as a box behind the heading
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    textId = canvas.create_text(app.width / 2, 20,
                            text = "BATTY CAVE HOME SCREEN(h)", fill = "white",
                            font = "Arial 24 bold", anchor = "n")
    x0, y0, x1, y1 = canvas.bbox(textId)
    canvas.create_rectangle(x0 - 5, y0 - 5, x1 + 5, y1 + 5, outline = "hot pink", fill = "black", width = 3)
    canvas.create_text(app.width / 2, 20,
                            text = "BATTY CAVE HOME SCREEN(h)", fill = "white",
                            font = "Arial 24 bold", anchor = "n")
    
    app.homeScreenBat.draw(canvas) # draw the home screen bat

    # draw the commands and buttons to go to other screens
    canvas.create_text(app.width / 2, app.height * 0.55,
                            text = "press (SPACE) to play", fill = "white",
                            font = "Arial 18", anchor = "s")
    for button in app.buttons:
        button.draw(canvas)

def drawGameScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = app.backgroundColors[app.backgroundColorIndex])
    drawCircle(app, canvas)
    drawSpikes(app, canvas)
    drawPlayer(app, canvas)
    drawMessageAndTimer(app, canvas)

def drawInstructionScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_rectangle(10, 10, app.width - 10, app.height - 10, fill = "lime green")

    yInc = app.height / (len(app.instructions) + 3)
    y = 2 * yInc
    for line in app.instructions:
        canvas.create_text(app.width / 2, y, text = line, fill = "black",
                            font = "Arial 15")
        y += yInc

def drawMapScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_rectangle(10, 10, app.width - 10, app.height - 10, fill = "skyblue")

    canvas.create_text(app.width / 2, app.height - 10, text = "to go back to the home screen, press (h)", fill = "black",
                            font = "Arial 15", anchor = "s")
    if len(app.savedMaps) == 0:
        canvas.create_text(app.width / 2, app.height / 2,
                            text = "You have no saved maps", fill = "black",
                            font = "Arial 24 bold")
        return False
    
    yInc = app.height / (len(app.savedMaps) + 3)
    y = 2 * yInc
    canvas.create_text(app.width / 2, yInc, text = "To play a map, press the corresponding number on your keyboard",
                        fill = "black", font = "Arial 14")
    canvas.create_text(app.width / 2, yInc + 20, text = "*Note: the map may be blank if you reach the end",
                        fill = "black", font = "Arial 10")
    
    index = 1
    for name in app.savedMaps:
        canvas.create_text(app.width / 2, y, text = f"{index}. {name}", fill = "black",
                            font = "Arial 14")
        index += 1
        y += yInc

def drawAboutScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_rectangle(10, 10, app.width - 10, app.height - 10, fill = "hot pink")
    
    yInc = app.height / (len(app.about) + 3)
    y = 2 * yInc
    for line in app.about:
        canvas.create_text(app.width / 2, y, text = line, fill = "black",
                            font = "Arial 15")
        y += yInc

def redrawAll(app, canvas):
    if app.screen == "homeScreen":
        drawHomeScreen(app, canvas)
    elif app.screen == "gameScreen":
        drawGameScreen(app, canvas)
    elif app.screen == "instructionScreen":
        drawInstructionScreen(app, canvas)
    elif app.screen == "mapScreen":
        drawMapScreen(app, canvas)
    elif app.screen == "aboutScreen":
        drawAboutScreen(app, canvas)
    else:
        print(app.screen, "error!")

def playBatty():
    runApp(width = 600, height = 400)

def main():
    playBatty()

if __name__ == '__main__':
    main()
