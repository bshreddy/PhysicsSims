import pyglet
from pyglet.window import key, FPSDisplay

class SurfaceRender(pyglet.window.Window):

    def __init__(self, width=1152, height=720):
        super(SurfaceRender, self).__init__(width, height, vsync=False, caption="Surface Render")
    
    def on_draw(self):
        self.clear()
        pyglet.graphics.draw(8, pyglet.graphics.GL_QUADS, 
                                ('v2i', (0, 0, 
                                        0, 100, 
                                        100, 100, 
                                        100, 0,

                                        100, 0,
                                        100, 100,
                                        200, 100,
                                        200, 0)),
                                ('c3B', (255, 0, 0, 
                                        0, 255, 0, 
                                        0, 0, 255, 
                                        255, 255, 255, 

                                        255, 255, 255,
                                        0, 0, 255, 
                                        0, 255, 0, 
                                        255, 0, 0, )),
                            )
        pyglet.graphics.draw(8, pyglet.graphics.GL_LINES, 
                                ('v2i', (0, 0, 
                                        0, 100, 
                                        100, 100, 
                                        100, 0,

                                        100, 0,
                                        100, 100,
                                        200, 100,
                                        200, 0)),
                                ('c3B', (255, 255, 255, 
                                        255, 255, 255, 
                                        255, 255, 255, 
                                        255, 255, 255, 

                                        255, 255, 255,
                                        255, 255, 255, 
                                        255, 255, 255, 
                                        255, 255, 255,)),
                            )
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q and modifiers == key.MOD_COMMAND:
            pyglet.app.exit()
    
sr = SurfaceRender()
pyglet.app.run()