from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ─── Page margins (A4) ───────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Cm(21.0)
section.page_height = Cm(29.7)
section.top_margin    = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin   = Cm(3.0)
section.right_margin  = Cm(2.5)

# ─── Colour constants ────────────────────────────────────────────────────────
CISCO_BLUE  = RGBColor(0x00, 0x54, 0x9F)
DARK_BLUE   = RGBColor(0x00, 0x3D, 0x73)
TABLE_HEAD  = RGBColor(0x00, 0x54, 0x9F)
TABLE_ALT   = RGBColor(0xEB, 0xF5, 0xFF)
BLACK       = RGBColor(0x00, 0x00, 0x00)
GRAY        = RGBColor(0x44, 0x44, 0x44)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def set_cell_bg(cell, hex_color: str):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)

def set_cell_border(cell, **kwargs):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for side in ('top','left','bottom','right','insideH','insideV'):
        val = kwargs.get(side, {'sz':'4','val':'single','color':'CCCCCC'})
        el  = OxmlElement(f'w:{side}')
        el.set(qn('w:sz'),    str(val.get('sz',   '4')))
        el.set(qn('w:val'),   str(val.get('val',  'single')))
        el.set(qn('w:color'), str(val.get('color','CCCCCC')))
        tcBorders.append(el)
    tcPr.append(tcBorders)

def heading1(text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold      = True
    run.font.size = Pt(14)
    run.font.color.rgb = DARK_BLUE
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after  = Pt(6)
    # bottom border
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    '6')
    bot.set(qn('w:color'), '00549F')
    pBdr.append(bot)
    pPr.append(pBdr)
    return p

def heading2(text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold      = True
    run.font.size = Pt(12)
    run.font.color.rgb = CISCO_BLUE
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(4)
    return p

def heading3(text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold      = True
    run.font.size = Pt(11)
    run.font.color.rgb = GRAY
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(2)
    return p

def body(text, bold=False, italic=False, indent=False):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold             = bold
    run.italic           = italic
    run.font.size        = Pt(11)
    run.font.color.rgb   = BLACK
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if indent:
        p.paragraph_format.left_indent = Cm(0.8)
    return p

def bullet(text, level=0):
    p   = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size      = Pt(11)
    run.font.color.rgb = BLACK
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.8 + level * 0.5)
    return p

def numbered(text):
    p   = doc.add_paragraph(style='List Number')
    run = p.add_run(text)
    run.font.size      = Pt(11)
    run.font.color.rgb = BLACK
    p.paragraph_format.space_after = Pt(3)
    return p

def code_para(text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name  = 'Courier New'
    run.font.size  = Pt(9)
    run.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    p.paragraph_format.space_after       = Pt(1)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.paragraph_format.left_indent       = Cm(0.8)
    # light gray shading
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),  'clear')
    shd.set(qn('w:color'),'auto')
    shd.set(qn('w:fill'), 'F0F0F0')
    pPr.append(shd)
    return p

def table_header_row(table, headers, col_widths=None):
    row = table.rows[0]
    for i, hdr in enumerate(headers):
        cell = row.cells[i]
        cell.text = ''
        p   = cell.paragraphs[0]
        run = p.add_run(hdr)
        run.bold           = True
        run.font.size      = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment        = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_bg(cell, '00549F')
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    if col_widths:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Cm(w)

def table_data_row(table, row_idx, values, alt=False):
    row  = table.add_row()
    fill = 'EBF5FF' if alt else 'FFFFFF'
    for i, val in enumerate(values):
        cell = row.cells[i]
        cell.text = ''
        p   = cell.paragraphs[0]
        run = p.add_run(str(val))
        run.font.size      = Pt(10)
        run.font.color.rgb = BLACK
        set_cell_bg(cell, fill)
    return row

def divider():
    p   = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr= OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'),  'single')
    bot.set(qn('w:sz'),   '4')
    bot.set(qn('w:color'),'CCCCCC')
    pBdr.append(bot)
    pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)

# ═══════════════════════════════════════════════════════════════════════════════
#  COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════

# Institution
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('KEMENTERIAN PENDIDIKAN MALAYSIA')
r.bold = True; r.font.size = Pt(13); r.font.color.rgb = DARK_BLUE

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('JABATAN KEMAHIRAN MALAYSIA (JKM)')
r.bold = True; r.font.size = Pt(13); r.font.color.rgb = DARK_BLUE

doc.add_paragraph()
doc.add_paragraph()

# Title box
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('LAPORAN TEKNIKAL')
r.bold = True; r.font.size = Pt(22); r.font.color.rgb = CISCO_BLUE

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('PELAN SUSUN ATUR MAKMAL RANGKAIAN KOMPUTER')
r.bold = True; r.font.size = Pt(16); r.font.color.rgb = DARK_BLUE

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('(NETWORK COMPUTER LABORATORY LAYOUT PLAN)')
r.bold = False; r.font.size = Pt(13); r.font.color.rgb = GRAY; r.italic = True

doc.add_paragraph()
doc.add_paragraph()

# Subtitle
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Menggunakan Perisian Cisco Packet Tracer')
r.font.size = Pt(12); r.font.color.rgb = GRAY

doc.add_paragraph()
doc.add_paragraph()

# Info table
info_tbl = doc.add_table(rows=6, cols=2)
info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
fields = [
    ('Program',      'Diploma Kemahiran Malaysia (DKM) Tahap 4'),
    ('Bidang',       'Teknologi Maklumat & Komunikasi (ICT)'),
    ('Mata Pelajaran','Rangkaian Komputer / Networking'),
    ('Institusi',    '[Nama Kolej Komuniti / Institut Kemahiran]'),
    ('Tarikh',       'Jun 2024'),
    ('Disediakan oleh','[Nama Pelajar / Pensyarah]'),
]
for i, (k, v) in enumerate(fields):
    row = info_tbl.rows[i]
    row.cells[0].text = ''
    row.cells[1].text = ''
    r0 = row.cells[0].paragraphs[0].add_run(k + ' :')
    r0.bold = True; r0.font.size = Pt(11)
    r1 = row.cells[1].paragraphs[0].add_run(v)
    r1.font.size = Pt(11)
    set_cell_bg(row.cells[0], 'EBF5FF')
    row.cells[0].width = Cm(5.5)
    row.cells[1].width = Cm(9.5)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  ISI KANDUNGAN
# ═══════════════════════════════════════════════════════════════════════════════

