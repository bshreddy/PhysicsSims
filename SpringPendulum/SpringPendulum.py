import pyglet
from pyglet.window import key, FPSDisplay
from pyglet.graphics import Group
from math import pi, sin, cos, radians


class SpringPendulum:

    def __init__(self, m=1, position=(0, 0), g=980, l=100, r=20, k=1000, theta=pi/4):
        self.m = m
        self.x, self.y = position
        self.g = g
        self.l = l
        self.r = r
        self.k = k
        self.theta = theta

        self.dl = 0
        self.v, self.omega = 0, 0

        self.res = 200
        self.scale = 5
        self.trace = []

    def step(self, dt):
        a = round((self.k * self.dl - self.m * self.g * cos(self.theta)) / self.m, 3)
        self.v += a * dt

        alpha = (-self.g * sin(self.theta)) / (self.l + self.dl)
        self.omega += alpha * dt

        self.dl += 0 if self.l + self.dl <= 0.75 * self.l and self.v >= 0 else -self.v * dt
        self.theta += self.omega * dt

    def draw(self, offset=(0, 0)):
        offset_x, offset_y = offset

        x1, y1 = self.x + offset_x, self.y + offset_y
        x2, y2 = x1 + sin(self.theta) * (self.l + self.dl) * self.scale, \
                 y1 - cos(self.theta) * (self.l + self.dl) * self.scale
        self.trace.extend([x2, y2])
        self.trace = self.trace[-2500:]

        verts = self.makeVertices(x2, y2, self.r)

        trace_group = Group()
        arm_group = Group(trace_group)
        circle_group = Group(trace_group)

        pyglet.gl.glLineWidth(4)
        batch = pyglet.graphics.Batch()
        batch.add(2, pyglet.gl.GL_LINE_STRIP, arm_group,
                  ('v2f', (x1, y1, x2, y2)),
                  )
        batch.add(self.res, pyglet.gl.GL_POLYGON, circle_group, ('v2f', verts))
        batch.add(len(self.trace) // 2, pyglet.gl.GL_LINE_STRIP, trace_group,
                  ('v2f', self.trace),
                  ('c3B', [255, 0, 0] * (len(self.trace) // 2)),
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
        super().__init__(width, height, vsync=False, caption="Spring Pendulum")
        self.refresh_rate = 500.0
        self.fps = FPSDisplay(self)
        self.spring_pendulum = SpringPendulum(m=5)
        self.T = 0

        self.is_playing = False

    def update(self, dt):
        self.spring_pendulum.step(dt)
        self.T += dt

    def on_draw(self):
        self.clear()
        self.spring_pendulum.draw((self.width // 2, self.height - 50))
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
            else:
                pyglet.clock.schedule_interval(self.update, 1 / self.refresh_rate)

            self.is_playing = not self.is_playing


if __name__ == "__main__":
    sim = Simulation()
    pyglet.app.run()
