from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(2.5)

# ── Styles ────────────────────────────────────────────────────────────────────
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(12)

def set_heading(para, text, level=1, color=RGBColor(0x1F, 0x49, 0x7D)):
    para.clear()
    run = para.add_run(text)
    run.bold = True
    run.font.size = Pt(14) if level == 1 else Pt(13)
    run.font.color.rgb = color
    run.font.name = 'Times New Roman'
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para.paragraph_format.space_before = Pt(12)
    para.paragraph_format.space_after  = Pt(6)

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    set_heading(p, text, level)
    return p

def add_subheading(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
    run.font.name = 'Times New Roman'
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(4)
    return p

def add_body(doc, text):
    p = doc.add_paragraph(text)
    p.style = doc.styles['Normal']
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Cm(0)
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        p.add_run(text).font.name = 'Times New Roman'
    else:
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    return p

def shade_cell(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def style_table(table):
    table.style = 'Table Grid'
    for i, row in enumerate(table.rows):
        for j, cell in enumerate(row.cells):
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11)
            if i == 0:
                shade_cell(cell, '2E74B5')
                for para in cell.paragraphs:
                    for run in para.runs:
                        run.bold = True
                        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif i % 2 == 0:
                shade_cell(cell, 'D6E4F0')

# ═════════════════════════════════════════════════════════════════════════════
#  COVER PAGE
# ═════════════════════════════════════════════════════════════════════════════
doc.add_paragraph()
doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('TUGASAN PELATIH')
r.bold = True
r.font.size = Pt(22)
r.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
r.font.name = 'Times New Roman'

doc.add_paragraph()

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = subtitle.add_run('Topologi Rangkaian Komputer, Trunking, Cable Tray & Conduit')
r2.font.size = Pt(14)
r2.font.name = 'Times New Roman'

doc.add_paragraph()
doc.add_paragraph()

info_lines = [
    ('Mata Pelajaran', 'Rangkaian Komputer & Pendawaian'),
    ('Tahun', '2026'),
]
for label, val in info_lines:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f'{label}: ')
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    p.add_run(val).font.name = 'Times New Roman'

doc.add_page_break()

# ═════════════════════════════════════════════════════════════════════════════
#  SOALAN 1 – Topologi Mesh
# ═════════════════════════════════════════════════════════════════════════════
add_heading(doc, 'SOALAN 1: Topologi Mesh dalam Rangkaian Komputer')

add_subheading(doc, '1.1 Definisi Topologi Mesh')
add_body(doc,
    'Topologi mesh ialah satu susunan rangkaian komputer di mana setiap peranti (nod) '
    'disambungkan secara langsung kepada satu atau lebih peranti lain dalam rangkaian tersebut. '
    'Dalam topologi ini, terdapat laluan (path) yang berbeza-beza untuk penghantaran data, '
    'menjadikan rangkaian ini sangat tahan terhadap kegagalan.')

add_body(doc,
    'Istilah "mesh" bermaksud jaring atau jaringan — menggambarkan bagaimana sambungan-sambungan '
    'antara nod membentuk satu jaringan yang saling berkait rapat seperti jaring ikan.')

add_subheading(doc, '1.2 Cara Sambungan Berlaku')
add_body(doc,
    'Dalam topologi mesh, setiap nod disambungkan terus kepada nod-nod yang lain menggunakan '
    'kabel dedikasi (point-to-point). Bilangan sambungan yang diperlukan bagi rangkaian penuh '
    'dikira menggunakan formula:')

p_formula = doc.add_paragraph()
r = p_formula.add_run('    Bilangan Sambungan = n(n – 1) / 2')
r.bold = True
r.font.name = 'Courier New'
r.font.size = Pt(12)

add_body(doc,
    'di mana n ialah bilangan nod/peranti dalam rangkaian. Contohnya, 4 nod memerlukan '
    '4(4–1)/2 = 6 sambungan.')

add_body(doc,
    'Data boleh dihantar melalui laluan terus (direct path) atau laluan tidak langsung '
    '(indirect path / multi-hop) bergantung kepada ketersediaan pautan.')

add_subheading(doc, '1.3 Tujuan Penggunaan Topologi Mesh')
bullets_q1 = [
    ('Kebolehpercayaan Tinggi: ',
     'Jika satu sambungan gagal, data masih boleh dihantar melalui laluan alternatif.'),
    ('Keselamatan Data: ',
     'Setiap sambungan adalah eksklusif antara dua nod, mengurangkan risiko penyadapan.'),
    ('Pengurusan Trafik: ',
     'Bebanan trafik boleh diagihkan secara seimbang melalui pelbagai laluan.'),
    ('Infrastruktur Kritikal: ',
     'Digunakan dalam rangkaian telekomunikasi, tentera, dan pusat data yang memerlukan '
     'masa operasi (uptime) hampir 100%.'),
    ('Diagnosis Mudah: ',
     'Kegagalan pada satu pautan mudah dikesan dan dipencilkan tanpa menjejaskan seluruh rangkaian.'),
]
for bold, text in bullets_q1:
    add_bullet(doc, text, bold)

doc.add_page_break()

# ═════════════════════════════════════════════════════════════════════════════
#  SOALAN 2 – Jenis Topologi Mesh
# ═════════════════════════════════════════════════════════════════════════════
add_heading(doc, 'SOALAN 2: Jenis-Jenis Topologi Mesh')

