# -*- coding: utf-8 -*-
"""결과물의 숫자가 근거 폴더 어디에 있는지 대조한다. 표준 라이브러리만 쓴다.

  python3 number_check.py <결과물 파일> <근거 폴더> [--also <파일 또는 폴더> ...]

- 결과물: md, txt, html. html은 태그를 지우고 본다
- 근거: 폴더 아래의 md, txt, csv, py, json, html (결과물 자신과 이름에 '설득점검'이 든 파일은 뺀다)
- 같다고 보는 경우: 소수 자리를 맞춰 반올림하면 같을 때 (61.2 = 61.16), 앞에 '약', '~', '안팎'이 붙으면 5% 안,
  만 원, 백만 원, 억은 원으로 환산해서도 본다 (약 383백만 원 = 382,710,500)
- 빼고 보는 숫자: 날짜(2026-09-30, 9/14, 9월, 14일), 12 이하의 맨 정수(단계 번호, 개수), 연도 4자리
결과: 근거에서 찾지 못한 숫자와 그 줄. 찾지 못했다고 틀린 숫자는 아니다. 출처를 사람에게 묻는다
"""
import os, re, sys, html

NUM = re.compile(r"(약\s*|~\s*)?([-+−]?\d[\d,]*(?:\.\d+)?)\s*(%p|%|배|건|명|원|만 원|백만 원|억|회|일|주|개)?(\s*안팎)?")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}|\d{1,2}월|\d{1,2}일|\d{4}년|\d{1,2}:\d{2}")
SRC_EXT = (".md", ".txt", ".csv", ".py", ".json", ".html")
SCALE = {"만원": 1e4, "백만원": 1e6, "억": 1e8}


def text_of(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        t = f.read()
    if path.endswith(".html"):
        t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return t


def to_float(s):
    return float(s.replace(",", "").replace("−", "-"))


def numbers(text):
    out = []
    clean = DATE.sub(" ", text)
    for m in NUM.finditer(clean):
        approx = bool(m.group(1) or m.group(4))
        raw = m.group(2)
        try:
            v = to_float(raw)
        except ValueError:
            continue
        dec = len(raw.split(".")[1]) if "." in raw else 0
        out.append((v, dec, approx, m.group(0).strip()))
        unit = (m.group(3) or "").replace(" ", "")
        if unit in SCALE:   # 383백만원 → 383,000,000원 으로도 대조
            out.append((v * SCALE[unit], 0, True, None))
    return out


def source_values(root, skip):
    vals = []
    paths = [root] if os.path.isfile(root) else [os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs]
    for p in paths:
        if not p.endswith(SRC_EXT) or os.path.abspath(p) in skip or "설득점검" in os.path.basename(p):
            continue
        vals += [(v, d) for v, d, *_ in numbers(text_of(p))]
    return vals


def found(v, dec, approx, pool, pct):
    for y, ydec in pool:
        if approx and v and abs(y - v) / abs(v) <= 0.05:
            return True
        if round(y, dec) == round(v, dec) or round(abs(y), dec) == round(abs(v), dec):
            return True
        if pct and abs(y) < 1 and ydec >= 2 and round(y * 100, dec) == round(v, dec):   # 0.612 과 61.2%
            return True
    return False


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    target, roots = sys.argv[1], [sys.argv[2]]
    if "--also" in sys.argv:
        roots += sys.argv[sys.argv.index("--also") + 1:]
    skip = {os.path.abspath(target)}
    pool = []
    for r in roots:
        pool += source_values(r, skip)
    miss, total = [], 0
    for ln, line in enumerate(text_of(target).splitlines(), 1):
        nums = numbers(line)
        for k, (v, dec, approx, shown) in enumerate(nums):
            if shown is None:
                continue
            scaled = nums[k + 1] if k + 1 < len(nums) and nums[k + 1][3] is None else None
            if dec == 0 and abs(v) <= 12 and not shown.endswith(("%", "%p", "배")):
                continue
            if dec == 0 and 1900 <= v <= 2100:
                continue
            total += 1
            if not found(v, dec, approx, pool, shown.endswith(("%", "%p"))) and not (scaled and found(scaled[0], 0, True, pool, False)):
                miss.append((ln, shown, line.strip()[:90]))
    print(f"결과물 숫자 {total}개 중 근거에서 찾지 못한 것 {len(miss)}개")
    for ln, shown, line in miss:
        print(f"  {ln}줄  {shown}  | {line}")


if __name__ == "__main__":
    main()
