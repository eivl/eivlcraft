import numbers


class BlockType:
    def __init__(self, texture_manager, name='unknown',
                 block_face_texture=None):
        if block_face_texture is None:
            self.block_face_texture = {'all': 'cobblestone'}

        self.name = name
        self.vertex_positions = numbers.vertex_positions
        self.indices = numbers.indices
        self.text_coords = numbers.tex_coords[:]

        def set_block_face(side, texture):
            for vertex in range(4):
                self.text_coords[side * 12 + vertex * 3 + 2] = texture

        for face, texture in block_face_texture.items():
            texture_manager.add_texture(texture)
            texture_index = texture_manager.textures.index(texture)

            if face == 'all':
                set_block_face(0, texture_index)
                set_block_face(1, texture_index)
                set_block_face(2, texture_index)
                set_block_face(3, texture_index)
                set_block_face(4, texture_index)
                set_block_face(5, texture_index)

            elif face == 'sides':
                set_block_face(0, texture_index)
                set_block_face(1, texture_index)
                set_block_face(4, texture_index)
                set_block_face(5, texture_index)

            else:
                set_block_face(["right", "left", "top", "bottom", "front",
                                "back"].index(face), texture_index)