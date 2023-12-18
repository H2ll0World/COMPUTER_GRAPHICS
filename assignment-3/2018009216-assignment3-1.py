import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gTransform = np.identity(3)

def drawTriangleTransformedBy(M):
    glBegin(GL_TRIANGLES)
    glVertex3fv((M @ np.array([.0, .5,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.0, .0,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.5, .0,0.,1.]))[:-1])

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex3fv(np.array([.0,.5,0.]))
    glVertex3fv(np.array([.0,.0,0.]))
    glVertex3fv(np.array([.5,.0,0.]))
    glEnd()

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    #draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))

    glColor3ub(0,255,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    #draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255,255,255)
    glVertex2fv((T @ np.array([.0,.5,1.]))[:-1])
    glVertex2fv((T @ np.array([.0,.0,1.]))[:-1])
    glVertex2fv((T @ np.array([.5,.0,1.]))[:-1])
    glEnd()

def key_callback(window,key,scancode,action,mods):
    global gCamAng
    global gTransform
    # rotate the camera when 1 or 3 key is pressed or repeated
    # global coordinate : coordinate system attached to the world, fixed coordinate system
    # local  coordinate : attached to a moving object
    if action==glfw.PRESS or action==glfw.REPEAT:
        '''
        if key==glfw.KEY_1:
            gCamAng +=np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng +=np.radians(10)
        '''
        #local coordinate와 global coordinate가 무슨 차이?
        if key==glfw.KEY_Q: #translate by -0.1 in x direction w.r.t global coordinate
            #print("key==glfw.KEY_Q")
            #gTransform = np.identity(3)
            gTransform[0][2] += -0.1
            
        elif key==glfw.KEY_E: #translate by 0.1 in x direction w.r.t global coordinate
            #print("key==glfw.KEY_E")
            gTransform[0][2] +=  0.1

        #right-multiplication하면 local coordinate에 관한것
        elif key==glfw.KEY_A: #rotate by 10 degrees counterclockwise w.r.t local coordinate
            #print("key==glfw.KEY_A")
            #temp_arr = [gTransform[0][2], gTransform[1][2]]
            th = np.radians(10)
            gTransform = np.dot(gTransform, np.array([[np.cos(th), -np.sin(th), 0],
                                                      [np.sin(th), np.cos(th), 0],
                                                      [0,0,                    1]]))

        elif key==glfw.KEY_D: #rotate by 10 degrees clockwise w.r.t local coordinate
            #print("key==glfw.KEY_D")
            th = np.radians(-10)
            gTransform = np.dot(gTransform, np.array([[np.cos(th), -np.sin(th), 0],
                                                      [np.sin(th), np.cos(th), 0],
                                                      [0,0,                    1]]))

        elif key==glfw.KEY_1: #reset the triangle with identity matrix
            #print("key==glfw.KEY_1")
            gTransform = np.identity(3)

        elif key==glfw.KEY_W: #Scale by 0.9 times in x direction w.r.t global coordinate
            #print("key==glfw.KEY_W")
            gTransform = np.dot(np.array([[0.9, 0, 0],
                                          [0,   1, 0],
                                          [0   ,0, 1]]), gTransform)
            

        elif key==glfw.KEY_S: #rotate 10 by degress counterclockwise w.r.t global coordinate
            #print("key==glfw.KEY_S")
            th = np.radians(10)
            gTransform = np.dot(np.array([[np.cos(th), -np.sin(th), 0],
                                    [np.sin(th), np.cos(th), 0],
                                    [0,         0,           1]]), gTransform)


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, "2018009216-assignment3-1", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gTransform)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
