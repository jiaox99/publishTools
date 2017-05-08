# -*- encoding:utf-8 -*-
# written by:	Jiao Zhongxiao

import os
import shutil
import xml.etree.ElementTree as EleTree
import io
import binascii
import sys
from ftplib import FTP
import configparser
import VAPublishUtil

# 发布选项配置文件
CFG_FILE_NAME = "publish.cfg"


def print_menu_info(pub_config):
    """打印发布选项信息"""
    i = 0
    print("-----------------------------------------")
    print("可选配置标识序号配置选项：")
    print("        直接回车默认为从develop分支发版本到dev_branch!!!!!!")
    while pub_config.has_section("C" + str(i)):
        if pub_config.has_option("C" + str(i), 'info'):
            print(i, '---->', pub_config["C" + str(i)]['info'])
        i += 1


def check_config_file(p_root_dir):
    """检查配置文件"""
    pub_config = configparser.ConfigParser()
    pub_config_file_path = os.path.join(p_root_dir, VAPublishUtil.TOOL_DIR_NAME, CFG_FILE_NAME)
    if os.path.exists(pub_config_file_path):
        pub_config.read(pub_config_file_path)
        print("检测到配置")
        return pub_config
    else:
        pub_config['DEFAULT'] = {
            'publishDir': 'D:\\',
            'devDir': "E:\\workspace\\TowerFacebookDev\\branches\\TD_Branch_001\\release\\flash",
            'pubBranch': 'develop',
            'ftpDir': 'www/release/flash'
        }
        pub_config.write(open(pub_config_file_path, 'w'))
        input("找不到配置文件，已生成一份默认的，请填充相应配置后再尝试发布")
        return False


def publish_with_config(pub_config):
    print("开始发布版本")
    ftpDir = pub_config['ftpDir']
    publishDir = pub_config['publishDir']  # 缓存目录
    devDir = pub_config['devDir']  # 发布目录
    pubBranch = pub_config['pubBranch']  # 发布时选择的分支


def read_cfg(pub_config):
    """读取用户选择的发布配置"""
    while True:
        use_cfg = input("请输入配置标识序号：\n")
        if len(use_cfg) == 0:
            use_cfg = "DEFAULT"
        else:
            use_cfg = "C" + use_cfg
        if pub_config[use_cfg]:
            return pub_config[use_cfg]
        else:
            print("选择错误")

if __name__ == "__main__":
    project_root_dir = VAPublishUtil.try_find_project_root_dir()
    if project_root_dir:
        p_config = check_config_file(project_root_dir)
        if p_config:
            print_menu_info(p_config)
            cfg = read_cfg(p_config)
            publish_with_config(p_config)
    quit()


input("Pause")
# import subprocess
os.chdir(os.path.split(sys.argv[0])[0])


cfg = input("请输入配置标识序号：\n")
if len(cfg) == 0:
    cfg = "DEFAULT"
else:
    cfg = "C" + cfg
ftpDir = pubConfig[cfg]['ftpDir']
publishDir = pubConfig['DEFAULT']['publishDir']  # 缓存目录
devDir = pubConfig[cfg]['devDir']  # 发布目录
# workBranch = pubConfig['DEFAULT']['workBranch']	#当前工作分支
# print( workBranch )
pubBranch = pubConfig[cfg]['pubBranch']  # 发布时选择的分支
if pubBranch == '':
    pubBranch = open("..\\.git\\HEAD", "r", encoding="utf-8").read().replace("ref: refs/heads/", "")
# print( publishDir )
# print( devDir )
# print( workBranch )
# print( pubBranch )
# quit()
# ftp = FTP( "172.17.5.168", "root", "redhat123" )
ftp = FTP("172.17.5.168", "td-vikingage", "td2015")
assets = ".json,.jpg,.png,.swf,.xml,.mp3,.wdp,.td,.xcom"
# ver_config为必须
# bin-debug, bin-release目录的文件只会加上版本号后缀
# 其它目录文件的会根据算法生成CDN版本后缀
# （CRC32（文件内容）& 0xFFFFFFFF）的32进制表示
publishDirs = "ver_config,bin-debug,release"
# end config------------------------------------------------------

