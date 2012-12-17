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

# def DisplayControlsPoints(pMesh):
#     lControlPointsCount = pMesh.GetControlPointsCount()
#     lControlPoints = pMesh.GetControlPoints()

#     DisplayString("    Control Points")

#     for i in range(lControlPointsCount):
#         DisplayInt("        Control Point ", i)
#         Display3DVector("            Coordinates: ", lControlPoints[i])

#         for j in range(pMesh.GetLayerCount()):
#             leNormals = pMesh.GetLayer(j).GetNormals()
#             if leNormals:
#                 if leNormals.GetMappingMode() == FbxLayerElement.eByControlPoint:
#                     header = "            Normal Vector (on layer %d): " % j 
#                     if leNormals.GetReferenceMode() == FbxLayerElement.eDirect:
#                         Display3DVector(header, leNormals.GetDirectArray().GetAt(i))

#     DisplayString("")

# def DisplayPolygons(pMesh):
#     lPolygonCount = pMesh.GetPolygonCount()
#     lControlPoints = pMesh.GetControlPoints() 

#     DisplayString("    Polygons")

#     vertexId = 0
#     for i in range(lPolygonCount):
#         DisplayInt("        Polygon ", i)

#         for l in range(pMesh.GetLayerCount()):
#             lePolgrp = pMesh.GetLayer(l).GetPolygonGroups()
#             if lePolgrp:
#                 if lePolgrp.GetMappingMode() == FbxLayerElement.eByPolygon:
#                     if lePolgrp.GetReferenceMode() == FbxLayerElement.eIndex:
#                         header = "        Assigned to group (on layer %d): " % l 
#                         polyGroupId = lePolgrp.GetIndexArray().GetAt(i)
#                         DisplayInt(header, polyGroupId)
#                 else:
#                     # any other mapping modes don't make sense
#                     DisplayString("        \"unsupported group assignment\"")

#         lPolygonSize = pMesh.GetPolygonSize(i)

#         for j in range(lPolygonSize):
#             lControlPointIndex = pMesh.GetPolygonVertex(i, j)

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