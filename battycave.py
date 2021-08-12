#################################################
# FINAL TPPPP!!!!
#
# Version 10:
# What I've done: changing sprite instead of a dot
# Next step: circle view dots
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
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
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
    app.player = Player(app)
    color = (181, 51, 184)
    app.mainColor = "black"
    app.backgroundColors = colorBlender(color, (0, 0, 0), 50)
    app.backgroundColorIndex = 0
    app.gameOver = False
    app.spikeWidth = app.width / 30
    app.spikeOffset = app.width * 0.7 # change spike offset instead of the individual spike x values
    app.minSpikeHeight = app.height / 20
    app.maxSpikeHeight = app.height * 0.6
    app.spikeMargin = app.height / 13
    app.spikes = makeSpikes(app, 30, 0, app.height)
    app.paused = False
    app.speed = app.width // 120 # 5
    app.timer = 0
    app.spikeTimer = 0
    app.screen = "startScreen"

class Player(object):
    def __init__(self, app):
        self.app = app
        self.x = app.width * 0.4
        self.y = app.height / 2
        self.r = app.height / 20 # 15 before
        self.yV = 0  # velocity
        self.yA = app.height / 400  # acceleration

        # adapted from 15-112 course notes: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
        self.spriteIndex = 0
        spritestrip = app.loadImage('batspritesheet.png')
        spritestrip = app.scaleImage(spritestrip, 1/12)
        self.sprites = [ ]
        imageWidth, imageHeight = spritestrip.size
        for i in range(2):
            sprite = spritestrip.crop(((imageWidth / 2)*i, 0, (imageWidth / 2)*(i+ 1), imageHeight))
            self.sprites.append(sprite)
    
    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r,
                        self.x + self.r, self.y + self.r,
                        fill = "green")
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
        else: # check if intersects below
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
            # print(self.index, self.intersectionX - player.x)
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
        # canvas.create_text(self.x, self.app.height / 2, text = f"{self.index}",
        #                 fill = "white", anchor = "s")

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
        if topOldY < app.minSpikeHeight + app.spikeMargin:
            topNewY = topOldY + random.choice(range(minInc, maxInc))
            generalDirection = 1
        elif topOldY > app.maxSpikeHeight - app.spikeMargin:
            topNewY = topOldY + random.choice(range(-1 * maxInc, -1 * minInc))
            generalDirection = -1
        else:
            topNewY = topOldY + generalDirection * random.choice(range(-1 * smallerMinInc, smallerMaxInc))

        if bottomOldY > app.height - (app.minSpikeHeight + app.spikeMargin):
            bottomNewY = bottomOldY + random.choice(range(-1 * maxInc, -1 * minInc))
            generalDirection = -1
        elif bottomOldY < app.height - (app.maxSpikeHeight - app.spikeMargin):
            bottomNewY = bottomOldY + random.choice(range(minInc, maxInc))
            generalDirection = 1
        else:
            bottomNewY = bottomOldY + generalDirection * random.choice(range(-1 * smallerMinInc, smallerMaxInc))
        
        if abs(topNewY - bottomNewY) < app.player.r * 5:
            topNewY -= app.player.r * 0.5
            bottomNewY += app.player.r * 1.5
        downSpike = Spike(app, i + indexOffset, topOldY, topNewY, True)
        upSpike = Spike(app, i + indexOffset, bottomOldY, bottomNewY, False)
        spikes.append(downSpike)
        spikes.append(upSpike)
        oldYs = topNewY, bottomNewY
    return spikes

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
        app.screen = "gameScreen"
    elif event.key == "Space":
        app.screen = "gameScreen"
        app.player.yV = -1 * app.height // 70 # 6
    elif event.key == 'p':
        app.paused = not app.paused
    elif event.key == "x":
        for spike in app.spikes:
            if spike.pointingDown:
                print(spike.index, spike.slope, spike.cosalpha)
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
        
        for spike in app.spikes:
            spike.touching(app.player)
    pass

def mousePressed(app, event):
    pass

def timerFired(app):
    if not app.gameOver and not app.paused and app.screen == "gameScreen":
        app.timer += app.timerDelay
        app.spikeTimer += app.timerDelay
        app.player.y += app.player.yV
        app.player.yV += app.player.yA
        if app.player.yV > -1: # going down
            app.player.spriteIndex = 0
        else: # going up
            app.player.spriteIndex = 1

        if app.backgroundColorIndex < len(app.backgroundColors) - 1:
            app.backgroundColorIndex += 1

        app.spikeOffset -= app.speed
        for spike in app.spikes:
            if spike.touching(app.player):
                break
            spike.updateX()
    if app.player.y > app.height or app.player.y < 0:
        app.gameOver = True

    x = (app.spikeWidth / app.speed) * app.timerDelay # amount of time it takes for 1 spike to pass
    if app.spikeTimer > (15 * x):
        app.spikeTimer -= (30 * x)
        size = len(app.spikes)
        lastTopSpike = app.spikes[size - 2]
        lastBottomSpike = app.spikes[size - 1]

        topStartY = lastTopSpike.rightY
        bottomStartY = lastBottomSpike.rightY
        indexOffset = size //  2
        app.spikes += makeSpikes(app, 30, topStartY, bottomStartY, indexOffset)
        app.speed += 1

def drawSpikes(app, canvas):
    for spike in app.spikes:
        spike.draw(canvas)

def drawCircle(app, canvas):
    radius = app.player.r * 7
    canvas.create_oval(app.player.x - radius, app.player.y - radius,
                        app.player.x + radius, app.player.y + radius,
                        fill = "white", width = 0)

def drawPlayer(app, canvas):
    app.player.draw(canvas)

def drawStartScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "blue")
    canvas.create_text(app.width / 2, app.height / 2,
                            text = "Press 'SPACE' to start", fill = "white",
                            font = "Arial 24")

def drawGameScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = app.backgroundColors[app.backgroundColorIndex])
    drawCircle(app, canvas)
    drawSpikes(app, canvas)
    drawPlayer(app, canvas)
    if app.gameOver:
        canvas.create_text(app.width / 2, app.height / 2,
                            text = "GAME OVER", fill = "white")
    elif app.paused:
        canvas.create_text(app.width / 2, app.height / 2,
                            text = "PAUSED", fill = "white")
    canvas.create_text(5, 5, text = f"{app.timer / 1000}", anchor = "nw",
                        fill = "white")

def redrawAll(app, canvas):
    if app.screen == "startScreen":
        drawStartScreen(app, canvas)
    elif app.screen == "gameScreen":
        drawGameScreen(app, canvas)
    else:
        print(app.screen, "error!")

def playBatty():
    runApp(width = 600, height = 400)

def main():
    playBatty()

if __name__ == '__main__':
    main()
