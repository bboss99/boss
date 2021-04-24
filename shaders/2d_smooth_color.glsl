// Vertex Shader
uniform mat4 ModelViewProjectionMatrix;

in vec2 pos;
in vec4 color;

noperspective out vec4 finalColor;

void main()
{
  gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
  finalColor = color;
}

// Fragment Shader

noperspective in vec4 finalColor;
out vec4 fragColor;

void main()
{
  fragColor = finalColor;
}