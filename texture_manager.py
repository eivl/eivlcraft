import ctypes
import pyglet
import pyglet.gl as gl


class TextureManager:
    def __init__(self, texture_width, texture_height, max_textures):
        self.texture_width = texture_width
        self.texture_height = texture_height
        self.max_texture = max_textures

        self.texture = []

        self.texture_array = gl.GLuint(0)
        gl.glGenTextures(1, self.texture_array)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_array)

        gl.glTexImage3D(
            gl.GL_TEXTURE_2D_ARRAY, 0, gl.GL_RGBA,
            self.texture_width, self.texture_height, self.max_texture,
            0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None
        )

    def generate_mipmaps(self):
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D_ARRAY)

