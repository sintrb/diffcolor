# -*- coding: UTF-8 -*
from __future__ import print_function
import signal
import time
import sys
import io

__version__ = "0.0.2"


_color_norm = "\033[0m"
_color_ignore = "\033[90m"
_color_diff = "\033[31m"
_color_miss = "\033[32m"
_color_over = "\033[34m"
_color_end = "\033[0m"


def print_title(t, w=40, d="*"):
    l = int((w - len(t)) / 2)
    tl = len(t)
    print("%s %s %s" % (d * l, t, d * (w - tl - l - 1)))


def splits_text(text, splits):
    # 初始化结果列表
    texts = []
    current_word = ""
    i = 0
    while i < len(text):
        found_split = False
        # 检查 splits 中的每个分隔符
        for split in splits:
            if text.startswith(split, i):
                # 如果找到分隔符，先添加当前单词（如果有）
                if current_word:
                    texts.append(current_word)
                    current_word = ""
                # 添加分隔符
                texts.append(split)
                i += len(split)  # 移动索引
                found_split = True
                break
        if not found_split:
            # 如果没有找到分隔符，继续构建当前单词
            current_word += text[i]
            i += 1

    # 添加最后一个单词（如果有）
    if current_word:
        texts.append(current_word)
    return texts


def main(argv=None):
    import argparse

    if argv == None:
        argv = sys.argv
    parser = argparse.ArgumentParser(prog=argv[0], add_help=True)
    parser.add_argument(
        "-f",
        "--follow",
        action="store_true",
        help="output appended data as the file grows",
        default=False,
    )
    parser.add_argument(
        "-e",
        "--end",
        help="the end of the each frame",
        default="\n",
    )
    parser.add_argument(
        "-b",
        "--begin",
        help="the beginning of the each frame",
        default=None,
    )
    parser.add_argument(
        "-s",
        "--split",
        help="split each word, default is space",
        action="append",
        default=[],
    )
    parser.add_argument(
        "-i",
        "--ignore",
        help="ignore not frame character",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show detail output"
    )
    parser.add_argument("file", help="the input files", type=str, nargs="?")
    titlew = 20
    args = parser.parse_args(argv[1:])
    if args.verbose:
        print_title("COLORS define", w=titlew)
        colors = [
            ("NORMAL", _color_norm),
            ("DIFF", _color_diff),
            ("IGNORE", _color_ignore),
            ("MISS", _color_miss),
            ("OVER", _color_over),
        ]
        for c in colors:
            t = "%8s" % c[0]
            print(t, ":", c[1] + c[0] + _color_end)
        print_title("end define", w=titlew)
    splits = [r.encode().decode("unicode_escape") for r in args.split if r]

    if args.file:
        file = io.open(args.file, "r", encoding="utf8")
    else:
        file = sys.stdin
    if args.verbose:
        print("Read data from %s..." % (args.file or "STDIN"))

    begin = args.begin
    end = args.end.encode().decode(
        "unicode_escape"
    )  # replace("\\t", "\t").replace("\\n", "\n")
    cxt = {"lasttm": 0}
    dsegs = []  # 分割数据
    datas = ""  # 第一个数据

    def signal_handler(signal, frame):
        if (time.time() - cxt["lasttm"]) > 3:
            print("")
            print("")
            del dsegs[:]
            cxt["lasttm"] = time.time()
            print("Color reseted!, Ctrl+C again to exit!")
        else:
            print("You pressed Ctrl+C, Exit...")
            exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    follow = args.follow
    status = 0  # 0:wait frame begin, 1:frame body
    datab = ""  # 数据帧缓冲
    headb = ""  # 头缓冲
    while True:
        # ready, _, _ = select.select([sys.stdin], [], [], 1)
        ready = True
        if ready:
            c = file.read(1)
            if not c or len(c) == 0:
                if not follow:
                    break
                time.sleep(0.1)
                continue
        elif not follow:
            break

        if status == 0:
            # 等待头
            if begin:
                headb += c
                if headb.endswith(begin):
                    # 等到了
                    status = 1
                    v = headb[0 : len(headb) - len(begin)]
                    if not args.ignore:
                        print(_color_ignore + v + _color_end, end="")
                    datab = begin
                    headb = ""
                elif len(headb) > len(begin) * 10:
                    v = headb[0 : len(headb) - len(begin)]
                    if not args.ignore:
                        print(_color_ignore + v + _color_end, end="")
                    headb = headb[len(v) :]
            else:
                # 没有头
                status = 1
                datab = c
            # if status == 0 and not args.ignore:
            #     # 未识别，输出
            #     print(_color_ignore + c + _color_end, end="")
        elif status == 1:
            # 等待数据
            datab += c
            if datab.endswith(end):
                # 接收完成，处理帧
                # if begin:
                #     datab = datab[len(datab):]
                status = 0
                misix = len(datab)
                if not dsegs:
                    # 不存在数据模板，需要生成
                    if len(splits):
                        for d in splits_text(datab, splits):
                            if not d:
                                continue
                            dsegs.append(
                                (d, set([d])),
                            )
                    else:
                        dsegs = [(d, set([d])) for d in datab]
                    datas = datab
                elif len(datab) < len(datas):
                    # 数据比目标数据短，补全
                    misix = len(datab) - len(end)
                    datab = (
                        datab[0 : len(datab) - len(end)]
                        + "?" * (len(datas) - len(datab))
                        + end
                    )
                ix = 0
                for d, ds in dsegs:
                    dl = len(d)
                    v = datab[ix : ix + dl]
                    if (ix + dl) > misix:
                        v = _color_miss + v + _color_end
                    else:
                        ds.add(v)
                        if len(ds) > 1:
                            ds.add(v)
                            v = _color_diff + v + _color_end
                        else:
                            v = _color_norm + v + _color_end
                    print(v, end="")
                    ix += dl
                if len(datab) > ix:
                    # 还有数据未完
                    v = datab[ix:]
                    v = _color_over + v + _color_end
                    print(v, end="")
                datab = ""
                headb = ""
    # print("")
    if args.verbose and dsegs:
        # 输出差异
        import math

        print_title("diffs", w=titlew)
        ix = 0
        ln = len(dsegs)
        bw = str(int(math.log10(ln) + 1.0001))
        fmt = "%" + bw + "d"
        for d, ds in dsegs:
            if len(ds) <= 1:
                continue
            print(fmt % ix, d.encode(), ds)
            ix += 1
        print_title("end diffs", w=titlew)
    file.close()


if __name__ == "__main__":
    import sys, io
    main(sys.argv)