# ── 2.i Full Mesh ─────────────────────────────────────────────────────────────
add_subheading(doc, '2(i) Full Mesh Topology')

add_body(doc,
    'Full Mesh Topology ialah topologi di mana SETIAP nod dalam rangkaian disambungkan '
    'secara langsung kepada SEMUA nod yang lain. Tiada nod yang tidak mempunyai sambungan '
    'terus ke setiap nod lain.')

p = doc.add_paragraph()
r = p.add_run('Konsep Sambungan:')
r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
add_body(doc,
    'Setiap nod mempunyai sambungan point-to-point yang dedikasi dengan setiap nod yang lain. '
    'Formula: n(n–1)/2 sambungan. Contoh: 5 nod → 10 sambungan.')

p = doc.add_paragraph()
r = p.add_run('Cara Beroperasi:')
r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
add_body(doc,
    'Data dihantar terus dari nod sumber ke nod destinasi tanpa perlu melalui mana-mana nod '
    'perantara. Jika pautan terus terputus, sistem boleh mencari laluan alternatif melalui nod lain. '
    'Setiap nod mempunyai kad rangkaian (NIC) yang berbeza untuk setiap sambungan.')

p = doc.add_paragraph()
r = p.add_run('Kelebihan Full Mesh:')
r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
kelebihan_full = [
    'Kebolehpercayaan sangat tinggi — tiada single point of failure.',
    'Penghantaran data pantas kerana laluan terus tersedia.',
    'Keselamatan tinggi — setiap pautan adalah eksklusif.',
    'Mudah mengesan dan mengasingkan kerosakan.',
    'Kapasiti trafik yang besar boleh dikendalikan.',
]
for k in kelebihan_full:
    add_bullet(doc, k)

p = doc.add_paragraph()
r = p.add_run('Kekurangan Full Mesh:')
r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
kekurangan_full = [
    'Kos pemasangan sangat tinggi — memerlukan banyak kabel dan port.',
    'Kompleks untuk dipasang dan diuruskan terutama bagi rangkaian besar.',
    'Pemeliharaan sukar kerana bilangan sambungan yang banyak.',
    'Tidak praktikal untuk rangkaian yang mempunyai ramai nod.',
]
for k in kekurangan_full:
    add_bullet(doc, k)

doc.add_paragraph()

# ── 2.ii Partial Mesh ─────────────────────────────────────────────────────────
add_subheading(doc, '2(ii) Partial Mesh Topology')

add_body(doc,
    'Partial Mesh Topology ialah versi yang diubahsuai daripada Full Mesh, di mana HANYA '
    'SEBAHAGIAN nod sahaja yang disambungkan terus antara satu sama lain. Nod-nod yang kurang '
    'kritikal disambungkan melalui nod perantara.')

p = doc.add_paragraph()
r = p.add_run('Konsep Sambungan:')
r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
add_body(doc,
    'Tidak semua nod mempunyai sambungan terus. Hanya nod-nod yang kerap berkomunikasi atau '
    'yang kritikal disambungkan secara langsung. Bilangan sambungan lebih sedikit berbanding '
    'Full Mesh, dikira mengikut keperluan rangkaian.')

p = doc.add_paragraph()
r = p.add_run('Cara Beroperasi:')
r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
add_body(doc,
    'Nod yang mempunyai pautan terus akan menghantar data secara langsung. Nod yang tidak '
    'mempunyai pautan terus perlu menghantar data melalui satu atau beberapa nod perantara. '
    'Router atau switch digunakan untuk memilih laluan terbaik.')

p = doc.add_paragraph()
r = p.add_run('Kelebihan Partial Mesh:')
r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
kelebihan_partial = [
    'Kos lebih rendah berbanding Full Mesh — kurang kabel diperlukan.',
    'Lebih mudah dipasang dan diuruskan.',
    'Masih menyediakan laluan redundan untuk nod-nod penting.',
    'Fleksibel — boleh direka bentuk mengikut keperluan spesifik.',
    'Sesuai untuk rangkaian bersaiz sederhana hingga besar.',
]
for k in kelebihan_partial:
    add_bullet(doc, k)

p = doc.add_paragraph()
r = p.add_run('Kekurangan Partial Mesh:')
r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
kekurangan_partial = [
    'Kebolehpercayaan lebih rendah berbanding Full Mesh.',
    'Nod yang tidak mempunyai pautan terus bergantung kepada nod perantara.',
    'Perancangan yang teliti diperlukan untuk menentukan sambungan yang perlu.',
    'Latensi mungkin lebih tinggi untuk nod tanpa sambungan terus.',
]
for k in kekurangan_partial:
    add_bullet(doc, k)

doc.add_page_break()

# ═════════════════════════════════════════════════════════════════════════════
#  SOALAN 3 – Gambarajah (ASCII art dalam dokumen)
# ═════════════════════════════════════════════════════════════════════════════
add_heading(doc, 'SOALAN 3: Gambarajah Topologi Mesh')

add_subheading(doc, '3(i) Gambarajah Full Mesh (4 Nod)')

add_body(doc,
    'Rajah di bawah menunjukkan topologi Full Mesh dengan 4 nod (A, B, C, D). '
    'Setiap nod disambungkan terus kepada semua nod yang lain dengan 6 sambungan.')

