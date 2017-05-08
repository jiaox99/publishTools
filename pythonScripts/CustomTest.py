__author__ = 'Administrator'
import VAPublishUtil as VAUtil
import VACommonPublishTool as CommonTool
import EchoItemXML
import SyncResourceFiles as SyncRes


# VAUtil.clear_or_create_dir("e:\\temp\GitTreeTest")
# CommonTool.publish_feature_branch("e:\\workspace\\PrePublish\\trunk", "test002")
# EchoItemXML.scan_dir("e:\\workspace\\PrePublish\\trunk\\release")
VAUtil.try_find_project_root_dir()
VAUtil.parse_publish_config()
# CommonTool.FEATURE_BRANCH = "release"
# ftp = CommonTool.prepare_ftp()
# CommonTool.sync_to_ftp(CommonTool.collect_files())
SyncRes.sync_resource_files()
