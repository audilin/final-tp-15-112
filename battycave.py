#################################################
# FINAL TPPPP!!!!
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
    app.timer = 0

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
        

def keyPressed(app, event):
    if event.key == "Space":
        app.player.jumping = True
        app.player.jumpingTimer = 0
    pass

def mousePressed(app, event):
    pass

def timerFired(app):
    app.timer += app.timerDelay
    if not app.gameOver:
        if app.player.jumping and app.player.jumpingTimer < 3:
            app.player.y -= app.player.jumpHeight
            app.player.jumpingTimer += 1
        else:
            app.player.jumpingTimer = 0
            app.player.jumping = False
            app.player.y += 0.5 * app.player.jumpHeight

def drawSpikes(app, canvas):
    pass

def drawCircle(app, canvas):
    pass

def drawPlayer(app, canvas):
    app.player.draw(canvas)

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    drawCircle(app, canvas)
    drawSpikes(app, canvas)
    drawPlayer(app, canvas)
    pass

def playBatty():
    runApp(width = 600, height = 400)

def main():
    playBatty()

if __name__ == '__main__':
    main()
