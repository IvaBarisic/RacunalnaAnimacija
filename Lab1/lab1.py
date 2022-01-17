import math
from math import cos
from time import sleep

from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import numpy as np


window = pyglet.window.Window(resizable=True)
#batch = pyglet.graphics.Batch()

V=[]
F=[]

P=[]
Pd=[]
os=[]
kut=[]
s=[0,1,0]

B=np.array([[-1,3,-3,1],[3,-6,3,0],[-3,0,3,0],[1,4,1,0]])
Bt=np.array([[-1,3,-3,1],[2,-4,2,0],[-1,0,1,0]])
spirala=[[0,0,0], [0,10,5],[10,10,10],[10,0,15],[0,0,20],[0,10,25],[10,10,30],[10,0,35],[0,0,40],[0,10,45],[10,10,50],[10,0,55]]



def krivulja(tocke):
    global P,Pd,os,kut,s,Bt,B
    
    for i in range(0,len(tocke)-3):
        
        t=0
        step=0.1
        
        R=[tocke[i],tocke[i+1],tocke[i+2],tocke[i+3]]
        while t<=1:
            p=(1/6*np.dot(np.dot([t*t*t,t*t,t,1],B),R))     # odrediti potrebnu translaciju objekta
            P.append(p)
            e=1/2*np.dot(np.dot([t*t,t,1],Bt),R)      # odrediti ciljnu orijentaciju objekta
            Pd.append(e)
            os.append([s[1]*e[2]-e[1]*s[2],-(s[0]*e[2]-e[0]*s[2]),s[0]*e[1]-e[1]*s[0]])   # odrediti os i kut rotacije
            sn=math.sqrt(s[0]**2+s[1]**2+s[2]**2)
            en=math.sqrt(e[0]**2+e[1]**2+e[2]**2)
            cos=np.matmul(s,e)/(sn*en)
            kut.append(math.acos(cos)*180)
            t+=step
            s=p+e
    #print("spirala")



def ucitajVrhove():
    global V,F,spirala,P,Pd,os,kut
    path='./avion.obj'
    f=open(path,'r')
    text=f.read().split("\n")
    for t in text:
        #print(t)
        if t!='':
            if t[0]=='#':
                continue
            elif t[0]=='v':
                V.append(t.split()[1::])
            elif t[0]=='f':
                F.append(t.split()[1::])

    Vx=[float(V[i][0]) for i in range(0,len(V))]
    Vy=[float(V[i][1]) for i in range(0,len(V))]
    Vz=[float(V[i][2]) for i in range(0,len(V))]

    xmin=min(Vx)
    xmax=max(Vx)
    ymin=min(Vy)
    ymax=max(Vy)
    zmin=min(Vz)
    zmax=max(Vz)

    S=[(xmax+xmin)/2,(ymax+ymin)/2,(zmax+zmin)/2]

    M=max(xmax-xmin,ymax-ymin,zmax-zmin)
    #print(M)

    for i in range(0,len(V)):
        V[i][0] = (float(V[i][0]) - S[0])*10/M
        V[i][1] = (float(V[i][1]) - S[1])*10/M
        V[i][2] = (float(V[i][2]) - S[2])*10/M


    krivulja(spirala)
    crtaj()

def crtajTrokut(v1,v2,v3):
    
    glBegin(GL_LINE_LOOP)
    glColor3f(0.0,5.0,5.0)
    glVertex3f(v1[0],v1[1],v1[2]) #np.clip(v1[2],-1,1))
    glVertex3f(v2[0],v2[1],v2[2]) #np.clip(v2[2],-1,1))
    glVertex3f(v3[0],v3[1], v3[2])#np.clip(v3[2],-1,1))
    glEnd()
 
def crtaj():
    global P,Pd,kut,spirala,os,k,F,V

    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glTranslatef(0.0,0.0,-100.0)
    glRotatef(50,1,15,10)
    glColor3f(0.5,0,0)

    glBegin(GL_LINE_STRIP)
    for i in P:
        glVertex3f(i[0],i[1],i[2])#np.clip(i[2],-1,1))

    glEnd()

    glColor3f(0.5,0,0.5)

    glBegin(GL_LINES)
    for p in range(0,len(P)):
        i=P[p]
        j=Pd[p]
        glVertex3f(i[0],i[1],i[2])
        glVertex3f((i[0]+j[0]),(i[1]+j[1]),(i[2]+j[2])) #np.clip((i[2]+j[2])*2,-1,1))
    glEnd()
    

    s=P[k]+Pd[k]
    glTranslatef(P[k][0],P[k][1],P[k][2])
    #print(kut[k],Pd[k][0],Pd[k][1],Pd[k][2])
    glRotatef(kut[k],Pd[k][0],Pd[k][1],Pd[k][2])
    #glTranslatef(-s[0],-s[1],-s[2])
    


    for i in range(0,len(F)):
        v1=V[int(F[i][0])-1]
        v2=V[int(F[i][1])-1]
        v3=V[int(F[i][2])-1]

        crtajTrokut(v1,v2,v3)

    k+=1 
    if k==len(P)-1:
        k=0
    sleep(0.1)
       

@window.event
def on_draw():

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
   # glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45.0,600/400,0.1,100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(1.0,0.0,1.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glEnd()

def update(x,y):
    global k
    crtaj()

k=0
ucitajVrhove()
pyglet.clock.schedule(update, 1/1000000.0)
pyglet.app.run()

