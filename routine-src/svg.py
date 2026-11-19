from html import escape
INK='#111827'; SUB='#4B5563'; MUTE='#9CA3AF'; LINE='#D1D5DB'; BG='#F3F4F6'; WHITE='#FFFFFF'
BLUE='#2563EB'; BLUE_L='#DBEAFE'; RED='#DC2626'; RED_L='#FEE2E2'; GREEN='#16A34A'; GREEN_L='#DCFCE7'
AMBER='#D97706'; AMBER_L='#FEF3C7'; PURPLE='#7C3AED'; PURPLE_L='#EDE9FE'; YELLOW='#FDE68A'; GRAY_D='#6B7280'
FONT="'Noto Sans CJK KR','Noto Sans KR',sans-serif"

class S:
    def __init__(self, w, h):
        self.w, self.h = w, h; self.p = []
    def add(self, s): self.p.append(s); return self
    def rect(self, x, y, w, h, fill=WHITE, stroke=LINE, r=6, sw=1, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')
    def line(self, x1, y1, x2, y2, c=LINE, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"{d}/>')
    def circle(self, x, y, r, fill=WHITE, stroke=LINE, sw=1):
        return self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def text(self, x, y, s, size=12, w=400, fill=INK, anchor='start', italic=False, halo=False):
        it = ' font-style="italic"' if italic else ''
        h = ' stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' if halo else ''
        return self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" font-family="{FONT}"{it}{h}>{escape(s)}</text>')
    def lines(self, x, y, arr, size=12, w=400, fill=INK, lh=None, anchor='start'):
        lh = lh or round(size*1.45)
        for i, s in enumerate(arr):
            self.text(x, y+i*lh, s, size, w, fill, anchor)
        return self
    def arrow(self, x1, y1, x2, y2, c=SUB, sw=1.4, dash=None, head=True):
        mid = f'a{abs(hash(c))%9999}'
        d = f' stroke-dasharray="{dash}"' if dash else ''
        m = f' marker-end="url(#{mid})"' if head else ''
        self.add(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker></defs>')
        return self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"{d}{m}/>')
    def path(self, d, c=SUB, sw=1.4, fill='none', head=False, dash=None):
        mid = f'p{abs(hash(c))%9999}'
        m = ''
        if head:
            self.add(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker></defs>')
            m = f' marker-end="url(#{mid})"'
        da = f' stroke-dasharray="{dash}"' if dash else ''
        return self.add(f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{m}{da}/>')
    def badge(self, x, y, s, fg=BLUE, bg=BLUE_L, size=10.5, pad=7, h=19):
        w = len(s)*size*0.98 + pad*2 if any(ord(ch)>255 for ch in s) else len(s)*size*0.6 + pad*2
        self.rect(x, y, w, h, bg, bg, r=h/2)
        self.text(x+w/2, y+h/2+size*0.36, s, size, 600, fg, 'middle')
        return w
    def num(self, x, y, n, c=BLUE, r=10):
        self.circle(x, y, r, c, c)
        return self.text(x, y+4, str(n), 11, 700, WHITE, 'middle')
    def phone(self, x, y, w=150, h=280, title=''):
        self.rect(x, y, w, h, WHITE, '#9CA3AF', 14, 1.2)
        self.rect(x+w/2-18, y+6, 36, 5, '#E5E7EB', '#E5E7EB', 2.5)
        if title:
            self.text(x+12, y+32, title, 12.5, 700, INK)
        return self
    def svg(self):
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="100%" style="display:block">' + ''.join(self.p) + '</svg>'

def tw(s, size):
    """대략적인 텍스트 폭"""
    return sum(size*0.98 if ord(c)>255 else size*0.58 for c in s)
