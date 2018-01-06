# -*- coding: utf-8 -*-

from lxml import etree

import argparse
import codecs


def to_kgl(songs, name, output):
    root = etree.Element("List", ListName=name)
    for song in songs:
        songname = song + ".mp3"
        file_node = etree.SubElement(root, "File")
        name_node = etree.SubElement(file_node, "FileName")
        name_node.text = songname

    etree.ElementTree(root).write(output,
                                  xml_declaration=True,
                                  encoding="utf8",
                                  pretty_print=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="歌单列表文件")
    parser.add_argument("name", help="歌单名称")
    parser.add_argument("out", help="输出文件")

    args = parser.parse_args()
    songs = []
    with codecs.open(args.file, "r", encoding="utf-8") as f:
        for line in f:
            songs.append(line.rstrip("\n"))

    to_kgl(songs, args.name, args.out)
