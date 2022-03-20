import ctypes
import pyglet
pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False
import pyglet.gl as gl
import math

import matrix
import shader
import block_type


class Window(pyglet.window.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create blocks
        self.cobblestone = block_type.BlockType('cobblestone', {'all': 'cobblestone'})
        self.grass = block_type.BlockType('grass', {'top': 'grass',
                                                    'bottom': 'dirt',
                                                    'sides': 'grass_side'})
        self.dirt = block_type.BlockType('dirt', {'all': 'dirt'})
        self.stone = block_type.BlockType('stone', {'all': 'stone'})
        self.sand = block_type.BlockType('sand', {'all': 'sand'})
        self.planks = block_type.BlockType('planks', {'all': 'planks'})
        self.log = block_type.BlockType('log', {'top': 'top_log',
                                                'bottom': 'log_top',
                                                'sides': 'log_sides'})

        # create VAO or vertex array object
        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        # create VBO or vertex buffer object
        self.vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLfloat * len(self.grass.vertex_positions)),
            (gl.GLfloat * len(self.grass.vertex_positions))(*self.grass.vertex_positions),
            gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        # create IBO or index bugger object
        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLuint * len(self.grass.indices)),
            (gl.GLuint * len(self.grass.indices))(*self.grass.indices),
            gl.GL_STATIC_DRAW)

        # create shader
        self.shader = shader.Shader('vert.glsl', 'frag.glsl')
        self.shader_matrix_location = self.shader.find_uniform(b'matrix')
        self.shader.use()

        # create matrices, Model View and Projection
        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()

        self.x = 0
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)

    def update(self, delta_time):
        self.x += delta_time

    def on_draw(self):
        # create projection matrix
        self.p_matrix.load_identity()
        self.p_matrix.perspective(90, self.width / self.height, 0.1, 500)

        # create modelview matrix
        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0, 0, -2)
        self.mv_matrix.rotate_2d(self.x, math.sin(self.x / 3 * 2) / 2)

        # modelviewprojection matrix
        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        self.clear()

        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.grass.indices),
            gl.GL_UNSIGNED_INT,
            None
        )

    def on_resize(self, width, height):
        print(f'Resizing window to:\t{width}\t{height}')
        gl.glViewport(0, 0, width, height)


class Game:
    def __init__(self):
        self.config = gl.Config(double_buffer=True, major_version=3, minor_version=3, depth_size=16)
        self.window = Window(config=self.config,
                             width=800,
                             height=600,
                             caption="eivlcraft Minecraft clone",
                             resizable=True,
                             vsync=False)

    def run(self):
        pyglet.app.run()


if __name__ == '__main__':
    game = Game()
    game.run()
