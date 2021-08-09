#################################################
# FINAL TPPPP!!!!
#
# Version 1:
# What I've done: sidescroll, bat & spike class, jumping, pause
# Next step: checking for when the player touches the spikes
#               ^ or do a different type of terrain thats smoother?
# 
# Your name: Audi Lin
# Your andrew id: audil
#################################################

import math, copy, random, time

from cmu_112_graphics import *

#################################################

def appStarted(app):
    app.player = Bat(app)
    app.gameOver = False
    app.spikeWidth = app.width / 10
    app.spikes = makeSpikes(app, 30)
    app.paused = False

class Bat(object):
    def __init__(self, app):
        self.app = app
        self.x = app.width * 0.4
        self.y = app.height / 2
        self.r = 20
        self.jumpHeight = app.height / 40
        self.jumping = False
        self.jumpingTimer = 0
    
    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r,
                        self.x + self.r, self.y + self.r,
                        fill = "white")
        
class Spike(object):
    def __init__(self, app, x, height, pointingDown):
        self.app = app
        self.width = self.app.spikeWidth
        self.x = x
        self.height = height
        self.pointingDown = pointingDown # bool

    def move(self, dx):  # idk if this is really necessary but oh well
        self.x += dx

    def draw(self, canvas):
        halfWidth = self.width / 2
        if self.pointingDown:
            canvas.create_polygon(self.x - halfWidth, 0,
                            self.x + halfWidth, 0,
                            self.x, self.height,
                            fill = "red")
        else:
            canvas.create_polygon(self.x - halfWidth, self.app.height,
                            self.x + halfWidth, self.app.height,
                            self.x, self.app.height - self.height,
                            fill = "red")
    
def makeSpikes(app, n):
    spikes = []
    for i in range(n):
        x = i * app.spikeWidth + app.width * 0.75
        height = random.choice(range(70, 180, 5))
        downSpike = Spike(app, x, height, True)
        spikes.append(downSpike)
        height = random.choice(range(70, 180, 5))
        upSpike = Spike(app, x, height, False)
        spikes.append(upSpike)
    return spikes

def keyPressed(app, event):
    if event.key == "Space":
        app.player.jumping = True
        app.player.jumpingTimer = 0
    elif event.key == 'p':
        app.paused = not app.paused
    pass

def mousePressed(app, event):
    pass

def timerFired(app):
    if not app.gameOver and not app.paused:
        if app.player.jumping and app.player.jumpingTimer < 3:
            app.player.y -= app.player.jumpHeight
            app.player.jumpingTimer += 1
        else:
            app.player.jumpingTimer = 0
            app.player.jumping = False
            app.player.y += 0.5 * app.player.jumpHeight
        
        for spike in app.spikes:
            spike.move(-5)

def drawSpikes(app, canvas):
    for spike in app.spikes:
        spike.draw(canvas)

def drawCircle(app, canvas):
    pass

def drawPlayer(app, canvas):
    app.player.draw(canvas)

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "purple")
    drawCircle(app, canvas)
    drawSpikes(app, canvas)
    drawPlayer(app, canvas)
    if app.paused:
        canvas.create_text(app.width / 2, app.height / 2,
                            text = "PAUSED", fill = "white")

def playBatty():
    runApp(width = 600, height = 400)

def main():
    playBatty()

if __name__ == '__main__':
    main()
