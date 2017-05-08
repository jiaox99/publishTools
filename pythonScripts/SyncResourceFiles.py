import VAPublishUtil as VAUtil
import os
import shutil
import EchoItemXML

__author__ = 'Administrator'

IGNORE_DIR_NAMES = ["swffile", "font"]


def collect_update_files():
    """收集有修改的文件列表"""
    scan_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, VAUtil.MAIN_FEATURE_BRANCH, VAUtil.RES_RELEASE_DIR_NAME)
    svn_status_file_path = os.path.join(scan_dir, "svnStatus.txt")
    print("SVNStatusFile->" + svn_status_file_path)
    VAUtil.svn_command("status {} >{}".format(scan_dir, svn_status_file_path))
    file_exist = os.path.exists(svn_status_file_path)
    all_files = []
    print("svnStatus.txt exist status : {}".format(file_exist))
    if file_exist:
        status_file = open(svn_status_file_path)
        for line in status_file:
            file_status = line[0]
            file_path = line[8:len(line)].rstrip()
            if file_status == "!":
                VAUtil.svn_command("rm {}".format(file_path))
            elif file_status == "?" and file_path.find("svnStatus.txt") == -1:
                VAUtil.svn_command("add {}".format(file_path))
            rel_path = os.path.relpath(file_path, scan_dir)
            all_files.append(rel_path)
            print("UpdateFile: {}".format(rel_path))
        status_file.close()
        os.remove(svn_status_file_path)
    return all_files


def sync_resource_files():
    """同步 release 目录资源到其它功能分支
    目前仅支持
    1. 添加、修改、删除文件
    2. 添加、删除文件夹
    """
    feature_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, VAUtil.MAIN_FEATURE_BRANCH)
    EchoItemXML.scan_dir(feature_dir)
    all_files = collect_update_files()
    src_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, VAUtil.MAIN_FEATURE_BRANCH, VAUtil.RES_RELEASE_DIR_NAME)

    for xml_node in VAUtil.PUBLISH_CONFIG_DOC.findall("feature"):
        if xml_node.get("branchDir") != VAUtil.MAIN_FEATURE_BRANCH:
            branch_dir = xml_node.get("branchDir")
            print("sync to feature {}-----------------------------".format(branch_dir))
            dst_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, branch_dir, VAUtil.RES_RELEASE_DIR_NAME)
            print("SyncDstDir:{}".format(dst_dir))
            if not os.path.exists(dst_dir):
                continue
            for update_file in all_files:
                print("Syncing File:{}".format(update_file))
                src_file = os.path.join(src_dir, update_file)
                dst_file = os.path.join(dst_dir, update_file)
                if os.path.exists(src_file):  # 目标文件存在
                    print("Sync {} --> {}".format(src_file, dst_file))
                    if os.path.isdir(src_file):
                        shutil.copytree(src_file, dst_file)
                    else:
                        shutil.copy(src_file, dst_file)
                    VAUtil.svn_command("add {}".format(dst_file))
                elif os.path.exists(dst_file):
                    print("Sync Remove: {}".format(dst_file))
                    if os.path.isdir(dst_file):
                        shutil.rmtree(dst_file)
                    else:
                        os.remove(dst_file)
                    VAUtil.svn_command("rm {}".format(dst_file))
            feature_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, branch_dir)
            EchoItemXML.scan_dir(feature_dir)
            VAUtil.svn_commit(feature_dir, "更新资源", False)
    # 最后提交 release 目录，避免同步失败时丢失更新信息
    feature_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, VAUtil.MAIN_FEATURE_BRANCH)
    VAUtil.svn_commit(feature_dir, "更新资源", False)


if __name__ == '__main__':
    print("开始同步资源")
    VAUtil.try_find_project_root_dir()
    # VAUtil.svn_update(VAUtil.PRE_PUBLISH_ROOT_DIR)
    VAUtil.parse_publish_config()
    sync_resource_files()
    input("同步资源完成")