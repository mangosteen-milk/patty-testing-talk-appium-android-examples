""" 相关视频：https://www.youtube.com/watch?v=cEhUKWZMon4 """

import os
import re
from lxml import etree


def dump_ui_hierarchy():
    cmd1 = 'adb shell uiautomator dump /sdcard/ui_hierchary.xml'
    os.system(cmd1)
    cmd2 = 'adb pull /sdcard/ui_hierchary.xml'
    os.system(cmd2)


def get_xml_root(xml_file):
    tree = etree.parse(xml_file)
    xml_root = tree.getroot()
    return xml_root


def get_element_central_position(element):
    results = re.findall(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', element.attrib['bounds'])
    start_x, start_y, end_x, end_y = [int(item) for item in results[0]]
    return (start_x + end_x)/2, (start_y + end_y)/2


def click_element(element):
    pos_x, pos_y = get_element_central_position(element)
    cmd = f'adb shell input tap {pos_x} {pos_y}'
    os.system(cmd)


def input_text(text):
    cmd = f'adb shell input text {text}'
    os.system(cmd)


if __name__ == '__main__':
    dump_ui_hierarchy()
    root = get_xml_root('ui_hierchary.xml')
    els = root.xpath('//*[@text="搜索设置"]')
    print(f'找到匹配的元素个数：{len(els)}个')
    print(els[0].attrib)
    click_element(els[0])
    input_text('youtube')
