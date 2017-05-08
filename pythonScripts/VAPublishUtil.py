from ftplib import FTP
import io
import binascii
import zlib

__author__ = 'Jiao Zhongxiao'
import os
import sys
from pathlib import Path
import xml.etree.ElementTree as EleTree

# 资源文件目录
RES_RELEASE_DIR_NAME = "release"

# 资源配置文件存储目录
RES_CONFIG_STORE_DIR_NAME = "ver_config"

# 工具链目录
TOOL_DIR_NAME = "bin"

SVN_DIR_NAME = "subversion"

JRE_DIR_NAME = "jre"

# 发布配置文件名
PUBLISH_CONFIG_FILE = "publishConfig.xml"

# 主功能分支
MAIN_FEATURE_BRANCH = "release"

# 发布用的缓存目录名
PUBLISH_TEMP_DIR = "temp"

# 发布目录
PUBLISH_DIR = "publish"

# 预发布项目根目录
PRE_PUBLISH_ROOT_DIR = None


# 发布配置
PUBLISH_CONFIG_DOC = None


def prepare_ftp():
    """准备 FTP"""
    print("准备 FTP")
    ftp = FTP("172.17.5.168", "td-vikingage", "td2015")
    return ftp


def temp_dir():
    """获取真实的缓存目录"""
    # noinspection PyTypeChecker
    return os.path.join(PRE_PUBLISH_ROOT_DIR, PUBLISH_TEMP_DIR)


def compress_file(file_path, com_file_path):
    """压缩文件
    :param file_path: 源文件路径
    :param com_file_path: 压缩后保存文件路径
    """
    fio = io.FileIO(file_path, "r")
    f_data = fio.readall()
    fio.close()

    com_file = zlib.compress(f_data, 9)
    fio = io.FileIO(com_file_path, "w")
    fio.write(com_file)
    fio.close()


def parse_publish_config():
    """解析配置"""
    global PUBLISH_CONFIG_DOC
    if PUBLISH_CONFIG_DOC:
        return PUBLISH_CONFIG_DOC
    try_find_project_root_dir()
    # noinspection PyTypeChecker
    config_file_path = os.path.join(PRE_PUBLISH_ROOT_DIR, TOOL_DIR_NAME, PUBLISH_CONFIG_FILE)
    PUBLISH_CONFIG_DOC = EleTree.parse(config_file_path)
    return PUBLISH_CONFIG_DOC


def try_find_project_root_dir():
    """切换到项目根目录"""
    global PRE_PUBLISH_ROOT_DIR

    if PRE_PUBLISH_ROOT_DIR:
        return PRE_PUBLISH_ROOT_DIR
    path = Path(os.getcwd())
    PRE_PUBLISH_ROOT_DIR = find_project_root_dir(path.parents)
    if PRE_PUBLISH_ROOT_DIR:
        return PRE_PUBLISH_ROOT_DIR
    else:
        path = Path(sys.argv[0])
        PRE_PUBLISH_ROOT_DIR = find_project_root_dir(path.parents)
        if PRE_PUBLISH_ROOT_DIR:
            return PRE_PUBLISH_ROOT_DIR
    print("尝试查找项目根目录失败，请在项目目录中执行相关脚本")
    return False


def find_project_root_dir(path_lists):
    """从所给目录列表中尝试找到项目根目录
    :param path_lists: 要尝试的目录列表
    :return: 如果找到返回相应目录，否则返回 False
    """
    for path in path_lists:
        if check_is_project_root_dir(path):
            str_dir = str(path)
            return str_dir
    return False


def check_is_project_root_dir(test_dir):
    """检查所给目录是否是项目根目录
    :param test_dir: 可能的路径
    """
    publish_config_file = Path(test_dir, TOOL_DIR_NAME, PUBLISH_CONFIG_FILE)
    return publish_config_file.exists()


def read_select_index():
    """读取用户选择的"""
    use_cfg = input("请输入配置标识序号：(e.g. 0)\n")
    return int(use_cfg)


# 打版本
crc32_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
               "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
               "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", ]


def get_crc32_str(crc):
    """获取给定数字的 32 进制表示
    :param crc: 任意整数
    :return: 所给数字的 32 进制表示 e.g. c7hjv98
    """
    crc32 = []
    while crc >= 0:
        res = crc % 32
        crc32.append(crc32_chars[res])
        if crc <= 0 or crc == res:
            break
        else:
            crc = int((crc - res) / 32)
    crc32.reverse()
    return "".join(crc32)


def version_file_with_crc32(file_path, xml_node):
    """将给定文件用 CRC32 重命名
    :param file_path: 文件路径
    :param xml_node: 资源配置中 XML 节点
    """
    ext = os.path.splitext(file_path)[1]
    print("version_file_with_crc32 Processing:" + file_path)
    fio = io.FileIO(file_path, "r")
    f_binary_data = fio.readall()
    fio.close()
    crc = binascii.crc32(f_binary_data) & 0xFFFFFFFF
    crc = get_crc32_str(crc)
    xml_node.set("size", str(os.path.getsize(file_path)))
    xml_node.text = xml_node.text.replace(ext, "_" + crc + ext)
    new_file = file_path.replace(ext, "_" + crc + ext)
    os.replace(file_path, new_file)


def svn_command(command):
    """执行 SVN 命令
    :param command: 要执行的 SVN 命令 e.g. commit -m SomeMessage
    """
    p_root_dir = try_find_project_root_dir()
    svn_exe_file = os.path.join(p_root_dir, TOOL_DIR_NAME, SVN_DIR_NAME, "svn.exe")
    command_str = svn_exe_file + " " + command
    print(command_str)
    os.system(command_str)


def svn_update(dir_path):
    """在指定目录更新 SVN
    :param dir_path: 要更新的目录
    """
    print("更新 SVN -->" + dir_path)
    svn_command("update " + dir_path)


def check_dir(dir_path):
    if os.path.isdir(dir_path):
        return True
    else:
        input("dir_path 不是目录-->" + dir_path)
        return False


def svn_commit(dir_path, msg, auto_add=True):
    """在指定目录提交 SVN
    :param dir_path: 要执行提交的目录
    :param msg: 日志信息
    :param auto_add: 自动检测添加
    """
    print("提交 SVN -->" + dir_path)
    if check_dir(dir_path):
        if auto_add:
            svn_command("add " + dir_path + "/* --force ")
        svn_command("commit -m " + msg + " " + dir_path)


def clear_or_create_dir(dir_path):
    """清理或新建文件夹
    :param dir_path: 路径
    """
    if os.path.exists(dir_path):
        os.system("rd /s /q " + dir_path)
    os.mkdir(dir_path)


def publish_dir():
    """获取真实的发布目录"""
    return os.path.join(try_find_project_root_dir(), PUBLISH_DIR)


if __name__ == "__main__":
    print(try_find_project_root_dir())
    quit()
