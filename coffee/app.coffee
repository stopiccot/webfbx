gl = null

compileShaderPart = (type, source) ->
    shader = gl.createShader(type)
    gl.shaderSource(shader, source)
    gl.compileShader(shader)

    if not gl.getShaderParameter(shader, gl.COMPILE_STATUS)
        alert(gl.getShaderInfoLog(shader))

    return shader

compileShader = (vertex, pixel) ->
    vertexShader = compileShaderPart(gl.VERTEX_SHADER, vertex)
    pixelShader = compileShaderPart(gl.FRAGMENT_SHADER, pixel)

    shader = gl.createProgram()
    gl.attachShader(shader, vertexShader)
    gl.attachShader(shader, pixelShader)

    gl.linkProgram(shader)

    if not gl.getProgramParameter(shader, gl.LINK_STATUS)
        alert("Failed to compile shader")

    return shader

initGL = (canvas) ->
    try
        gl = canvas.getContext("experimental-webgl")
        gl.viewportWidth = canvas.width
        gl.viewportHeight = canvas.height
    catch error
    if gl == null
        alert("Could not initialise WebGL, sorry :-(")

createMeshFromJSON = (json) ->
    vertices = json["vertices"]
    colors = []

    avaliable_colors = [
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 0.5, 0.0, 1.0],
        [1.0, 0.0, 0.0, 1.0],
        [1.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0, 1.0]        
    ]

    for i in [0..vertices.length / 3]
        j = i
        c = avaliable_colors[j % avaliable_colors.length]
        colors = colors.concat(c)

    if json["indexed"]
        return createIndexedObject(vertices, colors, json["indices"])
    else
        return createObject(vertices, colors)

createObject = (vertices, colors) ->
    obj = new Object()
    obj.indexed = false
    obj.vertexBuffer = createBuffer(3, vertices)
    obj.colorBuffer = createBuffer(4, colors)
    return obj

createIndexedObject = (vertices, colors, indices) ->
    obj = new Object()
    obj.indexed = true
    obj.vertexBuffer = createBuffer(3, vertices)
    obj.colorBuffer = createBuffer(4, colors)
    obj.indexBuffer = createIndexBuffer(indices)
    return obj

createBuffer = (itemSize, data) ->
    buffer = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW)
    buffer.itemSize = itemSize
    buffer.numItems = data.length / itemSize

    return buffer

createIndexBuffer = (data) ->
    buffer = gl.createBuffer()
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffer)
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(data), gl.STATIC_DRAW)
    buffer.itemSize = 1
    buffer.numItems = data.length

    return buffer

drawObject = (obj, shader, mvMatrix, pMatrix, alpha) ->
    gl.bindBuffer(gl.ARRAY_BUFFER, obj.vertexBuffer)
    gl.vertexAttribPointer(shader.vertexPositionAttribute, obj.vertexBuffer.itemSize, gl.FLOAT, false, 0, 0)

    gl.bindBuffer(gl.ARRAY_BUFFER, obj.colorBuffer)
    gl.vertexAttribPointer(shader.vertexColorAttribute, obj.colorBuffer.itemSize, gl.FLOAT, false, 0, 0)

    gl.uniformMatrix4fv(shader.pMatrixUniform, false, pMatrix)
    gl.uniformMatrix4fv(shader.mvMatrixUniform, false, mvMatrix)
    gl.uniform1f(shader.alphaUniform, alpha)

    if obj.indexed
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, obj.indexBuffer)
        gl.drawElements(gl.TRIANGLES, obj.indexBuffer.numItems, gl.UNSIGNED_SHORT, 0)
    else
        gl.drawArrays(gl.TRIANGLES, 0, obj.vertexBuffer.numItems)

map = (list, f) ->
    (f(x) for x in list)

dump_obj = (obj) =>
    (key + " -> " + obj[key] for key in obj)

webGLStart = ->
    # Initialize WebGL
    initGL($("#webgl-canvas")[0])

    # Handle window resize
    $(window).bind("resize", () -> 
        w = $(window).width()
        h = $(window).height()

        w = h = Math.min(w, h)

        $("#webgl-canvas").css("width", w + "px")
        $("#webgl-canvas").css("height", h + "px")

        gl.viewportWidth = w
        gl.viewportHeight = h
    ).resize()

    mesh = null

    # Helper for loading uploaded FBX models
    loadFBX = (name) -> $.get(name, (data) -> mesh = createMeshFromJSON(JSON.parse(data)))

    # Initialize file upload
    $("#fileupload").fileupload({
        dataType: 'json',
        add:  (e, data) -> data.submit()
        done: (e, data) -> loadFBX(data.result.url)
    })

    gl.enable(gl.BLEND)
    gl.enable(gl.DEPTH_TEST)
    gl.depthFunc(gl.LESS);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_APLHA)

    shader = compileShader($("#vertex-shader").html(), $("#pixel-shader").html())

    # Shader
    gl.useProgram(shader);

    # Shader attributes
    [shader.vertexPositionAttribute, shader.vertexColorAttribute] = map ["aVertexPosition", "aVertexColor"], (x) ->
        a = gl.getAttribLocation(shader, x)
        gl.enableVertexAttribArray(a)
        return a
    
    # Shader uniforms
    [shader.pMatrixUniform, shader.mvMatrixUniform,  shader.alphaUniform] = map ["uPMatrix", "uMVMatrix", "uAlpha"], (x) ->
        gl.getUniformLocation(shader, x)

    # Matrices
    mvMatrix = mat4.create();
    pMatrix = mat4.create();

    # Load default model
    loadFBX('fbx/test.fbx')

    angle = 0.0

    rotate = (angle) ->
        mat4.rotate(mvMatrix, 5 * angle, [1, 0, 0])
        mat4.rotate(mvMatrix, 2 * angle, [0, 1, 0])
        mat4.rotate(mvMatrix, 1 * angle, [0, 0, 1])

    render = ->
        gl.clearColor(0.1, 0.1, 0.1, 1.0)
        gl.clearDepth(1.0)
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)

        angle -= 0.01

        mat4.identity(pMatrix)   
        mat4.perspective(45, 1, 0.1, 100.0, pMatrix)

        mat4.identity(mvMatrix)   
        mat4.translate(mvMatrix, [0.0, 0.0, -20.0])
        rotate(angle)

        if mesh != null
            drawObject(mesh, shader, mvMatrix, pMatrix, 1.0)

    setInterval(render, 1000 / 60)

$(webGLStart)