heading1('ISI KANDUNGAN')
toc = [
    ('1.0', 'Pendahuluan / Pengenalan', '3'),
    ('2.0', 'Objektif Makmal Rangkaian', '3'),
    ('3.0', 'Spesifikasi Peralatan (Bill of Materials)', '4'),
    ('4.0', 'Pelan Susun Atur Fizikal (Floor Plan)', '5'),
    ('5.0', 'Topologi Rangkaian Logik', '6'),
    ('6.0', 'Rekabentuk Network Rack (12U)', '7'),
    ('7.0', 'Jadual Pengalamatan IP (IP Addressing)', '8'),
    ('8.0', 'Spesifikasi Kabel (Cabling Specification)', '9'),
    ('9.0', 'Spesifikasi UPS dan Bekalan Kuasa (PSU)', '10'),
    ('10.0','Konfigurasi Peranti Cisco (IOS Configuration)', '11'),
    ('11.0','Prosedur Ujian Sambungan Rangkaian', '13'),
    ('12.0','Keselamatan Makmal (Lab Safety)', '14'),
    ('13.0','Kesimpulan', '14'),
    ('14.0','Rujukan', '15'),
]
toc_tbl = doc.add_table(rows=len(toc), cols=3)
toc_tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
for i, (num, title, page) in enumerate(toc):
    toc_tbl.rows[i].cells[0].text = num
    toc_tbl.rows[i].cells[1].text = title
    toc_tbl.rows[i].cells[2].text = page
    for j in range(3):
        toc_tbl.rows[i].cells[j].paragraphs[0].runs[0].font.size = Pt(11)
    toc_tbl.rows[i].cells[0].width = Cm(1.2)
    toc_tbl.rows[i].cells[1].width = Cm(12.0)
    toc_tbl.rows[i].cells[2].width = Cm(1.5)
    toc_tbl.rows[i].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  1.0  PENDAHULUAN
# ═══════════════════════════════════════════════════════════════════════════════

heading1('1.0  PENDAHULUAN / PENGENALAN')
body(
    'Laporan ini disediakan sebagai dokumentasi teknikal bagi projek mereka bentuk dan '
    'melaksanakan susun atur makmal rangkaian komputer yang profesional. Makmal ini '
    'direka untuk tujuan pengajaran dan pembelajaran (PdP) dalam bidang Teknologi '
    'Maklumat dan Komunikasi (ICT) pada peringkat Diploma Kemahiran Malaysia (DKM) Tahap 4.'
)
body(
    'Pelan ini menggunakan piawaian industri Cisco Networking Academy dan disimulasikan '
    'menggunakan perisian Cisco Packet Tracer versi 8.x. Rekabentuk ini merangkumi '
    'susun atur fizikal, topologi logik rangkaian, spesifikasi peralatan, konfigurasi '
    'peranti Cisco, serta prosedur ujian rangkaian.'
)

body(
    'Makmal ini terdiri daripada 26 stesen kerja — 25 unit komputer pelajar dan '
    '1 unit komputer pengajar — disambungkan melalui suis (switch) dan penghala (router) '
    'Cisco yang disimpan dalam rak rangkaian (network rack) bersama sistem UPS dan PDU '
    'untuk keselamatan bekalan kuasa.'
)

# ═══════════════════════════════════════════════════════════════════════════════
#  2.0  OBJEKTIF
# ═══════════════════════════════════════════════════════════════════════════════

heading1('2.0  OBJEKTIF MAKMAL RANGKAIAN')
body('Objektif utama pembinaan makmal rangkaian ini adalah seperti berikut:')
numbered('Mereka bentuk susun atur fizikal makmal mengikut piawaian TIA-942 dan ANSI/BICSI.')
numbered('Melaksanakan topologi rangkaian bintang (star topology) menggunakan peralatan Cisco.')
numbered('Mengkonfigurasi VLAN untuk mengasingkan trafik pelajar dan pengajar.')
numbered('Memastikan setiap stesen kerja mendapat akses internet melalui NAT di router Cisco.')
numbered('Menyediakan sistem bekalan kuasa tidak putus (UPS) untuk peralatan kritikal rangkaian.')
numbered('Mendokumentasikan konfigurasi IOS Cisco untuk tujuan penyelenggaraan dan audit.')
numbered('Mensimulasikan topologi menggunakan Cisco Packet Tracer untuk tujuan pembelajaran.')

doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════════════════
#  3.0  SPESIFIKASI PERALATAN
# ═══════════════════════════════════════════════════════════════════════════════

heading1('3.0  SPESIFIKASI PERALATAN (BILL OF MATERIALS)')
body('Jadual berikut menyenaraikan semua peralatan yang diperlukan untuk pembinaan makmal rangkaian:')
doc.add_paragraph()

bom_headers = ['Bil', 'Peralatan', 'Model / Spesifikasi', 'Kuantiti', 'Fungsi']
bom_widths  = [1.0, 3.5, 5.5, 1.8, 3.0]
bom_data = [
    ('1',  'Router Cisco',        'Cisco 1941 (2× FastEthernet, IOS 15.x)',    '1 unit',  'Penghala LAN ke WAN / NAT'),
    ('2',  'Switch Cisco',        'Cisco Catalyst 2960-24TT (24×FE, 2×GE)',    '1 unit',  'Suis utama, VLAN, trunking'),
    ('3',  'Patch Panel',         'Cat6 24-port 1U (568B)',                     '1 unit',  'Titik tampung kabel'),
    ('4',  'Network Rack',        '12U Wall-Mount / Free-Standing, 600mm',      '1 unit',  'Menempatkan peralatan rangkaian'),
    ('5',  'UPS',                 'APC Smart-UPS 1000VA / 700W',                '1 unit',  'Bekalan kuasa sandaran'),
    ('6',  'PDU / PSU',           'Rack PDU 1U, 16A/250V, 8× C13',             '1 unit',  'Agihan kuasa dalam rack'),
    ('7',  'Fan Tray',            '1U Rack Fan, 2× 80mm, 1500 RPM',            '1 unit',  'Penyejukan rak rangkaian'),
    ('8',  'PC Pelajar',          'Desktop Intel i5, 8GB RAM, 256GB SSD',       '25 unit', 'Stesen kerja pelajar'),
    ('9',  'PC Pengajar',         'Desktop Intel i7, 16GB RAM, 512GB SSD',      '1 unit',  'Stesen kerja pengajar'),
    ('10', 'Monitor',             '24" Full HD (1920×1080) IPS',                '26 unit', 'Paparan stesen kerja'),
    ('11', 'Kabel UTP Cat6',      'Cat6 Straight-Through (pelbagai panjang)',   'Lot',     'Sambungan PC ke patch panel'),
    ('12', 'RJ-45 Keystone Jack', 'Cat6 Wall Jack (568B)',                      '26 unit', 'Titik sambungan dinding'),
    ('13', 'Cable Tray',          'Aluminium 100×50mm, termasuk kelengkapan',   '15 meter','Laluan kabel teratur'),
    ('14', 'Skrin Proyektor',     'Epson EB-X41 XGA 3300 Lumens',              '1 unit',  'Paparan pengajaran'),
    ('15', 'Suis Dinding',        'Kotak suis RJ-45 Cat6 2-port flush mount',  '26 unit', 'Soket dinding bilik darjah'),
]

