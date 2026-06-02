"""Insert the 5 generated diagrams into the existing DKM Word report."""

from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy, os

SRC  = '/home/user/DocuMate/Laporan_Makmal_Rangkaian_DKM.docx'
OUT  = '/home/user/DocuMate/Laporan_Makmal_Rangkaian_DKM_GAMBAR.docx'
IMGS = '/home/user/DocuMate/images'

doc = Document(SRC)

CISCO_BLUE = RGBColor(0x00, 0x54, 0x9F)
DARK_BLUE  = RGBColor(0x00, 0x3D, 0x73)
GRAY       = RGBColor(0x71, 0x80, 0x96)
BLACK      = RGBColor(0x00, 0x00, 0x00)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)


def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)


def add_figure(doc, img_path, caption, width_cm=15.5):
    """Insert a centred image with a styled caption."""
    # image paragraph
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(10)
    p_img.paragraph_format.space_after  = Pt(2)
    run = p_img.add_run()
    run.add_picture(img_path, width=Cm(width_cm))

    # caption paragraph
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after  = Pt(14)
    r = p_cap.add_run(caption)
    r.italic   = True
    r.bold     = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = DARK_BLUE

    # thin line under caption
    pPr  = p_cap._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    '4')
    bot.set(qn('w:color'), '00549F')
    pBdr.append(bot)
    pPr.append(pBdr)


def add_heading1(doc, text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold      = True
    run.font.size = Pt(14)
    run.font.color.rgb = DARK_BLUE
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after  = Pt(6)
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    '6')
    bot.set(qn('w:color'), '00549F')
    pBdr.append(bot)
    pPr.append(pBdr)


