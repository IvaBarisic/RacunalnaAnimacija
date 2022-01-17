
import time, math
from pyglet.gl import *
from pyglet import shapes
from random import *

window = pyglet.window.Window()
batch = pyglet.graphics.Batch()
window.set_visible(visible=True)
tex = pyglet.image.load('corona.bmp').get_texture()

class particle:
    def __init__(self):
        self.pos = [0,0,0]
        self.pos[0]= randint(30, 600)
        self.pos[1]= randint(30, 380)
        self.ds=[0,0,0]
        self.ds[0] = randint(-50,50)
        self.ds[1] = randint(-50,50)
        self.count=0
        self.time = 0
        self.size=15
        self.color=(0, 0, 225)

    def update(self, dt):
        x=self.pos[0]
        y=self.pos[1]
        r=self.size
        if x - r <= 10 or x + r >= 630 or x+self.ds[0]*dt - r <= 10 or x+self.ds[0]*dt + r >= 630:
            self.ds[0]*= -1
        if y - r <= 10 or y + r >=400 or y+self.ds[1]*dt - r <= 10 or y+self.ds[1]*dt + r >=400:
            self.ds[1]*= -1
        self.pos[0]+=self.ds[0]*dt
        self.pos[1]+=self.ds[1]*dt

    def collision(self, other):
        x = other.pos[0] - self.pos[0]
        y = other.pos[1] - self.pos[1]
        distance = math.sqrt(x**2 + y**2)
        result = (other.size/2 + self.size/2)>=distance
        return result

def drawRectangle(x,y,w,h):
    glColor3f(1,0,0)
    glBegin(GL_LINE_STRIP)
    glVertex3f(x, y, 0)
    glVertex3f(x,h, 0)
    glVertex3f(w, h, 0)
    glVertex3f(w, y, 0)
    glVertex3f(x, y, 0)
    glEnd()

  
class particleSystem:
    def __init__(self, num=1):
        self.particles= []
        self.covidList=[]
        self.recoverList=[]
        self.addParticles(num)
    def addParticles(self, num):
        for i in range(0,num-1):
            p = particle()
            self.particles.append(p)
        covid=particle()
        covid.color=(255,0,0)
        covid.pos=self.particles[0].pos
        covid.pos[0]+=5
        covid.pos[1]+=5
        self.particles.append(covid)
        self.covidList.append(covid)
        covid.time=time.time()+10

    def draw(self):

        drawRectangle(10,10,630,400)
        document = pyglet.text.document.FormattedDocument(
                        ' Broj zaraženih:'+str(len(self.covidList)) 
                     +"\n Broj zdravih:"+str(len(self.particles)-len(self.covidList))
                     +'\n Broj ozdravljenih: '+str(len(self.recoverList)))
        document.set_style(0,len(document.text),dict(color=(0,0,0,255)))
        text = pyglet.text.layout.TextLayout(document,240,470,multiline=True)
        text.draw()

        remove=[]
        for p19 in self.covidList:
            t = time.time()
            if p19.time<=t:
                p19.color=(120,0,105)
                self.recoverList.append(p19)
                remove.append(p19)
        for x in remove:
            self.covidList.remove(x)
        #print(len(self.covidList))
        for p in self.particles:
            for p19 in self.covidList:
                #print(p19.count)
                if p19.collision(p) and p19!=p and p not in self.covidList and p not in self.recoverList and p19.count<2:
                    p19.count+=1
                    p.color=(255,0,0)
                    p.time=time.time()+10
                    if p not in self.covidList:
                        self.covidList.append(p)
        for p in self.particles:
            if p not in self.covidList:
                size = p.size
                circle1 = shapes.Circle(p.pos[0], p.pos[1],p.size, color=p.color, batch = batch)
                batch.draw()
            else:
                glColor3f(1,1,1)
                glEnable(tex.target)
                glBindTexture(tex.target, tex.id)
                glEnable(GL_COLOR_MATERIAL)
                glBlendFunc(GL_ONE, GL_ONE)
                glBegin(GL_QUADS)
                size = p.size
                glTexCoord2f(0,0)
                glVertex3f(p.pos[0]-size, p.pos[1]-size, p.pos[2])
                glTexCoord2f(0.7,0)
                glVertex3f(p.pos[0]+size, p.pos[1]-size, p.pos[2])
                glTexCoord2f(0.7,0.7)
                glVertex3f(p.pos[0]+size, p.pos[1]+size, p.pos[2])
                glTexCoord2f(0,0.7)
                glVertex3f(p.pos[0]-size, p.pos[1]+size, p.pos[2])
                glEnd()
                glDisable(GL_BLEND)
                glDisable(tex.target)      
       
    def update(self, dt):
        for p in self.particles:
            p.update(dt)
    

systems = [particleSystem(50)]
 
@window.event
def on_draw():
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    for s in systems:
        s.draw()

def update(dt):
    for s in systems: 
        s.update(dt)
        
pyglet.clock.schedule_interval(update,1/10000.0)
pyglet.app.run()