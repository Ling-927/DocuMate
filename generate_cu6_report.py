"""
LAPORAN TUGASAN CU6: NETWORK CABLING MANAGEMENT
Full Word document – all 6 sections, max 10 pages
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

OUT  = '/home/user/DocuMate/Laporan_Tugasan_CU6.docx'
IMGS = '/home/user/DocuMate/images'

# ── colours ───────────────────────────────────────────────────────────────────
DARK  = RGBColor(0x00,0x3D,0x73)
BLUE  = RGBColor(0x00,0x54,0x9F)
BLACK = RGBColor(0x00,0x00,0x00)
GRAY  = RGBColor(0x71,0x80,0x96)
WHITE = RGBColor(0xFF,0xFF,0xFF)
GREEN = RGBColor(0x27,0x67,0x49)
ORANGE= RGBColor(0xC0,0x50,0x11)

doc = Document()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE SETUP  (A4 portrait default)
# ══════════════════════════════════════════════════════════════════════════════
def set_portrait(section):
    section.page_width    = Cm(21.0)
    section.page_height   = Cm(29.7)
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.0)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.0)
    section.orientation   = WD_ORIENT.PORTRAIT

def set_landscape(section):
    section.page_width    = Cm(29.7)
    section.page_height   = Cm(21.0)
    section.top_margin    = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin   = Cm(2.0)
    section.right_margin  = Cm(2.0)
    section.orientation   = WD_ORIENT.LANDSCAPE

set_portrait(doc.sections[0])

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def cell_bg(cell, hex6):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),  'clear')
    shd.set(qn('w:color'),'auto')
    shd.set(qn('w:fill'), hex6)
    tcPr.append(shd)

def cell_borders(cell, color='AAAAAA', sz='4'):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBd = OxmlElement('w:tcBorders')
    for side in ('top','left','bottom','right'):
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'),  'single')
        el.set(qn('w:sz'),   sz)
        el.set(qn('w:color'),color)
        tcBd.append(el)
    tcPr.append(tcBd)

def h_border(p, color='00549F', sz='6'):
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'),  'single')
    bot.set(qn('w:sz'),   sz)
    bot.set(qn('w:color'),color)
    pBdr.append(bot)
    pPr.append(pBdr)

def heading1(text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True; run.font.size = Pt(13); run.font.color.rgb = DARK
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after  = Pt(5)
    h_border(p, '00549F', '8')
    return p

def heading2(text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True; run.font.size = Pt(11.5); run.font.color.rgb = BLUE
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    return p

def body(text, justify=True, size=11):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size); run.font.color.rgb = BLACK
    p.paragraph_format.space_after  = Pt(5)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

def bullet(text, size=11):
    p   = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size = Pt(size); run.font.color.rgb = BLACK
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.8)
    return p

def figure(img_path, caption, width_cm=15.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)
    p.add_run().add_picture(img_path, width=Cm(width_cm))
    pc = doc.add_paragraph()
    pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pc.paragraph_format.space_after = Pt(10)
    rc = pc.add_run(caption)
    rc.italic = True; rc.bold = True
    rc.font.size = Pt(9); rc.font.color.rgb = DARK
    h_border(pc, '00549F', '4')

def make_table(headers, rows, col_widths, head_color='00549F',
               alt_color='EBF5FF', font_size=9.5):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.style     = 'Table Grid'
    # header
    hrow = tbl.rows[0]
    for i,(h,w) in enumerate(zip(headers,col_widths)):
        c = hrow.cells[i]
        c.text = ''
        p = c.paragraphs[0]; r = p.add_run(h)
        r.bold=True; r.font.size=Pt(font_size); r.font.color.rgb=WHITE
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell_bg(c, head_color)
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        c.width = Cm(w)
    # data rows
    for ri, row in enumerate(rows):
        dr = tbl.add_row()
        bg = alt_color if ri%2==1 else 'FFFFFF'
        for j, val in enumerate(row):
            c = dr.cells[j]
            c.text = ''
            p = c.paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(font_size); r.font.color.rgb = BLACK
            cell_bg(c, bg)
            c.width = Cm(col_widths[j])
    return tbl

def spacer(n=1):
    for _ in range(n):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)

def page_break():
    doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  COVER PAGE
# ══════════════════════════════════════════════════════════════════════════════
spacer(2)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('LAPORAN TUGASAN CU6')
r.bold=True; r.font.size=Pt(22); r.font.color.rgb=DARK

p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('NETWORK CABLING MANAGEMENT')
r.bold=True; r.font.size=Pt(18); r.font.color.rgb=BLUE

spacer(1)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('Makmal Rangkaian Komputer  |  Topologi Bintang (Star Topology)')
r.font.size=Pt(12); r.font.color.rgb=GRAY; r.italic=True

spacer(3)
info=[
    ('Program',        'Diploma Kemahiran Malaysia (DKM) Tahap 4'),
    ('Bidang',         'Teknologi Maklumat & Komunikasi (ICT)'),
    ('Mata Pelajaran', 'Network Cabling Management (CU6)'),
    ('Institusi',      '[Nama Kolej Komuniti / Institut Kemahiran]'),
    ('Tarikh Hantar',  '________________'),
    ('Nama Pelajar',   '________________'),
    ('No. Matrik',     '________________'),
    ('Pensyarah',      '________________'),
]
itbl=doc.add_table(rows=len(info),cols=2)
itbl.alignment=WD_TABLE_ALIGNMENT.CENTER
for i,(k,v) in enumerate(info):
    itbl.rows[i].cells[0].text=''; itbl.rows[i].cells[1].text=''
    r0=itbl.rows[i].cells[0].paragraphs[0].add_run(k+' :')
    r0.bold=True; r0.font.size=Pt(11)
    r1=itbl.rows[i].cells[1].paragraphs[0].add_run(v)
    r1.font.size=Pt(11)
    cell_bg(itbl.rows[i].cells[0],'EBF5FF')
    itbl.rows[i].cells[0].width=Cm(5.5)
    itbl.rows[i].cells[1].width=Cm(9.5)

page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  BAHAGIAN 1 – PENGENALAN  (1 muka surat penuh)
# ══════════════════════════════════════════════════════════════════════════════
heading1('1.0  PENGENALAN KEPADA PEMBANGUNAN MAKMAL RANGKAIAN')

body(
    'Makmal rangkaian komputer merupakan kemudahan penting dalam institusi pendidikan '
    'teknikal dan vokasional, khususnya bagi program Diploma Kemahiran Malaysia (DKM) '
    'dalam bidang Teknologi Maklumat dan Komunikasi. Tujuan utama pembangunan makmal '
    'rangkaian ini adalah untuk menyediakan persekitaran pembelajaran praktikal yang '
    'membolehkan pelajar menguasai kemahiran konfigurasi rangkaian, pengurusan kabel, '
    'dan penyelesaian masalah rangkaian secara langsung menggunakan peralatan Cisco '
    'yang digunakan dalam industri. Makmal ini menempatkan 25 stesen kerja pelajar '
    'dan satu stesen kerja pengajar, semuanya disambungkan melalui infrastruktur '
    'rangkaian yang terancang dan berstruktur.'
)

body(
    'Sebelum makmal rangkaian ini wujud, pelajar terpaksa bergantung sepenuhnya kepada '
    'perisian simulasi seperti Cisco Packet Tracer untuk memahami konsep rangkaian. '
    'Pendekatan ini terbukti tidak mencukupi kerana pelajar tidak mendapat pendedahan '
    'kepada cabaran sebenar seperti pemasangan kabel fizikal, konfigurasi peralatan '
    'rangkaian sebenar, dan penyelesaian masalah pada peralatan Cisco. Selain itu, '
    'tiada prasarana yang membolehkan pelajar berlatih secara berkumpulan dalam '
    'persekitaran rangkaian yang realistik, menyebabkan jurang yang ketara antara '
    'teori yang dipelajari di dalam kelas dan keperluan industri sebenar.'
)

body(
    'Pengurusan kabel memainkan peranan kritikal dalam memastikan kebolehpercayaan '
    'dan prestasi makmal rangkaian. Kabel yang tidak terurus bukan sahaja menjejaskan '
    'estetika makmal, malah boleh menyebabkan gangguan sambungan, kesukaran dalam '
    'penyelenggaraan, dan risiko keselamatan. Oleh itu, makmal ini direka dengan '
    'menggunakan sistem cable tray aluminium yang dipasang di sepanjang dinding bagi '
    'menyalurkan semua kabel UTP Kategori 6 (Cat6) secara teratur dari setiap stesen '
    'kerja ke patch panel dalam rak rangkaian. Setiap kabel dilabelkan mengikut '
    'piawaian TIA-606-B untuk memudahkan pengenalpastian dan penyelenggaraan. '
    'Patch cord pendek (0.5 meter) digunakan untuk menyambungkan patch panel ke '
    'switch Cisco, manakala kabel panjang (antara 5 hingga 15 meter) digunakan '
    'untuk sambungan dari stesen kerja ke patch panel.'
)

body(
    'Susun atur kabel yang digunakan dalam makmal ini mengikut kaedah structured '
    'cabling (pengkabelan berstruktur) berdasarkan piawaian EIA/TIA-568B. Semua kabel '
    'UTP Cat6 straight-through dipasang menggunakan teknik kabel terbaring (horizontal '
    'cabling) di mana kabel disalurkan secara mendatar di atas meja dan kemudiannya '
    'diarahkan melalui cable tray yang dipasang secara menegak di sepanjang dinding '
    'kanan bilik sebelum disambungkan ke patch panel dalam rak rangkaian 12U. '
    'Jarak minimum antara stesen kerja dikekalkan pada 90 sentimeter bagi memastikan '
    'keselesaan dan keselamatan pelajar semasa sesi pembelajaran.'
)

body(
    'Topologi yang digunakan dalam makmal rangkaian ini ialah Topologi Bintang '
    '(Star Topology). Dalam topologi ini, switch Cisco Catalyst 2960-24TT berfungsi '
    'sebagai peranti pusat (central device) atau "pusat bintang" di mana semua 26 '
    'stesen kerja, termasuk 25 komputer pelajar dan satu komputer pengajar, '
    'disambungkan secara langsung menggunakan kabel UTP Cat6. Topologi bintang '
    'dipilih kerana beberapa kelebihan utama: pertama, jika berlaku kerosakan pada '
    'kabel atau stesen kerja, hanya stesen kerja tersebut yang terjejas manakala '
    'stesen kerja lain terus berfungsi tanpa gangguan; kedua, mudah untuk mengesan '
    'masalah (troubleshoot) dengan memeriksa port switch secara individu; ketiga, '
    'prestasi rangkaian adalah lebih tinggi kerana setiap stesen kerja mempunyai '
    'jalur lebar (bandwidth) yang tidak dikongsi; dan keempat, senang untuk '
    'menambah atau mengurangkan bilangan stesen kerja pada masa hadapan. '
    'Router Cisco 1941 pula berfungsi sebagai pintu keluar (default gateway) yang '
    'menghubungkan rangkaian LAN makmal ke internet melalui protokol NAT (Network '
    'Address Translation), membolehkan semua stesen kerja mengakses internet '
    'menggunakan satu alamat IP awam.'
)

page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  BAHAGIAN 2 – JADUAL PEMBANGUNAN
# ══════════════════════════════════════════════════════════════════════════════
heading1('2.0  JADUAL PEMBANGUNAN MAKMAL RANGKAIAN')

# 2.1 Floor plan
heading2('2.1  Pelan Lantai dan Rekabentuk Struktur Makmal Rangkaian')
body('Rajah berikut menunjukkan pelan lantai penuh makmal rangkaian bersaiz 10m × 8m '
     'dengan susun atur topologi bintang. Semua 25 PC pelajar disusun dalam '
     'format 5 baris × 5 lajur, dengan laluan kabel Cat6 melalui cable tray ke '
     'Network Rack 12U di sudut belakang kanan.', justify=True)
spacer()
figure(f'{IMGS}/cu6_tajuk2_floor_plan.png',
       'Rajah 2.1: Pelan Lantai Makmal Rangkaian – Topologi Bintang (Star Topology) | 25 PC Pelajar + 1 PC Pengajar',
       width_cm=16.5)

spacer()
# 2.2 Hardware specs
heading2('2.2  Senarai Spesifikasi Perkakasan Rangkaian dan Infrastruktur Rak')
hw_headers=['Perkakasan','Spesifikasi Teknikal','Lokasi dalam Rak']
hw_widths=[4.5,8.5,3.5]
hw_rows=[
    ('Cisco 1941 Router',         '2× FastEthernet, IOS 15.x, 512MB RAM, NAT/PAT',        '4U'),
    ('Cisco 2960-24TT Switch',    '24× FE 10/100, 2× GE Uplink, VLAN, STP, PoE',          '2U–3U'),
    ('Patch Panel Cat6 24-port',  'Cat6 568B, 110-punchdown, 1U',                          '1U'),
    ('APC Smart-UPS 1000VA',      '700W, Lead-Acid VRLA, AVR, USB mgmt, ~15min backup',    '8U–9U'),
    ('Rack PDU 1U (PSU)',         '16A/250V, 8× C13, surge protection, MCB',               '10U'),
    ('Fan Tray 1U',               '2× 80mm, 1500 RPM, cooling',                            '11U'),
    ('Cable Management 1U',       'D-Ring horizontal, Velcro ties',                        '5U'),
    ('Network Rack 12U',          '600×600×600mm, steel, wall-mount/free-stand, 60kg max', 'Rack'),
]
make_table(hw_headers,hw_rows,hw_widths)
spacer()

# 2.3 Work schedule
heading2('2.3  Jadual Pelaksanaan Kerja Makmal Rangkaian')
ws_headers=['Bil','Aktiviti / Kerja','Tempoh','Minggu','Status']
ws_widths=[0.8,7.0,2.5,2.5,3.0]
ws_rows=[
    ('1','Perancangan dan lukisan pelan lantai makmal',                '2 hari','Minggu 1','✔ Selesai'),
    ('2','Perolehan peralatan rangkaian dan bahan kabel',              '3 hari','Minggu 1','✔ Selesai'),
    ('3','Pemasangan rak rangkaian (network rack) 12U',                '1 hari','Minggu 2','✔ Selesai'),
    ('4','Pemasangan cable tray dan pendawaian dinding',               '2 hari','Minggu 2','✔ Selesai'),
    ('5','Penghantaran dan pemasangan 25 PC pelajar + 1 PC pengajar',  '2 hari','Minggu 3','✔ Selesai'),
    ('6','Pemasangan kabel UTP Cat6 dan crimp RJ-45',                  '3 hari','Minggu 3','✔ Selesai'),
    ('7','Punchdown patch panel dan pelabelan kabel (TIA-606-B)',       '1 hari','Minggu 4','✔ Selesai'),
    ('8','Konfigurasi Router Cisco 1941 (NAT, routing)',               '1 hari','Minggu 4','✔ Selesai'),
    ('9','Konfigurasi Switch Cisco 2960 (VLAN, port security)',        '1 hari','Minggu 4','✔ Selesai'),
    ('10','Penetapan alamat IP statik pada setiap PC',                 '1 hari','Minggu 5','✔ Selesai'),
    ('11','Ujian sambungan rangkaian (ping test, internet test)',       '1 hari','Minggu 5','✔ Selesai'),
    ('12','Dokumentasi akhir dan penyerahan laporan',                  '2 hari','Minggu 5','✔ Selesai'),
]
make_table(ws_headers,ws_rows,ws_widths)
spacer()

# 2.4 Label scheme
heading2('2.4  Jadual Skema Pelabelan (Labeling Scheme)')
lb_headers=['Kod Label','Peranti / Kabel','Contoh Label','Piawaian']
lb_widths=[2.5,4.5,4.0,4.5]
lb_rows=[
    ('SW-01',    'Switch Cisco 2960',        'SW-01-MAKMAL',       'TIA-606-B'),
    ('RT-01',    'Router Cisco 1941',        'RT-01-MAKMAL',       'TIA-606-B'),
    ('PP-01',    'Patch Panel 24-port',      'PP-01-PORT01–24',    'TIA-606-B'),
    ('PC-01..25','PC Pelajar 1 hingga 25',   'PC-01 / PC-25',      'TIA-606-B'),
    ('PCG-01',   'PC Pengajar',              'PCG-01-PENGAJAR',    'TIA-606-B'),
    ('CAB-01..26','Kabel UTP Cat6 per stesen','CAB-01 (PC-01→PP1)','TIA-606-B'),
    ('VLAN-10',  'VLAN Pelajar',             'VLAN10-PELAJAR',     'IEEE 802.1Q'),
    ('VLAN-20',  'VLAN Pengajar',            'VLAN20-PENGAJAR',    'IEEE 802.1Q'),
    ('VLAN-99',  'VLAN Pengurusan',          'VLAN99-MGMT',        'IEEE 802.1Q'),
]
make_table(lb_headers,lb_rows,lb_widths)

page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  BAHAGIAN 3 – SENARAI PERALATAN DAN PERISIAN
# ══════════════════════════════════════════════════════════════════════════════
heading1('3.0  SENARAI PERALATAN DAN PERISIAN YANG DIGUNAKAN')
body('Jadual berikut menyenaraikan semua peralatan, perisian dan bahan yang '
     'digunakan dalam pembangunan makmal rangkaian, diasingkan mengikut kategori.')
spacer()

eq_headers=['Kategori','Nama','Spesifikasi','Kuantiti','Fungsi']
eq_widths=[2.2,3.8,5.8,1.5,3.5]
eq_rows=[
    # PERALATAN
    ('PERALATAN','Cisco 1941 Router',         '2× FastEthernet, IOS 15.x',        '1 unit', 'Penghala LAN–WAN, NAT'),
    ('PERALATAN','Cisco Catalyst 2960-24TT',  '24×FE, 2×GE, VLAN support',        '1 unit', 'Suis pusat topologi bintang'),
    ('PERALATAN','Patch Panel Cat6 24-port',  '1U, 568B, 110-punchdown',           '1 unit', 'Titik tampung kabel'),
    ('PERALATAN','Network Rack 12U',          '600×600×600mm, steel',              '1 unit', 'Menempatkan peralatan'),
    ('PERALATAN','APC Smart-UPS 1000VA',      '700W, VRLA, AVR, USB',              '1 unit', 'Bekalan kuasa sandaran'),
    ('PERALATAN','Rack PDU (PSU)',            '16A/250V, 8× C13',                 '1 unit', 'Agihan kuasa dalam rack'),
    ('PERALATAN','Fan Tray 1U',              '2× 80mm, 1500 RPM',                 '1 unit', 'Penyejukan rack'),
    ('PERALATAN','PC Pelajar',               'Intel i5, 8GB RAM, 256GB SSD',       '25 unit','Stesen kerja pelajar'),
    ('PERALATAN','PC Pengajar',              'Intel i7, 16GB RAM, 512GB SSD',      '1 unit', 'Stesen kerja pengajar'),
    ('PERALATAN','Monitor 24"',              'Full HD 1920×1080, IPS',             '26 unit','Paparan stesen kerja'),
    ('PERALATAN','Projektor',               'Epson EB-X41, 3300 Lumen, XGA',      '1 unit', 'Paparan pengajaran'),
    # PERISIAN
    ('PERISIAN', 'Cisco Packet Tracer 8.x',  'Simulasi rangkaian Cisco',           '26 lesen','Simulasi topologi'),
    ('PERISIAN', 'Windows 10 Pro',           '64-bit, Education license',          '26 lesen','OS stesen kerja'),
    ('PERISIAN', 'Cisco IOS 15.x',           'Router & Switch OS',                 '2 lesen', 'OS peralatan Cisco'),
    # BAHAN
    ('BAHAN',    'Kabel UTP Cat6',           'Straight-Through, 568B, 305m/box',   '1 kotak','Sambungan rangkaian'),
    ('BAHAN',    'Konektor RJ-45 Cat6',      '8P8C, booted, gold-plated',          '1 kotak','Hujung kabel'),
    ('BAHAN',    'Keystone Jack Cat6',       'Wall jack, 568B, 90°',              '26 unit','Soket dinding'),
    ('BAHAN',    'Cable Tray Aluminium',     '100×50mm, termasuk kelengkapan',     '15 meter','Laluan kabel'),
    ('BAHAN',    'Patch Cord Cat6 0.5m',    'Straight-through, pelbagai warna',   '28 unit','Rack ke switch'),
    ('BAHAN',    'Velcro Cable Ties',        'Reusable, 20cm, pelbagai warna',     '2 pek',  'Mengikat kabel'),
    ('BAHAN',    'Label Kabel',             'Brady/Panduit, waterproof',           '1 set',  'Pelabelan TIA-606-B'),
]
make_table(eq_headers,eq_rows,eq_widths,font_size=9)

page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  BAHAGIAN 4 – SENARAI KOS
# ══════════════════════════════════════════════════════════════════════════════
heading1('4.0  SENARAI KOS PEMBANGUNAN MAKMAL RANGKAIAN')
body('Jadual berikut menyenaraikan anggaran kos pembangunan makmal rangkaian '
     'mengikut kuantiti yang digunakan.')
spacer()

cost_headers=['Kategori','Nama Peralatan / Bahan','Kuantiti','Harga Seunit (RM)','Jumlah (RM)']
cost_widths=[2.2,5.5,1.8,2.8,2.8]
cost_rows=[
    # PERALATAN
    ('PERALATAN','Cisco 1941 Router',              '1 unit', '3,500.00', '3,500.00'),
    ('PERALATAN','Cisco Catalyst 2960-24TT Switch','1 unit', '2,800.00', '2,800.00'),
    ('PERALATAN','Patch Panel Cat6 24-port',       '1 unit', '180.00',   '180.00'),
    ('PERALATAN','Network Rack 12U',               '1 unit', '650.00',   '650.00'),
    ('PERALATAN','APC Smart-UPS 1000VA',           '1 unit', '1,200.00', '1,200.00'),
    ('PERALATAN','Rack PDU (PSU) 1U 16A',          '1 unit', '280.00',   '280.00'),
    ('PERALATAN','Fan Tray 1U',                    '1 unit', '120.00',   '120.00'),
    ('PERALATAN','PC Pelajar (i5/8GB/256SSD)',      '25 unit','2,500.00', '62,500.00'),
    ('PERALATAN','PC Pengajar (i7/16GB/512SSD)',    '1 unit', '3,800.00', '3,800.00'),
    ('PERALATAN','Monitor 24" Full HD',             '26 unit','650.00',   '16,900.00'),
    ('PERALATAN','Projektor Epson EB-X41',          '1 unit', '2,200.00', '2,200.00'),
    # PERISIAN
    ('PERISIAN', 'Cisco Packet Tracer 8.x',        '26 lesen','0.00',    '0.00 (Percuma)'),
    ('PERISIAN', 'Windows 10 Pro Education',        '26 lesen','450.00',  '11,700.00'),
    # BAHAN
    ('BAHAN',    'Kabel UTP Cat6 (305m/box)',        '1 kotak','380.00',  '380.00'),
    ('BAHAN',    'Konektor RJ-45 Cat6 (100pcs)',    '1 kotak','45.00',   '45.00'),
    ('BAHAN',    'Keystone Jack Cat6',              '26 unit','8.00',    '208.00'),
    ('BAHAN',    'Cable Tray Aluminium 100mm',      '15 meter','35.00',  '525.00'),
    ('BAHAN',    'Patch Cord Cat6 0.5m',            '28 unit','12.00',   '336.00'),
    ('BAHAN',    'Velcro Cable Ties (50pcs/pek)',   '2 pek',  '25.00',   '50.00'),
    ('BAHAN',    'Label Kabel (set)',               '1 set',  '85.00',   '85.00'),
    ('BAHAN',    'Pemasangan & Kos Buruh',          '–',      '–',       '2,500.00'),
]
make_table(cost_headers,cost_rows,cost_widths,font_size=9)

spacer()
# Total row
p=doc.add_paragraph()
r=p.add_run('JUMLAH KESELURUHAN ANGGARAN KOS:   RM 110,159.00')
r.bold=True; r.font.size=Pt(12); r.font.color.rgb=DARK
p.alignment=WD_ALIGN_PARAGRAPH.RIGHT

page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  BAHAGIAN 5 – PELAN SUSUN ATUR (CISCO PACKET TRACER)
# ══════════════════════════════════════════════════════════════════════════════
heading1('5.0  PELAN SUSUN ATUR MAKMAL RANGKAIAN')
body('Rajah berikut menunjukkan pelan susun atur kedudukan komputer dan sambungan '
     'perkakasan rangkaian yang dibina menggunakan perisian Cisco Packet Tracer 8.x. '
     'Topologi bintang (star topology) digunakan dengan Switch Cisco Catalyst 2960-24TT '
     'sebagai pusat bintang (central device) yang menyambungkan kesemua 26 stesen kerja. '
     'Rajah ini berpandukan pelan lantai dalam Tajuk 2.')
spacer()
figure(f'{IMGS}/cu6_tajuk5_packet_tracer.png',
       'Rajah 5.1: Pelan Susun Atur Makmal Rangkaian – Cisco Packet Tracer 8.x | Topologi Bintang | 25 PC Pelajar + 1 PC Pengajar',
       width_cm=16.5)

spacer()
body('Penerangan komponen utama dalam rajah Cisco Packet Tracer:')
bullet('Router0 (Cisco 1941): Penghala utama yang menyambungkan rangkaian LAN makmal ke internet melalui NAT. IP gateway: 192.168.1.254.')
bullet('Switch0 (Cisco 2960-24TT): Pusat bintang topologi rangkaian. Semua 26 stesen kerja disambung ke switch ini menggunakan kabel Copper Straight-Through.')
bullet('PC-01 hingga PC-25: Stesen kerja pelajar. Setiap PC disambung ke port FastEthernet0/1 hingga Fa0/25 pada switch, dengan IP statik 192.168.1.10 hingga 192.168.1.34.')
bullet('PC-Pengajar: Stesen kerja pengajar disambung ke port Fa0/24 dengan IP 192.168.1.1 pada VLAN 20.')
bullet('UPS-1000VA: Sistem bekalan kuasa sandaran yang melindungi router, switch dan patch panel.')

page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  BAHAGIAN 6 – PENETAPAN ALAMAT IP
# ══════════════════════════════════════════════════════════════════════════════
heading1('6.0  PENETAPAN ALAMAT IP PADA SETIAP PC')
body('Jadual berikut menunjukkan penetapan alamat IP statik bagi setiap stesen kerja '
     'dalam makmal rangkaian. Semua PC menggunakan subnet 192.168.1.0/24 dengan '
     'gateway 192.168.1.254 (Router Cisco 1941) dan DNS Google (8.8.8.8).')
spacer()

ip_headers=['Bil','Nama PC','Port Switch','IP Address','Subnet Mask','Default GW','DNS','VLAN','Lokasi']
ip_widths=[0.7,2.5,2.2,3.0,3.2,3.0,2.5,1.5,2.0]
ip_rows=[]
# Teacher
ip_rows.append(('0','PC-Pengajar','Fa0/24','192.168.1.1','255.255.255.0','192.168.1.254','8.8.8.8','VLAN 20','Meja Pengajar'))
# Students
row_map={1:'Baris 1',2:'Baris 1',3:'Baris 1',4:'Baris 1',5:'Baris 1',
         6:'Baris 2',7:'Baris 2',8:'Baris 2',9:'Baris 2',10:'Baris 2',
         11:'Baris 3',12:'Baris 3',13:'Baris 3',14:'Baris 3',15:'Baris 3',
         16:'Baris 4',17:'Baris 4',18:'Baris 4',19:'Baris 4',20:'Baris 4',
         21:'Baris 5',22:'Baris 5',23:'Baris 5',24:'Baris 5',25:'Baris 5'}
for i in range(1,26):
    ip_rows.append((
        str(i),
        f'PC-{i:02d}',
        f'Fa0/{i}',
        f'192.168.1.{9+i}',
        '255.255.255.0',
        '192.168.1.254',
        '8.8.8.8',
        'VLAN 10',
        row_map[i],
    ))
make_table(ip_headers,ip_rows,ip_widths,font_size=8.8)

spacer()

# Summary network info box
summ=doc.add_table(rows=1,cols=2)
summ.alignment=WD_TABLE_ALIGNMENT.CENTER
summ.style='Table Grid'
cell_bg(summ.rows[0].cells[0],'EBF5FF')
cell_bg(summ.rows[0].cells[1],'EBF5FF')
summ.rows[0].cells[0].width=Cm(8.0)
summ.rows[0].cells[1].width=Cm(8.0)
left_txt=[
    'Rangkaian: 192.168.1.0 / 24',
    'Subnet Mask: 255.255.255.0',
    'Gateway: 192.168.1.254',
    'DNS Primer: 8.8.8.8  |  DNS Sekunder: 8.8.4.4',
]
right_txt=[
    'Julat IP Pelajar: 192.168.1.10 – 192.168.1.34',
    'IP Pengajar: 192.168.1.1',
    'VLAN Pelajar: VLAN 10  |  VLAN Pengajar: VLAN 20',
    'Kabel: UTP Cat6 Straight-Through (TIA-568B)',
]
for j,(lt,rt) in enumerate(zip(left_txt,right_txt)):
    if j==0:
        p0=summ.rows[0].cells[0].paragraphs[0]
        p1=summ.rows[0].cells[1].paragraphs[0]
    else:
        p0=summ.rows[0].cells[0].add_paragraph()
        p1=summ.rows[0].cells[1].add_paragraph()
    r0=p0.add_run(lt); r0.font.size=Pt(9.5); r0.font.color.rgb=DARK; r0.bold=(j==0)
    r1=p1.add_run(rt); r1.font.size=Pt(9.5); r1.font.color.rgb=DARK; r1.bold=(j==0)

spacer()

# SIGN-OFF
p=doc.add_paragraph()
p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('— Laporan ini tidak melebihi 10 muka surat mengikut arahan tugasan —')
r.italic=True; r.font.size=Pt(9); r.font.color.rgb=GRAY

spacer(2)
sign=doc.add_table(rows=3,cols=2)
sign.alignment=WD_TABLE_ALIGNMENT.CENTER
for ri2,(l2,r2) in enumerate([
    ('Disediakan oleh:','Disahkan oleh:'),
    ('',''),
    ('[Nama Pelajar / No. Matrik]','[Nama Pensyarah / Cop Jabatan]')
]):
    sign.rows[ri2].cells[0].text=l2; sign.rows[ri2].cells[1].text=r2
    for c2 in sign.rows[ri2].cells:
        c2.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
        if c2.paragraphs[0].runs:
            c2.paragraphs[0].runs[0].font.size=Pt(10)
            if ri2==2: c2.paragraphs[0].runs[0].font.size=Pt(9)

# ─── SAVE ─────────────────────────────────────────────────────────────────────
doc.save(OUT)
print(f'Saved: {OUT}')
