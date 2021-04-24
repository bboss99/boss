// Vertex Shader
uniform mat4 ModelViewProjectionMatrix;

in vec2 pos;
in vec4 color;

noperspective out vec4 finalColor;

void main()
{
    // gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
    gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
    finalColor = color;
}

// Fragment Shader

noperspective in vec4 finalColor;
out vec4 fragColor;
uniform vec4 clipRect;

void main()
{
    // float x = finalColor.x * gl_FragCoord.x / clipRect.w;
    // float x = clipRect.z*finalColor.y*.05;
    
    // float y = gl_FragCoord.y/512;
    
    fragColor = finalColor;
    
    // fragColor = vec4(x,0,0, 1);

    if (gl_FragCoord.x > clipRect.z || gl_FragCoord.x < clipRect.x || gl_FragCoord.y < clipRect.y || gl_FragCoord.y > clipRect.w ) {
        discard; 
    }

}