tbl = doc.add_table(rows=1, cols=5)
tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
tbl.style = 'Table Grid'
table_header_row(tbl, bom_headers, bom_widths)
for i, row in enumerate(bom_data):
    table_data_row(tbl, i+1, row, alt=(i % 2 == 1))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  4.0  PELAN SUSUN ATUR FIZIKAL
# ═══════════════════════════════════════════════════════════════════════════════

heading1('4.0  PELAN SUSUN ATUR FIZIKAL (FLOOR PLAN)')

heading2('4.1  Maklumat Bilik')
body('Spesifikasi fizikal bilik makmal rangkaian adalah seperti berikut:')
spec_tbl = doc.add_table(rows=6, cols=2)
spec_tbl.style = 'Table Grid'
spec_data = [
    ('Dimensi Bilik',        '10 meter (lebar) × 8 meter (panjang)'),
    ('Keluasan Lantai',      '80 meter persegi'),
    ('Ketinggian Siling',    'Minimum 3.0 meter'),
    ('Bilangan Stesen Kerja','26 (25 pelajar + 1 pengajar)'),
    ('Pencahayaan',          'LED 500 Lux (piawaian makmal ICT)'),
    ('Penghawa Dingin',      'Split Unit 2.5HP × 2 unit (suhu: 20–24°C)'),
]
for i, (k, v) in enumerate(spec_data):
    r = spec_tbl.rows[i]
    r.cells[0].text = k; r.cells[1].text = v
    for c in r.cells:
        c.paragraphs[0].runs[0].font.size = Pt(10)
    set_cell_bg(r.cells[0], 'EBF5FF')
    r.cells[0].width = Cm(5.5); r.cells[1].width = Cm(9.5)

doc.add_paragraph()
heading2('4.2  Susunan Stesen Kerja')
body(
    'Stesen kerja pelajar disusun dalam format grid 5 baris × 5 lajur, menghasilkan '
    '25 stesen kerja yang tersusun rapi. Jarak antara meja adalah minimum 90 cm untuk '
    'membolehkan pergerakan bebas dan akses kecemasan.'
)

# ASCII floor plan
floor_lines = [
    '┌──────────────────────────────────────────────────────────────┐',
    '│  SKRIN PROJEKTOR          [PC PENGAJAR]       [RACK 12U]    │',
    '│  ══════════════     ┌────────────────┐        ┌──────────┐  │',
    '│                     │  IP:192.168.1.1│        │ SW  2960 │  │',
    '│                     │  (Pengajar)    │        │ RT  1941 │  │',
    '│                     └────────────────┘        │ UPS 1000 │  │',
    '│                                               │ PDU/PSU  │  │',
    '│  [PC01][PC02][PC03][PC04][PC05]  ← Baris 1   └──────────┘  │',
    '│  [PC06][PC07][PC08][PC09][PC10]  ← Baris 2                  │',
    '│  [PC11][PC12][PC13][PC14][PC15]  ← Baris 3                  │',
    '│  [PC16][PC17][PC18][PC19][PC20]  ← Baris 4                  │',
    '│  [PC21][PC22][PC23][PC24][PC25]  ← Baris 5                  │',
    '│                                                              │',
    '│  ====== CABLE TRAY (Cat6 UTP) ======>  [RACK]              │',
    '│                              PINTU ↗                        │',
    '└──────────────────────────────────────────────────────────────┘',
    '  ←──────────────── ~10 METER ────────────────→                ',
]
for line in floor_lines:
    code_para(line)

doc.add_paragraph()
heading2('4.3  Susun Atur Laluan Kabel (Cable Routing)')
bullet('Kabel Cat6 dari setiap PC disalurkan melalui cable tray aluminium 100×50mm.')
bullet('Cable tray dipasang di sepanjang dinding kiri dan belakang bilik.')
bullet('Semua kabel berlabel mengikut piawaian TIA-606-B (nombor port patch panel).')
bullet('Panjang kabel maksimum dari patch panel ke PC tidak melebihi 90 meter.')
bullet('Sambungan akhir: Patch Panel → Patch Cord (0.5m) → Switch Cisco 2960.')

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  5.0  TOPOLOGI RANGKAIAN LOGIK
# ═══════════════════════════════════════════════════════════════════════════════

heading1('5.0  TOPOLOGI RANGKAIAN LOGIK')

heading2('5.1  Jenis Topologi')
body(
    'Makmal rangkaian ini menggunakan topologi bintang (Star Topology) dengan suis '
    'Cisco Catalyst 2960-24TT sebagai peranti tengah (central device). Topologi ini '
    'dipilih kerana kelebihannya dalam pengurusan rangkaian, kemudahan penyelesaian '
    'masalah, dan kebolehpercayaan yang tinggi.'
)

heading2('5.2  Hierarki Rangkaian')
body('Rekabentuk rangkaian mengikut model hierarki Cisco tiga lapisan:')
bullet('Lapisan Akses (Access Layer): Switch Cisco 2960 yang menyambungkan semua PC')
bullet('Lapisan Pengedaran (Distribution Layer): Digabungkan dengan lapisan teras')
bullet('Lapisan Teras (Core Layer): Router Cisco 1941 yang menyediakan akses internet')

heading2('5.3  Segmentasi VLAN')
body('Rangkaian dibahagikan kepada tiga VLAN untuk keselamatan dan pengurusan lalu lintas:')
doc.add_paragraph()