# Full Mesh diagram using a styled paragraph (monospace)
full_mesh_diagram = """\
         [A]
        / | \\
       /  |  \\
      /   |   \\
    [B]---+---[C]
      \\   |   /
       \\  |  /
        \\ | /
         [D]

  Sambungan:  A-B  |  A-C  |  A-D
              B-C  |  B-D  |  C-D
  Jumlah: 6 sambungan  [n(n-1)/2 = 4(3)/2 = 6]"""

p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(2)
run = p.add_run(full_mesh_diagram)
run.font.name = 'Courier New'
run.font.size = Pt(10)

doc.add_paragraph()
add_subheading(doc, '3(ii) Gambarajah Partial Mesh (5 Nod)')

add_body(doc,
    'Rajah di bawah menunjukkan topologi Partial Mesh dengan 5 nod (A, B, C, D, E). '
    'Hanya sebahagian nod sahaja yang mempunyai sambungan terus. '
    'Nod E berkomunikasi melalui nod perantara.')

partial_mesh_diagram = """\
         [A]─────────[B]
         |  \\         |
         |   \\        |
         |    \\       |
        [C]   [D]────[E]
         |
        (C tidak disambung terus ke D, B, atau E)

  Sambungan terus:  A-B  |  A-C  |  A-D
                    B-E  |  D-E
  Tiada sambungan:  C-D  |  C-E  |  B-C  |  B-D
  Jumlah: 5 sambungan sahaja (berbanding 10 bagi Full Mesh)"""

p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(2)
run = p.add_run(partial_mesh_diagram)
run.font.name = 'Courier New'
run.font.size = Pt(10)

doc.add_paragraph()
add_body(doc,
    'Nota: Dalam gambarajah sebenar, setiap garisan (─) mewakili satu kabel rangkaian '
    'yang menghubungkan dua nod secara terus (point-to-point).')

doc.add_page_break()

# ═════════════════════════════════════════════════════════════════════════════
#  SOALAN 4 – Jadual Perbandingan
# ═════════════════════════════════════════════════════════════════════════════
add_heading(doc, 'SOALAN 4: Jadual Perbandingan Full Mesh dan Partial Mesh')

table4 = doc.add_table(rows=1, cols=3)
table4.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = table4.rows[0].cells
for cell, text in zip(hdr, ['Aspek Perbandingan', 'Full Mesh', 'Partial Mesh']):
    cell.text = text
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

rows_data = [
    ('Definisi', 'Semua nod disambungkan terus antara satu sama lain', 'Hanya sebahagian nod yang mempunyai sambungan terus'),
    ('Bilangan Sambungan', 'n(n–1)/2  (maksimum)', 'Kurang daripada n(n–1)/2 (bergantung keperluan)'),
    ('Redundansi', 'Sangat tinggi — banyak laluan alternatif', 'Sederhana — laluan terhad'),
    ('Kebolehpercayaan', 'Sangat tinggi', 'Sederhana hingga tinggi'),
    ('Kos Pemasangan', 'Sangat mahal', 'Lebih rendah dan ekonomikal'),
    ('Kerumitan Pemasangan', 'Sangat kompleks', 'Sederhana'),
    ('Penggunaan Kabel', 'Sangat banyak', 'Sederhana'),
    ('Keselamatan', 'Sangat tinggi (pautan eksklusif)', 'Sederhana'),
    ('Latensi', 'Sangat rendah (laluan terus)', 'Mungkin lebih tinggi untuk nod tanpa pautan terus'),
    ('Pengurusan', 'Sukar dan kompleks', 'Lebih mudah'),
    ('Skala (Scalability)', 'Tidak sesuai untuk rangkaian besar', 'Lebih sesuai untuk rangkaian besar'),
    ('Kegagalan Nod', 'Tidak menjejaskan nod lain', 'Bergantung pada kedudukan nod dalam rangkaian'),
    ('Kegunaan Utama', 'Infrastruktur kritikal, tentera, telekomunikasi teras', 'Rangkaian korporat, kampus, ISP'),
    ('Contoh Penggunaan', 'Rangkaian backbone telekomunikasi antarabangsa', 'Rangkaian WAN syarikat besar'),
]

for aspect, full, partial in rows_data:
    row = table4.add_row().cells
    row[0].text = aspect
    row[1].text = full
    row[2].text = partial

style_table(table4)

# fix column widths
for i, row in enumerate(table4.rows):
    row.cells[0].width = Cm(5)
    row.cells[1].width = Cm(6)
    row.cells[2].width = Cm(6)

doc.add_page_break()

# ═════════════════════════════════════════════════════════════════════════════
#  SOALAN 5 – Jenis-Jenis Trunking
# ═════════════════════════════════════════════════════════════════════════════
add_heading(doc, 'SOALAN 5: Jenis-Jenis Trunking')

add_body(doc,
    'Trunking ialah saluran pelindung yang digunakan untuk menyusun, melindungi, dan '
    'menyembunyikan kabel-kabel elektrik atau data di dalam bangunan. Ia memastikan '
    'keselamatan, kekemasan, dan kemudahan penyelenggaraan sistem pendawaian.')

