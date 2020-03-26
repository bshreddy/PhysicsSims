import pyglet
from pyglet.window import key, FPSDisplay
from pyglet.graphics import Group
from math import pi, sin, cos, radians


class DoublePendulum:

    def __init__(self, m1=1, m2=1, position=(0, 0), g=980, l1=100, l2=100, r1=20, r2=20, theta1=pi/4, theta2=pi/3):
        self.m1, self.m2 = m1, m2
        self.x, self.y = position
        self.g = g
        self.l1, self.l2 = l1, l2
        self.r1, self.r2 = r1, r2
        self.theta1, self.theta2 = theta1, theta2

        self.omega1, self.omega2 = 0, 0
        
        self.res = 200
        self.scale = 2
        self.trace = []

    def step(self, dt):
        num1 = -self.g * (2 * self.m1 + self.m2) * sin(self.theta1)
        num2 = -self.m2 * self.g * sin(self.theta1 - 2 * self.theta2)
        num3 = -2 * sin(self.theta1 - self.theta2) * self.m2
        num4 = self.omega2 * self.omega2 * self.l2 + self.omega1 * self.omega1 * self.l1 * cos(self.theta1 - self.theta2)
        den = self.l1 * (2 * self.m1 + self.m2 - self.m2 * cos(2 * self.theta1 - 2 * self.theta2))
        alpha1 = (num1 + num2 + num3 * num4) / den

        num1 = 2 * sin(self.theta1 - self.theta2)
        num2 = self.omega1 ** 2 * self.l1 * (self.m1 + self.m2)
        num3 = self.g * (self.m1 + self.m2) * cos(self.theta1)
        num4 = self.omega2 ** 2 * self.l2 * self.m2 * cos(self.theta1 - self.theta2)
        den = self.l2 * (2 * self.m1 + self.m2 - self.m2 * cos(2 * self.theta1 - 2 * self.theta2))
        alpha2 = (num1 * (num2 + num3 + num4)) / den

        self.omega1 += alpha1 * dt
        self.omega2 += alpha2 * dt
        
        self.theta1 += self.omega1 * dt
        self.theta2 += self.omega2 * dt

    def draw(self, offset=(0, 0)):
        offset_x, offset_y = offset

        x1, y1 = self.x + offset_x, self.y + offset_y
        x2, y2 = x1 + sin(self.theta1) * self.l1 * self.scale, \
            y1 - cos(self.theta1) * self.l1 * self.scale
        x3, y3 = x2 + sin(self.theta2) * self.l2 * self.scale, \
            y2 - cos(self.theta2) * self.l2 * self.scale
        self.trace.extend([x3, y3])
        self.trace = self.trace[-5000:]

        verts1 = self.makeVertices(x2, y2, self.r1)
        verts2 = self.makeVertices(x3, y3, self.r2)

        trace_group = Group()
        arm_group = Group(trace_group)
        first_circle_group = Group(arm_group)
        second_circle_group = Group(arm_group)
        

        pyglet.gl.glLineWidth(4)
        batch = pyglet.graphics.Batch()
        batch.add(3, pyglet.gl.GL_LINE_STRIP, arm_group,
                  ('v2f', (x1, y1, x2, y2, x3, y3)),
                  )
        batch.add(self.res, pyglet.gl.GL_POLYGON, first_circle_group, ('v2f', verts1))
        batch.add(self.res, pyglet.gl.GL_POLYGON, second_circle_group, ('v2f', verts2))
        batch.add(len(self.trace)//2, pyglet.gl.GL_LINE_STRIP, trace_group, 
                  ('v2f', self.trace),
                  ('c3B', [255, 0, 0]*(len(self.trace)//2)),
                  )
        
        batch.draw()

    def makeVertices(self, X, Y, r):
        verts = []

        for i in range(self.res):
            angle = radians(i / self.res * 360.0)
            x = r * cos(angle) + X
            y = r * sin(angle) + Y
            verts += [x, y]
        return verts


class Simulation(pyglet.window.Window):

    def __init__(self, width=1152, height=720):
        super().__init__(width, height, vsync=False, caption="Double Pendulum")
        self.fps = FPSDisplay(self)
        self.double_pendulum = DoublePendulum(m1=5)
        self.T = 0
        self.refresh_rate = 500.0

        self.is_playing = False

    def update(self, dt):
        self.double_pendulum.step(dt)
        self.T += dt

    def on_draw(self):
        self.clear()
        self.double_pendulum.draw((self.width//2, self.height-150))
        label = pyglet.text.Label(f"T = {self.T:.6f}",
                                  font_name='Halvetica Nenu',
                                  font_size=16, x=self.width - 10, y=10,
                                  anchor_x="right", anchor_y="bottom")
        label.draw()
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q and modifiers == key.MOD_COMMAND:
            pyglet.app.exit()
    
    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE:
            if self.is_playing:
                pyglet.clock.unschedule(self.update)
            else :
                pyglet.clock.schedule_interval(self.update, 1 / self.refresh_rate)

            self.is_playing = not self.is_playing


if __name__ == "__main__":
    sim = Simulation()
    # pyglet.clock.set_fps_limit(sim.refresh_rate)
    pyglet.app.run()
