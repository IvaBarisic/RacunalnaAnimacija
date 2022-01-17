
import sys, time, math
from pyglet.gl import *
from euclid import *
from random import *

window = pyglet.window.Window()

gravity = Vector3(0, -100, 0)

tex = pyglet.image.load('snow.bmp').get_texture()


class particle:
    def __init__(self, pos):
        self.pos = pos.copy()
        self.pos[0] += uniform(-400,400)
        self.pos[1] += uniform(-300,300)
        self.ds = Vector3(10, 100, 0)
        self.removeTime = time.time() +100
        self.size=20
    def update(self, dt):
        self.pos-= self.ds *dt
        self.size-=5*dt

class particleSystem:
    def __init__(self, num=1):
        self.particles= []
        self.addParticles(num)
    def addParticles(self, num):
        for i in range(0,num):
            p = particle(Vector3(300,500,0))
            self.particles.append(p)
    def draw(self):
        global S
        glColor3f(1,1,1)
        glEnable(tex.target)
        glBindTexture(tex.target, tex.id)
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE)
        glBegin(GL_QUADS)
        for p in self.particles:
            size = p.size
            glTexCoord2f(0,0)
            glVertex3f(p.pos[0]-size, p.pos[1]-size, p.pos[2])
            glTexCoord2f(1,0)
            glVertex3f(p.pos[0]+size, p.pos[1]-size, p.pos[2])
            glTexCoord2f(1,1)
            glVertex3f(p.pos[0]+size, p.pos[1]+size, p.pos[2])
            glTexCoord2f(0,1)
            glVertex3f(p.pos[0]-size, p.pos[1]+size, p.pos[2])
        glEnd()
        glDisable(GL_BLEND)
        glDisable(tex.target)
    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        t = time.time()
        for i in range(len(self.particles)-1, -1, -1):
            if (self.particles[i].removeTime <= t) or (self.particles[i].pos[1] < -100):
                del self.particles[i]
                self.addParticles(1)

systems = [particleSystem(300)]

@window.event
def on_draw():
    glClearColor(0, 0.4, 0.6, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    for s in systems:
        s.draw()


def update(dt):
    for s in systems: 
        s.update(dt)
    for i in range(len(systems)-1, -1, -1):
        if len(systems[i].particles) == 0:
            del systems[i]


pyglet.clock.schedule_interval(update,1/1000.0)
pyglet.app.run()