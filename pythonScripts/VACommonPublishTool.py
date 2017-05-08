from ftplib import FTP
import ftplib
import os
import xml.etree.ElementTree as EleTree
import VAPublishUtil as VAUtil
import shutil
import EchoItemXML

__author__ = 'Jiao Zhongxiao'


# 选择的功能分支
FEATURE_BRANCH = None


# 确认的版本号
VERSION_NUM = None

ASSET_EXT = ".json,.jpg,.png,.swf,.xml,.mp3,.wdp,.xcom"
IGNORE_EXT = ".xcom"
IGNORE_FILES = ["towerDefenseFight", "PvpPlayerPanel", "commonLang_config"]


def print_branch_select_menu():
    """展示功能分支选择菜单"""
    publish_config = VAUtil.parse_publish_config()
    print("可以发布的功能分支：")
    i = 0
    for feature_node in publish_config.findall("feature"):
        print(str(i) + ": " + feature_node.get("name"))
        i += 1


def publish_feature_branch():
    """发布指定功能分支"""
    print("开始发布功能分支: --> " + FEATURE_BRANCH)
    publish_dir = VAUtil.publish_dir()
    # 更新 config.xml
    EchoItemXML.scan_dir(os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, FEATURE_BRANCH))
    # 拷贝到临时目录
    copy_file_to_temp_dir()
    # 打版本
    version_files()
    # 同步到发布目录
    # sync_to_publish_dir()
    # 提交 SVN
    # VAUtil.svn_commit(publish_dir, "版本更新" + VERSION_NUM)
    # 同步 FTP
    sync_to_ftp(collect_files())
    input("版本发布完成")


def sync_to_ftp(all_files):
    """上传到 FTP"""
    ftp = VAUtil.prepare_ftp()
    ftp_dir = "/www/" + FEATURE_BRANCH + "/flash"
    ftp.cwd(ftp_dir)
    temp_dir = VAUtil.temp_dir()
    while len(all_files) > 0:
        upload_file = all_files.pop(0)
        print("Uploading:" + upload_file)
        rel_path = os.path.relpath(upload_file, temp_dir).replace("\\", "/")
        file_dir = os.path.dirname(rel_path)
        if len(file_dir) > 0:
            print("创建目录" + file_dir)
            try:
                ftp.mkd(file_dir)
            except ftplib.error_perm:
                print("目录已经存在")
        cur_uploading_file = open(upload_file, 'rb')
        ftp.storbinary("STOR " + rel_path, cur_uploading_file)


def collect_files():
    """收集要同步的文件"""
    temp_dir = VAUtil.temp_dir()
    all_files = []
    for rootDir, assetsDirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(temp_dir, os.path.join(rootDir, file))
            all_files.append(file_path)
    return all_files


def sync_to_publish_dir():
    """复制到发布目录"""
    temp_dir = VAUtil.temp_dir()
    publish_dir = VAUtil.publish_dir()
    for rootDir, assetsDirs, files in os.walk(temp_dir):
        for file in files:
            print("Copying:" + file)
            if os.path.isfile(os.path.join(rootDir, file)):
                rel_path = os.path.relpath(os.path.join(rootDir, file), temp_dir)
                print("原始：" + rel_path)
                rel_path = os.path.join(publish_dir, rel_path)
                print("新的：" + rel_path)
                file_dir = os.path.dirname(rel_path)
                print("FileDir:" + file_dir)
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                shutil.copyfile(os.path.join(rootDir, file), rel_path)
                print("Copy " + os.path.join(rootDir, file) + " 完成")


def copy_file_to_temp_dir():
    """将相关资源拷贝到临时目录"""
    temp_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, VAUtil.PUBLISH_TEMP_DIR)
    source_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, FEATURE_BRANCH)
    print("拷贝资源到缓存目录:\nsourceDir:->" + temp_dir + "\n缓存目录" + temp_dir)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)
    wrapper_file = "wrapper.swf"
    # wrapper.swf
    src = os.path.join(source_dir, wrapper_file)
    dst = os.path.join(temp_dir, wrapper_file)
    shutil.copy(src, dst)
    # release & ver_config
    dirs = [VAUtil.RES_RELEASE_DIR_NAME, VAUtil.RES_CONFIG_STORE_DIR_NAME]
    for copy_dir in dirs:
        src = os.path.join(source_dir, copy_dir)
        dst = os.path.join(temp_dir, copy_dir)
        copy_files(src, dst)
    print("拷贝资源完成")


