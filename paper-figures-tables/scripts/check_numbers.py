"""数字与来源核对：docx 表里的每个数字，能不能在原始材料里找到。

用途是「抄表」这一步的质量检查——从 PDF、软件输出或截图抄进表格时，
最容易出的是**抄错一位数**、**漏抄一行**、**凭空多一个数**。

**只报「找不到」，不判对错。** 找不到可能因为：来源页码给错、数字被格式化了
（千分位）、或者真的抄错。这几种要人去看。

它抓不到的两件事，必须另外核：
1. **符号**——PDF 文本层常丢负号（本轮复刻里 8 个负号全丢）。所以本脚本会单独报
   「docx 里有负数，来源文本层里却没有负号」，提醒你去看渲染图。
2. **位置**——数字对但放错格子。这一条只能目视。

用法：

    python scripts/check_numbers.py table.docx source.pdf --page 15
    python scripts/check_numbers.py table.docx source.txt --json report.json
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from qc import E, I, W, Finding, print_findings, write_report  # noqa: E402

# 只认「带小数点的数」与「整数」，不认 2022 年这类四位以上无小数的编号？
# 认——AIC 之类的整数也要核。但年份/页码会带来噪声，所以给 --min-digits 让它可调。
# 要能匹配 "-.08" 这种省略前导零的写法（APA 表里到处都是）
NUM = re.compile(r"-?(?:\d+\.\d+|\.\d+|\d+)")


def _norm(tok: str) -> str:
    return tok.replace(",", "").replace("\u2212", "-")


def _abs(tok: str) -> str:
    """比对只用绝对值——PDF 文本层会丢负号，带符号比必然全红。符号另用 sign_warning 交代。"""
    return tok[1:] if tok.startswith("-") else tok


def _tokens(text: str) -> tuple[Counter, int]:
    cnt: Counter = Counter()
    neg = 0
    for raw in NUM.findall(text):
        tok = _norm(raw)
        cnt[_abs(tok)] += 1
        if tok.startswith("-") and float(tok) != 0:
            neg += 1
    return cnt, neg


def docx_numbers(path: Path) -> tuple[Counter, int]:
    """表内数字（多重集）与负数个数。

    合并单元格在 python-docx 的 `row.cells` 里会重复出现（一个 tc 占多列），
    所以按 `w:tc` 逐个取，否则同一个数会被数好几遍——本轮复刻就踩过这个坑。
    """
    from docx import Document
    from docx.oxml.ns import qn
    doc = Document(str(path))
    cnt: Counter = Counter()
    neg = 0
    for t in doc.tables:
        for row in t.rows:
            for tc in row._tr.findall(qn("w:tc")):
                # 按段落取，段间补一个空格：一格多行时直接把 w:t 粘起来
                # 会得到 "0.750.90" 这种假数字
                text = " ".join(
                    "".join(node.text or "" for node in p.iter(qn("w:t")))
                    for p in tc.iter(qn("w:p")))
                sub, sub_neg = _tokens(text)
                cnt += sub
                neg += sub_neg
    return cnt, neg


def source_numbers(path: Path, page: int | None = None,
                   page_end: int | None = None) -> tuple[Counter, int]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        try:
            import pymupdf
        except ImportError:
            raise SystemExit("读 PDF 需要 PyMuPDF：pip install pymupdf\n"
                             "也可以先把来源导出成 .txt 再核。")
        with pymupdf.open(str(path)) as doc:
            lo = (page or 1) - 1
            hi = (page_end or page or len(doc))
            text = "".join(doc[i].get_text() for i in range(lo, min(hi, len(doc))))
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")

    return _tokens(text)


def compare(mine: Counter, src: Counter) -> list[Finding]:
    out: list[Finding] = []
    missing = {k: v - src.get(k, 0) for k, v in mine.items() if v > src.get(k, 0)}
    if missing:
        top = sorted(missing.items(), key=lambda kv: -kv[1])[:12]
        detail = "；".join(f"{k}（多 {v} 次）" for k, v in top)
        out.append(Finding("PFT-QC-002", E,
                           f"{len(missing)} 个数字在来源里找不到或次数更少：{detail}",
                           limit="可能因为页码给错、来源被格式化（千分位）、或真的抄错；"
                                 "本检查只报「找不到」，不判对错"))
    return out


def sign_warning(mine_neg: int, src_neg: int) -> list[Finding]:
    if mine_neg > src_neg:
        return [Finding("PFT-QC-003", W,
                        f"docx 里有 {mine_neg} 个负数，来源文本层只找到 {src_neg} 个负号——"
                        "PDF 文本层常丢负号，请对着渲染图逐个核符号",
                        limit="文本层丢负号时无法机器核对；只能用高 DPI 裁图目视")]
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description="数字与来源核对（只报找不到，不判对错）")
    ap.add_argument("docx")
    ap.add_argument("source")
    ap.add_argument("--page", type=int, help="PDF 起始页（从 1 起）")
    ap.add_argument("--page-end", type=int, help="PDF 结束页")
    ap.add_argument("--json", help="把结论写成 JSON 报告")
    args = ap.parse_args()

    docx_path, src_path = Path(args.docx), Path(args.source)
    for p in (docx_path, src_path):
        if not p.exists():
            print(f"✗ 找不到 {p}")
            return 2

    mine, mine_neg = docx_numbers(docx_path)
    src, src_neg = source_numbers(src_path, args.page, args.page_end)
    findings = compare(mine, src) + sign_warning(mine_neg, src_neg)

    print(f"docx 中数字 {sum(mine.values())} 个（负数 {mine_neg} 个）；"
          f"来源中数字 {sum(src.values())} 个（负号 {src_neg} 个）")
    if not findings:
        print("  ✓ 表内数字都能在来源中找到")
        print("  · 位置（数字对但放错格子）仍需目视核对")
    else:
        print_findings(findings)
    n_err = sum(1 for f in findings if f.severity == E)
    if args.json:
        p = write_report(args.json, findings, targets=[str(docx_path), str(src_path)],
                         tool="paper-figures-tables/check_numbers")
        print(f"报告：{p}")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
