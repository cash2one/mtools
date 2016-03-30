# coding=gbk

import os
import util

MCDNDIR = "/Res_Weiduan"
MRESDIR = "../Data"

_g_resource = {
    "UI":[("./UI/Image", "(dds|tga)"),
           ("./UI/Image_New", "(tga|dds)"),
           ("./UI/effect", "(dds|tga)"),
           ("./UI/UIModel", "(mz|dds|fb)")],

    "Models":[("./Models", "(mz|dds|tga|fb|fbx|obj|rar|db)")],

    "Effect":[("./Effect", "(mz|dds|tga|fb)"),
                ("./Effect", "skilleffects", "ActorSkillEffect\\SkillEffect")],

    "Creature":[("./Creature", "(mz|fb|dds)")],

    "Scene":[("./Scene/Maps", "(jpg|dds)"),
               ("./Scene/Grass", "(dds)"),
               ("./Scene/Model", "(dds|tga|fb|obj)")],

    "Music":[("./Music", "(wav|mp3)")],

    "Environment":[("./Environment", "(mz|dds)")],

    "Texture":[("./Texture", "(dds)")],

    "Lightmap":[("./Lightmap", "(dds)")],
}


def migrateRes(relSrcDir, tarDir, rebuildSrcDir = False):
    """资源迁移"""

    curDir = os.path.abspath(".")
    srcDir = os.path.abspath(relSrcDir)
    tarDir = os.path.abspath(tarDir)
    for key, val in _g_resource.items():
        for item in val:
            strdir = item[0]
            strpat = item[1]
            igndir = len(item) > 2 and item[2] or ""
            os.chdir(srcDir)
            util.mvRes(strdir, tarDir, strpat, igndir)
            os.chdir(curDir)

    if rebuildSrcDir:
        dirList = _g_resource.keys()
        for name in dirList:
            dirname = os.path.join(relSrcDir, name)
            if not os.path.exists(dirname):
                while True:
                    try:
                        os.makedirs(dirname)
                        break
                    except:
                        pass
                    # print("mkdir %s failed, current directory:%s"%(dirname, os.path.abspath(".")))
