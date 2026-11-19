import subprocess, json, re, sys, io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import render

def html2pdf(html_path, pdf_path):
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={pdf_path}', html_path], check=True, capture_output=True, timeout=300)

def find_pages(pdf_path):
    r = PdfReader(pdf_path); toc = {}
    for i, p in enumerate(r.pages):
        t = p.extract_text() or ''
        for w in render.WEEKS:
            key = f'w{w.n:02d}'
            if key in toc: continue
            if re.search(rf'(^|\n)\s*{w.n}주차\s', t) and '이번 주 결과물' in t:
                toc[key] = i + 1
    return toc, len(r.pages)

def number(pdf_in, pdf_out, skip=1):
    r = PdfReader(pdf_in); w = PdfWriter()
    pdfmetrics.registerFont(TTFont('NS', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', subfontIndex=1)) if False else None
    for i, p in enumerate(r.pages):
        if i >= skip:
            buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=A4)
            c.setFont('Helvetica', 8); c.setFillGray(0.55)
            c.drawRightString(A4[0]-14*2.835, 8*2.835, f'{i+1} / {len(r.pages)}')
            c.drawString(14*2.835, 8*2.835, 'UI/UX 24-week routine')
            c.save(); buf.seek(0)
            p.merge_page(PdfReader(buf).pages[0])
        w.add_page(p)
    w.add_metadata({'/Title': 'UI/UX 취업 준비 24주 루틴 (2–24주차 일별 계획)', '/Author': 'UI Study Path'})
    with open(pdf_out, 'wb') as f: w.write(f)

if __name__ == '__main__':
    open('plan.html', 'w').write(render.build({}))
    html2pdf('plan.html', 'pass1.pdf')
    toc, n = find_pages('pass1.pdf')
    print('pass1 pages', n, 'found', len(toc))
    open('plan.html', 'w').write(render.build(toc))
    html2pdf('plan.html', 'pass2.pdf')
    toc2, n2 = find_pages('pass2.pdf')
    assert toc == toc2, (toc, toc2)
    number('pass2.pdf', 'UIUX_24주_루틴_20261108.pdf')
    print('pages', n2, toc2)