trunking_data = [
    {
        'name': '5(i) PVC Trunking (Polyvinyl Chloride Trunking)',
        'ciri': [
            'Diperbuat daripada bahan plastik PVC yang ringan dan tahan lasak.',
            'Tersedia dalam pelbagai saiz: 16mm × 16mm hingga 100mm × 60mm.',
            'Warna putih standard, tersedia dalam warna lain mengikut keperluan.',
            'Boleh dipotong, dibengkok dan dipasang dengan mudah.',
            'Dilengkapi penutup (lid) yang boleh ditanggalkan.',
        ],
        'kegunaan': [
            'Menyusun kabel elektrik dan data di dalam bangunan.',
            'Pemasangan di dinding, siling, dan lantai.',
            'Perumahan, pejabat, dan premis komersial.',
        ],
        'kelebihan': [
            'Ringan dan mudah dipasang.',
            'Kos rendah dan mudah didapati.',
            'Tahan air dan lembapan.',
            'Tidak berkarat.',
            'Tersedia dalam pelbagai saiz.',
        ],
        'kekurangan': [
            'Tidak sesuai untuk suhu tinggi.',
            'Mudah retak jika terkena hentaman keras.',
            'Tidak sesuai untuk persekitaran luar bangunan tanpa perlindungan tambahan.',
            'Tidak menahan api (kecuali jenis fire-rated).',
        ],
        'lokasi': 'Dalam bangunan — pejabat, rumah kediaman, bilik kawalan, gudang.',
    },
    {
        'name': '5(ii) Metal Trunking (Keluli/Aluminium Trunking)',
        'ciri': [
            'Diperbuat daripada keluli galvanized atau aluminium.',
            'Lebih keras dan tahan daripada PVC trunking.',
            'Permukaan boleh dicat atau dilapisi untuk perlindungan karat.',
            'Tersedia dalam saiz besar untuk kapasiti kabel yang tinggi.',
            'Penutup diikat dengan skru atau klip logam.',
        ],
        'kegunaan': [
            'Pendawaian industri dan komersial berskala besar.',
            'Kawasan yang memerlukan perlindungan mekanikal tinggi.',
            'Laluan kabel utama dalam kilang dan loji.',
        ],
        'kelebihan': [
            'Daya tahan mekanikal sangat tinggi.',
            'Tahan api dan haba.',
            'Sesuai untuk persekitaran industri yang keras.',
            'Bertindak sebagai pelindung EMI (electromagnetic interference).',
            'Jangka hayat panjang.',
        ],
        'kekurangan': [
            'Berat — memerlukan sokongan pemasangan yang kukuh.',
            'Kos lebih tinggi berbanding PVC.',
            'Memerlukan kemahiran lebih untuk pemasangan.',
            'Boleh berkarat jika lapisan pelindung rosak.',
        ],
        'lokasi': 'Kilang, loji perindustrian, bangunan komersial besar, bilik mekanikal.',
    },
    {
        'name': '5(iii) Floor Trunking (Trunking Lantai)',
        'ciri': [
            'Direka khusus untuk dipasang di bawah atau rata dengan permukaan lantai.',
            'Diperbuat daripada logam atau PVC dengan penutup yang kuat.',
            'Tahan beban berat di atasnya (dilalui orang dan peralatan).',
            'Dilengkapi sistem pengunci selamat.',
            'Mempunyai bahagian untuk kabel kuasa dan data secara berasingan.',
        ],
        'kegunaan': [
            'Menyalurkan kabel di bawah lantai pejabat atau dewan.',
            'Menyediakan akses kabel di tengah-tengah ruangan tanpa kabel tergantung.',
            'Sesuai untuk kawasan yang memerlukan fleksibiliti susun atur perabot.',
        ],
        'kelebihan': [
            'Kemas — kabel tersembunyi di bawah lantai.',
            'Boleh diakses bila-bila masa dengan membuka penutup.',
            'Selamat — tiada kabel terdedah yang boleh menyebabkan bahaya tersadung.',
            'Sesuai untuk pejabat moden dengan susun atur fleksibel.',
        ],
        'kekurangan': [
            'Pemasangan kompleks memerlukan kerja-kerja pemotong lantai.',
            'Kos pemasangan tinggi.',
            'Sukar untuk dikembangkan kapasiti setelah dipasang.',
            'Berisiko jika berlaku kebocoran air atau banjir.',
        ],
        'lokasi': 'Dewan persidangan, pejabat open-plan, studio penyiaran, pusat data.',
    },
    {
        'name': '5(iv) Mini Trunking',
        'ciri': [
            'Saiz kecil: biasanya 16mm × 16mm atau 25mm × 16mm.',
            'Diperbuat daripada PVC.',
            'Ringan, nipis, dan cekap ruang.',
            'Direka untuk kapasiti kabel yang sedikit.',
            'Dipasang terus pada permukaan dinding menggunakan pelekat atau skru kecil.',
        ],
        'kegunaan': [
            'Menyusun kabel telefon, LAN, atau TV.',
            'Pemasangan di rumah kediaman atau pejabat kecil.',
            'Menyembunyikan kabel di sepanjang skirting board atau frame pintu.',
        ],
        'kelebihan': [
            'Sangat ringan dan mudah dipasang tanpa alatan khusus.',
            'Kos sangat rendah.',
            'Tersedia dalam pelbagai warna — boleh dicat.',
            'Tidak memerlukan kemahiran teknikal tinggi.',
            'Kemas dan menarik dari segi estetik.',
        ],
        'kekurangan': [
            'Kapasiti kabel sangat terhad.',
            'Tidak sesuai untuk kabel berkuasa tinggi.',
            'Kurang tahan lama berbanding trunking saiz besar.',
            'Tidak sesuai untuk persekitaran industri.',
        ],
        'lokasi': 'Rumah kediaman, pejabat kecil, bilik hotel, bilik darjah.',
    },
    {
        'name': '5(v) Multi Compartment Trunking (Trunking Pelbagai Ruangan)',
        'ciri': [
            'Mempunyai dua atau lebih ruangan (compartment) berasingan dalam satu unit.',
            'Setiap ruangan direka untuk jenis kabel berbeza (kuasa, data, telefon).',
            'Biasanya diperbuat daripada PVC atau logam.',
            'Pemisah dalaman mengelakkan interferens antara jenis kabel.',
            'Tersedia dalam konfigurasi 2, 3, atau 4 ruangan.',
        ],
        'kegunaan': [
            'Pemasangan kabel kuasa dan data dalam satu trunking.',
            'Kawasan di mana pelbagai jenis kabel perlu disusun bersama.',
            'Bangunan pintar (smart building) dengan keperluan kabel pelbagai.',
        ],
        'kelebihan': [
            'Menjimatkan ruang — pelbagai jenis kabel dalam satu trunking.',
            'Pemisahan jenis kabel mengurangkan interferens EMI.',
            'Kemas dan teratur.',
            'Memenuhi piawaian keselamatan pendawaian.',
            'Memudahkan penyelenggaraan kabel.',
        ],
        'kekurangan': [
            'Lebih mahal berbanding trunking biasa.',
            'Bersaiz lebih besar — memerlukan lebih ruang dinding.',
            'Kompleks semasa pemasangan awal.',
            'Penambahan kabel baharu mungkin memerlukan pembongkaran.',
        ],
        'lokasi': 'Pejabat korporat, hospital, hotel, bangunan pendidikan, pusat membeli-belah.',
    },
]

