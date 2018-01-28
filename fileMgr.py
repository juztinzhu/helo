import web
from pathlib import Path
import json
import re
from datetime import datetime
import random
from functools import partial


def no_comments(text):
    return re.sub(r'\/\*(.*)\*\/', '', text)


class FileMgr:
    map = {}
    conf = {}
    result = {}

    def __init__(self):
        self.conf = json.loads(
            no_comments(
                Path("./static/js/ueditor/php/config.json").read_text()))
        self.map = {'config': self.Config,
                    'uploadimg': partial(
                        self.Upload,
                        self.conf['imagePathFormat'],
                        self.conf['imageMaxSize'],
                        self.conf['imageAllowFiles']),
                    #    /* 上传涂鸦 */    case 'uploadscrawl':
                    #    /* 上传视频 */    case 'uploadvideo':
                    'uploadfile': partial(
                        self.Upload,
                        self.conf['filePathFormat'],
                        self.conf['fileMaxSize'],
                        self.conf['fileAllowFiles']),
                    #    /* 列出图片 */
                    'listimage': self.ListImg,
                    #    /* 列出文件 */
                    'listfile': self.ListFile,
                    #    /* 抓取远程文件 */    case 'catchimage':
                    }

    def getAct(self):
        print(web.input()['action'])
        return web.input()['action']

    def GET(self):
        # print (act)
        return self.map.get(self.getAct(), self.Error)()

    def POST(self):
        return self.map.get(self.getAct(), self.Error)()

    def Error(self):
        print("Error()")
        return ""

    def Config(self):
        # print('self.Config()')
        return Path("./static/js/ueditor/php/config.json").read_text()

    def Upload(self, pathfmt, maxsize, allowExt):
        # upfile
        x = web.input()
        # print(x)
        # pathfmt = self.conf['imagePathFormat']
        print(pathfmt)
        filename = x.name
        self.result['original'] = filename
        size = x.size
        print(size)
        if int(size) > maxsize:
            raise web.NotAcceptable
        # todo: add ext check
        path = self.getFilePath(pathfmt, filename)
        print(path)
        self.saveFile(path, x.upfile)
        self.success()
        return json.dumps(self.result)

    def success(self):
        self.result['state'] = 'SUCCESS'

    def getFileData(self):
        pass

    def getFilePath(self, fmt, filename):
        tm = datetime.now()
        keylist = tm.strftime("%Y-%m-%d-%H-%M-%S-%y").split('-')
        stamp = tm.timestamp()
        fmt = re.sub(r'\{yyyy\}', keylist[0], fmt)
        fmt = re.sub(r'\{mm\}', keylist[1], fmt)
        fmt = re.sub(r'\{dd\}', keylist[2], fmt)
        fmt = re.sub(r'\{hh\}', keylist[3], fmt)
        fmt = re.sub(r'\{ii\}', keylist[4], fmt)
        fmt = re.sub(r'\{ss\}', keylist[5], fmt)
        fmt = re.sub(r'\{yy\}', keylist[6], fmt)
        fmt = re.sub(r'\{time\}', '%d' % stamp, fmt)
        fmt = re.sub(r'\{filename\}', filename, fmt)
        # re.sub(r'\{rand\:(.d)\}'), random.sample())
        self.result['url'] = fmt
        return str(Path.cwd())+fmt

    def saveFile(self, filepath, filedata):
        p = Path(filepath)
        if p.exists():
            raise web.conflict("file already exists!")
        if not p.parent.exists():
            p.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
        self.result['title'] = p.name
        writtenbytes = Path(filepath).write_bytes(filedata)
        if writtenbytes <= 0:
            raise web.internalerror("write_bytes return %d" % writtenbytes)

    def ListFile(self):
        pass

    def ListImg(self):
        pass
