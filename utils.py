import json
from os.path import join,exists,dirname,basename,realpath,isfile,isdir,normpath
import bpy
from copy import copy as copy_copy
from functools import partial
from pprint import pprint
import gpu
import time
import importlib
import os
import sys
import subprocess

def getModule(filePath):
    moduleName = basename(filePath).split('.')[0]
    spec = importlib.util.spec_from_file_location(moduleName, filePath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def explore(dir_path):
    FILEBROWSER_PATH = join(os.getenv('WINDIR'), 'explorer.exe')
    dir_path = normpath(dir_path)

    if isdir(dir_path):
        subprocess.run([FILEBROWSER_PATH, dir_path])
    elif isfile(dir_path):
        subprocess.run([FILEBROWSER_PATH, '/select,', normpath(dir_path)])

def openFile(file_path):
    if sys.platform == "win32":
        os.startfile(file_path)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, file_path])

def openDir(dir_path):
    if sys.platform == "win32":
        explore(dir_path)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"

        if isfile(dir_path):
            dir_path = dirname(dir_path)
        subprocess.call([opener, dir_path])

def mesh_combineVertsFaces(verts0,verts1,faces0,faces1):
    verts = verts0 + verts1

    offset = len(verts0)

    faces = []
    faces.extend(faces0)

    for faceTuple in faces1:
        newFace = []
        for index in faceTuple:
            newFace.append(index+offset)
        faces.append(tuple(newFace))
    return verts,faces

def mesh_combineVertsFacesList(vertsListList, facesListList):
    verts = []

    for vertList in vertsListList:
        verts.extend(vertList)

    faces = []
    faces.extend(facesListList[0])

    offset = 0

    for i in range(1, len(facesListList)):
        offset = offset + len(vertsListList[i - 1])

        for faceTuple in facesListList[i]:
            newFace = []
            for index in faceTuple:
                newFace.append(index + offset)
            faces.append(tuple(newFace))

    return verts, faces

def Float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

def Int(value):
    try:
        return int(value)
    except ValueError:
        return 0

def copy(pObj):
    return copy_copy(pObj)

def appendCheck(aList,element):
    if element not in aList:
        aList.append(element)
        return True
    return False

def removeCheck(aList,element):
    if element in aList:
        aList.remove(element)
        return True
    return False

def removeCheckFunc(aList,func):
    for fn in aList:
        if fn.func == func:
            aList.remove(fn)
            return True
    return False

def correctFuncFormat(param):
    if param is None:
        param = (None, )
    else:
        if type(param) in (tuple,list):
            if len(param) > 0:
                if callable(param[0]):
                    pass
                else:
                    param = (None,)
        else:
            if callable(param):
                param = (param,)
            else:
                param = (None, )
    return param

def correctFuncFormat2(param):
    if param is None:
        param = (None, )
    else:
        if type(param) in (tuple,list):
            if len(param) > 0:
                if callable(param[0]):
                    pass
                else:
                    if type(param[0]) in (tuple,list):
                        return correctFuncFormat2(param[0])                    
                    param = (None,)
        else:
            if callable(param):
                param = (param,)
            else:
                param = (None, )
    return param

def _addCallback(caller, pList, *_params):
    func,*params = correctFuncFormat2(_params)
    if func:
        if 'caller' in func.__code__.co_varnames:
            if len(params) > 0:
                pList.append(partial(func,caller,*params))
            else:
                pList.append(partial(func,caller))
        else:
            if len(params) > 0:
                pList.append(partial(func,*params))
            else:
                pList.append(partial(func))
        return True
    return False

def getJsonDict(pObj):
    jDict = {}
    for att in dir(pObj):
        if not att[:2] == '__':
            oDotA = getattr(pObj,att)

            if oDotA is None:
                jDict[att] = ''
            else:
                if not callable(oDotA):
                    if is_jsonable(oDotA):
                        jDict[att] = oDotA
                    else:
                        jDict[att] = getJsonDict(oDotA)
    return jDict

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def get_dict_imageName_imagePath(dirPath = ''):
   img_dir = join(dirname(__file__),'src_img') if dirPath == '' else dirPath
   imageFiles = getFileList(img_dir,'png')
   dict_imageName_imagePath = {img:join(img_dir,img) for img in imageFiles}
   return dict_imageName_imagePath

def getShader(path:str):
    with open(path) as f:
        lines = f.readlines()
        verts = []
        for i, line in enumerate(lines):
            if "Fragment Shader" in line:
                fragIndex = i
                break
            else:
                verts.append(line)
        frags = lines[fragIndex:]
    return gpu.types.GPUShader("\n".join(verts), "\n".join(frags))

