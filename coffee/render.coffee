gl = null

window.render = {}

# Simple WebGL initialization
window.render = 
    initGL: (canvas) ->
        try
            window.gl = gl = null#canvas.getContext("webgl")
            if gl == null
                window.gl = gl = canvas.getContext("experimental-webgl")
            gl.viewportWidth = canvas.width
            gl.viewportHeight = canvas.height
        catch error
        if gl == null
            alert("Could not initialise WebGL, sorry :-(")

    compileShaderPart: (type, source) ->
        shader = gl.createShader(type)
        gl.shaderSource(shader, source)
        gl.compileShader(shader)

        if not gl.getShaderParameter(shader, gl.COMPILE_STATUS)
            alert(gl.getShaderInfoLog(shader))

        return shader

    compileShader: (vertex, pixel) ->
        vertexShader = this.compileShaderPart(gl.VERTEX_SHADER, vertex)
        pixelShader = this.compileShaderPart(gl.FRAGMENT_SHADER, pixel)

        shader = gl.createProgram()
        gl.attachShader(shader, vertexShader)
        gl.attachShader(shader, pixelShader)

        gl.linkProgram(shader)

        if not gl.getProgramParameter(shader, gl.LINK_STATUS)
            alert("Failed to compile shader")

        return shader