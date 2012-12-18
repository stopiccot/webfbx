precision mediump float;

varying vec4 vColor;
uniform float uAlpha;

void main(void) {
    vec4 c = vColor;
    c.a = uAlpha;
    gl_FragColor = c;
}