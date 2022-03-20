import numbers


class BlockType:
    def __init__(self, texture_manager, name='unknown',
                 block_face_texture=None):
        if block_face_texture is None:
            self.block_face_texture = {'all': 'cobblestone'}

        self.name = name
        self.vertex_positions = numbers.vertex_positions
        self.indices = numbers.indices


        for texture in block_face_texture.values():
            texture_manager.add_texture(texture)