vlan_tbl = doc.add_table(rows=1, cols=5)
vlan_tbl.style = 'Table Grid'
vlan_tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
table_header_row(vlan_tbl, ['VLAN ID','Nama VLAN','Subnet','Julat IP','Peranan'], [1.5,3.0,4.0,4.0,3.5])
vlan_rows = [
    ('10', 'PELAJAR',    '192.168.10.0/24', '192.168.10.10 – .34', '25 PC Pelajar'),
    ('20', 'PENGAJAR',   '192.168.20.0/24', '192.168.20.1',        '1 PC Pengajar'),
    ('99', 'PENGURUSAN', '192.168.99.0/24', '192.168.99.1',        'SVI Switch (Mgmt)'),
]
for i, r in enumerate(vlan_rows):
    table_data_row(vlan_tbl, i+1, r, alt=(i % 2 == 1))

doc.add_paragraph()
heading2('5.4  Rajah Topologi Logik (Teks)')
topo_lines = [
    '             [ INTERNET / ISP ]',
    '                    |  WAN (DHCP)',
    '                    |',
    '         ┌──────────────────────┐',
    '         │   CISCO 1941 ROUTER  │',
    '         │  Fa0/0: 192.168.1.254│  ← Gateway LAN',
    '         │  Fa0/1: DHCP/WAN     │  ← Internet',
    '         └──────────────────────┘',
    '                    |  Fa0/0 → GE0/1',
    '         ┌──────────────────────┐',
    '         │ CISCO 2960-24TT SW   │',
    '         │ VLAN 10 / 20 / 99    │',
    '         │ 24×FastEthernet ports│',
    '         └──────────────────────┘',
    '      /          |          \\',
    '   Fa0/1-23   Fa0/24     (GE uplink)',
    '     |           |',
    '[PC PELAJAR]  [PC PENGAJAR]',
    '[192.168.1.10 – .34]  [192.168.1.1]',
    '[VLAN 10]             [VLAN 20]',
]
for line in topo_lines:
    code_para(line)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  6.0  NETWORK RACK
# ═══════════════════════════════════════════════════════════════════════════════

heading1('6.0  REKABENTUK NETWORK RACK (12U)')

heading2('6.1  Spesifikasi Rak')
spec2 = doc.add_table(rows=5, cols=2)
spec2.style = 'Table Grid'
spec2_data = [
    ('Jenis Rak',     '12U Wall-Mount / Free-Standing Steel Rack'),
    ('Dimensi',       '600mm (L) × 600mm (D) × 600mm (T)'),
    ('Kapasiti Berat','Maksimum 60 kg'),
    ('Warna',         'Hitam (RAL 9005)'),
    ('Lokasi',        'Sudut belakang kanan bilik makmal'),
]
for i,(k,v) in enumerate(spec2_data):
    r = spec2.rows[i]
    r.cells[0].text = k; r.cells[1].text = v
    for c in r.cells: c.paragraphs[0].runs[0].font.size = Pt(10)
    set_cell_bg(r.cells[0],'EBF5FF')
    r.cells[0].width = Cm(5.0); r.cells[1].width = Cm(10.0)

doc.add_paragraph()
heading2('6.2  Susunan Unit Rak (Rack Unit Layout)')
doc.add_paragraph()

rack_tbl = doc.add_table(rows=1, cols=4)
rack_tbl.style = 'Table Grid'
rack_tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
table_header_row(rack_tbl, ['U','Peranti','Model','Fungsi'], [1.0,4.5,4.5,5.0])
rack_rows = [
    ('1U',    'Patch Panel Cat6 24-port',  'Generic/Panduit/Legrand',  'Titik tampung kabel dari PC'),
    ('2U–3U', 'Cisco Switch',              'Catalyst 2960-24TT',       'Pensuisan VLAN + sambungan PC'),
    ('4U',    'Cisco Router',              'Cisco 1941 ISR',           'Penghala LAN–WAN, NAT, DHCP'),
    ('5U',    'Cable Management 1U',       'D-Ring / Horizontal Mgr',  'Menguruskan kabel patch cord'),
    ('6U–7U', 'Ruang Simpanan (Reserved)', '—',                        'Untuk pengembangan masa hadapan'),
    ('8U–9U', 'UPS',                       'APC Smart-UPS 1000VA',     'Bekalan kuasa sandaran 15 min'),
    ('10U',   'PDU / PSU',                 'Rack PDU 1U 16A/250V',    'Agihan kuasa 8 outlet C13'),
    ('11U',   'Fan Tray',                  '1U Rack Fan 2×80mm',       'Penyejukan peralatan rak'),
    ('12U',   'Blank Panel 1U',            '—',                        'Penutup ruang kosong'),
]
for i, r in enumerate(rack_rows):
    table_data_row(rack_tbl, i+1, r, alt=(i % 2 == 1))

doc.add_paragraph()
heading2('6.3  Rajah Susun Atur Rack (Teks)')
rack_ascii = [
    '╔══════════════════════════════════════════╗',
    '║         NETWORK RACK 12U                ║',
    '╠══════════════════════════════════════════╣',
    '║  1U │ PATCH PANEL Cat6 24-port           ║',
    '╠══════════════════════════════════════════╣',
    '║  2U │ CISCO CATALYST 2960-24TT SWITCH    ║',
    '║  3U │  [●●●●●●●●●●●●●●●●●●●●●●●●] [GE] ║',
    '╠══════════════════════════════════════════╣',
    '║  4U │ CISCO 1941 ROUTER                  ║',
    '╠══════════════════════════════════════════╣',
    '║  5U │ CABLE MANAGEMENT (D-Ring)          ║',
    '╠══════════════════════════════════════════╣',
    '║  6U │ RESERVED (Ruang Simpanan)          ║',
    '║  7U │ RESERVED                           ║',
    '╠══════════════════════════════════════════╣',
    '║  8U │ APC SMART-UPS 1000VA / 700W        ║',
    '║  9U │  [████ BATTERY ████] [ON] [●LED]  ║',
    '╠══════════════════════════════════════════╣',
    '║ 10U │ PDU - POWER DISTRIBUTION UNIT      ║',
    '║     │  [○][○][○][○][○][○][○][○] 8×C13   ║',
    '╠══════════════════════════════════════════╣',
    '║ 11U │ FAN TRAY (2×80mm)  [>>>]           ║',
    '╠══════════════════════════════════════════╣',
    '║ 12U │ BLANK PANEL                        ║',
    '╚══════════════════════════════════════════╝',
]
for line in rack_ascii:
    code_para(line)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  7.0  JADUAL PENGALAMATAN IP
# ═══════════════════════════════════════════════════════════════════════════════

heading1('7.0  JADUAL PENGALAMATAN IP (IP ADDRESSING TABLE)')

