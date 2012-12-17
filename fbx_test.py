from fbx import *
import FbxCommon

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

def fbx_test():
    lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
    lResult = FbxCommon.LoadScene(lSdkManager, lScene, './test.fbx')
    if not lResult:
        return 'Failed to open FBX scene'

    result = 'FBX scene successfully opened<br>'
    result += '------------------------------------------<br>'
    result += DisplayHierarchy(lScene)
    result += '------------------------------------------<br>'

    lSdkManager.Destroy()

    return result