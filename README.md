# Music Exporter

导出各大主流音乐网站歌单到本地

## 支持的列表

- [x] 虾米音乐
- [ ] 网易云音乐
- [ ] QQ音乐
- [ ] 百度音乐


## 使用方法

- 安装依赖

  请先安装python-lxml模块，linux可通过各发行版相应的包管理安装，Windows可通过pip安装（python -m pip install lxml）

- 虾米音乐

  运行xme.py脚本，传入你的虾米音乐ID，导出到本地文件的路径（不指定则输出在终端）

  比如 python xme.py 12345 myfav.txt

  如需要输出为酷狗音乐列表格式，请加上-k参数

## 导出格式

艺人1 - 歌名1

艺人1、艺人2 - 歌名2

艺人n - 歌名n