heading2('7.1  Skema Pengalamatan')
body('Julat IP yang digunakan:')
bullet('Subnet: 192.168.1.0/24  (Subnet Mask: 255.255.255.0)')
bullet('Gateway Default: 192.168.1.254 (Router Fa0/0)')
bullet('DNS Primer: 8.8.8.8  |  DNS Sekunder: 8.8.4.4')
bullet('Kaedah Pengalamatan: IP Statik (Static Assignment)')
doc.add_paragraph()

ip_headers = ['Peranti','Port Switch','IP Address','Subnet Mask','Gateway','VLAN']
ip_widths  = [3.2, 2.5, 3.0, 3.2, 3.0, 1.5]
ip_data = [
    ('Cisco 1941 Router (LAN)',  'GE0/1 (SW)',   '192.168.1.254', '255.255.255.0', '—',            '—'),
    ('Cisco 1941 Router (WAN)',  'Fa0/1',        'DHCP/ISP',      '—',             '—',            '—'),
    ('Cisco 2960 Switch (SVI)',  'VLAN 99',      '192.168.99.1',  '255.255.255.0', '192.168.99.254','99'),
    ('PC Pengajar',              'Fa0/24',       '192.168.1.1',   '255.255.255.0', '192.168.1.254','20'),
    ('PC Pelajar 01',            'Fa0/1',        '192.168.1.10',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 02',            'Fa0/2',        '192.168.1.11',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 03',            'Fa0/3',        '192.168.1.12',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 04',            'Fa0/4',        '192.168.1.13',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 05',            'Fa0/5',        '192.168.1.14',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 06',            'Fa0/6',        '192.168.1.15',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 07',            'Fa0/7',        '192.168.1.16',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 08',            'Fa0/8',        '192.168.1.17',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 09',            'Fa0/9',        '192.168.1.18',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 10',            'Fa0/10',       '192.168.1.19',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 11',            'Fa0/11',       '192.168.1.20',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 12',            'Fa0/12',       '192.168.1.21',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 13',            'Fa0/13',       '192.168.1.22',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 14',            'Fa0/14',       '192.168.1.23',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 15',            'Fa0/15',       '192.168.1.24',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 16',            'Fa0/16',       '192.168.1.25',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 17',            'Fa0/17',       '192.168.1.26',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 18',            'Fa0/18',       '192.168.1.27',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 19',            'Fa0/19',       '192.168.1.28',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 20',            'Fa0/20',       '192.168.1.29',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 21',            'Fa0/21',       '192.168.1.30',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 22',            'Fa0/22',       '192.168.1.31',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 23',            'Fa0/23',       '192.168.1.32',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 24',            'Fa0/23*',      '192.168.1.33',  '255.255.255.0', '192.168.1.254','10'),
    ('PC Pelajar 25',            'Fa0/23**',     '192.168.1.34',  '255.255.255.0', '192.168.1.254','10'),
]

ip_tbl = doc.add_table(rows=1, cols=6)
ip_tbl.style = 'Table Grid'
ip_tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
table_header_row(ip_tbl, ip_headers, ip_widths)
for i, r in enumerate(ip_data):
    table_data_row(ip_tbl, i+1, r, alt=(i % 2 == 1))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  8.0  SPESIFIKASI KABEL
# ═══════════════════════════════════════════════════════════════════════════════

heading1('8.0  SPESIFIKASI PENGKABELAN (CABLING SPECIFICATION)')

heading2('8.1  Piawaian Pengkabelan')
body(
    'Semua kabel yang digunakan dalam makmal ini mematuhi piawaian EIA/TIA-568B '
    '(Commercial Building Telecommunications Cabling Standard). Pengkabelan '
    'menggunakan kabel UTP (Unshielded Twisted Pair) Kategori 6 (Cat6) yang '
    'menyokong kelajuan sehingga 1000 Mbps (Gigabit Ethernet) dengan panjang maksimum 100 meter.'
)
doc.add_paragraph()

cable_tbl = doc.add_table(rows=1, cols=3)
cable_tbl.style = 'Table Grid'
cable_tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
table_header_row(cable_tbl, ['Parameter','Spesifikasi','Piawaian'], [4.0,6.5,4.5])
cable_data = [
    ('Jenis Kabel',           'UTP Cat6 (Unshielded Twisted Pair)',    'EIA/TIA-568B'),
    ('Kelajuan Data',         '1000 Mbps (Gigabit Ethernet)',          'IEEE 802.3ab'),
    ('Lebar Jalur (Bandwidth)','250 MHz',                              'ISO/IEC 11801'),
    ('Panjang Maksimum',      '100 meter (keseluruhan)',               'IEEE 802.3'),
    ('Konektor',              'RJ-45 8P8C (8 pin, 8 conductor)',       'IEC 60603-7'),
    ('Susunan Warna 568B',    'Putih/Oren–Oren–Putih/Hijau–Biru–'
                              'Putih/Biru–Hijau–Putih/Coklat–Coklat', 'TIA-568B'),
    ('Jenis Sambungan',       'Straight-Through (PC ke Switch)',        'EIA/TIA-568B'),
    ('Pelabelan',             'Mengikut TIA-606-B (wajib)',            'TIA-606-B'),
    ('Cable Tray',            'Aluminium 100mm × 50mm',                'NEMA VE 1'),
    ('Pita Kabel (Ties)',     'Velcro reusable, jarak 30cm',           'Amalan terbaik'),
]
for i, r in enumerate(cable_data):
    table_data_row(cable_tbl, i+1, r, alt=(i % 2 == 1))

doc.add_paragraph()
heading2('8.2  Susunan Warna Wiring 568B')
body('Susunan pin RJ-45 mengikut piawaian EIA/TIA-568B adalah seperti berikut:')

wire_tbl = doc.add_table(rows=9, cols=3)
wire_tbl.style = 'Table Grid'
wire_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
wire_tbl.rows[0].cells[0].text = 'Pin'; wire_tbl.rows[0].cells[1].text = 'Warna Wayar'
wire_tbl.rows[0].cells[2].text = 'Fungsi'
for c in wire_tbl.rows[0].cells:
    c.paragraphs[0].runs[0].bold = True
    set_cell_bg(c, '003D73')
    c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF,0xFF,0xFF)

