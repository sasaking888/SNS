#!/usr/bin/env python3
"""全部門ダッシュボード生成スクリプト。

`.company/` 配下の各部門フォルダを走査し、成果物のステータス・TODO・
最終更新（git）を集計して、次の2ファイルを生成する。

- `.company/dashboard/dashboard.md`   … GitHubアプリ（スマホ）で見る用
- `.company/dashboard/dashboard.html` … ブラウザで見るカード型ダッシュボード

実行: `python3 .company/dashboard/generate.py`（リポジトリのどこからでも可）
"""

import html
import re
import subprocess
from datetime import datetime
from pathlib import Path

COMPANY = Path(__file__).resolve().parent.parent
ROOT = COMPANY.parent
OUT_DIR = Path(__file__).resolve().parent

# 部門定義: (フォルダ名, 表示名, 役割一行, ロンデル文字, カラー)
DEPTS = [
    ("secretary", "秘書室", "窓口・TODO管理・壁打ち・メモ", "秘", "#12915C"),
    ("sns", "SNS部門", "X / Instagram / TikTok の投稿企画・運用", "S", "#D0611F"),
    ("note", "note部門", "note記事の執筆・有料コンテンツ管理", "n", "#1F93AD"),
    ("youtube", "YouTube部門", "動画の企画・台本・公開管理", "Y", "#CE3D66"),
    ("affiliate", "アフィリエイト部門", "案件リサーチ・LP制作・収支管理", "ア", "#8B7B00"),
    ("study", "勉強部屋", "教材の分析と知識の蓄積（全社学習）", "勉", "#3B74D1"),
    ("philosophy", "思想DB", "オーナーの判断軸の外部記憶", "思", "#A94ACB"),
]

# 成果物ステータス → (日本語ラベル, 種別)  種別: active=進行中 / done=完了
STATUS_MAP = {
    "idea": ("アイデア", "active"),
    "draft": ("下書き", "active"),
    "review": ("レビュー", "active"),
    "scheduled": ("予約済", "active"),
    "script": ("台本", "active"),
    "filming": ("撮影中", "active"),
    "editing": ("編集中", "active"),
    "posted": ("投稿済", "done"),
    "published": ("公開済", "done"),
}

# 成果物を置くサブフォルダ（部門ごと）
ITEM_DIRS = {
    "sns": ["posts"],
    "note": ["articles"],
    "youtube": ["videos"],
    "affiliate": ["pages", "reports"],
}


def read_head(path, n=20):
    try:
        with open(path, encoding="utf-8") as f:
            return [next(f).rstrip("\n") for _ in range(n)]
    except StopIteration:
        return path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []


def md_files(directory):
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.glob("*.md") if p.name != ".gitkeep")


def parse_deliverables(dept):
    """posts/articles/videos などから (タイトル, ラベル, 種別) を集める。"""
    items = []
    for sub in ITEM_DIRS.get(dept, []):
        for f in md_files(COMPANY / dept / sub):
            head = read_head(f)
            title = next(
                (l.lstrip("# ").strip() for l in head if l.startswith("# ")),
                f.stem,
            )
            m = next(
                (
                    re.search(r"ステータス[:：]\s*([a-zA-Z_]+)", l)
                    for l in head
                    if re.search(r"ステータス[:：]", l)
                ),
                None,
            )
            status = m.group(1).lower() if m else "draft"
            label, kind = STATUS_MAP.get(status, (status, "active"))
            items.append((title, label, kind))
    return items


def parse_todos():
    """secretary/todos/ の最新ファイルから未完了・完了タスクを取る。"""
    files = md_files(COMPANY / "secretary" / "todos")
    open_items, done = [], 0
    if files:
        for line in files[-1].read_text(encoding="utf-8").splitlines():
            m = re.match(r"-\s*\[( |x)\]\s*(\S.*)", line)
            if not m:
                continue
            if m.group(1) == "x":
                done += 1
            else:
                open_items.append(m.group(2).split("|")[0].strip())
    return open_items, done, files[-1].stem if files else None


def last_activity(dept):
    """部門フォルダの最終コミット (日付, メッセージ)。"""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad\t%s", "--date=format:%Y-%m-%d",
             "--", f".company/{dept}"],
            capture_output=True, text=True, cwd=ROOT, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None
    if not out:
        return None, None
    date, _, msg = out.partition("\t")
    return date, msg