for item in trunking_data:
    add_subheading(doc, item['name'])
    categories = [
        ('Ciri-Ciri:', item['ciri']),
        ('Kegunaan:', item['kegunaan']),
        ('Kelebihan:', item['kelebihan']),
        ('Kekurangan:', item['kekurangan']),
    ]
    for cat_name, cat_items in categories:
        p = doc.add_paragraph()
        r = p.add_run(cat_name)
        r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
        for ci in cat_items:
            add_bullet(doc, ci)

    p = doc.add_paragraph()
    r = p.add_run('Lokasi Pemasangan yang Sesuai: ')
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
    r2 = p.add_run(item['lokasi'])
    r2.font.name = 'Times New Roman'; r2.font.size = Pt(12)
    doc.add_paragraph()

doc.add_page_break()

# ═════════════════════════════════════════════════════════════════════════════
#  SOALAN 6 – Jenis-Jenis Cable Tray
# ═════════════════════════════════════════════════════════════════════════════
add_heading(doc, 'SOALAN 6: Jenis-Jenis Cable Tray')

add_body(doc,
    'Cable tray ialah sistem sokongan kabel terbuka yang digunakan untuk mengurus dan '
    'menampung kabel elektrik dan kabel data dalam bangunan atau kemudahan industri. '
    'Berbeza dengan trunking, cable tray adalah sistem terbuka yang membolehkan pengudaraan kabel.')