def add_heading2(doc, text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold      = True
    run.font.size = Pt(12)
    run.font.color.rgb = CISCO_BLUE
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(4)


def add_body(doc, text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size      = Pt(11)
    run.font.color.rgb = BLACK
    p.paragraph_format.space_after = Pt(5)
    from docx.enum.text import WD_LINE_SPACING
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE


def add_bullet(doc, text):
    p   = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size      = Pt(11)
    run.font.color.rgb = BLACK
    p.paragraph_format.space_after  = Pt(3)
    p.paragraph_format.left_indent  = Cm(0.8)


def add_note(doc, text):
    """Blue callout box (simulated with a 1-column table)."""
    tbl = doc.add_table(rows=1, cols=1)
    cell = tbl.rows[0].cells[0]
    cell.text = ''
    p   = cell.paragraphs[0]
    run = p.add_run('📌  ' + text)
    run.font.size      = Pt(10)
    run.font.color.rgb = DARK_BLUE
    set_cell_bg(cell, 'EBF5FF')
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for side in ('top','left','bottom','right'):
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:sz'),    '6' if side=='left' else '4')
        el.set(qn('w:val'),   'single')
        el.set(qn('w:color'), '00549F' if side=='left' else 'BEE3F8')
        tcBorders.append(el)
    tcPr.append(tcBorders)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


# ─── Build new document with images inserted at correct sections ──────────────

new_doc = Document()

# Copy page setup from original
section = new_doc.sections[0]
orig_s  = doc.sections[0]
section.page_width    = orig_s.page_width
section.page_height   = orig_s.page_height
section.top_margin    = orig_s.top_margin
section.bottom_margin = orig_s.bottom_margin
section.left_margin   = orig_s.left_margin
section.right_margin  = orig_s.right_margin

# ── Copy all paragraphs & tables from original up to section 4 ───────────────
def copy_element(new_doc, elem):
    new_doc._body.append(copy.deepcopy(elem))

# Copy everything from original (all XML elements)
for child in doc._body._body:
    new_doc._body._body.append(copy.deepcopy(child))

# ── Now APPEND new image sections at the end ─────────────────────────────────

new_doc.add_page_break()

# ═══ LAMPIRAN A – GAMBAR RAJAH ════════════════════════════════════════════════
add_heading1(new_doc, 'LAMPIRAN A:  GAMBAR RAJAH TEKNIKAL')
add_body(new_doc,
    'Bahagian ini mengandungi gambar rajah teknikal lengkap yang direka untuk '
    'laporan DKM makmal rangkaian komputer. Semua rajah dihasilkan mengikut '
    'piawaian industri dan boleh digunakan secara terus dalam laporan teknikal.')

new_doc.add_paragraph()

# ── Rajah 1: Floor Plan ───────────────────────────────────────────────────────
add_heading2(new_doc, 'Rajah A-1:  Pelan Susun Atur Fizikal Makmal (Floor Plan)')
add_body(new_doc,
    'Rajah berikut menunjukkan pandangan atas (bird-eye view) makmal rangkaian '
    'komputer dengan saiz bilik 10m × 8m. Terdapat 25 stesen kerja pelajar '
    'disusun dalam format 5 baris × 5 lajur, 1 komputer pengajar di bahagian hadapan, '
    'dan rak rangkaian 12U di sudut belakang kanan.')

add_figure(new_doc,
    f'{IMGS}/01_floor_plan.png',
    'Rajah A-1: Pelan Susun Atur Fizikal Makmal Rangkaian (Pandangan Atas)',
    width_cm=15.5)

add_note(new_doc,
    'Pelan ini menunjukkan susun atur fizikal bilik makmal. Jarak minimum '
    'antara meja ialah 90cm untuk memenuhi piawaian keselamatan dan akses. '
    'Cable tray dipasang di sepanjang dinding untuk pengurusan kabel yang kemas.')

new_doc.add_page_break()

# ── Rajah 2: Network Topology ──────────────────────────────────────────────────
add_heading2(new_doc, 'Rajah A-2:  Topologi Rangkaian Logik (Logical Network Topology)')
add_body(new_doc,
    'Rajah ini menunjukkan topologi bintang (star topology) rangkaian makmal. '
    'Router Cisco 1941 berfungsi sebagai penghala utama antara rangkaian LAN '
    'dan internet (WAN). Switch Cisco 2960-24TT menguruskan sambungan semua '
    'stesen kerja dengan pembahagian VLAN yang sesuai.')

add_figure(new_doc,
    f'{IMGS}/02_network_topology.png',
    'Rajah A-2: Topologi Rangkaian Logik dengan Segmentasi VLAN',
    width_cm=15.5)

add_note(new_doc,
    'Tiga VLAN digunakan: VLAN 10 (Pelajar), VLAN 20 (Pengajar), dan VLAN 99 '
    '(Pengurusan). Router bertindak sebagai inter-VLAN routing untuk membenarkan '
    'komunikasi terkawal antara VLAN. NAT dikonfigurasi untuk akses internet.')

new_doc.add_page_break()

# ── Rajah 3: Network Rack ──────────────────────────────────────────────────────
add_heading2(new_doc, 'Rajah A-3:  Rekabentuk Rak Rangkaian 12U (Network Rack Layout)')
add_body(new_doc,
    'Rajah ini menunjukkan susun atur peralatan dalam rak rangkaian 12U. '
    'Setiap unit rak (1U) diletak mengikut keperluan operasi dan pengurusan '
    'haba. Peralatan kritikal (router dan switch) diletakkan di bahagian atas, '
    'manakala UPS dan PDU di bahagian bawah.')

add_figure(new_doc,
    f'{IMGS}/03_network_rack.png',
    'Rajah A-3: Susun Atur Rak Rangkaian 12U dengan Spesifikasi Lengkap',
    width_cm=14.0)

add_note(new_doc,
    'UPS mesti disambung antara bekalan kuasa dinding dan PDU untuk memastikan '
    'semua peralatan dalam rak mendapat perlindungan kuasa tidak putus. '
    'Fan tray dipasang di bahagian atas bawah untuk pengudaraan yang baik.')

new_doc.add_page_break()

# ── Rajah 4: Cabling 568B ─────────────────────────────────────────────────────
add_heading2(new_doc, 'Rajah A-4:  Spesifikasi Kabel UTP Cat6 – Piawaian TIA-568B')
add_body(new_doc,
    'Rajah ini menunjukkan susunan warna wayar mengikut piawaian EIA/TIA-568B '
    'untuk kabel UTP Cat6. Konfigurasi straight-through digunakan untuk '
    'menyambungkan PC ke switch (kedua-dua hujung kabel mempunyai susunan pin '
    'yang sama mengikut 568B).')

add_figure(new_doc,
    f'{IMGS}/04_cabling_568B.png',
    'Rajah A-4: Susunan Warna Pin RJ-45 EIA/TIA-568B & Keratan Rentas Cat6',
    width_cm=15.5)

add_note(new_doc,
    'PENTING: Gunakan HANYA piawaian 568B di KEDUA-DUA hujung kabel untuk '
    'konfigurasi straight-through. Pastikan setiap kabel dilabel mengikut '
    'piawaian TIA-606-B setelah pemasangan selesai.')

new_doc.add_page_break()

# ── Rajah 5: IP Addressing ────────────────────────────────────────────────────
add_heading2(new_doc, 'Rajah A-5:  Ringkasan Jadual Pengalamatan IP')
add_body(new_doc,
    'Rajah ini memberikan gambaran keseluruhan skim pengalamatan IP yang '
    'digunakan dalam makmal rangkaian. Semua peranti menggunakan IP statik '
    'dalam subnet 192.168.1.0/24 dengan gateway 192.168.1.254.')

add_figure(new_doc,
    f'{IMGS}/05_ip_addressing.png',
    'Rajah A-5: Jadual Pengalamatan IP Lengkap – 26 Stesen Kerja + Peralatan Rangkaian',
    width_cm=15.5)

add_note(new_doc,
    'Semua IP adalah statik (bukan DHCP) untuk memudahkan pengurusan dan '
    'penyelesaian masalah rangkaian. Setiap PC wajib dikonfigurasikan dengan '
    'IP Address, Subnet Mask, Default Gateway, dan DNS Server yang betul.')

# ── Final note ────────────────────────────────────────────────────────────────
new_doc.add_paragraph()
add_heading2(new_doc, 'Nota Penggunaan Rajah dalam Laporan DKM')
add_bullet(new_doc, 'Semua rajah di atas adalah dalam resolusi tinggi (180 DPI) sesuai untuk cetakan A4.')
add_bullet(new_doc, 'Rajah boleh disisipkan terus ke dalam laporan Word menggunakan Insert → Picture.')
add_bullet(new_doc, 'Pastikan setiap rajah mempunyai nombor rujukan (contoh: Rajah 4.1, Rajah 5.1).')
add_bullet(new_doc, 'Senaraikan semua rajah dalam "Senarai Rajah" di bahagian hadapan laporan.')
add_bullet(new_doc, 'Gambar rajah boleh diedit lanjut menggunakan Microsoft Visio atau draw.io.')

new_doc.save(OUT)
print(f'Saved final document: {OUT}')
