#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import html

import io
import pycurl
import sys
import argparse
import re
import codecs

import tokgl


def parse_data(data):
    songs = []

    tree = html.fromstring(data)
    song_nodes = tree.xpath('//table[@class="track_list"]//tr')
    if len(song_nodes):
        for node in song_nodes:
            name_nodes = node.xpath("td[@class='song_name']/a/@title")
            artist_nodes = node.xpath(
                "td[@class='song_name']/a[@class='artist_name']/@title")
            if name_nodes and artist_nodes:
                song_name = name_nodes[0]
                artist_name = u"、".join(artist_nodes)
                info = artist_name + " - " + song_name
                songs.append(info)

    return songs


def get_lib_song(uid):
    buffer = io.BytesIO()

    c = pycurl.Curl()
    #c.setopt(c.VERBOSE, True)
    c.setopt(c.COOKIEFILE, "")
    c.setopt(c.WRITEDATA, buffer)
    # can not be the default user agent, LoL
    c.setopt(
        c.USERAGENT, "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0")

    # must visit this page to get those cookies
    c.setopt(c.URL, "http://www.xiami.com")
    c.perform()

    url = "http://www.xiami.com/space/lib-song/u/{}".format(uid)
    c.setopt(c.URL, url)
    c.perform()

    songs = []
    next_page_exp = re.compile(
        u'<a class="p_redirect_l" href="/space/lib-song/u/[0-9]*/page/[0-9]{1,}">下一页</a>')
    i = 1

    while True:
        # write to stderr to avoid mixing with stdout when no file specify
        sys.stderr.write("正在处理第{}页\r".format(i))
        sys.stderr.flush()

        content = buffer.getvalue()
        # FIXME: detect encoding from header
        content = content.decode("utf-8")
        s = parse_data(content)
        if not s:
            sys.stderr.write("No songs for page {}\n".format(i))
            break
        songs.extend(s)
        i += 1

        if not next_page_exp.search(content):
            break

        next_page = "{}/page/{}".format(url, i)
        buffer.truncate(0)
        buffer.seek(0)
        c.setopt(c.URL, next_page)
        c.perform()

    c.close()

    return songs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("uid", help="虾米用户ID")
    parser.add_argument("file", nargs='?', help="导出到文件，不指定则输出到终端")
    parser.add_argument("-k", "--kgl",
                        action="store_true",
                        help="输出为酷狗音乐列表格式")

    args = parser.parse_args()

    songs = get_lib_song(args.uid)
    if not songs:
        sys.stderr.write("Can't get songs or empty?\n")
        sys.exit(-1)

    output = sys.stdout

    if args.kgl:
        if args.file:
            output = args.file
        # FIXME: python 3 can't use sys.stdout
        tokgl.to_kgl(songs, u"虾米红心", output)
    else:
        if args.file:
            output = codecs.open(args.file, "w+", encoding="utf-8")

        for song in songs:
            output.write(song + "\n")

        if args.file:
            output.close()


if __name__ == "__main__":
    main()


# vim: ai et sta sts=4 sw=4