ver_config = "ver_config"
projectDir = os.getcwd() + "/../../"
newFile = 0

print("欢迎使用Tower版本发布工具")
print("使用前请确保已编辑配置此文件做好了相关配置")
# 检查运行环境
# print( os.environ["PATH"] )
version = ""


def checkVersion():
    if len(version) > 0:
        return True
    return False


while True:
    version = input("请输入这次的版本号后 <Enter 回车> 继续：\n")
    if checkVersion():
        break
# version = "13"

# 更新SVN-------------------------------------------------------
print("1、更新SVN")


def checkToolPath(tool):
    environ = os.environ["PATH"].split(";")
    for possiblePath in environ:
        possiblePath = os.path.join(possiblePath, tool)
        # print( possiblePath )
        if os.path.exists(possiblePath):
            return True;
    return False;


hasSVN = checkToolPath("svn.exe")
hasGIT = checkToolPath("git.exe")


def updateSVN():
    if hasSVN:
        # os.system( "svn update " + projectDir )
        os.system("svn update " + devDir)
    else:
        print("没有SVN工具或没有添加到环境变量")
        input("请手动更新SVN，完成后 <Enter 回车> 继续")


def updateGIT():
    if hasGIT:
        os.system("git checkout " + pubBranch)
        os.system("git pull")
    else:
        print("没有GIT工具或没有添加到环境变量")
        input("请手动切换到发布分支并更新GIT，完成后 <Enter 回车> 继续")


# 更新DEV目录
print("更新DEV目录")
updateSVN()
# 切换到发布目录
print("更新项目目录")


# updateGIT()

# 清理bin-debug目录
def clearDir(dirPath):
    print("清理目录：" + dirPath)
    for file in os.listdir(dirPath):
        filepath = os.path.join(dirPath, file)
        os.system("rd /s /q " + filepath)


# clearDir( os.path.abspath( os.path.join( projectDir, "bin-debug" ) ) )
# clearDir( os.path.abspath( os.path.join( projectDir, "release/swffile/towerDefenseFight" ) ) )

# 重新生成缓存目录
topDir = os.path.join(publishDir, str(version))
os.system("rd /s /q " + topDir)
os.mkdir(topDir)


# Copy所有文件
def copyFiles():
    dirs = publishDirs.split(",")
    for dir in dirs:
        print("Now working in:" + dir)
        fixDir = os.path.join(projectDir, dir)
        for rootDir, assetsDirs, files in os.walk(fixDir):
            for file in files:
                ext = os.path.splitext(file)[1]
                # print( ext )
                if ext != "" and assets.find(ext) != -1:
                    if dir == "bin-debug" or dir == "bin-release":
                        #
                        # shutil.copy( os.path.join( rootDir, file ), topDir )
                        print("Do nothing!")
                    else:
                        relPath = os.path.relpath(os.path.join(rootDir, file), projectDir)
                        print("原始：" + relPath)
                        relPath = os.path.join(topDir, relPath)
                        print("新的：" + relPath)
                        fileDir = os.path.dirname(relPath)
                        print("FileDir:" + fileDir)
                        if not os.path.exists(fileDir):
                            os.makedirs(fileDir)
                        shutil.copyfile(os.path.join(rootDir, file), relPath)
                    print("Copy " + os.path.join(rootDir, file) + " 完成")


copyFiles()


