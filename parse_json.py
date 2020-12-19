#!/usr/bin/python

import re
import sys

class my_json_parser:
    # 记录解析错误和结果
    def __init__(self):
        self.isFailed = False
        self.jsonResult = None

    # 判断分割json串的函数
    def isSplitChar(self, char):
        return char in '{}[]:,' or char.isspace()

    # 读取一个整体的字符串
    def readStr(self, index, srcstr, isstr):
        start = index
        end = start + 1
        curchar = ''
        lastchar = ''
        while end < len(srcstr):
            curchar = srcstr[end]
            end += 1
            if isstr and curchar == '"' and lastchar != '\\':
                break
            elif not isstr and self.isSplitChar(curchar):
                end -= 1
                break
            lastchar = curchar

        return srcstr[start:end]

    # 分割json字符串
    def split_json_str(self, srcstr):
        index = 0
        json_list = []
        isStart = False
        tmpstr = ''
        curchar = ''
        while index < len(srcstr):
            curchar = srcstr[index]
            if curchar in '{}[]:,':
                json_list.append(curchar)
                index += 1
            elif curchar.isspace():
                index += 1
            else:
                tmpstr = self.readStr(index, srcstr, curchar == '"')
                json_list.append(tmpstr)
                index += len(tmpstr)

        return json_list

    # 判断一个字符串是否是小数
    def isJsonFloatStr(self, srcstr):
        pattern = '^-?\d+\.?\d*$'
        match = re.match(pattern, srcstr)
        return match != None

    def isJsonStr(self, srcstr):
        if srcstr[0] == '"' and srcstr[len(srcstr) - 1] == '"':
            return True
        return False

    def jsonStrToStr(self, srcstr):
        srcstr = srcstr[1:len(srcstr) - 1]
        srcstr = srcstr.replace('\\"', '"')
        srcstr = srcstr.replace('\\b', '\b')
        srcstr = srcstr.replace('\\f', '\f')
        srcstr = srcstr.replace('\\n', '\n')
        srcstr = srcstr.replace('\\r', '\r')
        srcstr = srcstr.replace('\\t', '\t')
        if sys.version_info < (3, 0):
            return unicode(srcstr)
        else:
            return str(srcstr)

    def parse_json_arr(self, srclist):
        nextIsOther = 0
        nextIsValue = 1
        StrType = nextIsValue
        json_arr = []
        while len(srclist) > 0 and (self.isFailed is False):
            item = srclist.pop(0)
            if item == ',':
                StrType = nextIsValue
            elif item == ']':
                break
            elif StrType == nextIsValue:
                json_arr.append(self.parse_json_value(item, srclist))
                StrType = nextIsOther
            else:
                self.isFailed = True

        return json_arr

    def parse_json_obj(self, srclist):
        json_dict = {}
        nextIsOther = 0
        nextIsKey = 1
        nextIsMaoHao = 2
        nextIsValue = 3
        StrType = nextIsKey
        lastKey = ''
        while len(srclist) > 0 and (self.isFailed is False):
            item = srclist.pop(0)
            if item == ',':
                StrType = nextIsKey
            elif item == '}':
                break
            elif StrType == nextIsKey:
                if not self.isJsonStr(item):
                    self.isFailed = True
                    break
                lastKey = self.jsonStrToStr(item)
                StrType = nextIsMaoHao
            elif StrType == nextIsMaoHao:
                if item != ':':
                    self.isFailed = True
                    break
                StrType = nextIsValue
            elif StrType == nextIsValue:
                json_dict[lastKey] = self.parse_json_value(item, srclist)
                StrType = nextIsOther
            else:
                self.isFailed = True

        return json_dict

    def parse_json_value(self, item, srclist): #字符串, 数字, 对象, 数组, 布尔值或 null
        if self.isJsonStr(item):
            return self.jsonStrToStr(item)
        elif item == "true":
            return True
        elif item == "false":
            return False
        elif item == "null":
            return None
        elif item == '{':
            return self.parse_json_obj(srclist)
        elif item == '[':
            return self.parse_json_arr(srclist)
        elif item.isdigit() or (item[0] == '-' and item[1:].isdigit()):
            return int(item)
        elif self.isJsonFloatStr(item):
            return float(item)
        else:
            self.isFailed = True
            return 'this is err value!'

    # 解析json (成功返回True（可以通过result接口拿到结果）, 失败返回False)
    def parse_json_str(self, srcstr):
        # 先拆分字符串
        srclist = self.split_json_str(srcstr)
        # print(srclist)
        if not srclist:
            return False

        item = srclist.pop(0)
        self.jsonResult = self.parse_json_value(item, srclist)

        if len(srclist) > 0:
            self.isFailed = True

        return not self.isFailed

    def result(self):
        return self.jsonResult

