#coding=gbk

import util
from command import *
from migrate import *
from optimize import *


DefaultCdnDir = "/Res_Weiduan"
DefaultResDir = "../Data"


class MigrateRes(Command):
    def __init__(self, srcDir, tarDir, resList, rebuildSrcDir = False):
        Command.__init__(self)

        self.mName = "资源迁移：%s -> %s"%(srcDir, tarDir)
        self.mSrcDir = srcDir
        self.mTarDir = tarDir
        self.mResList = resList
        self.mRebuildSrcDir = rebuildSrcDir

    def run(self):
        self.preRun()
        migrateRes(self.mSrcDir, self.mTarDir, self.mResList, self.mRebuildSrcDir)
        self.postRun()
        return 0


class RestoreMustFile(Command):
    def __init__(self):
        Command.__init__(self)
        self.mName = "恢复必要资源"

    def run(self):
        self.preRun()
        moveBackMustFile(DefaultResDir, DefaultCdnDir)
        self.postRun()
        return 0


class Optimization(Command):
    def __init__(self):
        Command.__init__(self)
        self.mName = "体验优化"

    def run(self):
        self.preRun()
        optimize(DefaultResDir, DefaultCdnDir)
        self.postRun()
        return 0


class UnlinkCommand(Command):
    def __init__(self, dirName, suffix):
        Command.__init__(self)
        self.mSuffix = suffix
        self.mDir = dirName
        self.mName = "删除%s文件"%suffix

    def run(self):
        self.preRun()
        util.unlinkRes(self.mDir, self.mSuffix)
        self.postRun()
        return 0


## 不败传说微端资源分离
MIGRATE_RULES = {
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
               ("./Scene/Model", "(dds|tga|fb|obj|mz)")],

    "Music":[("./Music", "(wav|mp3)")],

    "Environment":[("./Environment", "(mz|dds)")],

    "Texture":[("./Texture", "(dds|tga|max)")],

    "Lightmap":[("./Lightmap", "(dds)")],
}

CmdId_MigrateToCdn = 1
CmdId_MigrateToRes = 2
CmdId_RestoreMustFile = 3
CmdId_Optimize = 4
CmdId_UnlinkZip = 5

GlobalCmds = {
    CmdId_MigrateToCdn:MigrateRes(DefaultResDir, DefaultCdnDir, MIGRATE_RULES, True),
    CmdId_MigrateToRes:MigrateRes(DefaultCdnDir, DefaultResDir, MIGRATE_RULES),
    CmdId_RestoreMustFile:RestoreMustFile(),
    CmdId_Optimize:Optimization(),
    CmdId_UnlinkZip:UnlinkCommand(DefaultResDir, "zip"),
}


## 临时命令
TempSceneDir = "/Res_Scene"

TempSceneCmd_MigrateToRoot = 6
TempSceneCmd_MigrateToRes = 7

GlobalCmds[TempSceneCmd_MigrateToRoot] = MigrateRes(DefaultResDir, TempSceneDir, {"Scene":[("./Scene/Model", "(mz)")]}, False)
GlobalCmds[TempSceneCmd_MigrateToRes] = MigrateRes(TempSceneDir, DefaultResDir, {"Scene":[("./Scene/Model", "(mz)")]}, False)


## 联运微端资源分离
PartnerCdnDir = "/Res_Partner"
PartnerResDir = "../Data"
PartnerPatchDir = "../Partner_Patch"

PARTNER_MIGRATE_RULES = {
    "UI":[("./UI/Image", "(dds|tga)"),
          ("./UI/Image_New", "(tga|dds)"),
          ("./UI/effect", "(dds|tga)"),
          ("./UI/UIModel", "(mz|dds|fb)"),

          # 联运
          ("./UI/bg", "(dds|tga)"),],

    "Models":[("./Models", "(mz|dds|tga|fb|fbx|obj|rar|db)")],

    "Effect":[("./Effect", "(mz|dds|tga|fb)"),
              ("./Effect", "skilleffects", "ActorSkillEffect\\SkillEffect")],

    "Creature":[("./Creature", "(mz|fb|dds)")],

    "Scene":[("./Scene/Maps", "(jpg|dds)"),
             ("./Scene/Grass", "(dds)"),
             ("./Scene/Model", "(dds|tga|fb|obj|mz)"),

             # 联运
             ("./Scene/Maps", "(mps|terrain)"),
             ("./Scene/Texture", "(tga|dds)")],

    "Music":[("./Music", "(wav|mp3)")],

    "Environment":[("./Environment", "(mz|dds)")],

    "Texture":[("./Texture", "(dds|tga|max)")],

    "Lightmap":[("./Lightmap", "(dds)")],

    "Video":[("./Video", "(mp4)")],

    "Helper":[("./Helper", "(html|jpg|png|css|gif)")],
}

class PatchPartnerRes(Command):
    def __init__(self):
        Command.__init__(self)
        self.mName = "联运端资源打包(lianyun*.csv)"

    def run(self):
        self.preRun()
        param = {}
        param["pattern"] = ".*lianyun.*\.csv$"
        param["resdir"] = PartnerPatchDir
        param["cdndir"] = PartnerCdnDir
        util.walktree("./", visitCsvFile, param)
        self.postRun()
        return 0

CmdId_Partner_MigrateToCdn = 100
CmdId_Partner_MigrateToRes = 101
CmdId_Partner_PatchRes = 102

GlobalCmds[CmdId_Partner_MigrateToCdn] = MigrateRes(PartnerResDir, PartnerCdnDir, PARTNER_MIGRATE_RULES, True)
GlobalCmds[CmdId_Partner_MigrateToRes] = MigrateRes(PartnerCdnDir, PartnerResDir, PARTNER_MIGRATE_RULES, True)
GlobalCmds[CmdId_Partner_PatchRes] = PatchPartnerRes()
