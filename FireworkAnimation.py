"""
Created on Thu May 08 12:07:14 2020
CSE 30 Spring 2020 Program 3 starter code
@author: Fahim

Name: John Mai
Assignment: Programming Assignment 3
Date: 5/19/2020
Due Date: Monday 5/25/2020
"""

'''
Notes from lecture:
(initial velocity) V0x = V0cosTheta // V0y = V0sinTheta
(gravity) Vgx = 0 // Vgy = gt -- g = 9.8m/s^2 // t = time ie velocity increases w time
(net velocity) 
(displacement after time b) 

1. modify the update function so it incorporates physics, so rather the particles shoot to infinity they shoot 
and drop down (render method) 
2. Given in 2d, need to change it to 3d by adding the 3rd dimension in. 
'''

#step 1: fireworks class
#step 2: gravitational effect and lifetime for each particle
#step 3: comet trails
#step 4: secondary explosion (recursion)

import random
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
pygame.init()

#firework sounds
firework_explode = pygame.mixer.Sound('Explosion+3.wav') #downloaded from freesoundeffects.com

class Particle:
    def __init__(self, x=0, y=0, z=0, color = (0, 0, 0, 1), firework_Lifetime = 500, recursive_Vel = (0,0,0)):
        self.x = []
        self.y = []
        self.z = []
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        self.color = color
        self.exploded = False
        self.velocity = [random.uniform(-.01, .01), random.uniform(-.01, .01), random.uniform(-.01, .01), ]

        #Recursive firework
        self.recursive_Time = 1
        self.recursive_Vel = recursive_Vel
        self.independent = False
        self.independent_Time = 1

        #lifetime
        self.firework_Lifetime = int(firework_Lifetime * random.uniform(1, 1))
        self.time = 1

    """movement of recursive firework """
    """1/2 gt ^2"""
    """(1/2) * .0000098 * self.time ** 2"""
    def update(self):
        if self.recursive_Vel[0] == 0:
            trail = len(self.y) - 1
            if self.recursive_Time > 100 and self.exploded == False:
                self.exploded = True
                firework_explode.play()
            if self.exploded:
                self.x.append(self.velocity[0] + self.x[trail])
                self.y.append(self.y[trail] + (self.velocity[1] - ((1/2) * (.0000098) * (self.time) ** 2)))
                self.z.append(self.velocity[2] + self.z[trail])
                self.time += 1
            if trail > 15:
                self.x.pop(0)
                self.y.pop(0)
                self.z.pop(0)
            else:
                self.y[0] += 0.1
                self.recursive_Time += 1

        else:
            trail = len(self.y) - 1
            if self.independent_Time > 100 and self.independent == False:
                self.independent = True
                firework_explode.play()
            if self.independent:
                self.x.append(self.recursive_Vel[0] + self.x[trail])
                self.y.append(self.y[trail] + (self.recursive_Vel[1] - ((1/2) * (0.0000098) * (self.time) ** 2)))
                self.z.append(self.recursive_Vel[2] + self.z[trail])
                self.recursive_Time += 1
                if trail > 45:
                    self.x.pop(0)
                    self.y.pop(0)
                    self.z.pop(0)

            if self.recursive_Time > 300 and self.exploded == False:
                self.exploded = True
                pop.play()
            if self.exploded:
                self.x.append(self.velocity[0] + self.x[trail])
                self.y.append(self.y[trail] + (self.velocity[1] - ((1/2) * (.0000098) * (self.time) ** 2)))
                self.z.append(self.velocity[2] + self.z[trail])
                self.time += 1
                if trail > 45:
                    self.x.pop(0)
                    self.y.pop(0)
                    self.z.pop(0)

            else:
                self.y[0] += 0.1
                self.independent_Time += 1