def loadStyle(stylePath):
    return json_loadPath(stylePath)
    styleDict = json_loadPath(stylePath)

    dict_uiStyels = {}

    for k,v in styleDict.items():
        dict_uiStyels[k] = convertToObjFromJson(v)

    return styleDict

def convertToObjFromJson(uiStyleDict):
    from .Geo.base_geo.GeoData import GeoData
    from .Text import TextData
    uiObjDict = {}

    uiObjDict['geoType'] = uiStyleDict['geoType']

    uiObjDict['geoData'] = GeoData(
        uiStyleDict['geoData']['geo_type'],
        uiStyleDict['geoData']['normal_color'],
        uiStyleDict['geoData']['hover_color'],
        uiStyleDict['geoData']['image_path']
    )

    uiObjDict['textData'] = TextData(
        uiStyleDict['textData']['fontSize'],
        uiStyleDict['textData']['font_id'],
        uiStyleDict['textData']['align'],
        uiStyleDict['textData']['color'],
    )
    return  uiObjDict

def json_loadPath(jsonPath):
    with open(jsonPath) as f:
        jDict = json.load(f)
    return jDict

def json_dump(jsonPath,dictObj):
    try:
        with open(jsonPath, 'w') as f:
            json.dump(dictObj, f, indent=4)
        return True
    except:
        return False

def getStylesDict():
    stylesDir = join(dirname(__file__), "styles")
    stylesFiles = getFileList(stylesDir, 'json')

    dict_styles = {}
    for each in stylesFiles:
        dict_styles[each[:-5]] = join(stylesDir, each)

    return dict_styles

def getShaderDict():
    shaderDir   = join(dirname(__file__), "shaders")
    shaderFiles = getFileList(shaderDir, 'glsl')

    dict_shaders = {each[:-5] : getShader(join(shaderDir,each)) for each in shaderFiles}
    return dict_shaders

def get_dict_imageName_imageData(dirPath = ''):
    dict_imageName_imagePath = get_dict_imageName_imagePath(dirPath)
    
    dict_imageName_imageData = {}
    
    for iN,iP in dict_imageName_imagePath.items():
        imageData = bpy.data.images.load(iP, check_existing = True)
        if imageData.gl_load():
            raise Exception()
        dict_imageName_imageData[iN] = imageData
    
    return dict_imageName_imageData

getImgDataDict = get_dict_imageName_imageData

def getNextFilePath(exportDir,fileName,pFormat):
    fn = join(exportDir,fileName+pFormat)
    if not exists(fn):
        return fn
    else:
        for i in range(100):
            fn = join(exportDir,fileName+'_{}{}'.format(str(i),pFormat))
            if not exists(fn):
                return fn

def getFileAndFolderInfoBySearch(folderPath,pFormat):
    fileNamesPaths = []

    from os.path import isfile, join, getmtime

    onlyFiles = []
    i = 0
    for level1 in os.listdir(folderPath):
        level1Path = join(folderPath, level1)  
        if isfile(level1Path):
            temp = level1.split('\\')[-1].rsplit('.',1)  
            if temp[1] == pFormat:
                onlyFiles.append((str(i),temp[0],level1Path))
                i += 1
        elif not isfile(level1Path):
            for level2 in os.listdir(level1Path):
                level2Path = join(level1Path, level2)
                if isfile(level2Path):
                    temp = level2.split('\\')[-1].rsplit('.',1)  
                    if temp[1] == pFormat:
                        onlyFiles.append((str(i),temp[0],level2Path))
                        i += 1
    return onlyFiles

def getFileList(folderPath, pFormat = ''):
    pFormat = pFormat.split('.')[-1]
    if pFormat == '':
        only_files = [f for f in os.listdir(folderPath) if isfile(join(folderPath, f))]
    else:
        only_files = [f for f in os.listdir(folderPath) if isfile(join(folderPath, f)) and f.split('.')[-1] == pFormat]
    return only_files

def getFolderList(folderPath):
    only_folders = [f for f in os.listdir(folderPath) if not isfile(join(folderPath, f))]
    return only_folders

def readFileData(filePath):
    with open(filePath) as f:
        lines = [line.rstrip('\n\r') for line in f]
    return lines

def printTime(func):
    def innerFunc(*args, **kwargs):
        start_time = time.perf_counter()
        func(*args, **kwargs)
        invokeTime = time.perf_counter() - start_time
        print(invokeTime*1000)
    return innerFunc

