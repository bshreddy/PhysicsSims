import math, time
import pyglet
from pyglet.window import FPSDisplay, key


class Pendulum:

    def __init__(self, position=(0, 0), length=1, radius=20, theta = math.pi/8, angular_velocity=0):
        self.x, self.y = position
        self.length = length
        self.radius = radius
        self.theta = theta
        self.res = 200
        self.angular_velocity = angular_velocity

    def draw(self, offset=(0, 0)):
        offset_x, offset_y = offset

        x1, y1 = self.x + offset_x, self.y + offset_y
        x2, y2 = self.x + math.sin(self.theta) * self.length * 4 + offset_x, self.y - math.cos(
            self.theta) * self.length * 4 + offset_y
        self.makeVertices(x2, y2)

        pyglet.gl.glLineWidth(4)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                             ('v2f', (x1, y1, x2, y2)),
                             )
        circle = pyglet.graphics.vertex_list(self.res, ('v2f', self.verts))
        circle.draw(pyglet.gl.GL_POLYGON)

    def step(self, dt):
        angular_accleration = (-980*.35 / self.length) * math.sin(self.theta)
        self.angular_velocity += angular_accleration * dt
        self.theta += self.angular_velocity * dt

    def makeVertices(self, X, Y):
        self.verts = []

        for i in range(self.res):
            angle = math.radians(i / self.res * 360.0)
            x = self.radius * math.cos(angle) + X
            y = self.radius * math.sin(angle) + Y
            self.verts += [x, y]


class Simulation(pyglet.window.Window):

    def __init__(self, width=1152, height=720, fullscreen=False):
        super().__init__(width, height, vsync=False, fullscreen=fullscreen, caption="Simple Pendulum")
        self.fps = FPSDisplay(self)
        self.T = 0
        self.pendulums = [Pendulum(length=100)]
        # self.pendulums = [Pendulum(length=x, theta=math.pi/16) for x in range(25, 200, 25)]

    @property
    def center(self):
        return self.width // 2, self.height // 2

    def update(self, dt):
        for pendulum in self.pendulums:
            pendulum.step(dt)

        self.T += dt

    def on_draw(self):
        self.clear()

        for pendulum in self.pendulums:
            pendulum.draw((self.width // 2, self.height))

        label = pyglet.text.Label(f"T = {self.T:.3f}",
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
            pyglet.clock.schedule_interval(self.update, 1 / 500.0)


if __name__ == "__main__":
    sim = Simulation()
    # pyglet.clock.set_fps_limit(500)
    pyglet.app.run()
