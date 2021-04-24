
// Vertex Shader

uniform mat4 ModelViewProjectionMatrix;
/* Keep in sync with intern/opencolorio/gpu_shader_display_transform_vertex.glsl */
in vec2 uvs;
in vec2 pos;
in vec4 color;

noperspective out vec4 finalColor;
out vec2 o_uvs;

void main()
{
    gl_Position = ModelViewProjectionMatrix * vec4(pos.xy, 0.0f, 1.0f);
    gl_Position.z = 1.0;
    o_uvs = uvs;
    finalColor = color;
}

// Fragment Shader

noperspective in vec4 finalColor;
in vec2 o_uvs;
out vec4 fragColor;

uniform sampler2D image;

void main()
{
    fragColor = texture(image, o_uvs)*finalColor;
}