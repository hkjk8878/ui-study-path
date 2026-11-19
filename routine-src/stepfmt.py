# 할 일 글: 줄바꿈 → <br>, ‘| a | b |’ 줄 묶음 → 표 (첫 줄은 머리글)
import html
TD = 'style="border:1px solid #D1D5DB;padding:3px 6px;vertical-align:top;text-align:left"'
TH = 'style="border:1px solid #D1D5DB;padding:3px 6px;background:#F3F4F6;text-align:left;font-weight:700"'
def fmt(text):
    out, rows = [], []
    def flush():
        if not rows: return
        h = '<table style="border-collapse:collapse;margin:4px 0;font-size:.95em">'
        for i, r in enumerate(rows):
            cells = [c.strip() for c in r.strip().strip('|').split('|')]
            tag, st = ('th', TH) if i == 0 else ('td', TD)
            h += '<tr>' + ''.join(f'<{tag} {st}>{html.escape(c)}</{tag}>' for c in cells) + '</tr>'
        out.append(h + '</table>'); rows.clear()
    for line in text.split('\n'):
        if line.strip().startswith('|'):
            rows.append(line)
        else:
            flush(); out.append(html.escape(line) + '<br>')
    flush()
    s = ''.join(out)
    return s[:-4] if s.endswith('<br>') else s