cable_tray_data = [
    {
        'name': '6(i) Ladder Cable Tray (Dulang Kabel Tangga)',
        'struktur': [
            'Reka bentuk menyerupai tangga — dua palang sisi (side rail) dan rung melintang.',
            'Rung (anak tangga) dipasang pada jarak 150mm hingga 300mm.',
            'Diperbuat daripada keluli galvanized, aluminium, atau stainless steel.',
            'Tersedia dalam lebar 150mm hingga 900mm.',
            'Kedalaman (depth) biasanya 50mm, 75mm, atau 100mm.',
        ],
        'fungsi': [
            'Menyokong kabel-kabel berat seperti kabel kuasa tegangan tinggi.',
            'Membenarkan pengudaraan semula jadi pada kabel.',
            'Digunakan untuk membawa kabel dalam kuantiti dan saiz besar.',
        ],
        'kelebihan': [
            'Kuat dan mampu menanggung beban berat.',
            'Pengudaraan baik — mengelakkan kabel daripada terlalu panas.',
            'Mudah dipasang dan dikembangkan.',
            'Senang menambah atau mengeluarkan kabel.',
            'Tahan lama dan bersesuaian dengan persekitaran industri.',
        ],
        'kekurangan': [
            'Kabel tidak terlindung daripada habuk, cecair, dan serpihan.',
            'Berat berbanding jenis cable tray lain.',
            'Penampilan kurang kemas berbanding trunking.',
            'Memerlukan ruang yang lebih besar.',
        ],
    },
    {
        'name': '6(ii) Perforated Cable Tray (Dulang Kabel Berlubang)',
        'struktur': [
            'Dulang logam rata dengan lubang-lubang kecil di bahagian bawah dan tepi.',
            'Lubang berfungsi untuk pengudaraan dan pengurangan berat.',
            'Diperbuat daripada keluli galvanized atau aluminium.',
            'Tersedia dalam pelbagai lebar dan kedalaman.',
            'Mempunyai tepi yang dilipat ke atas untuk mengelak kabel tergelincir.',
        ],
        'fungsi': [
            'Menyokong kabel data, kabel elektrik, dan kabel kawalan.',
            'Membenarkan pengudaraan yang mencukupi.',
            'Sesuai untuk kabel ringan hingga sederhana.',
        ],
        'kelebihan': [
            'Lebih ringan daripada Ladder Cable Tray.',
            'Pengudaraan baik melalui lubang-lubang.',
            'Sesuai untuk pelbagai jenis kabel.',
            'Mudah dipasang.',
            'Kos sederhana.',
        ],
        'kekurangan': [
            'Perlindungan terhad daripada habuk dan cecair.',
            'Kurang sesuai untuk kabel sangat berat.',
            'Lubang boleh menjadi sarang habuk dalam persekitaran kotor.',
        ],
    },
    {
        'name': '6(iii) Solid Bottom Cable Tray (Dulang Kabel Bawah Pepejal)',
        'struktur': [
            'Dulang dengan bahagian bawah yang rata dan pepejal tanpa lubang.',
            'Bahagian tepi dilipat ke atas membentuk profil berbentuk U.',
            'Diperbuat daripada keluli, aluminium, atau PVC.',
            'Tersedia dengan atau tanpa penutup atas.',
            'Permukaan dalaman licin untuk mengelakkan kerosakan kabel.',
        ],
        'fungsi': [
            'Perlindungan penuh kabel daripada habuk, cecair, dan serpihan.',
            'Sesuai untuk kabel sensitif seperti kabel serat optik.',
            'Digunakan di kawasan yang memerlukan perlindungan lebih tinggi.',
        ],
        'kelebihan': [
            'Perlindungan menyeluruh terhadap habuk dan cecair.',
            'Sesuai untuk kabel sensitif dan mahal.',
            'Perlindungan EMI yang lebih baik berbanding jenis terbuka.',
            'Boleh digunakan di kawasan lembap.',
        ],
        'kekurangan': [
            'Pengudaraan terhad — kabel boleh terlalu panas.',
            'Lebih berat berbanding perforated tray.',
            'Sukar menambah kabel setelah dipasang jika penuh.',
            'Kos lebih tinggi.',
        ],
    },
    {
        'name': '6(iv) Wire Mesh Cable Tray (Dulang Kabel Dawai Jaring)',
        'struktur': [
            'Diperbuat daripada wayar keluli yang dikimpal membentuk jaring tiga dimensi.',
            'Reka bentuk ringan berbentuk jaring kotak atau heksagon.',
            'Saiz dawai biasanya 4mm hingga 6mm.',
            'Tersedia dalam bahan keluli galvanized, stainless steel, atau bersalut epoxy.',
            'Boleh dipotong dan dilentur dengan mudah.',
        ],
        'fungsi': [
            'Menyokong kabel data dan rangkaian dalam pusat data.',
            'Sesuai untuk persekitaran yang memerlukan pengudaraan maksimum.',
            'Digunakan dalam pemasangan yang memerlukan fleksibiliti tinggi.',
        ],
        'kelebihan': [
            'Sangat ringan berbanding cable tray lain.',
            'Pengudaraan terbaik — aliran udara maksimum.',
            'Mudah dipotong dan dipasang mengikut keperluan.',
            'Fleksibel — mudah dilentur untuk sudut dan belokan.',
            'Sesuai untuk penambahan kabel pada bila-bila masa.',
        ],
        'kekurangan': [
            'Perlindungan fizikal yang lemah.',
            'Tidak sesuai untuk kawasan berhabuk atau ada cecair.',
            'Kapasiti beban rendah berbanding Ladder Tray.',
            'Kabel mudah tersangkut pada dawai jika tidak diuruskan dengan betul.',
        ],
    },
    {
        'name': '6(v) Channel Cable Tray (Dulang Kabel Saluran)',
        'struktur': [
            'Profil berbentuk U atau C yang mudah dan ringkas.',
            'Lebih kecil dan sempit berbanding jenis cable tray lain.',
            'Diperbuat daripada keluli galvanized atau aluminium.',
            'Lebar biasanya 50mm hingga 150mm.',
            'Tidak mempunyai bahagian melintang (rung) seperti Ladder Tray.',
        ],
        'fungsi': [
            'Menyokong bilangan kabel yang sedikit.',
            'Digunakan sebagai pelanjutan atau cabang dari sistem cable tray utama.',
            'Sesuai untuk laluan kabel pendek dan spesifik.',
        ],
        'kelebihan': [
            'Ringan dan mudah dipasang.',
            'Kos rendah berbanding jenis lain.',
            'Sesuai untuk kapasiti kabel yang kecil.',
            'Fleksibel untuk pemasangan di kawasan sempit.',
        ],
        'kekurangan': [
            'Kapasiti terhad — hanya sesuai untuk beberapa kabel.',
            'Tidak sesuai sebagai sistem cable tray utama.',
            'Pengudaraan sederhana.',
            'Kekuatan mekanikal lebih rendah.',
        ],
    },
]

