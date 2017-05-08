import VAPublishUtil as VAUtil
import EchoItemXML
import os


__author__ = 'Administrator'


def echo_all():
    """重新生成所有版本的配置文件"""
    for xml_node in VAUtil.PUBLISH_CONFIG_DOC.findall("feature"):
        branch_dir = xml_node.get("branchDir")
        feature_dir = os.path.join(VAUtil.PRE_PUBLISH_ROOT_DIR, branch_dir)
        EchoItemXML.scan_dir(feature_dir)
        config_dir = os.path.join(feature_dir, VAUtil.RES_CONFIG_STORE_DIR_NAME)
        VAUtil.svn_commit(config_dir, "更新资源")


if __name__ == "__main__":
    VAUtil.try_find_project_root_dir()
    VAUtil.parse_publish_config()
    echo_all()
    input("重新生成所有版本的配置文件结束")