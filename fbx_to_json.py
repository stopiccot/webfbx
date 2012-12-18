from fbx import *
import json, FbxCommon

def DisplayHierarchy(pScene):
    lRootNode = pScene.GetRootNode()

    result = ''
    for i in range(lRootNode.GetChildCount()):
        result += DisplayNodeHierarchy(lRootNode.GetChild(i), 0)

    return result

def DisplayNodeHierarchy(pNode, pDepth):
    result = ""
    for i in range(pDepth):
        result += "     "

    result += pNode.GetName() + " - "
    nodeAttributeType = pNode.GetNodeAttribute().GetAttributeType()
    if nodeAttributeType == FbxNodeAttribute.eMarker:
        result += "eMarker"
    elif nodeAttributeType == FbxNodeAttribute.eSkeleton:
        result += "eSkeleton"
    elif nodeAttributeType == FbxNodeAttribute.eMesh:
        result += "eMesh"
    elif nodeAttributeType == FbxNodeAttribute.eNurbs:
        result += "eNurbs"
    elif nodeAttributeType == FbxNodeAttribute.ePatch:
        result += "ePatch"
    elif nodeAttributeType == FbxNodeAttribute.eCamera:
        result += "eCamera"
    elif nodeAttributeType == FbxNodeAttribute.eLight:
        result += "eLight"
    result += '<br>'

    for i in range(pNode.GetChildCount()):
        result += DisplayNodeHierarchy(pNode.GetChild(i), pDepth + 1)

    return result

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
    unique_points = []
    pointsCount = mesh.GetControlPointsCount()
    points = mesh.GetControlPoints()

    for i in range(pointsCount):
        unique_points.append([points[i][0], points[i][1], points[i][2]])

    return unique_points

def print_mesh(node):
    mesh = node.GetNodeAttribute()

    result = {}

    v = getMeshVertices(mesh)

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

    result["indexed"] = True
    result["vertices"] = []

    if result["indexed"]:
        result["indices"] = triangleIndicies
        result["lineIndicies"] = lineIndicies
        for value in v:
            result["vertices"] += value

    return result

def fbx_to_json(file):
    lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
    lResult = FbxCommon.LoadScene(lSdkManager, lScene, file)
    if not lResult:
        return 'Failed to open FBX scene'

    result = 'FBX scene successfully opened<br>'
    result += '------------------------------------------<br>'
    result += DisplayHierarchy(lScene)
    result += '------------------------------------------<br>'

    meshNode = find_mesh(lScene)
    mesh_str = json.dumps(print_mesh(meshNode))

    lSdkManager.Destroy()

    return mesh_str
    result += mesh_str
    return result