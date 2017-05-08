import ftplib

__author__ = 'Administrator'

import os
import VAPublishUtil as VAUtil


SHEET_DATA_PATH = "release/configfile"
ALL_LANG_ARR = [".td", "_de.td", "_fr.td", "_zh.td", "_tw.td", "_ru.td"]


def pull_and_sync_lang_sheets():
    """拉取并更新 lang.td 等语言包"""
    ftp = VAUtil.prepare_ftp()
    for xml_node in VAUtil.PUBLISH_CONFIG_DOC.findall("feature"):
        feature_dir_name = xml_node.get("branchDir")
        local_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, feature_dir_name, SHEET_DATA_PATH)
        server_dir = "/www/{}/flash/{}".format(feature_dir_name, SHEET_DATA_PATH)
        print(server_dir)
        ftp.cwd(server_dir)
        for lang in ALL_LANG_ARR:
            local_file = os.path.join(local_dir, "lang{}".format(lang))
            try:
                ftp.retrbinary("RETR lang{}".format(lang), open(local_file, "wb").write)
            except ftplib.error_perm:
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!\n拉取多语言sheet出错 --> ftp:://{}/lang{}\n\n\n".format(server_dir, lang))
        VAUtil.svn_commit(local_dir, "更新lang表")


if __name__ == "__main__":
    VAUtil.try_find_project_root_dir()
    VAUtil.parse_publish_config()
    pull_and_sync_lang_sheets()
    input("同步 lang 完成")