for item in cable_tray_data:
    add_subheading(doc, item['name'])
    categories = [
        ('Struktur Binaan:', item['struktur']),
        ('Fungsi:', item['fungsi']),
        ('Kelebihan:', item['kelebihan']),
        ('Kekurangan:', item['kekurangan']),
    ]
    for cat_name, cat_items in categories:
        p = doc.add_paragraph()
        r = p.add_run(cat_name)
        r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
        for ci in cat_items:
            add_bullet(doc, ci)
    doc.add_paragraph()

doc.add_page_break()

# ═════════════════════════════════════════════════════════════════════════════
#  SOALAN 7 – Jenis-Jenis Conduit
# ═════════════════════════════════════════════════════════════════════════════
add_heading(doc, 'SOALAN 7: Jenis-Jenis Conduit')

add_body(doc,
    'Conduit ialah tiub atau paip yang digunakan untuk melindungi dan menyalurkan kabel '
    'elektrik dalam sistem pendawaian. Ia melindungi kabel daripada kerosakan fizikal, '
    'lembapan, bahan kimia, dan bahaya kebakaran.')

conduit_data = [
    {
        'name': '7(i) PVC Conduit (Polyvinyl Chloride Conduit)',
        'bahan': 'Polyvinyl Chloride (PVC) — plastik termoplastik yang ringan dan tahan kakisan.',
        'kegunaan': [
            'Pendawaian domestik dan komersial biasa.',
            'Pemasangan tersembunyi dalam dinding dan siling.',
            'Sistem pendawaian di kawasan lembap (tidak termasuk kawasan berbahaya).',
        ],
        'kelebihan': [
            'Ringan dan mudah dipasang.',
            'Tahan karat dan kakisan.',
            'Kos rendah.',
            'Tersedia dalam pelbagai diameter.',
            'Mudah dipotong dan disambungkan.',
        ],
        'kekurangan': [
            'Tidak sesuai untuk suhu tinggi (>60°C).',
            'Mudah retak akibat hentaman atau cuaca sejuk.',
            'Tidak memberikan perlindungan EMI.',
            'Tidak sesuai untuk pendawaian di kawasan berbahaya atau industri berat.',
        ],
        'perlindungan': 'Perlindungan sederhana — melindungi daripada lembapan, habuk, dan sentuhan fizikal ringan. Tidak sesuai untuk persekitaran tegangan tinggi atau bahan kimia.',
    },
    {
        'name': '7(ii) Flexible Conduit (Conduit Fleksibel)',
        'bahan': 'PVC fleksibel, getah, atau dawai keluli bersalut PVC — direka untuk lenturan.',
        'kegunaan': [
            'Penyambung antara konduit tegar dengan peralatan bergerak atau bergetar.',
            'Kawasan yang memerlukan lenturan seperti motor, mesin, dan pam.',
            'Bahagian akhir sambungan (final connection) bagi peralatan.',
        ],
        'kelebihan': [
            'Sangat fleksibel — mudah dilentur tanpa retak.',
            'Menyerap getaran dan hentaman mekanikal.',
            'Sesuai untuk kawasan yang sukar dicapai.',
            'Mengelakkan tekanan pada sambungan kabel.',
        ],
        'kekurangan': [
            'Kurang tahan daripada conduit tegar.',
            'Tidak sesuai sebagai laluan utama panjang.',
            'Mungkin mengecut atau mengembang akibat perubahan suhu.',
            'Perlindungan mekanikal lebih rendah.',
        ],
        'perlindungan': 'Perlindungan sederhana — terutama daripada kerosakan akibat pergerakan dan getaran. Tahap perlindungan bergantung kepada bahan salutan.',
    },
    {
        'name': '7(iii) Metal Conduit (Conduit Logam)',
        'bahan': 'Keluli galvanized, besi, atau aluminium yang ditarik atau dikimpal.',
        'kegunaan': [
            'Pemasangan industri dan komersial yang memerlukan perlindungan tinggi.',
            'Kawasan yang terdedah kepada kerosakan mekanikal.',
            'Persekitaran yang memerlukan penebatan EMI.',
        ],
        'kelebihan': [
            'Perlindungan mekanikal sangat tinggi.',
            'Tahan api dan haba.',
            'Memberikan perlindungan EMI yang baik.',
            'Jangka hayat sangat panjang.',
            'Sesuai untuk kabel tegangan tinggi.',
        ],
        'kekurangan': [
            'Berat dan mahal.',
            'Memerlukan kemahiran tinggi untuk pemasangan.',
            'Boleh berkarat jika lapisan pelindung rosak.',
            'Memerlukan grounding (pembumian) yang betul.',
        ],
        'perlindungan': 'Perlindungan tinggi — IP (Ingress Protection) tinggi terhadap habuk dan air. Perlindungan mekanikal, haba, dan EMI yang sangat baik.',
    },
    {
        'name': '7(iv) Rigid Steel Conduit (RSC) — Conduit Keluli Tegar',
        'bahan': 'Keluli karbon atau keluli galvanized berkualiti tinggi dengan dinding tebal.',
        'kegunaan': [
            'Pemasangan luar bangunan (outdoor) yang terdedah kepada cuaca.',
            'Kawasan industri berat dengan risiko kerosakan tinggi.',
            'Laluan kabel utama dalam loji dan kilang.',
        ],
        'kelebihan': [
            'Perlindungan mekanikal tertinggi dalam kalangan semua conduit.',
            'Tahan cuaca, UV, dan perubahan suhu melampau.',
            'Sesuai untuk kawasan berbahaya (hazardous areas).',
            'Boleh digunakan sebagai grounding conductor.',
            'Sangat tahan lama.',
        ],
        'kekurangan': [
            'Sangat berat dan mahal.',
            'Memerlukan alatan khas (conduit bender, threader) untuk pemasangan.',
            'Masa pemasangan yang panjang.',
            'Perlu diteroka (threading) pada setiap sambungan.',
        ],
        'perlindungan': 'Perlindungan tertinggi — IP68 boleh dicapai. Tahan terhadap kerosakan fizikal, bahan kimia, cuaca, dan tekanan mekanikal yang sangat tinggi.',
    },
    {
        'name': '7(v) EMT Conduit (Electrical Metallic Tubing)',
        'bahan': 'Keluli galvanized nipis atau aluminium — lebih ringan daripada RSC.',
        'kegunaan': [
            'Pemasangan dalam bangunan komersial dan industri.',
            'Kawasan yang memerlukan perlindungan logam tetapi lebih mudah dipasang.',
            'Laluan kabel di dinding, siling, dan ruang bawah lantai.',
        ],
        'kelebihan': [
            'Lebih ringan daripada RSC — lebih mudah dipasang.',
            'Boleh dibengkok menggunakan conduit bender biasa.',
            'Memberikan perlindungan logam yang mencukupi.',
            'Kos lebih rendah daripada RSC.',
            'Perlindungan EMI yang baik.',
        ],
        'kekurangan': [
            'Tidak sesuai untuk penggunaan luar (outdoor) tanpa perlindungan tambahan.',
            'Tidak tahan seperti RSC terhadap kerosakan mekanikal berat.',
            'Dinding nipis — mudah kemek jika terkena hentaman kuat.',
            'Tidak sesuai untuk kawasan berbahaya.',
        ],
        'perlindungan': 'Perlindungan sederhana hingga tinggi — melindungi daripada kerosakan mekanikal ringan-sederhana, lembapan (dalam bangunan), dan EMI. Tidak sesuai untuk persekitaran luar atau kawasan berbahaya.',
    },
]

