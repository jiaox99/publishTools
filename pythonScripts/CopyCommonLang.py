__author__ = 'Administrator'

import VAPublishUtil as VAUtil
import os
import shutil


def copy_common_lang_files():
    """拷贝多语言导出文件到功能分支目录"""
    all_files = []
    src_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, VAUtil.TOOL_DIR_NAME)
    # 收集
    for file in os.listdir(src_dir):
        if os.path.isfile(file) and "commonLang" in file:
            print(file)
            all_files.append(file)
    # 同步
    pub_cfg = VAUtil.parse_publish_config()
    common_lang_dir = "release/configfile/textConfig/panel_config"
    for xml_node in pub_cfg.findall("feature"):
        dst_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, xml_node.get("branchDir"), common_lang_dir)
        if os.path.exists(dst_dir):
            for file in all_files:
                src = os.path.join(src_dir, file)
                dst = os.path.join(dst_dir, file)
                shutil.copy(src, dst)
            VAUtil.svn_commit(dst_dir, "更新多语言")
    # 清理
    for file in all_files:
        src = os.path.join(src_dir, file)
        os.remove(src)

if __name__ == '__main__':
    print("开始拷贝资源")
    VAUtil.try_find_project_root_dir()
    copy_common_lang_files()
    print("拷贝结束")