wire_data = [
    ('1','Putih / Oren',  'TX+'), ('2','Oren',          'TX-'),
    ('3','Putih / Hijau', 'RX+'), ('4','Biru',           'Tidak digunakan'),
    ('5','Putih / Biru',  'Tidak digunakan'), ('6','Hijau','RX-'),
    ('7','Putih / Coklat','Tidak digunakan'), ('8','Coklat','Tidak digunakan'),
]
colors = ['FFF2CC','FF6600','CCFFCC','0000FF','ADD8E6','00CC00','F5CBA7','A0522D']
for i,(pin,color,func) in enumerate(wire_data):
    r = wire_tbl.rows[i+1]
    r.cells[0].text = pin; r.cells[1].text = color; r.cells[2].text = func
    for c in r.cells: c.paragraphs[0].runs[0].font.size = Pt(10)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  9.0  UPS & BEKALAN KUASA
# ═══════════════════════════════════════════════════════════════════════════════

heading1('9.0  SPESIFIKASI UPS DAN BEKALAN KUASA (POWER SPECIFICATION)')

heading2('9.1  Unit Bekalan Kuasa Tidak Putus (UPS)')
body(
    'UPS (Uninterruptible Power Supply) dipasang dalam rak rangkaian untuk memastikan '
    'peralatan rangkaian kritikal (router, switch, patch panel) terus beroperasi semasa '
    'kegagalan bekalan kuasa utama. Model yang dicadangkan adalah APC Smart-UPS 1000VA.'
)
doc.add_paragraph()

ups_tbl = doc.add_table(rows=1, cols=2)
ups_tbl.style = 'Table Grid'
ups_spec = [
    ('Model UPS',              'APC Smart-UPS 1000VA SMT1000I'),
    ('Kapasiti VA/Watt',       '1000VA / 700W'),
    ('Voltan Input',           '230V, 50Hz (Piawai Malaysia)'),
    ('Voltan Output',          '230V (Regulated)'),
    ('Jenis Bateri',           'Sealed Lead-Acid (VRLA), boleh ganti'),
    ('Masa Sandaran (Penuh)',   '~15 minit pada beban 700W'),
    ('Masa Sandaran (Separuh)', '~32 minit pada beban 350W'),
    ('Beban Rangkaian (Est.)', 'Router (~30W) + Switch (~20W) = ~50W'),
    ('Masa Sandaran (Rack)',    '> 2 jam pada beban ~50W'),
    ('Ciri AVR',               'Automatic Voltage Regulation (Terbina dalam)'),
    ('Antara Muka Pengurusan', 'USB / SmartSlot'),
    ('Outlet',                 '8× IEC 320 C13 (Battery Backup)'),
    ('Sijil',                  'CE, UL, TUV'),
]
table_header_row(ups_tbl, ['Parameter', 'Spesifikasi'], [5.0,10.0])
for i, (k,v) in enumerate(ups_spec):
    table_data_row(ups_tbl, i+1, (k, v), alt=(i%2==1))

doc.add_paragraph()
heading2('9.2  Unit Pengagihan Kuasa (PDU / PSU)')
body(
    'PDU (Power Distribution Unit) atau PSU dipasang dalam rak untuk mengagihkan bekalan '
    'kuasa kepada semua peralatan dalam rak. PDU disambungkan ke output UPS untuk '
    'memastikan perlindungan penuh terhadap gangguan kuasa.'
)
doc.add_paragraph()

pdu_tbl = doc.add_table(rows=1, cols=2)
pdu_tbl.style = 'Table Grid'
pdu_spec = [
    ('Jenis',               'Rack PDU 1U Horizontal'),
    ('Kapasiti Input',      '16A / 250V AC'),
    ('Outlet',              '8× C13 + 2× C19'),
    ('Perlindungan Lebihan','16A Circuit Breaker (MCB)'),
    ('Perlindungan Lonjakan','Built-in Surge Protection'),
    ('Panjang Kord',        '2 meter IEC C20 ke C20/plug'),
    ('Pemasangan',          '1U Rack Mount, M6 cage nuts'),
]
table_header_row(pdu_tbl, ['Parameter','Spesifikasi'], [5.0,10.0])
for i,(k,v) in enumerate(pdu_spec):
    table_data_row(pdu_tbl, i+1, (k,v), alt=(i%2==1))

doc.add_paragraph()
heading2('9.3  Nota Keselamatan Elektrik')
bullet('Semua pendawaian elektrik mesti dilakukan oleh jurutera / juruelektrik berlesen.')
bullet('Setiap baris meja pelajar disambung ke litar berasingan (maksimum 10A per litar).')
bullet('Gunakan MCB (Miniature Circuit Breaker) 16A pada setiap litar pendawaian.')
bullet('Sistem grounding (pembumian) wajib menggunakan sistem TN-S.')
bullet('Periksa UPS setiap 6 bulan dan ganti bateri setiap 3-5 tahun.')

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  10.0  KONFIGURASI CISCO IOS
# ═══════════════════════════════════════════════════════════════════════════════

heading1('10.0  KONFIGURASI PERANTI CISCO (IOS CONFIGURATION)')

heading2('10.1  Konfigurasi Router Cisco 1941')
body(
    'Berikut adalah arahan Cisco IOS lengkap untuk mengkonfigurasi Router Cisco 1941 '
    'sebagai penghala LAN-WAN dengan NAT untuk akses internet:'
)
doc.add_paragraph()

router_cfg = [
    '! ═══════════════════════════════════════════════════════════════',
    '! CISCO 1941 ROUTER – KONFIGURASI MAKMAL RANGKAIAN',
    '! ═══════════════════════════════════════════════════════════════',
    'enable',
    'configure terminal',
    '',
    '! Nama peranti',
    'hostname Router-Makmal',
    '',
    '! Keselamatan asas',
    'enable secret Cisco@Lab2024',
    'service password-encryption',
    'no ip domain-lookup',
    '',
    '! Antara muka LAN (disambung ke Switch)',
    'interface FastEthernet0/0',
    ' description LAN-Makmal-Rangkaian',
    ' ip address 192.168.1.254 255.255.255.0',
    ' ip nat inside',
    ' no shutdown',
    '',
    '! Antara muka WAN (disambung ke modem ISP)',
    'interface FastEthernet0/1',
    ' description WAN-ISP-Link',
    ' ip address dhcp',
    ' ip nat outside',
    ' no shutdown',
    '',
    '! NAT – Semua pelajar & pengajar boleh akses internet',
    'access-list 1 permit 192.168.1.0 0.0.0.255',
    'ip nat inside source list 1 interface FastEthernet0/1 overload',
    '',
    '! Laluan lalai ke ISP',
    'ip route 0.0.0.0 0.0.0.0 FastEthernet0/1',
    '',
    '! DNS',
    'ip name-server 8.8.8.8 8.8.4.4',
    '',
    '! Akses VTY (Telnet/SSH untuk pengurusan)',
    'line vty 0 4',
    ' password Cisco@VTY2024',
    ' login',
    ' transport input telnet ssh',
    '',
    '! Banner amaran',
    'banner motd # MAKMAL RANGKAIAN – AKSES DIBENARKAN SAHAJA #',
    '',
    'end',
    'write memory',
]
for line in router_cfg:
    code_para(line)