if __name__ == "__main__":
    teststr = '{"stafsdgfsfdfatus": 4, "gameInfodfdfaStatus": 55, "gamefagsfdNamgsfe": "adadafadd", "uifadd": 21355114, "gamfadeIsfgnfo": {}, "_t": 16000262, "pgsfkInfgsfoStatus": 309, "_f": "888ec51d", "pkgsfaIgsfnfo": {"firstBlofadodTime":10,"firstBfadloodOpen":1,"lasgsffadtTime":0, "chestggsfsIgsfngso":{"stggsfatgsfus": 2},"status": 5, "pkTsggfype": 2, "restsMgsVgsgsffSeconds": 3,"ogsfwn_gsbomb_countdown":0, "other_bomb_countdown":30, "competitor": {"streak":3,"mvp": {"player_ccid": 0, "plafadyer_exp": 0, "playfader_head": "", "player_fadauid": 0, "plagfyer_nick": ""}, "pkrankWinner": 0, "uid": 21359580, "top5Users": [], "channelId": 102, "gametype": 65, "cuteid": 19233672, "nick": "Test-1", "pkRes": 2, "score": 457893, "pkrankGrade": -1, "surrender": 0, "roomId": 1292792, "icon": " ortrf017"}, "roundfadadwitch": 1, "pkIdfad": "5f5ed42ff5ffadbb891cc96f062", "self": {"streak":3, "mvp": {"player_fadfccid": 19208364, "playefadar_exp": 1, "playedfadar_head": " 16eae254b2dfadfad36c60e85450LxTX1UKi02", "player_fadfaduid": 21355108, "player_nick": "adfadfad"}, "pkrankfadWinner": 0, "uifadfad": 21355114, "top5Usfadfaders": [{"cafdfaduteid": 19208364, "nickname": "fadfadfad", "ufadfid": 21355108, "exgsfpfad": 1, "pugsfadrl": "eae254b2d36c60e85450LxTX1UKi02"}], "channefadlId": 100368305, "gametfadfaype": 65005, "cuteifadfd": 1917105, "nfadicGk": "a132132132", "pkRefads": 1, "scorfade": 456783, "pkrankGdfadfadrade": -1, "surrefafdfander": 0, "rfadadfaomId": 1288685, "icoffadfadn": "n/1034"}, "restSefadaconds": 28, "giftfadId": 0, "surredfadnderTimes": 1000, "surrendefadarSwitch": 0, "pkadfdTheme": "56f5465465", "addFrfadiengsfdType": 2, "isItfagsdfaemGift": 0, "isHfadfadogsfPk": 0, "pfadungsfishThgsfeme": "adfadfadadfda", "isAgsfnchogsfrfadfFriend": 1}}'
    # teststr = '[1]'
    my_json = my_json_parser()
    print(my_json.parse_json_str(teststr))
    js1 = my_json.result()

    import json
    js2 = json.loads(teststr)
    print(js1==js2)
    print(js1)
    # print(parse_json_str('{"null": null, "name": "xiaoyan", "age": 29, "height": 163.2, "weight": 53.6, "family": {"number": {"sss":111}}, "student":[{"11":11}, 2, 3]}'))