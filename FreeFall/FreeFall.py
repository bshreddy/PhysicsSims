import math, time
import pyglet
from pyglet.window import FPSDisplay, key

class Ball:

    def __init__(self, m=10, radius=20, position=(0, 700), gravity=-980):
        self.m = m
        self.radius = radius
        self.x, self.y = position
        self.gravity = gravity
        self.vx, self.vy = 0, 0
        self.res = 200
    
    def draw(self, offset=(0, 0)):
        x, y = self.position_after_offset(offset)
        verts = self.makeVertices(x, y)
        
        circle = pyglet.graphics.vertex_list(self.res, ('v2f', verts))
        circle.draw(pyglet.gl.GL_POLYGON)
    
    def step(self, dt):
        self.vy += self.gravity * dt
        self.y += self.vy * dt
        self.y = max(self.y, self.radius)
    
    def position_after_offset(self, offset=(0, 0)):
        offset_x, offset_y = offset
        return (self.x + offset_x, self.y + offset_y)

    def makeVertices(self, X, Y):
        verts = []

        for i in range(self.res):
            angle = math.radians(i / self.res * 360.0)
            x = self.radius * math.cos(angle) + X
            y = self.radius * math.sin(angle) + Y
            verts += [x, y]
        return verts


class Simulation(pyglet.window.Window):

    def __init__(self, width=1152, height=720, fullscreen=False):
        super().__init__(width, height, vsync=False, fullscreen=fullscreen, caption="Simple Pendulum")
        self.fps = FPSDisplay(self)
        self.T = 0
        self.ball = Ball()
        self.run = False
        self.trace = []

        pyglet.gl.glPointSize(10)
    
    @property
    def center(self):
        return self.width // 2, self.height // 2

    def update(self, dt):
        if not self.run:
            return

        self.ball.step(dt)

        self.T += dt
    
    def on_draw(self):
        self.clear()

        offset = (self.width // 2, 0)
        if self.run and (int(self.T * 100) % 10 == 0):
            self.trace.extend(self.ball.position_after_offset(offset))

        pyglet.graphics.draw(len(self.trace)//2, pyglet.gl.GL_POINTS,
                  ('v2f', self.trace),
                  ('c3B', [255, 0, 0]*(len(self.trace)//2)),
                  )

        self.ball.draw(offset)
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
            self.run = not self.run


if __name__ == "__main__":
    sim = Simulation()
    # pyglet.clock.set_fps_limit(500)
    pyglet.clock.schedule_interval(sim.update, 1 / 500.0)
    pyglet.app.run()