def collect():
    """全部門のカードデータを組み立てる。"""
    cards = []
    for dept, name, role, initial, color in DEPTS:
        items = parse_deliverables(dept)
        stats = []

        if dept == "secretary":
            open_todos, done_todos, todo_date = parse_todos()
            items = [(t, "TODO", "active") for t in open_todos]
            notes = len(md_files(COMPANY / "secretary" / "notes"))
            inbox = len(md_files(COMPANY / "secretary" / "inbox"))
            stats.append(f"メモ {notes}件 / Inbox {inbox}件")
            if todo_date:
                stats.append(f"TODO {todo_date}: 未完了 {len(open_todos)} / 完了 {done_todos}")
        elif dept == "study":
            books = len(md_files(COMPANY / "study" / "library"))
            briefs = md_files(COMPANY / "study" / "briefs")
            stats.append(f"蔵書 {books}冊 / ブリーフ {len(briefs)}本")
            items = [(f"全社ニュースブリーフ {b.stem}", "作成済", "done") for b in briefs[-3:]]
        elif dept == "philosophy":
            themes = len(md_files(COMPANY / "philosophy" / "themes"))
            has_soron = (COMPANY / "philosophy" / "soron.md").is_file()
            stats.append(f"総論 {'整備済' if has_soron else '未作成'} / テーマ別DB {themes}件")
        else:
            research = len(md_files(COMPANY / dept / "research"))
            has_knowledge = (COMPANY / dept / "knowledge.md").is_file()
            stats.append(
                f"調査ログ {research}件 / knowledge.md {'あり' if has_knowledge else 'なし'}"
            )

        active = sum(1 for _, _, k in items if k == "active")
        done = sum(1 for _, _, k in items if k == "done")
        state = "作業中" if active else ("完了" if done else "待機中")
        date, msg = last_activity(dept)
        cards.append({
            "dept": dept, "name": name, "role": role, "initial": initial,
            "color": color, "items": items, "stats": stats,
            "active": active, "done": done, "state": state,
            "last_date": date, "last_msg": msg,
        })
    return cards


# ---------------------------------------------------------------- markdown

def render_md(cards, now):
    lines = [
        "# 会社ダッシュボード（全部門ステータス）",
        "",
        f"生成: {now}　※更新するには `python3 .company/dashboard/generate.py`",
        "",
        "| 部門 | 状態 | 進行中 | 完了 | 最終更新 |",
        "|------|------|-------:|-----:|----------|",
    ]
    for c in cards:
        lines.append(
            f"| {c['name']} | {c['state']} | {c['active']} | {c['done']} "
            f"| {c['last_date'] or '-'} |"
        )
    lines.append("")
    for c in cards:
        lines += [f"## {c['name']} — {c['state']}", "", f"役割: {c['role']}", ""]
        if c["items"]:
            for title, label, _ in c["items"]:
                lines.append(f"- [{label}] {title}")
        else:
            lines.append("- 進行中の成果物はまだありません")
        for s in c["stats"]:
            lines.append(f"- {s}")
        if c["last_date"]:
            lines.append(f"- 最終更新: {c['last_date']} 「{c['last_msg']}」")
        lines.append("")
    return "\n".join(lines)


# -------------------------------------------------------------------- html

CSS = """
:root {
  --ground: #F4F5F1; --surface: #FFFFFF; --ink: #23291F;
  --muted: #67705F; --line: #E1E4DB; --accent: #12915C;
  --chip-active-bg: #FDF3E7; --chip-active-ink: #8A4D12;
  --chip-done-bg: #E8F4EE; --chip-done-ink: #116A45;
  --chip-idle-bg: #EDEFE8; --chip-idle-ink: #67705F;
  --shadow: 0 1px 3px rgba(35, 41, 31, .08);
}
@media (prefers-color-scheme: dark) {
  :root {
    --ground: #171A15; --surface: #20241D; --ink: #E7EAE1;
    --muted: #9BA391; --line: #333829; --accent: #3DB584;
    --chip-active-bg: #3A2C17; --chip-active-ink: #EBB877;
    --chip-done-bg: #17352A; --chip-done-ink: #7ED0A9;
    --chip-idle-bg: #2A2E24; --chip-idle-ink: #9BA391;
    --shadow: 0 1px 3px rgba(0, 0, 0, .4);
  }
}
:root[data-theme="light"] {
  --ground: #F4F5F1; --surface: #FFFFFF; --ink: #23291F;
  --muted: #67705F; --line: #E1E4DB; --accent: #12915C;
  --chip-active-bg: #FDF3E7; --chip-active-ink: #8A4D12;
  --chip-done-bg: #E8F4EE; --chip-done-ink: #116A45;
  --chip-idle-bg: #EDEFE8; --chip-idle-ink: #67705F;
  --shadow: 0 1px 3px rgba(35, 41, 31, .08);
}
:root[data-theme="dark"] {
  --ground: #171A15; --surface: #20241D; --ink: #E7EAE1;
  --muted: #9BA391; --line: #333829; --accent: #3DB584;
  --chip-active-bg: #3A2C17; --chip-active-ink: #EBB877;
  --chip-done-bg: #17352A; --chip-done-ink: #7ED0A9;
  --chip-idle-bg: #2A2E24; --chip-idle-ink: #9BA391;
  --shadow: 0 1px 3px rgba(0, 0, 0, .4);
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--ground); color: var(--ink);
  font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic UI",
    "Yu Gothic", "Noto Sans JP", "Meiryo", sans-serif;
  line-height: 1.6; padding: 24px 16px 48px;
}
.wrap { max-width: 1080px; margin: 0 auto; }
header { display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 16px; margin-bottom: 20px; }
h1 { font-size: 1.35rem; margin: 0; letter-spacing: .02em; }
.gen { color: var(--muted); font-size: .8rem; font-variant-numeric: tabular-nums; }
.summary {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 10px; margin-bottom: 22px;
}
.tile {
  background: var(--surface); border: 1px solid var(--line); border-radius: 10px;
  padding: 12px 14px; box-shadow: var(--shadow);
}
.tile .num { font-size: 1.6rem; font-weight: 700; font-variant-numeric: tabular-nums; line-height: 1.2; }
.tile .lbl { color: var(--muted); font-size: .75rem; letter-spacing: .06em; }
.grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 14px;
}
.card {
  background: var(--surface); border: 1px solid var(--line); border-radius: 12px;
  padding: 16px; box-shadow: var(--shadow);
  display: flex; flex-direction: column; gap: 10px;
}
.card-head { display: flex; align-items: center; gap: 10px; }
.roundel {
  width: 40px; height: 40px; border-radius: 50%; flex: none;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-weight: 700; font-size: 1rem;
}
.dept-name { font-weight: 700; font-size: 1rem; }
.dept-role { color: var(--muted); font-size: .75rem; }
.pill {
  margin-left: auto; flex: none; font-size: .72rem; font-weight: 600;
  padding: 3px 10px; border-radius: 999px; display: flex; align-items: center; gap: 5px;
}
.pill::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.pill.active { background: var(--chip-active-bg); color: var(--chip-active-ink); }
.pill.done { background: var(--chip-done-bg); color: var(--chip-done-ink); }
.pill.idle { background: var(--chip-idle-bg); color: var(--chip-idle-ink); }
ul.items { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px; }
ul.items li {
  display: flex; align-items: baseline; gap: 8px; font-size: .85rem;
  border-top: 1px dashed var(--line); padding-top: 6px;
}
ul.items li:first-child { border-top: 0; padding-top: 0; }
.chip {
  flex: none; font-size: .68rem; font-weight: 600; padding: 1px 8px;
  border-radius: 999px; background: var(--chip-idle-bg); color: var(--chip-idle-ink);
}
.chip.active { background: var(--chip-active-bg); color: var(--chip-active-ink); }
.chip.done { background: var(--chip-done-bg); color: var(--chip-done-ink); }
.empty { color: var(--muted); font-size: .82rem; }
.meta { margin-top: auto; border-top: 1px solid var(--line); padding-top: 8px;
  color: var(--muted); font-size: .74rem; display: flex; flex-direction: column; gap: 2px; }
.meta .date { font-variant-numeric: tabular-nums; }
"""

