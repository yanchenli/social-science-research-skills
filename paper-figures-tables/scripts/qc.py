"""检查结论的统一形式：一条 finding = 代码 + 严重度 + 说明 + 局限。

为什么要有这个文件
------------------
原来检查器只打印中文句子。句子适合人读，不适合**比对**：
这次报了 7 条、上次 5 条，是哪两条消失了？换个学生重跑，同一条问题会不会换个说法？
把结论写成 (code, severity, message, limit)，就能存成 JSON、能 diff、能按代码统计。

`Finding` 继承 `str`，所以 `"；".join(errs)`、`if not errs` 这些老写法全部照旧——
不需要把调用方全部改一遍。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

E = "error"      # 必须改，否则印刷/投稿会出问题
W = "warn"       # 应当核对，可能是规范差异而非错误
I = "info"       # 没查或查不了，如实交代


def skill_version() -> str:
    """从 SKILL.md 的 frontmatter 读版本号——版本只有一处，避免报告里写另一个数。"""
    try:
        text = (Path(__file__).resolve().parent.parent / "SKILL.md").read_text(encoding="utf-8")
        m = re.search(r"^version:\s*(\S+)", text, re.M)
        return m.group(1) if m else ""
    except OSError:
        return ""


def load_spec(path, required=()):
    """读一个规格 JSON，三种常见手误都给出能照着改的一句话，而不是二十行栈。

    文件名打错、JSON 少个引号、忘了写 `columns`——这三件事占了用户第一次使用时
    的绝大多数失败，不该让它们看到 traceback。
    """
    p = Path(str(path))
    if not p.exists():
        raise SystemExit(f"找不到规格文件：{p}\n"
                         f"用法：python scripts/{_caller()} 规格.json 输出\n"
                         f"现成的例子在 assets/table_specs/ 与 references/ 里。")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"{p.name} 不是有效的 JSON：第 {e.lineno} 行第 {e.colno} 列，{e.msg}\n"
                         "常见原因：用了中文引号、末尾多一个逗号、少了括号。") from None
    if not isinstance(data, dict):
        raise SystemExit(f"{p.name} 的顶层应当是一个对象（{{…}}），实际是 {type(data).__name__}")
    missing = [k for k in required if k not in data]
    if missing:
        raise SystemExit(f"{p.name} 缺必填字段：{', '.join(missing)}\n"
                         f"已有的字段：{', '.join(sorted(data)) or '（空）'}")
    return data


def _caller() -> str:
    """报错里指出是哪个脚本——同一句话要能直接复制去跑。"""
    import sys
    return Path(sys.argv[0]).name if sys.argv and sys.argv[0] else "make_table.py"


class Finding(str):
    """一条结论。字符串内容是给人看的句子，附带机器可读的代码与局限。"""

    def __new__(cls, code: str, severity: str, message: str, limit: str = ""):
        obj = super().__new__(cls, message)
        obj.code = code
        obj.severity = severity
        obj.limit = limit
        return obj

    def as_dict(self, target: str = "") -> dict:
        return {"code": self.code, "severity": self.severity,
                "message": str(self), "limit": self.limit,
                **({"target": target} if target else {})}


def collect(*groups) -> list[Finding]:
    """把多组结果拼起来，过滤掉非 Finding 的（例如旧代码返回的普通字符串）。"""
    out: list[Finding] = []
    for g in groups:
        for f in g or []:
            out.append(f if isinstance(f, Finding) else Finding("PFT-GEN-000", W, str(f)))
    return out


def write_report(path: str | Path, findings, *, targets=None, tool="paper-figures-tables",
                 version: str = "", extra: dict | None = None) -> Path:
    """写一份 JSON 报告。

    固定不含时间戳——同一批文件重复跑，报告必须逐字节相同，否则无法用 diff 判断
    「这次改好了没有」。需要时间戳时由调用方塞进 extra。
    """
    findings = collect(findings)
    errors = [f for f in findings if f.severity == E]
    warns = [f for f in findings if f.severity == W]
    skipped = [f for f in findings if f.severity == I]
    report = {
        "report_version": "1.0",
        "tool": tool,
        "tool_version": version or skill_version(),
        "targets": list(targets or []),
        "summary": {"error": len(errors), "warn": len(warns), "info": len(skipped),
                    "total": len(findings)},
        # 本工具不构成期刊合规认证。这一句写进报告本体，而不是只写在文档里。
        "publication_ready_claim": False,
        "claim_note": "本报告只覆盖规则目录里列明的自动检查项；"
                      "PASS 不等于符合目标期刊或学校的全部要求。",
        "findings": [f.as_dict() for f in findings],
        **(extra or {}),
    }
    p = Path(path)
    p.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")
    return p


def print_findings(findings) -> tuple[int, int]:
    """按严重度分组打印，返回 (错误数, 警告数)。"""
    findings = collect(findings)
    errs = [f for f in findings if f.severity == E]
    warns = [f for f in findings if f.severity == W]
    infos = [f for f in findings if f.severity == I]
    for f in errs:
        print(f"  ✗ [{f.code}] {f}")
    for f in warns:
        print(f"  ! [{f.code}] {f}")
    for f in infos:
        print(f"  · [{f.code}] {f}")
    return len(errs), len(warns)
