"""文本宽度的估算：生成时定列宽，检查时验列宽——两边必须用同一份。

原来的实现一律按 0.55 em 估，把拉丁文高估约三成。后果不只是「列有点松」：
标签列虚胖会把数据列挤到装不下一个单词，Word 就从词中间断开
（实测 `Relational` 被断成 `Relationa / l`）。所以这里按 Times New Roman
的真实字宽表算，误差控制在 5% 以内。
"""
from __future__ import annotations

import re

TAG_RE = re.compile(r"</?(?:i|b|sup|sub)>")
WIDTH_SLACK = 1.06          # 实际渲染字距有波动，留 6% 余量

_ADV: dict[str, int] = {}
for _chars, _w in [
    (" ", 250), ("!", 333), ('"', 408), ("#", 500), ("$", 500), ("%", 833),
    ("&", 778), ("'", 333), ("(", 333), (")", 333), ("*", 500), ("+", 564),
    (",", 250), ("-", 333), (".", 250), ("/", 278), (":", 278), (";", 278),
    ("<", 564), ("=", 564), (">", 564), ("?", 444), ("@", 921), ("[", 333),
    ("\\", 278), ("]", 333), ("^", 469), ("_", 500), ("`", 333), ("{", 480),
    ("|", 200), ("}", 480), ("~", 541),
    ("0123456789", 500),
]:
    for _c in _chars:
        _ADV[_c] = _w

for _c, _w in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                  [722, 667, 667, 722, 611, 556, 722, 722, 333, 389, 722, 611, 889,
                   722, 722, 556, 722, 667, 556, 611, 722, 722, 944, 722, 722, 611]):
    _ADV[_c] = _w
for _c, _w in zip("abcdefghijklmnopqrstuvwxyz",
                  [444, 500, 444, 500, 444, 333, 500, 500, 278, 278, 500, 278, 778,
                   500, 500, 500, 500, 333, 389, 278, 500, 500, 722, 500, 500, 444]):
    _ADV[_c] = _w
for _c, _w in [("\u2014", 1000), ("\u2013", 500), ("\u2212", 564), ("\u00d7", 564),
               ("\u2192", 1000), ("\u2019", 333), ("\u2018", 333), ("\u201c", 500),
               ("\u201d", 500), ("\u2022", 350), ("\u2026", 1000), ("\u03b1", 494),
               ("\u03b2", 500), ("\u03c7", 444), ("\u03bb", 500), ("\u03c3", 500),
               ("\u2264", 564), ("\u2265", 564), ("\u00b1", 564), ("\u2032", 333)]:
    _ADV[_c] = _w


def strip_tags(s) -> str:
    return TAG_RE.sub("", str(s))


def text_width(s: str, size: float) -> float:
    """估算一行文本的宽度（pt）。中日韩字符按 1 em，未登记符号按 0.5 em 兜底。"""
    em = 0.0
    for ch in str(s):
        if ord(ch) > 0x2E7F and not (0x2000 <= ord(ch) <= 0x206F):
            em += 1.0
        else:
            em += _ADV.get(ch, 500) / 1000.0
    return em * size * WIDTH_SLACK


def _segments(s: str) -> list[str]:
    """把文本切成「不可再分的最小片段」。

    拉丁文按空格断词；**中日韩文字可以在任意两字之间折行**，所以每个汉字
    自成一段——否则「信度与收敛效度」会被当成一个 7 字长词，逼着列宽放到
    67 pt，反而把表撑坏。
    """
    out: list[str] = []
    buf: list[str] = []

    def flush():
        if buf:
            out.append("".join(buf))
            buf.clear()

    for ch in strip_tags(s).replace("\u2192", " "):
        if ch.isspace():
            flush()
        elif ord(ch) > 0x2E7F and not (0x2000 <= ord(ch) <= 0x206F):
            flush()
            out.append(ch)
        else:
            buf.append(ch)
    flush()
    return out


def word_min_width(s: str, size: float) -> float:
    """单元格的硬下限：不可再分的最长片段必须放得下。

    Word 在单元格窄于单词时会从词中间断开。折行是排版差异，断词是缺陷——
    读者会把它当成拼写错误。箭头 `→` 两侧允许断行，汉字之间也可以。
    """
    return max([text_width(w, size) for w in _segments(s)] + [0.0])