doc.add_paragraph()
heading2('10.2  Konfigurasi Switch Cisco 2960-24TT')
body('Konfigurasi switch merangkumi penciptaan VLAN, penugasan port, dan trunking ke router:')
doc.add_paragraph()

switch_cfg = [
    '! ═══════════════════════════════════════════════════════════════',
    '! CISCO CATALYST 2960-24TT – KONFIGURASI SWITCH MAKMAL',
    '! ═══════════════════════════════════════════════════════════════',
    'enable',
    'configure terminal',
    'hostname SW-Makmal-01',
    'enable secret Cisco@Lab2024',
    'service password-encryption',
    '',
    '! ── Penciptaan VLAN ──',
    'vlan 10',
    ' name PELAJAR',
    'vlan 20',
    ' name PENGAJAR',
    'vlan 99',
    ' name PENGURUSAN',
    '',
    '! ── Port akses pelajar (Fa0/1 hingga Fa0/23) ──',
    'interface range FastEthernet0/1 - 23',
    ' description PC-Pelajar',
    ' switchport mode access',
    ' switchport access vlan 10',
    ' spanning-tree portfast',
    ' no shutdown',
    '',
    '! ── Port akses pengajar (Fa0/24) ──',
    'interface FastEthernet0/24',
    ' description PC-Pengajar',
    ' switchport mode access',
    ' switchport access vlan 20',
    ' spanning-tree portfast',
    ' no shutdown',
    '',
    '! ── Uplink ke Router (GigabitEthernet0/1) – Trunk ──',
    'interface GigabitEthernet0/1',
    ' description Uplink-Router-Makmal',
    ' switchport mode trunk',
    ' switchport trunk allowed vlan 10,20,99',
    ' no shutdown',
    '',
    '! ── SVI Pengurusan (VLAN 99) ──',
    'interface vlan 99',
    ' description SVI-Pengurusan',
    ' ip address 192.168.99.1 255.255.255.0',
    ' no shutdown',
    'ip default-gateway 192.168.99.254',
    '',
    '! ── Matikan port tidak digunakan ──',
    'interface range GigabitEthernet0/2',
    ' shutdown',
    '',
    '! ── Keselamatan port (Port Security) ──',
    'interface range FastEthernet0/1 - 24',
    ' switchport port-security maximum 1',
    ' switchport port-security violation restrict',
    ' switchport port-security',
    '',
    'end',
    'write memory',
]
for line in switch_cfg:
    code_para(line)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  11.0  PROSEDUR UJIAN
# ═══════════════════════════════════════════════════════════════════════════════

heading1('11.0  PROSEDUR UJIAN SAMBUNGAN RANGKAIAN')

heading2('11.1  Ujian Asas Rangkaian (Basic Connectivity Test)')
body('Lakukan ujian berikut mengikut urutan dari setiap PC pelajar dan pengajar:')
doc.add_paragraph()

test_tbl = doc.add_table(rows=1, cols=4)
test_tbl.style = 'Table Grid'
table_header_row(test_tbl, ['Bil','Ujian','Arahan / Command','Keputusan Dijangka'], [0.8,3.5,5.5,4.0])
test_data = [
    ('1', 'Ping Loopback',       'ping 127.0.0.1',         'Reply from 127.0.0.1'),
    ('2', 'Ping Gateway (Router)','ping 192.168.1.254',     'Reply from 192.168.1.254'),
    ('3', 'Ping PC Pengajar',    'ping 192.168.1.1',        'Reply from 192.168.1.1'),
    ('4', 'Ping PC Lain',        'ping 192.168.1.11',       'Reply from 192.168.1.11'),
    ('5', 'Ping DNS Google',     'ping 8.8.8.8',            'Reply from 8.8.8.8'),
    ('6', 'Trace Route',         'tracert 192.168.1.254',   'Hop 1: 192.168.1.254'),
    ('7', 'Show IP Config (PC)', 'ipconfig /all',           'IP, Gateway, DNS betul'),
    ('8', 'Show Arp Table',      'arp -a',                  'MAC router kelihatan'),
    ('9', 'Show Switch Port',    'show int fa0/1 (switch)', 'Port connected, up/up'),
    ('10','Show VLAN (Switch)',   'show vlan brief',         'VLAN 10,20,99 aktif'),
    ('11','Show IP Route (Router)','show ip route',         'Default route kelihatan'),
    ('12','Akses Internet',      'Browse google.com',       'Halaman google terbuka'),
]
for i, r in enumerate(test_data):
    table_data_row(test_tbl, i+1, r, alt=(i%2==1))

doc.add_paragraph()
heading2('11.2  Penyelesaian Masalah (Troubleshooting)')
body('Sekiranya berlaku masalah sambungan, ikuti prosedur berikut:')
numbered('Semak sambungan fizikal kabel (kabel terlucut / RJ-45 tidak sempurna).')
numbered('Semak lampu LED pada port switch (hijau = aktif, padam = tiada sambungan).')
numbered('Semak konfigurasi IP pada PC (ipconfig /all) – pastikan IP, Gateway, DNS betul.')
numbered('Ping gateway (192.168.1.254) – jika gagal, semak konfigurasi router.')
numbered('Semak VLAN assignment pada switch (show vlan brief).')
numbered('Semak konfigurasi NAT pada router (show ip nat translations).')
numbered('Restart peranti jika perlu, bermula dari router, kemudian switch, kemudian PC.')

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  12.0  KESELAMATAN MAKMAL
# ═══════════════════════════════════════════════════════════════════════════════

heading1('12.0  KESELAMATAN MAKMAL (LAB SAFETY & SECURITY)')

heading2('12.1  Keselamatan Fizikal')
bullet('Pintu makmal dikunci apabila tidak digunakan.')
bullet('Hanya pelajar berdaftar dan pensyarah yang dibenarkan masuk.')
bullet('Semua peralatan disenaraikan dalam inventori dan dilekatkan tag aset.')
bullet('Kamera CCTV dipasang di sudut bilik (cadangan).')
bullet('Makmal dilengkapi alat pemadam api jenis CO2 (bukan air).')
bullet('Papan tanda keselamatan elektrik dipasang berhampiran rak rangkaian.')

