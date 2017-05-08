# Author Jiao Zhongxiao
import os
import xml.etree.ElementTree as EleTree
import xml.dom.minidom as mini_dom
import VAPublishUtil as vaUtil
import sys

# XML 配置文件名
XML_FILE_NAME = "config.xml"

# 压缩后的 XML 配置文件名
COM_XML_FILE_NAME = "config.xcom"


def scan_dir(p_root_dir):
    """扫描发布目录下的资源文件并生成配置文件
    :param p_root_dir: 指定目录
    """
    doc_root = EleTree.Element("root")
    top_dir = os.path.join(p_root_dir, vaUtil.RES_RELEASE_DIR_NAME)
    print("开始扫描资源目录:" + top_dir)
    base_dir = os.path.basename(top_dir)
    top_dirs = os.listdir(top_dir)
    for sub_dir in top_dirs:
        if os.path.isdir(os.path.join(top_dir, sub_dir)):
            if sub_dir.find('svn') == -1:
                # 目录元素
                folder_element = doc_root.find(sub_dir)
                if folder_element is None:
                    folder_element = EleTree.Element(sub_dir)
                    cur_dir = base_dir + "/" + sub_dir + "/"
                    folder_element.set('folder', cur_dir)
                    doc_root.append(folder_element)
                cur_dir = os.path.join(top_dir, sub_dir)
                print("当前主子目录:" + cur_dir)
                for root_dir, dirs, assets in os.walk(cur_dir):
                    # 计算当前目录的相对路径
                    cur_dir_rel_path = os.path.relpath(root_dir, cur_dir)
                    if len(assets) > 0:
                        for item in assets:
                            if item.find('svn') == -1\
                                    and item.find('fla') == -1\
                                    and item.find('entries') == -1 and item.find(".db") == -1:
                                info = item.split('.')
                                # 当前文件的相对路径
                                rel_path = os.path.join(cur_dir_rel_path, item)
                                # 去掉可能的 ./ 并转换 win 路径为 linux 风格通用路径
                                rel_path = '/'.join(rel_path.split(os.sep)).replace('./', '')

                                element = EleTree.Element('item')
                                element.set("id", info[0])
                                element.text = rel_path
                                folder_element.append(element)
    special_handle_map_files(doc_root)
    save_to_file(doc_root, p_root_dir)


def special_handle_map_files(doc_root):
    """
    特殊处理 map xml文件
    xml 文件和 jpg 文件在同一个目录，无法区分，手动放到 mapxml 节点下
    :param doc_root: XML 根节点
    """
    print("特殊处理 map xml 文件")
    src_element = doc_root.find('map')
    folder_element = doc_root.find("mapxml")
    if folder_element is None:
        folder_element = EleTree.Element('mapxml')
        doc_root.append(folder_element)
        folder_element.set('folder', src_element.get('folder'))
    xml_and_jpg_items = src_element.findall('item')
    for temp_item in xml_and_jpg_items:
        if temp_item.text.find('.xml') != -1:
            src_element.remove(temp_item)
            folder_element.append(temp_item)
    print("特殊处理 map xml 文件结束")


def save_to_file(doc_root, p_root_dir):
    """写入配置目录
    :param p_root_dir: 根目录
    :param doc_root: XML 根节点
    """
    print("开始写入配置目录")
    doc = mini_dom.parseString(EleTree.tostring(doc_root))
    xml_file_path = os.path.join(p_root_dir, vaUtil.RES_CONFIG_STORE_DIR_NAME, XML_FILE_NAME)
    f_handle = open(xml_file_path, "w")
    f_handle.write(doc.toprettyxml())
    f_handle.close()

    xcom_file_path = os.path.join(p_root_dir, vaUtil.RES_CONFIG_STORE_DIR_NAME,  COM_XML_FILE_NAME)
    vaUtil.compress_file(xml_file_path, xcom_file_path)
    print("写入配置文件结束")


if __name__ == "__main__":
    print('欢迎使用 VA 资源配置导出工具!')
    if len(sys.argv) > 1:
        scan_dir(sys.argv[1])
        print("导出完成")
    else:
        project_root_dir = vaUtil.try_find_project_root_dir()
        if project_root_dir:
            feature_branch = vaUtil.MAIN_FEATURE_BRANCH
            scan_dir(os.path.join(project_root_dir, feature_branch))
            print("导出完成")
    quit()