def addVersionFix():
    global newFile
    files = os.listdir(topDir)
    for file in files:
        oldFile = os.path.join(topDir, file)
        print(oldFile + "---" + str(os.path.isfile(oldFile)))
        if os.path.isfile(oldFile):
            ext = os.path.splitext(file)[1]
            newFile = oldFile.replace(ext, "_" + str(version) + ext)
            os.replace(oldFile, newFile)
            print("重命名：" + oldFile + "<>" + newFile)
            # 加版本号
    curDir = os.path.join(topDir, ver_config)
    files = os.listdir(curDir)
    for file in files:
        oldFile = os.path.join(curDir, file)
        newFile = os.path.join(curDir, file)
        print(oldFile + "---" + str(os.path.isfile(oldFile)))
        if os.path.isfile(oldFile):
            ext = os.path.splitext(file)[1]
            newFile = oldFile.replace(ext, "_" + str(version) + ext)
            os.replace(oldFile, newFile)
            print("重命名：" + oldFile + "<>" + newFile)


addVersionFix()

# 打版本
arr32 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
         "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", ]


def getcrc32(crc):
    crc32 = []
    while crc >= 0:
        res = crc % 32
        crc32.append(arr32[res])
        if crc <= 0 or crc == res:
            break
        else:
            crc = int((crc - res) / 32)
    crc32.reverse()
    return "".join(crc32)


def packVersion():
    global newFile
    configfile = newFile
    config = EleTree.parse(newFile)
    root = config.getroot()
    for folderElement in root:
        folder = folderElement.get("folder")
        for item in folderElement:
            file = os.path.join(topDir, folder + item.text)
            if os.path.exists(file):
                ext = os.path.splitext(file)[1]
                print("Processing:" + file)
                fio = io.FileIO(file, "r")
                fdata = fio.readall()
                fio.close()
                crc = binascii.crc32(fdata) & 0xFFFFFFFF
                crc = getcrc32(crc)
                item.set("size", str(os.path.getsize(file)))
                item.text = item.text.replace(ext, "_" + crc + ext)
                newFile = file.replace(ext, "_" + crc + ext)
                os.replace(file, newFile)
    config.write(configfile)


packVersion()


# 复制到DEV目录
def copyToDev():
    for rootDir, assetsDirs, files in os.walk(topDir):
        for file in files:
            print("Copying:" + file)
            if os.path.isfile(os.path.join(rootDir, file)):
                relPath = os.path.relpath(os.path.join(rootDir, file), topDir)
                print("原始：" + relPath)
                relPath = os.path.join(devDir, relPath)
                print("新的：" + relPath)
                fileDir = os.path.dirname(relPath)
                print("FileDir:" + fileDir)
                if not os.path.exists(fileDir):
                    os.makedirs(fileDir)
                shutil.copyfile(os.path.join(rootDir, file), relPath)
                print("Copy " + os.path.join(rootDir, file) + " 完成")


copyToDev()


# 提交SVN
def commitSVN():
    print("提交SVN----------------------------------------------")
    if hasSVN:
        os.chdir(devDir)
        os.system("svn add * --force")
        msg = input("请输入SVN日志：\n")
        if (len(msg) <= 1):
            msg = "版本更新，提交测试！"
        os.system("svn commit -m " + msg)
    else:
        input("请手动提交SVN后 <Enter 回车> 继续")


commitSVN()

# 上传FTP
print("上传FTP----------------------------------------------")
ftp.cwd(ftpDir)


def sendFile(allFiles):
    while len(allFiles) > 0:
        uploadfile = allFiles.pop(0)
        print("Uploading:" + uploadfile)
        relPath = os.path.relpath(uploadfile, topDir).replace("\\", "/")
        fileDir = os.path.dirname(relPath)
        if len(fileDir) > 0:
            try:
                ftp.mkd(fileDir)
            except:
                print("Dir is ok!")
        curUploadingFile = open(uploadfile, 'rb')
        ftp.storbinary("STOR " + relPath, curUploadingFile)


def collectFiles():
    allFiles = []
    for rootDir, assetsDirs, files in os.walk(topDir):
        for file in files:
            filePath = os.path.join(topDir, os.path.join(rootDir, file))
            allFiles.append(filePath)
    return allFiles


sendFile(collectFiles())

input("Well done!版本发布完成！ <Enter 回车> 退出")
