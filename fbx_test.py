import fbx
import FbxCommon
#from fbx import *

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

    result += pNode.GetName()
    result += '<br>'

    for i in range(pNode.GetChildCount()):
        result += DisplayNodeHierarchy(pNode.GetChild(i), pDepth + 1)

    return result

def fbx_test():
    lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
    lResult = FbxCommon.LoadScene(lSdkManager, lScene, './test.fbx')
    if not lResult:
        return 'Failed to open FBX scene'

    result = 'FBX scene successfully opened<br>------------------------------------------<br>'
    result += DisplayHierarchy(lScene)
    return result