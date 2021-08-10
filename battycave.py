#################################################
# FINAL TPPPP!!!!
#
# Version 6:
# What I've done: continuous terrain generation and gradual speed change
# Next step: smoother terrain(if possible), circle view dots
# 
# Your name: Audi Lin
# Your andrew id: audil
#################################################

import math, copy, random, time

# from the cmu 15-112 class notes
from cmu_112_graphics import *

#################################################

def appStarted(app):
    app.player = Bat(app)
    app.gameOver = False
    app.spikeWidth = 20
    app.spikeOffset = app.width * 0.7 # change spike offset instead of the individual spike x values
    app.minSpikeHeight = 20
    app.maxSpikeHeight = app.height * 0.6
    app.spikeMargin = 30
    app.spikes = makeSpikes(app, 20, 0, app.height)
    app.paused = False
    app.speed = 5
    app.timer = 0
    app.spikeTimer = 0

class Bat(object):
    def __init__(self, app):
        self.app = app
        self.x = app.width * 0.4
        self.y = app.height / 2
        self.r = 15
        self.yV = 0  # velocity
        self.yA = 1  # acceleration
    
    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r,
                        self.x + self.r, self.y + self.r,
                        fill = "black")
        
class Spike(object):
    def __init__(self, app, index, leftY, rightY, pointingDown):
        self.app = app
        self.width = self.app.spikeWidth
        self.index = index
        self.x = index * self.width + self.app.spikeOffset # dependent on index and offset
        self.color = "purple"
        self.leftY = leftY # left y-value
        self.rightY = rightY # right y-value
        self.slope = (self.rightY - self.leftY) / self.width
        self.alpha = math.atan(self.width / (self.rightY - self.leftY + 0.0001))
        self.intersectionX = 0
        self.pointingDown = pointingDown # bool

    def updateX(self):
        self.x = self.index * self.width + self.app.spikeOffset

    def touching(self, player): # checks if the spike is touching the player
        halfWidth = self.width / 2
        # if ((player.x + player.r > self.x - halfWidth) and
        #     (player.x - player.r < self.x + halfWidth)):
            # check if touching

        heightDifference = self.leftY - self.rightY
        length = ((self.width)**2 + (heightDifference)**2) ** 0.5 # for the terrain
        yOffset = length * (player.r / self.width) # using triangle similarity
        # point-slope formula : y - y1 = m * (x - x1)
        # y1 = leftHeight +/- yOffset, x1 = middleX - halfWidth

        if self.pointingDown: # check if intersects top "spikes"
            leftside = player.y - (self.leftY + yOffset)
            rightside = self.slope * (player.x - (self.x - halfWidth))
            if leftside <= rightside:
                if self.slope >= 0:
                    self.intersectionX = player.x + player.r * math.cos(self.alpha)
                else:
                    self.intersectionX = player.x - player.r * math.cos(self.alpha)
                if self.x - halfWidth <= self.intersectionX <= self.x + halfWidth:
                    self.color = "white"
                    self.app.gameOver = True
            else:
                self.intersectionX = 0
                self.color = "purple"

        else: # check if intersects below
            leftside = player.y - (self.leftY - yOffset)
            rightside = self.slope * (player.x - (self.x - halfWidth))
            if leftside >= rightside:
                if self.slope >= 0:
                    self.intersectionX = player.x - player.r * math.cos(self.alpha)
                else:
                    self.intersectionX = player.x + player.r * math.cos(self.alpha)
                if self.x - halfWidth <= self.intersectionX <= self.x + halfWidth:
                    self.color = "white"
                    self.app.gameOver = True
            else:
                self.intersectionX = 0
                self.color = "purple"
        return False

    def draw(self, canvas):
        halfWidth = self.width / 2
        if self.pointingDown:
            canvas.create_polygon(self.x - halfWidth, 0,
                            self.x + halfWidth, 0,
                            self.x + halfWidth, self.rightY,
                            self.x - halfWidth, self.leftY,
                            fill = self.color)
        else:
            canvas.create_polygon(self.x - halfWidth, self.app.height,
                            self.x + halfWidth, self.app.height,
                            self.x + halfWidth, self.rightY,
                            self.x - halfWidth, self.leftY,
                            fill = self.color)
        canvas.create_text(self.x, self.app.height / 2, text = f"{self.index}",
                        fill = "white", anchor = "s")

