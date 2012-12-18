from fbx import *
import json, FbxCommon

def find_mesh(scene, node = None):
    if node == None:
        node = scene.GetRootNode()

    if node.GetNodeAttribute() != None and node.GetNodeAttribute().GetAttributeType() == FbxNodeAttribute.eMesh:
        return node

    for i in range(node.GetChildCount()):
        result = find_mesh(scene, node.GetChild(i))
        if result != None:
            return result

    return None

def getMeshVertices(mesh):
    return reduce(lambda x, p: x + [p[0], p[1], p[2]], mesh.GetControlPoints(), [])

def print_mesh(node):
    mesh = node.GetNodeAttribute()
    vertices = getMeshVertices(mesh)

    triangleIndicies = []
    lineIndicies = []

    polygonCount = mesh.GetPolygonCount()
    for i in range(polygonCount):
        def m(idx): return map(lambda x: mesh.GetPolygonVertex(i, x), idx)
        polygonSize = mesh.GetPolygonSize(i)
        lineIndicies += m([polygonSize - 1, 0, 0, 1])
        for j in range(2, polygonSize):
            lineIndicies += m([j - 1, j])
            triangleIndicies += m([0, j - 1, j])

    return {
        "indexed": True,
        "vertices": vertices,
        "indices": triangleIndicies,
        "lineIndicies": lineIndicies
    }

def fbx_to_json(file):
    lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
    lResult = FbxCommon.LoadScene(lSdkManager, lScene, file)
    if not lResult:
        return 'Failed to open FBX scene'

    meshNode = find_mesh(lScene)
    mesh = print_mesh(meshNode)

    lSdkManager.Destroy()

    return mesh