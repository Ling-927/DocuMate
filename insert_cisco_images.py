"""Append Cisco Star Topology diagrams into the DKM Word report."""

from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC  = '/home/user/DocuMate/Laporan_Makmal_Rangkaian_DKM_GAMBAR.docx'
OUT  = '/home/user/DocuMate/Laporan_DKM_Cisco_Star_Topology.docx'
IMGS = '/home/user/DocuMate/images'

DARK_BLUE  = RGBColor(0x00, 0x3D, 0x73)
CISCO_BLUE = RGBColor(0x00, 0x54, 0x9F)
BLACK      = RGBColor(0x00, 0x00, 0x00)
GRAY       = RGBColor(0x71, 0x80, 0x96)

doc = Document(SRC)

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)

def add_pb(doc): doc.add_page_break()

def add_h1(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(14); r.font.color.rgb = DARK_BLUE
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after  = Pt(6)
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'),'single'); bot.set(qn('w:sz'),'6'); bot.set(qn('w:color'),'00549F')
    pBdr.append(bot); pPr.append(pBdr)

def add_h2(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(12); r.font.color.rgb = CISCO_BLUE
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(4)

def add_body(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(11); r.font.color.rgb = BLACK
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

def add_bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(text)
    r.font.size = Pt(11); r.font.color.rgb = BLACK
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.8)

def add_figure(doc, img_path, caption, w=15.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(2)
    p.add_run().add_picture(img_path, width=Cm(w))
    pc = doc.add_paragraph()
    pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pc.paragraph_format.space_before = Pt(2)
    pc.paragraph_format.space_after  = Pt(14)
    rc = pc.add_run(caption)
    rc.italic = True; rc.bold = True
    rc.font.size = Pt(9.5); rc.font.color.rgb = DARK_BLUE
    pPr  = pc._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'),'single'); bot.set(qn('w:sz'),'4'); bot.set(qn('w:color'),'00549F')
    pBdr.append(bot); pPr.append(pBdr)

def add_note(doc, text, color='EBF5FF', border='00549F'):
    tbl  = doc.add_table(rows=1, cols=1)
    cell = tbl.rows[0].cells[0]
    cell.text = ''
    p = cell.paragraphs[0]
    r = p.add_run('📌  ' + text)
    r.font.size = Pt(10); r.font.color.rgb = DARK_BLUE
    set_cell_bg(cell, color)
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for side in ('top','left','bottom','right'):
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:sz'), '8' if side=='left' else '4')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:color'), border)
        tcBorders.append(el)
    tcPr.append(tcBorders)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ════════════════════════════════════════════════════════════════════════════
#  LAMPIRAN B – CISCO STAR TOPOLOGY DIAGRAMS
# ════════════════════════════════════════════════════════════════════════════
add_pb(doc)
add_h1(doc, 'LAMPIRAN B:  GAMBAR RAJAH CISCO – TOPOLOGI BINTANG (STAR TOPOLOGY)')
add_body(doc,
    'Lampiran ini mengandungi tiga gambar rajah utama yang menggambarkan rekabentuk '
    'makmal rangkaian menggunakan ikon Cisco yang standard. Topologi bintang (star topology) '
    'dipilih kerana kebolehpercayaan yang tinggi – jika satu PC rosak, hanya stesen kerja '
    'tersebut terjejas manakala yang lain terus berfungsi.')
add_body(doc,
    'Dalam topologi bintang, switch Cisco 2960-24TT berfungsi sebagai PUSAT BINTANG '
    '(central hub/switch) di mana semua 26 stesen kerja disambung secara langsung. '
    'Router Cisco 1941 pula berfungsi sebagai pintu keluar (gateway) ke internet.')

add_h2(doc, 'Kelebihan Topologi Bintang untuk Makmal Rangkaian:')
add_bullet(doc, 'Mudah ditambah atau dikurangkan bilangan PC tanpa mengganggu rangkaian lain.')
add_bullet(doc, 'Senang mengesan masalah (troubleshoot) – periksa port switch individu.')
add_bullet(doc, 'Jika satu kabel rosak, hanya satu PC terjejas.')
add_bullet(doc, 'Prestasi tinggi – tiada perkongsian bandwidth seperti topologi bas.')
add_bullet(doc, 'Sesuai untuk persekitaran makmal pendidikan yang memerlukan kawalan terpusat.')

add_pb(doc)

# ── Rajah B-1: Star Topology ──────────────────────────────────────────────────
add_h2(doc, 'Rajah B-1:  Topologi Bintang Cisco – Pandangan Logik Lengkap')
add_body(doc,
    'Rajah berikut menunjukkan topologi bintang penuh dengan 26 peranti (25 PC pelajar + '
    '1 PC pengajar) bersambung ke switch Cisco 2960-24TT sebagai pusat bintang. Setiap '
    'sambungan mewakili satu kabel UTP Cat6 straight-through menggunakan piawaian TIA-568B. '
    'Router Cisco 1941 disambung ke switch melalui port GigabitEthernet untuk membolehkan '
    'akses internet melalui NAT.')

add_figure(doc,
    f'{IMGS}/CISCO_star_topology.png',
    'Rajah B-1: Topologi Bintang (Star Topology) – Cisco 1941 Router + Cisco 2960 Switch + 26 PC',
    w=15.5)

add_note(doc,
    'PUSAT BINTANG: Switch Cisco 2960-24TT ialah pusat topologi bintang. '
    'Semua 26 stesen kerja disambung TERUS ke switch ini. Router Cisco 1941 '
    'disambung ke switch melalui port GigabitEthernet0/1 (port uplink).',
    color='EBF5FF', border='00549F')

add_pb(doc)

# ── Rajah B-2: Physical Floor Plan with Star ─────────────────────────────────
add_h2(doc, 'Rajah B-2:  Pelan Lantai Fizikal – Susun Atur dengan Topologi Bintang')
add_body(doc,
    'Rajah ini menggabungkan pelan susun atur fizikal bilik makmal dengan laluan kabel '
    'topologi bintang. Semua kabel dari 25 PC pelajar dan 1 PC pengajar disalurkan '
    'melalui cable tray ke Network Rack 12U di sudut belakang kanan bilik. '
    'Switch dalam rack berfungsi sebagai pusat bintang.')

add_figure(doc,
    f'{IMGS}/CISCO_floor_plan.png',
    'Rajah B-2: Pelan Lantai Makmal Rangkaian – Susun Atur Fizikal dengan Topologi Bintang (Star)',
    w=15.5)

add_note(doc,
    'Semua kabel dari PC disalurkan melalui cable tray ke Patch Panel dalam rack. '
    'Dari Patch Panel, patch cord pendek (0.5m) disambung ke Switch Cisco 2960. '
    'Ini adalah rekabentuk "kabel terurus" (structured cabling) mengikut piawaian '
    'TIA-942 untuk makmal ICT.',
    color='F0FFF4', border='38A169')

add_pb(doc)

# ── Rajah B-3: Packet Tracer View ────────────────────────────────────────────
add_h2(doc, 'Rajah B-3:  Simulasi Cisco Packet Tracer – Pandangan Workspace')
add_body(doc,
    'Rajah ini menggambarkan paparan ruang kerja (workspace) Cisco Packet Tracer 8.x '
    'apabila topologi bintang makmal rangkaian telah dibina. Semua peranti Cisco '
    '(Router0 = Cisco 1941, Switch0 = Cisco 2960-24TT) dan 26 PC disusun dalam '
    'corak bintang. Warna biru pada sambungan menunjukkan kabel Copper Straight-Through '
    'yang aktif (connected).')

add_figure(doc,
    f'{IMGS}/CISCO_packet_tracer_view.png',
    'Rajah B-3: Pandangan Cisco Packet Tracer 8.x – Topologi Bintang Makmal Rangkaian (26 Peranti)',
    w=15.5)

add_note(doc,
    'Dalam Cisco Packet Tracer: (1) Gunakan kabel "Copper Straight-Through" untuk '
    'sambungan PC ke Switch. (2) Gunakan kabel "Copper Cross-Over" TIDAK diperlukan '
    'kerana Cisco 2960 menyokong Auto-MDIX. (3) Guna Simulation Mode untuk melihat '
    'perjalanan paket ICMP semasa ujian ping.',
    color='FFF9E6', border='D69E2E')

# ── Summary Table ─────────────────────────────────────────────────────────────
add_pb(doc)
add_h2(doc, 'Jadual B-1:  Ringkasan Konfigurasi Topologi Bintang')
doc.add_paragraph()

tbl = doc.add_table(rows=1, cols=3)
tbl.style = 'Table Grid'
hdrs = ['Parameter', 'Nilai / Konfigurasi', 'Piawaian / Rujukan']
widths = [Cm(4.5), Cm(7.0), Cm(4.5)]
for i, (h, w) in enumerate(zip(hdrs, widths)):
    c = tbl.rows[0].cells[i]
    c.text = ''; p = c.paragraphs[0]; r = p.add_run(h)
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
    set_cell_bg(c, '00549F'); c.width = w
    from docx.enum.table import WD_ALIGN_VERTICAL
    c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

rows_data = [
    ('Jenis Topologi',        'Star Topology (Bintang)',              'Cisco Network Academy'),
    ('Pusat Bintang',         'Cisco Catalyst 2960-24TT Switch',     'IEEE 802.3u'),
    ('Router / Gateway',      'Cisco 1941 ISR (Fa0/0: .254)',        'Cisco IOS 15.x'),
    ('Bilangan Hos',          '26 (25 pelajar + 1 pengajar)',         'Keperluan DKM'),
    ('IP Range Pelajar',      '192.168.1.10 – 192.168.1.34',        'IANA RFC 1918'),
    ('IP Pengajar',           '192.168.1.1 (VLAN 20)',               'IANA RFC 1918'),
    ('Subnet',                '192.168.1.0/24 (255.255.255.0)',      'CIDR Notation'),
    ('Jenis Kabel',           'UTP Cat6 Straight-Through',           'EIA/TIA-568B'),
    ('Kelajuan Sambungan',    '100/1000 Mbps (Auto-Negotiate)',      'IEEE 802.3ab'),
    ('Port Switch (Pelajar)', 'FastEthernet 0/1 – 0/23',            'Cisco IOS'),
    ('Port Switch (Pengajar)','FastEthernet 0/24',                   'Cisco IOS'),
    ('Uplink Router→Switch',  'GigabitEthernet 0/1 (Trunk)',        'IEEE 802.1Q'),
    ('VLAN Pelajar',          'VLAN 10 – PELAJAR',                   'IEEE 802.1Q'),
    ('VLAN Pengajar',         'VLAN 20 – PENGAJAR',                  'IEEE 802.1Q'),
    ('VLAN Pengurusan',       'VLAN 99 – PENGURUSAN',                'IEEE 802.1Q'),
    ('Protokol Routing',      'Static Route + NAT Overload',        'Cisco IOS 15.x'),
    ('DNS',                   '8.8.8.8 / 8.8.4.4 (Google)',         'RFC 1034/1035'),
    ('UPS',                   'APC Smart-UPS 1000VA / 700W',        'Rack PDU Standard'),
    ('Kabel (Simulasi PT)',   'Copper Straight-Through',             'Packet Tracer 8.x'),
]

for j, (k2, v2, ref) in enumerate(rows_data):
    row = tbl.add_row()
    row.cells[0].text = k2
    row.cells[1].text = v2
    row.cells[2].text = ref
    bg = 'EBF5FF' if j % 2 == 0 else 'FFFFFF'
    for c2 in row.cells:
        set_cell_bg(c2, bg)
        c2.paragraphs[0].runs[0].font.size = Pt(10)

doc.add_paragraph()
add_note(doc,
    'Topologi bintang dengan Cisco 2960 Switch sebagai pusat adalah rekabentuk PALING '
    'SESUAI untuk makmal ICT kerana: (1) Pengurusan mudah melalui VLAN. '
    '(2) Port Security untuk keselamatan. (3) Spanning Tree Protocol (STP) untuk '
    'pencegahan gelung. (4) QoS untuk kawalan kualiti perkhidmatan.',
    color='EBF5FF', border='00549F')

doc.save(OUT)
print(f'Saved: {OUT}')
