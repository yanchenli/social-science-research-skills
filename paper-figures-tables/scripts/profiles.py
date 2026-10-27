"""版式 profile：目标期刊或学校要求的一组取值，带出处、状态与未决事项。

为什么要从代码里搬出来
----------------------
原来三档格式是 `PRESETS` 里的三个字典。它们能跑，但答不了三个问题：
**这个值是哪来的？** **规范里没写的那些，现在用的是什么？** **哪些要求工具做不到？**
把取值放进 `assets/profiles/*.json` 之后，这三个问题都能在文件里回答，
生成与检查也读同一份规则——不会出现「生成按 APA、检查按另一套」。

状态决定提醒方式（`STATUS`）：
  documented  规则有原文出处，不提醒
  convention  通行做法，提醒「投稿前核对」
  observed    从已发表版式反推，提醒
  template    未填写的模板，警告
  simulated   虚构规范，警告「不可用于真实提交」
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

PROFILE_DIR = Path(__file__).resolve().parent.parent / "assets" / "profiles"

# 旧写法兼容：`format: "zh"` 仍可用
ALIASES = {"zh": "zh-journal", "apa": "apa7"}

STATUS_NOTICE = {
    "documented": "",
    "convention": "通行做法，未见规范原文；投稿前请核对目标期刊或学校的要求",
    "observed": "依据已发表版式反推，投稿要求未核对",
    "template": "未填写的模板：版式细节未经核对，请对照规范原文确认后再用",
    "simulated": "依据虚构规范建立，仅用于测试，不可用于真实投稿",
}

# 所有可用字段。写错字段名会被拒绝——静默忽略拼错的键，是这类工具最坏的行为。
TABLE_KEYS = {
    "font", "size", "title_font", "number_bold", "title_italic", "title_align",
    "title_on_separate_line", "header_bold", "header_align",
    "rule_top", "rule_header", "rule_bottom",
    "note_prefix", "note_italic_prefix", "note_size",
    "leading_zero", "cell_pad", "first_col_align",
}
FIGURE_KEYS = {
    "caption_position", "min_text_pt", "max_text_pt", "width_in",
    "min_dpi", "font_family",
}
PAGE_KEYS = {"size", "margins_in"}
TOP_KEYS = {
    "profile_id", "label", "status", "language", "source", "source_clauses",
    "verified_on", "table", "figure", "page",
    "pending_confirmation", "unsupported", "manual_checks", "unspecified_defaults",
    "notes", "_todo",
}

# 兜底默认值 = APA 7。任何 profile 只要覆盖需要改的项。
BASE_TABLE = dict(
    font="Times New Roman", size=10.5, title_font="Times New Roman",
    number_bold=True, title_italic=True, title_align="left",
    title_on_separate_line=True, header_bold=False, header_align="center",
    rule_top=8, rule_header=4, rule_bottom=8,
    note_prefix="Note.", note_italic_prefix=True, note_size=9.5,
    leading_zero=False, cell_pad=3.0, first_col_align="left",
)
BASE_FIGURE = dict(
    caption_position="above", min_text_pt=8.0, max_text_pt=14.0,
    width_in=6.5, min_dpi=300, font_family="sans",
)
# 页面尺寸（英寸）。版心宽 = 页宽 − 左右边距；横向页则是页高 − 左右边距。
PAGE_SIZES = {"letter": (8.5, 11.0), "a4": (8.27, 11.69)}
BASE_PAGE = dict(size="letter", margins_in=[1.0, 1.0, 1.0, 1.0])   # 上 右 下 左

_WARNED: set[str] = set()


def list_profiles() -> list[str]:
    return sorted(p.stem for p in PROFILE_DIR.glob("*.json"))


def validate(prof: dict) -> list[str]:
    """返回问题清单。空列表表示可用。"""
    errs: list[str] = []
    unknown = set(prof) - TOP_KEYS
    if unknown:
        errs.append(f"未知的顶层字段：{sorted(unknown)}；可用：{sorted(TOP_KEYS)}")
    for section, keys in (("table", TABLE_KEYS), ("figure", FIGURE_KEYS),
                          ("page", PAGE_KEYS)):
        obj = prof.get(section)
        if obj is None:
            continue
        if not isinstance(obj, dict):
            errs.append(f"{section} 必须是对象")
            continue
        bad = set(obj) - keys
        if bad:
            errs.append(f"{section} 里有未知字段：{sorted(bad)}；可用：{sorted(keys)}")
    page = prof.get("page")
    if isinstance(page, dict):
        size = page.get("size", "letter")
        if size not in PAGE_SIZES:
            errs.append(f"page.size 只能是 {sorted(PAGE_SIZES)}，收到 {size!r}")
        m = page.get("margins_in")
        if m is not None and (not isinstance(m, list) or len(m) != 4):
            errs.append("page.margins_in 必须是 4 个数：上 右 下 左（英寸）")
    status = prof.get("status", "documented")
    if status not in STATUS_NOTICE:
        errs.append(f"status 只能是 {sorted(STATUS_NOTICE)}，收到 {status!r}")
    return errs


def load(ref: str | None = None, overrides: dict | None = None,
         quiet: bool = False) -> dict:
    """读一个 profile，合并覆盖项，返回 {table:…, figure:…, …元信息}。

    ref 可以是内置名（`apa7`）、旧别名（`zh`）或 .json 路径。
    """
    ref = (ref or "apa7").strip()
    ref = ALIASES.get(ref, ref)
    path = Path(ref) if ref.endswith(".json") else PROFILE_DIR / f"{ref}.json"
    if not path.exists():
        raise SystemExit(
            f"找不到 profile：{ref}\n"
            f"内置的有：{', '.join(list_profiles())}\n"
            f"也可以给 .json 路径（例如学校规范的提取结果）")
    raw = json.loads(path.read_text(encoding="utf-8"))
    errs = validate(raw)
    if errs:
        raise SystemExit(f"profile {path.name} 有问题：\n  - " + "\n  - ".join(errs))

    prof = copy.deepcopy(raw)
    prof.setdefault("profile_id", path.stem)
    prof.setdefault("status", "documented")
    prof["table"] = {**BASE_TABLE, **(raw.get("table") or {})}
    prof["figure"] = {**BASE_FIGURE, **(raw.get("figure") or {})}
    prof["page"] = {**BASE_PAGE, **(raw.get("page") or {})}
    if overrides:
        bad = set(overrides) - TABLE_KEYS
        if bad:
            raise SystemExit(f"style 里有未知字段：{sorted(bad)}\n"
                             f"可用：{sorted(TABLE_KEYS)}")
        prof["table"].update({k: v for k, v in overrides.items() if k in TABLE_KEYS})

    if not quiet:
        _announce(prof)
    return prof


def page_pt(prof: dict, landscape: bool = False) -> tuple[float, float]:
    """返回 (页宽, 页高)，单位 pt。横向时把两者对调。"""
    w_in, h_in = PAGE_SIZES[prof["page"].get("size", "letter")]
    if landscape:
        w_in, h_in = h_in, w_in
    return w_in * 72.0, h_in * 72.0


def text_width_pt(prof: dict, landscape: bool = False) -> float:
    """版心宽（pt）——表最多能占多宽。"""
    w, _ = page_pt(prof, landscape)
    _top, right, _bottom, left = prof["page"].get("margins_in", [1, 1, 1, 1])
    return w - (left + right) * 72.0


def _announce(prof: dict) -> None:
    """把状态与未决事项打到 stderr。每个 profile 每次运行只提醒一次。

    这些提示不能只在文档里写一遍就算交代过了——用了 `template` 状态的
    profile 却没看见提醒，是这类工具最容易造成的误用。
    """
    pid = prof.get("profile_id", "?")
    if pid in _WARNED:
        return
    _WARNED.add(pid)
    notice = STATUS_NOTICE.get(prof.get("status", "documented"), "")
    if notice:
        print(f"[profile:{pid}] {prof.get('status')}——{notice}", file=sys.stderr)
    for item in prof.get("pending_confirmation") or []:
        print(f"[profile:{pid}·待确认] {item.get('clause', '')}：{item.get('question', '')}"
              f"（当前暂按：{item.get('provisional', '未定')}）", file=sys.stderr)
    for item in prof.get("unsupported") or []:
        print(f"[profile:{pid}·做不到] {item.get('clause', '')}：{item.get('what', '')}"
              f"（处理：{item.get('handling', '需手工处理')}）", file=sys.stderr)
    if prof.get("manual_checks"):
        print(f"[profile:{pid}] 另有 {len(prof['manual_checks'])} 条需人工核对，"
              f"见 profile 的 manual_checks 字段", file=sys.stderr)


def print_profiles() -> int:
    print(f"内置 profile（{PROFILE_DIR}）\n")
    for name in list_profiles():
        raw = json.loads((PROFILE_DIR / f"{name}.json").read_text(encoding="utf-8"))
        status = raw.get("status", "documented")
        flag = {"documented": "✓", "convention": "·", "observed": "·",
                "template": "!", "simulated": "!"}.get(status, "?")
        print(f" {flag} {name:16} {status:11} {raw.get('label', '')}")
        if raw.get("source"):
            print(f"     出处：{raw['source']}")
        todo = raw.get("_todo")
        if todo:
            print(f"     待填：{len(todo)} 项")
    print("\n✓ 有出处  · 需核对  ! 不可直接用于投稿")
    return 0


if __name__ == "__main__":
    raise SystemExit(print_profiles())