class Firework(Particle):
    def __init__(self, x=0, y=0, z=0, particles=250, color=(random.random(), random.random(), random.random(), 1),
                 firework_Lifetime=500, check_Explosion = False, recursive_Vel = (0, 0, 0)):

        self.particles = particles
        self.color = color
        self.x = x
        self.y = y
        self.z = z
        self.explosion = []
        self.check_Explosion = check_Explosion
        self.recursive_Vel = recursive_Vel
        self.firework_Lifetime = firework_Lifetime

        if self.check_Explosion == False:
            for i in range(self.particles):
                if self.color == random:
                    self.explosion.append(Particle(self.x, self.y, self.z, (random.random(), random.random(),
                                                          random.random(), 1), 500, self.recursive_Vel))

                else:
                    self.explosion.append(Particle(self.x, self.y, self.z, self.color, 500, self.recursive_Vel))

        else:
            for i in range(self.particles):
                if self.color == random:
                    self.explosion.append(Firework(self.x, self.y, self.z, self.particles,
                                              random, self.firework_Lifetime,
                                              False,(random.uniform(-.01, .01),
                                                     random.uniform(-.01, .01), random.uniform(-.01, .01))))

            else:
                self.explosion.append(Firework(self.x, self.y, self.z, self.particles,
                                          self.color, self.firework_Lifetime, False,
                                          (random.uniform(-.01, .01), random.uniform(-.01, .01),
                                           random.uniform(-.01, .01))))


    #recursive firework
    def render(self):
        if self.check_Explosion == False:
            glEnable(GL_POINT_SMOOTH)
            glPointSize(3)
            glBegin(GL_POINTS)
            for p in range(len(self.explosion)):
                trail = len(self.explosion[p].x)
                for i in range(trail):
                    if trail == 1:
                        alpha = 1
                    else:
                        alpha = i / trail
                    if self.explosion[p].y[i] >= 0 and self.explosion[p].firework_Lifetime >= self.explosion[p].time:
                        glColor4fv((self.explosion[p].color[0], self.explosion[p].color[1], self.explosion[p].color[2],
                                    alpha))
                        glVertex3fv((self.explosion[p].x[i], self.explosion[p].y[i], self.explosion[p].z[i]))
                self.explosion[p].update()
            glEnd()

        else:
            for i in self.explosion:
                i.render()




def terrain():
    ''' Draws a simple square as the terrain '''
    glBegin(GL_QUADS)
    glColor4fv((0, 0, 1, 1))  # Colors are now: RGBA, A = alpha for opacity
    glVertex3fv((10, 0, 10))  # These are the xyz coords of 4 corners of flat terrain.
    glVertex3fv((-10, 0, 10))  # If you want to be fancy, you can replace this method
    glVertex3fv((-10, 0, -10))  # to draw the terrain from your prog1 instead.
    glVertex3fv((10, 0, -10))
    glEnd()

def main():
    pygame.init()

    # Set up the screen
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Firework Simulation")
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, -5, -25)

    play = True
    sim_time = 0

    # A clock object for keeping track of fps
    clock = pygame.time.Clock()


    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(-10, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(10, 0, 1, 0)

                if event.key == pygame.K_UP:
                    glRotatef(-10, 1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(10, 1, 0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)

                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

        glRotatef(0.10, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        terrain()
        if 0 < sim_time:
            pList1.render()

        if 500 < sim_time:
            pList2.render()
            pList3.render()

        if 1000 < sim_time:
            pList4.render()
            pList5.render()

        if sim_time == 0:
            #rainbow
            pList1 = Firework(0, 0, 0, 250, random, 500)

            #red
            pList2 = Firework(5, 0, 5, 150, (1, 0, 0, 1), 500)

            #blue
            pList3 = Firework(-5, 0, -5, 150, (0, 0, 1, 1), 500)

            #recursive rainbow
            pList4 = Firework(5, 0, 0, 5, random, 500, True)

            #recursive green
            pList5 = Firework(0, 0, 5, 5, (0, 1, 0, 1), 500, True)

        pygame.display.flip()
        sim_time += 1
        clock.tick(150)

    pygame.quit()
if __name__ == "__main__":
    main()
