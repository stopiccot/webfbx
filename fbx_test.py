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

def get_vertices(mesh):
    unique_points = []
    pointsCount = mesh.GetControlPointsCount()
    points = mesh.GetControlPoints()

    for i in range(pointsCount):
        unique_points.append([points[i][0], points[i][1], points[i][2]])

    return unique_points

def print_mesh(node):
    mesh = node.GetNodeAttribute()

    result = {}
    result["name"] = node.GetName()
    v = get_vertices(mesh)
    result["vertexCount"] = mesh.GetControlPointsCount()
    result["polygonCount"] = mesh.GetPolygonCount()
    result["p"] = []

    pp = []
    for i in range(mesh.GetPolygonCount()):
        for j in range(2, mesh.GetPolygonSize(i)):
            pp.append(mesh.GetPolygonVertex(i, 0))
            pp.append(mesh.GetPolygonVertex(i, j - 1))
            pp.append(mesh.GetPolygonVertex(i, j))

    result["vertices"] = []
    for i in range(len(pp)):
        result["vertices"] += v[pp[i]]

    #result["p"] = pp

    result2 = {}
    result2["vertices"] = result["vertices"]
    return result2

def fbx_test():
    lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
    lResult = FbxCommon.LoadScene(lSdkManager, lScene, './test.fbx')
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