def copy_files(src_dir, dst_dir):
    """拷贝项目认可的资源文件"""
    for root_dir, assets_dirs, files in os.walk(src_dir):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext != "" and ASSET_EXT.find(ext) != -1:
                # 相对路径
                rel_path = os.path.relpath(os.path.join(root_dir, file), src_dir)
                print("原始：" + rel_path)
                dst_path = os.path.join(dst_dir, rel_path)
                print("新的：" + dst_path)
                file_dir = os.path.dirname(dst_path)
                print("FileDir:" + file_dir)
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                shutil.copyfile(os.path.join(root_dir, file), dst_path)
                print("Copy " + os.path.join(root_dir, file) + " 完成")


def check_is_ignore_file(file_name):
    """检查是否是是接加版本号的文件"""
    for ignore_file in IGNORE_FILES:
        if file_name.find(ignore_file) != -1:
            return True
    return False


def version_file_with_ver_num(file_path, xml_node):
    """将文件直接加上版本号"""
    ext = os.path.splitext(file_path)[1]
    print("尝试将文件直接加上版本号 Processing:" + file_path)
    if IGNORE_EXT.find(ext) != -1 or check_is_ignore_file(xml_node.get("id")):
        crc = VERSION_NUM
        xml_node.set("size", str(os.path.getsize(file_path)))
        xml_node.text = xml_node.text.replace(ext, "_" + crc + ext)
        new_file = file_path.replace(ext, "_" + crc + ext)
        os.replace(file_path, new_file)
        return True
    else:
        return False


def version_dir_with_ver_num(work_dir):
    """将目录下的文件直接加上版本号"""
    files = os.listdir(work_dir)
    for file in files:
        old_file = os.path.join(work_dir, file)
        is_file = os.path.isfile(old_file)
        print(old_file + "---" + str(is_file))
        if is_file:
            ext = os.path.splitext(file)[1]
            new_file = old_file.replace(ext, "_" + str(VERSION_NUM) + ext)
            print("重命名：" + old_file + "<>" + new_file)
            os.replace(old_file, new_file)


def res_config_file_path():
    """获取当前的资源配置路径"""
    return os.path.join(VAUtil.temp_dir(), VAUtil.RES_CONFIG_STORE_DIR_NAME, EchoItemXML.XML_FILE_NAME)


def com_res_config_file_path():
    """获取当前的资源配置压缩路径"""
    return os.path.join(VAUtil.temp_dir(), VAUtil.RES_CONFIG_STORE_DIR_NAME, EchoItemXML.COM_XML_FILE_NAME)


def version_file_with_crc32():
    """根据文件的 CRC32 校验加版本号"""
    temp_dir = VAUtil.temp_dir()
    config_file = res_config_file_path()
    config = EleTree.parse(config_file)
    root = config.getroot()
    for folderElement in root:
        folder = folderElement.get("folder")
        for item in folderElement:
            file = os.path.join(temp_dir, folder, item.text)
            if os.path.exists(file):
                if not version_file_with_ver_num(file, item):
                    VAUtil.version_file_with_crc32(file, item)
    config.write(config_file)
    VAUtil.compress_file(config_file, com_res_config_file_path())


def version_files():
    """给所有文件加上相应的版本后缀"""
    print("开始给所有文件加上版本后缀")
    root_dir = VAUtil.temp_dir()
    # 主目录 wrapper.swf
    version_dir_with_ver_num(root_dir)
    # release 目录
    version_file_with_crc32()
    # ver_config 目录
    version_dir_with_ver_num(os.path.join(root_dir, VAUtil.RES_CONFIG_STORE_DIR_NAME))


def feature_test():
    p_root_dir = VAUtil.try_find_project_root_dir()
    if p_root_dir:
        # 更新 SVN
        VAUtil.svn_update(p_root_dir)
        p_config = VAUtil.parse_publish_config()
        # 展示菜单
        print_branch_select_menu()
        # 读取选项
        select_i = VAUtil.read_select_index()
        # 设置发布分支
        global FEATURE_BRANCH
        FEATURE_BRANCH = p_config.findall("feature")[select_i].get("branchDir")
        global VERSION_NUM
        # 确认发布版本号
        if select_i < 0:
            VERSION_NUM = str(select_i)
        else:
            VERSION_NUM = input("确认发布版本号:\n")
        publish_feature_branch()


if __name__ == "__main__":
    feature_test()
