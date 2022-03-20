#version 330

out vec4 fragment_colour;

uniform sampler2DArray texture_array_sampler;

in vec3 local_position;

void main(void) {
    fragment_colour = texture(texture_array_sampler, vec3(0.5, 0.5, 1.0));
}