for item in conduit_data:
    add_subheading(doc, item['name'])

    p = doc.add_paragraph()
    r = p.add_run('Bahan Pembuatan: ')
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
    r2 = p.add_run(item['bahan'])
    r2.font.name = 'Times New Roman'; r2.font.size = Pt(12)

    categories = [
        ('Kegunaan:', item['kegunaan']),
        ('Kelebihan:', item['kelebihan']),
        ('Kekurangan:', item['kekurangan']),
    ]
    for cat_name, cat_items in categories:
        p = doc.add_paragraph()
        r = p.add_run(cat_name)
        r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
        for ci in cat_items:
            add_bullet(doc, ci)

    p = doc.add_paragraph()
    r = p.add_run('Tahap Perlindungan Kabel: ')
    r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
    r2 = p.add_run(item['perlindungan'])
    r2.font.name = 'Times New Roman'; r2.font.size = Pt(12)
    doc.add_paragraph()

# ═════════════════════════════════════════════════════════════════════════════
#  RUMUSAN
# ═════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
add_heading(doc, 'RUMUSAN')

add_body(doc,
    'Tugasan ini telah membincangkan dengan terperinci tentang tiga topik utama dalam '
    'bidang rangkaian komputer dan pendawaian bangunan:')

rumusan_points = [
    ('Topologi Mesh: ',
     'Merupakan susunan rangkaian yang memberikan kebolehpercayaan tinggi melalui '
     'pelbagai laluan sambungan. Full Mesh menawarkan kebolehpercayaan maksimum manakala '
     'Partial Mesh menyediakan keseimbangan antara kos dan prestasi.'),
    ('Sistem Trunking: ',
     'Digunakan untuk mengurus dan melindungi kabel dalam bangunan. Pemilihan jenis '
     'trunking bergantung kepada persekitaran pemasangan, jenis kabel, dan keperluan '
     'perlindungan.'),
    ('Cable Tray: ',
     'Sistem sokongan kabel terbuka yang membenarkan pengudaraan dan memudahkan '
     'pengurusan kabel berskala besar, terutama dalam persekitaran industri dan pusat data.'),
    ('Conduit: ',
     'Sistem perlindungan kabel yang memberikan tahap perlindungan berbeza-beza '
     'bergantung kepada jenis bahan dan reka bentuk, daripada PVC untuk penggunaan '
     'domestik hingga RSC untuk persekitaran industri berat.'),
]

for bold, text in rumusan_points:
    add_bullet(doc, text, bold)

add_body(doc,
    'Pemahaman tentang topik-topik ini adalah penting bagi juruteknik elektrik dan '
    'profesional IT dalam mereka bentuk dan melaksanakan infrastruktur rangkaian dan '
    'pendawaian yang selamat, cekap, dan menepati piawaian.')

# ─── Save ─────────────────────────────────────────────────────────────────────
output_path = '/home/user/DocuMate/TUGASAN_PELATIH_LAPORAN.docx'
doc.save(output_path)
print(f'Saved: {output_path}')