def makeSpikes(app, n, topStartY, bottomStartY, indexOffset = 0): # returns a list of n up & n down Spike objects
    spikes = []
    oldYs = topStartY, bottomStartY
    generalDirection = 1
    for i in range(n):
        topOldY, bottomOldY = oldYs
        x = i * app.spikeWidth + app.width * 0.75
        if topOldY < app.minSpikeHeight + app.spikeMargin:
            topNewY = topOldY + random.choice(range(20, 50))
            generalDirection = 1
        elif topOldY > app.maxSpikeHeight - app.spikeMargin:
            topNewY = topOldY + random.choice(range(-50, -20))
            generalDirection = -1
        else:
            topNewY = topOldY + generalDirection * random.choice(range(10, 30))

        if bottomOldY > app.height - (app.minSpikeHeight + app.spikeMargin):
            bottomNewY = bottomOldY + random.choice(range(-50, -20))
            generalDirection = -1
        elif bottomOldY < app.height - (app.maxSpikeHeight - app.spikeMargin):
            bottomNewY = bottomOldY + random.choice(range(20, 50))
            generalDirection = 1
        else:
            bottomNewY = bottomOldY + generalDirection * random.choice(range(-10, 30))
        
        if abs(topNewY - bottomNewY) < app.player.r * 6:
            topNewY -= app.player.r * 2
            bottomNewY += app.player.r * 2
        downSpike = Spike(app, i + indexOffset, topOldY, topNewY, True)
        upSpike = Spike(app, i + indexOffset, bottomOldY, bottomNewY, False)
        spikes.append(downSpike)
        spikes.append(upSpike)
        oldYs = topNewY, bottomNewY
    return spikes

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
    elif event.key == "Space":
        app.player.yV = -7
    elif event.key == 'p':
        app.paused = not app.paused
    elif event.key == "x":
        print(app.timer / 1000)
    if app.paused:
        if event.key == "Up":
            app.player.y -= 5
        elif event.key == "Down":
            app.player.y += 5
        elif event.key == "Left":
            app.spikeOffset += app.speed
            for spike in app.spikes:
                spike.updateX()
        elif event.key == "Right":
            app.spikeOffset -= app.speed
            for spike in app.spikes:
                spike.updateX()
        
        for spike in app.spikes:
            if spike.touching(app.player):
                break
    pass

def mousePressed(app, event):
    pass

def timerFired(app):
    if not app.gameOver and not app.paused:
        app.timer += app.timerDelay
        app.spikeTimer += app.timerDelay
        app.player.y += app.player.yV
        app.player.yV += app.player.yA

        app.spikeOffset -= app.speed
        for spike in app.spikes:
            if spike.touching(app.player):
                break
            spike.updateX()
        if app.player.y > app.height or app.player.y < 0:
            app.gameOver = True

        x = (app.spikeWidth / app.speed) * app.timerDelay # amount of time it takes for 1 spike to pass
        if app.spikeTimer > (20 * x):
            app.spikeTimer -= (20 * x)
            size = len(app.spikes)
            lastTopSpike = app.spikes[size - 2]
            lastBottomSpike = app.spikes[size - 1]
            print(f"making {size // 2}+")

            topStartY = lastTopSpike.rightY
            bottomStartY = lastBottomSpike.rightY
            indexOffset = size //  2
            app.spikes += makeSpikes(app, 20, topStartY, bottomStartY, indexOffset)
            app.speed += 1

def drawSpikes(app, canvas):
    for spike in app.spikes:
        spike.draw(canvas)

def drawCircle(app, canvas):
    radius = app.player.r * 10
    canvas.create_oval(app.player.x - radius, app.player.y - radius,
                        app.player.x + radius, app.player.y + radius,
                        fill = "grey")

def drawPlayer(app, canvas):
    app.player.draw(canvas)

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "purple")
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

def playBatty():
    runApp(width = 600, height = 400)

def main():
    playBatty()

if __name__ == '__main__':
    main()