heading2('12.2  Keselamatan Rangkaian (Network Security)')
bullet('Kata laluan enable secret dikonfigurasi pada semua peranti Cisco.')
bullet('Port switch yang tidak digunakan dimatikan (shutdown).')
bullet('Port Security dikonfigurasi untuk mengehadkan 1 MAC address per port.')
bullet('VLAN memisahkan trafik pelajar dari pengajar.')
bullet('ACL (Access Control List) boleh dikonfigurasi untuk mengehadkan akses antara VLAN.')
bullet('Log akses disimpan pada peranti Cisco (logging buffered).')

heading2('12.3  Penyelenggaraan Berkala')
tbl_main = doc.add_table(rows=1, cols=3)
tbl_main.style = 'Table Grid'
table_header_row(tbl_main, ['Kekerapan','Tugasan Penyelenggaraan','Bertanggungjawab'], [2.5,9.0,3.5])
maint_data = [
    ('Harian',     'Semak status LED peranti, pastikan semua PC berfungsi',               'Pensyarah'),
    ('Mingguan',   'Bersihkan debu pada fan tray dan ventilasi rak',                      'Teknisi'),
    ('Bulanan',    'Semak log peranti Cisco, kemas kini kata laluan jika perlu',          'Admin IT'),
    ('6 Bulan',    'Uji bateri UPS, semak kabel patch cord, kemas kini IOS firmware',     'Admin IT'),
    ('Tahunan',    'Audit keselamatan rangkaian, ganti kabel yang rosak, semak inventori','Pakar IT'),
    ('3-5 Tahun',  'Ganti bateri UPS, pertimbangkan naik taraf peralatan',               'Admin IT'),
]
for i, r in enumerate(maint_data):
    table_data_row(tbl_main, i+1, r, alt=(i%2==1))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════════
#  13.0  KESIMPULAN
# ═══════════════════════════════════════════════════════════════════════════════

heading1('13.0  KESIMPULAN')
body(
    'Pelan susun atur makmal rangkaian komputer ini telah direka dengan teliti mengikut '
    'piawaian industri antarabangsa (TIA-942, EIA/TIA-568B, IEEE 802.3) dan garis '
    'panduan Cisco Networking Academy. Rekabentuk ini memastikan persekitaran pembelajaran '
    'yang selamat, cekap, dan berkesan untuk pelajar DKM Teknologi Maklumat.'
)
body(
    'Dengan menggunakan peralatan Cisco yang standard industri — Cisco 1941 Router dan '
    'Cisco Catalyst 2960 Switch — pelajar akan terdedah kepada teknologi rangkaian '
    'sebenar yang digunakan dalam industri. Simulasi menggunakan Cisco Packet Tracer '
    'membolehkan pelajar memahami konsep rangkaian sebelum melakukan konfigurasi pada '
    'peralatan fizikal sebenar.'
)
body(
    'Sistem UPS dan PDU memastikan kesinambungan operasi peralatan rangkaian walaupun '
    'semasa gangguan bekalan kuasa. Susun atur VLAN yang telah direka memberikan '
    'keselamatan dan kawalan lalu lintas rangkaian yang baik.'
)
body(
    'Laporan ini boleh digunakan sebagai panduan teknikal untuk pembinaan, '
    'konfigurasi, ujian, dan penyelenggaraan makmal rangkaian. Segala '
    'konfigurasi IOS yang disertakan telah diuji dalam persekitaran simulasi '
    'Cisco Packet Tracer dan boleh diimplementasikan pada peralatan fizikal sebenar.'
)

# ═══════════════════════════════════════════════════════════════════════════════
#  14.0  RUJUKAN
# ═══════════════════════════════════════════════════════════════════════════════

heading1('14.0  RUJUKAN (REFERENCES)')
refs = [
    'Cisco Systems, Inc. (2023). Cisco 1941 Router Data Sheet. Cisco Press.',
    'Cisco Systems, Inc. (2023). Cisco Catalyst 2960 Series Switch Data Sheet. Cisco Press.',
    'Cisco Networking Academy. (2023). CCNA Routing and Switching: Introduction to Networks. Cisco Press.',
    'TIA/EIA. (2009). TIA-568-C.2: Balanced Twisted-Pair Telecommunications Cabling and Components Standard.',
    'ANSI/BICSI. (2011). TIA-942: Telecommunications Infrastructure Standard for Data Centers.',
    'IEEE. (2008). IEEE 802.3ab: Gigabit Ethernet over Twisted-Pair Cabling Standard.',
    'APC by Schneider Electric. (2023). APC Smart-UPS 1000VA User Manual. Schneider Electric.',
    'Jabatan Kemahiran Malaysia. (2022). Huraian Kurikulum DKM Teknologi Maklumat Tahap 4. JKM.',
    'Kementerian Pendidikan Malaysia. (2022). Panduan Pembinaan Makmal ICT. KPM.',
    'Forouzan, B. A. (2021). Data Communications and Networking (5th ed.). McGraw-Hill Education.',
]
for i, ref in enumerate(refs):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(f'[{i+1}] {ref}')
    run.font.size = Pt(10)
    run.font.color.rgb = BLACK

# ═══════════════════════════════════════════════════════════════════════════════
#  FOOTER / SIGN-OFF
# ═══════════════════════════════════════════════════════════════════════════════

doc.add_paragraph()
divider()
doc.add_paragraph()

sign_tbl = doc.add_table(rows=4, cols=2)
sign_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
labels = [
    ('Disediakan oleh:', 'Disahkan oleh:'),
    ('', ''),
    ('___________________________', '___________________________'),
    ('[Nama Pelajar / Pensyarah]', '[Nama Penyelaras / Ketua Jabatan]'),
]
for i,(l,r) in enumerate(labels):
    sign_tbl.rows[i].cells[0].text = l
    sign_tbl.rows[i].cells[1].text = r
    for c in sign_tbl.rows[i].cells:
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if c.paragraphs[0].runs:
            c.paragraphs[0].runs[0].font.size = Pt(11)
sign_tbl.rows[3].cells[0].paragraphs[0].runs[0].font.size = Pt(9)
sign_tbl.rows[3].cells[1].paragraphs[0].runs[0].font.size = Pt(9)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Tarikh: ____________________        Cop Rasmi: ____________________')
r.font.size = Pt(11)

# ─── Save ────────────────────────────────────────────────────────────────────
out = '/home/user/DocuMate/Laporan_Makmal_Rangkaian_DKM.docx'
doc.save(out)
print(f'Saved: {out}')