STATE_CLS = {"作業中": "active", "完了": "done", "待機中": "idle"}


def render_html(cards, now):
    e = html.escape
    total_active = sum(c["active"] for c in cards)
    total_done = sum(c["done"] for c in cards)
    books = len(md_files(COMPANY / "study" / "library"))
    working = sum(1 for c in cards if c["state"] == "作業中")

    tiles = "".join(
        f'<div class="tile"><div class="num">{n}</div><div class="lbl">{l}</div></div>'
        for n, l in [
            (working, "作業中の部門"),
            (total_active, "進行中の成果物・TODO"),
            (total_done, "完了・公開済み"),
            (books, "勉強部屋の蔵書"),
        ]
    )

    card_html = []
    for c in cards:
        if c["items"]:
            lis = "".join(
                f'<li><span class="chip {k}">{e(l)}</span><span>{e(t)}</span></li>'
                for t, l, k in c["items"]
            )
            body = f'<ul class="items">{lis}</ul>'
        else:
            body = '<p class="empty">進行中の成果物はまだありません</p>'
        stats = "".join(f"<div>{e(s)}</div>" for s in c["stats"])
        last = (
            f'<div class="date">最終更新 {e(c["last_date"])}　{e(c["last_msg"] or "")}</div>'
            if c["last_date"] else ""
        )
        card_html.append(
            f'<section class="card">'
            f'<div class="card-head">'
            f'<div class="roundel" style="background:{c["color"]}">{e(c["initial"])}</div>'
            f'<div><div class="dept-name">{e(c["name"])}</div>'
            f'<div class="dept-role">{e(c["role"])}</div></div>'
            f'<span class="pill {STATE_CLS[c["state"]]}">{c["state"]}</span>'
            f'</div>{body}<div class="meta">{stats}{last}</div></section>'
        )

    return (
        "<title>会社ダッシュボード</title>\n"
        f"<style>{CSS}</style>\n"
        '<div class="wrap">\n'
        "<header><h1>会社ダッシュボード</h1>"
        f'<span class="gen">生成 {now}</span></header>\n'
        f'<div class="summary">{tiles}</div>\n'
        f'<div class="grid">{"".join(card_html)}</div>\n'
        "</div>\n"
    )


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cards = collect()
    (OUT_DIR / "dashboard.md").write_text(render_md(cards, now), encoding="utf-8")
    (OUT_DIR / "dashboard.html").write_text(render_html(cards, now), encoding="utf-8")
    print(f"generated: {OUT_DIR / 'dashboard.md'}")
    print(f"generated: {OUT_DIR / 'dashboard.html'}")


if __name__ == "__main__":
    main()
