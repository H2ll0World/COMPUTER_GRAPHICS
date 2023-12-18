import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render(Key):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    #draw
    #1
    if Key == 1:
        print('1111')
        glBegin(GL_POINTS)
        for i in range(6):
            glColor3ub(255,255,255)
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()
    #2
    elif Key == 2:
        print('2222')
        glBegin(GL_LINES)
        for i in range(6):
            glColor3ub(255,255,255)
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()
    #3
    elif Key == 3:
        print('3333')
        glBegin(GL_LINE_STRIP)
        glColor3ub(255,255,255)
        for i in range(6):
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()
    #4
    elif Key == 4:
        print('4444')
        glBegin(GL_LINE_LOOP)
        glColor3ub(255,255,255)
        for i in range(6):
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glVertex2fv(np.array([1.,.0]))
        glEnd()

    #5
    elif Key == 5:
        print('555')
        glBegin(GL_TRIANGLES)
        glColor3ub(255,255,255)
        for i in range(6):
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()

    #6
    elif Key == 6:
        print('666')
        glBegin(GL_TRIANGLE_STRIP)
        glColor3ub(255,255,255)
        for i in range(6):
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()

    #7
    elif Key == 7:
        print('777')
        glBegin(GL_TRIANGLE_FAN)
        glColor3ub(255,255,255)
        for i in range(6):
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()

    #8
    elif Key == 8:
        print('888')
        glBegin(GL_QUADS)
        glColor3ub(255,255,255)
        for i in range(6):
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()
    #9
    elif Key == 9:
        print('999')
        glBegin(GL_QUAD_STRIP)
        glColor3ub(255,255,255)
        for i in range(6):
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()
    #0
    elif Key == 0:
        print('000')
        glBegin(GL_POLYGON)
        glColor3ub(255,255,255)
        for i in range(6):
            th1 = np.radians(30*(2*i))
            th2 = np.radians(30*(2*i+1))
            glVertex2fv(np.array([1.0*np.cos(th1), 1.0*np.sin(th1)]))
            glVertex2fv(np.array([1.0*np.cos(th2), 1.0*np.sin(th2)]))
        glEnd()

    



def key_callback(window, key, scancode, action, mods):
    global _KEY
    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            _KEY = 1
            print('PRESS 1')
    elif key == glfw.KEY_2:
        if action == glfw.PRESS:
            _KEY = 2
            print('PRESS 2')
    elif key == glfw.KEY_3:
        if action == glfw.PRESS:
            _KEY = 3
            print('PRESS 3')
    elif key == glfw.KEY_4:
        if action == glfw.PRESS:
            _KEY = 4
            print("KEY : ")
            print(_KEY)
            print('PRESS 4')
    elif key == glfw.KEY_5:
        if action == glfw.PRESS:
            _KEY = 5
            print('PRESS 5')
    elif key == glfw.KEY_6:
        if action == glfw.PRESS:
            _KEY = 6
            print('PRESS 6')
    elif key == glfw.KEY_7:
        if action == glfw.PRESS:
            _KEY = 7
            print('PRESS 7')
    elif key == glfw.KEY_8:
        if action == glfw.PRESS:
            _KEY = 8
            print('PRESS 8')
    elif key == glfw.KEY_9:
        if action == glfw.PRESS:
            _KEY = 9
            print('PRESS 9')
    elif key == glfw.KEY_0:
        if action == glfw.PRESS:
            _KEY = 0
            print('PRESS 0')



def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, "2018009216-2-2", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    global _KEY
    _KEY = 3
    while not glfw.window_should_close(window):
        glfw.poll_events()
        print("-------------")
        print("KEY :")
        print(_KEY)
        render(_KEY)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()