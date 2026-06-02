"""
Penjana dokumen Word: Pelan Lantai & Topologi Star
"""

import io
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
GOLD   = RGBColor(0xC8, 0x97, 0x3A)
DARK   = RGBColor(0x1A, 0x16, 0x12)
CREAM  = RGBColor(0xF7, 0xF3, 0xEC)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
MUTED  = RGBColor(0x8A, 0x7E, 0x72)
BLUE   = RGBColor(0x34, 0x98, 0xDB)
GREEN  = RGBColor(0x27, 0xAE, 0x60)
RED    = RGBColor(0xE7, 0x4C, 0x3C)
PURPLE = RGBColor(0x8E, 0x44, 0xAD)
TEAL   = RGBColor(0x16, 0xA0, 0x85)

# hex colours for matplotlib
MG     = '#C8973A'
MD     = '#1a1612'
MB     = '#3498db'
MGR    = '#27ae60'
MR     = '#e74c3c'
MP     = '#8e44ad'
MT     = '#16a085'
MBG    = '#f0ebe1'


# ─────────────────────────────────────────────
# HELPER: set_cell_bg
# ─────────────────────────────────────────────
def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color.lstrip('#'))
    tcPr.append(shd)


def set_cell_borders(cell, border_color='D0C8BE', size=4):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for side in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{side}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), str(size))
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), border_color)
        tcBorders.append(border)
    tcPr.append(tcBorders)


# ─────────────────────────────────────────────
# DIAGRAM 1: FLOOR PLAN (Matplotlib)
# ─────────────────────────────────────────────
def draw_floor_plan():
    fig, axes = plt.subplots(1, 2, figsize=(18, 9))
    fig.patch.set_facecolor('#f0ebe1')

    for ax_idx, (ax, floor, sw_xy) in enumerate(
            zip(axes,
                ['TINGKAT 1', 'TINGKAT 2'],
                [(5.5, 4.2), (5.5, 4.2)])):

        ax.set_facecolor('#faf7f2')
        ax.set_xlim(0, 11)
        ax.set_ylim(0, 8.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # Grid
        for x in np.arange(0, 11.5, 0.5):
            ax.axvline(x, color='#e8e2d8', lw=0.3, zorder=0)
        for y in np.arange(0, 8.5, 0.5):
            ax.axhline(y, color='#e8e2d8', lw=0.3, zorder=0)

        # ── Building outline ──
        ax.add_patch(mpatches.FancyBboxPatch(
            (0.1, 0.1), 10.8, 8.2, boxstyle="round,pad=0.05",
            linewidth=2.5, edgecolor='#8a7e72', facecolor='none', zorder=1))

        ax.text(5.5, 8.45, floor, ha='center', va='center',
                fontsize=11, fontweight='bold', color=MD, zorder=5)

        # Trunking bar (top)
        ax.add_patch(plt.Rectangle((0.1, 6.6), 10.8, 0.18,
                                   color=MG, alpha=0.3, zorder=2))
        ax.text(0.5, 6.72, '← Trunking Kabel (Atas Dinding)',
                fontsize=5.5, color='#8a7e72', va='center', zorder=3)

        if floor == 'TINGKAT 1':
            rooms = [
                # (x, y, w, h, label, sublabel, colour, pcs, pc_label_prefix)
                (0.1, 6.8, 2.8, 1.5, 'BILIK PENGURUS', '', MB,
                 [('PC-1', 0.9, 7.55), ('PRN-1', 2.0, 7.55)], MP),
                (2.9, 6.8, 3.0, 1.5, 'BILIK MESYUARAT', '', MGR,
                 [('PC-2', 3.7, 7.55), ('AP-1', 5.2, 7.55)], MT),
                (5.9, 6.8, 4.2, 1.5, 'RESEPSI', '', MR,
                 [('PC-3', 6.7, 7.55), ('PC-4', 8.5, 7.55)], MR),
                (0.1, 4.0, 2.8, 2.6, 'BILIK IT', '', MP,
                 [('PC-5', 0.8, 5.6), ('PC-6', 2.2, 5.6),
                  ('PRN-2', 1.4, 4.35)], MP),
                (5.9, 1.2, 4.2, 5.4, 'RUANG TERBUKA', '', MG,
                 [('PC-7', 6.7, 5.0), ('PC-8', 9.2, 5.0),
                  ('PC-9', 6.7, 3.1), ('PC-10', 9.2, 3.1),
                  ('AP-2', 9.8, 4.1)], MG),
                (2.9, 0.1, 3.1, 3.9, 'KORIDOR\n/ TANGGA', '', '#999999',
                 [], '#999999'),
            ]
            server_room = (2.9, 4.0, 3.0, 2.6, 'BILIK PELAYAN\n(Server Room)',
                           'MAIN SWITCH', MG, [], MG)
            sw_pos = (4.45, 5.3)

        else:  # TINGKAT 2
            rooms = [
                (0.1, 6.8, 2.8, 1.5, 'BILIK A', '', MB,
                 [('PC-11', 0.8, 7.55), ('PC-12', 2.3, 7.55)], MB),
                (2.9, 6.8, 3.0, 1.5, 'BILIK B', '', MGR,
                 [('PC-13', 3.6, 7.55), ('PC-14', 5.1, 7.55)], MGR),
                (5.9, 6.8, 4.2, 1.5, 'BILIK C', '', MR,
                 [('PC-15', 6.7, 7.55), ('PRN-3', 9.2, 7.55)], MR),
                (0.1, 1.2, 2.8, 5.4, 'RUANG TERBUKA T2', '', MP,
                 [('PC-16', 0.7, 5.0), ('PC-17', 2.2, 5.0),
                  ('PC-18', 0.7, 3.1), ('AP-3', 2.2, 3.1)], MP),
                (5.9, 1.2, 4.2, 5.4, 'BILIK D', '', MG,
                 [('PC-19', 6.7, 5.0), ('PC-20', 9.2, 5.0),
                  ('PRN-4', 7.9, 3.1)], MG),
            ]
            server_room = (2.9, 4.0, 3.0, 2.6, 'BILIK RANGKAIAN\n(Dist. Switch)',
                           'DIST. SWITCH T2', MG, [], MG)
            sw_pos = (4.45, 5.3)

        # Draw server/network room
        x, y, w, h, lbl, sublbl, col, _, _ = server_room
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, y), w, h, boxstyle='round,pad=0.05',
            linewidth=2.5, edgecolor=col, facecolor='#fff8ee', zorder=2))
        ax.text(x + w/2, y + h - 0.3, lbl, ha='center', va='top',
                fontsize=6.5, fontweight='bold', color=col, zorder=5)
        # Switch icon (rack)
        rx, ry = x + w/2 - 0.5, y + 0.3
        ax.add_patch(plt.Rectangle((rx, ry), 1.0, 0.7,
                                   color=MD, zorder=4))
        for i, c in enumerate([MB, MGR, MR, MG]):
            ax.add_patch(plt.Rectangle((rx+0.05, ry+0.52-i*0.13),
                                       0.9, 0.1, color=c, alpha=0.8, zorder=5))
        ax.add_patch(mpatches.FancyBboxPatch(
            (rx-0.05, ry+1.0), 1.1, 0.28, boxstyle='round,pad=0.02',
            color=MG, zorder=5))
        ax.text(rx + 0.5, ry + 1.14, sublbl, ha='center', va='center',
                fontsize=5, fontweight='bold', color='white', zorder=6)
        sw_pos = (x + w/2, y + 0.7)

        # Draw rooms
        for (rx2, ry2, rw, rh, rlbl, _, rcol, nodes, ncol) in rooms:
            alpha = 0.06 if rcol == '#999999' else 0.08
            ls = '--' if rcol == '#999999' else '-'
            ax.add_patch(mpatches.FancyBboxPatch(
                (rx2, ry2), rw, rh, boxstyle='round,pad=0.05',
                linewidth=1.5, edgecolor=rcol, facecolor=rcol, alpha=alpha,
                linestyle=ls, zorder=2))
            ax.add_patch(mpatches.FancyBboxPatch(
                (rx2, ry2), rw, rh, boxstyle='round,pad=0.05',
                linewidth=1.5, edgecolor=rcol, facecolor='none',
                linestyle=ls, zorder=3))
            ax.text(rx2 + rw/2, ry2 + rh - 0.2, rlbl, ha='center', va='top',
                    fontsize=6, fontweight='600', color=rcol, zorder=5)

            for (nlbl, nx, ny) in nodes:
                if 'AP' in nlbl:
                    ax.add_patch(plt.Circle((nx, ny), 0.22, color=ncol,
                                            alpha=0.2, zorder=4))
                    ax.add_patch(plt.Circle((nx, ny), 0.1, color=ncol,
                                            alpha=0.6, zorder=5))
                    ax.add_patch(plt.Circle((nx, ny), 0.04, color=ncol,
                                            zorder=6))
                elif 'PRN' in nlbl:
                    ax.add_patch(mpatches.FancyBboxPatch(
                        (nx-0.25, ny-0.15), 0.5, 0.3, boxstyle='round,pad=0.02',
                        color=MP, alpha=0.8, zorder=4))
                else:
                    ax.add_patch(plt.Rectangle((nx-0.2, ny-0.15), 0.4, 0.28,
                                               color=MD, zorder=4))
                    ax.add_patch(plt.Circle((nx, ny + 0.02), 0.12,
                                            color=ncol, alpha=0.7, zorder=5))
                ax.text(nx, ny - 0.32, nlbl, ha='center', va='top',
                        fontsize=5, fontweight='bold', color=ncol, zorder=6)

        # ── Draw cables from switch to all nodes ──
        sw_x, sw_y = sw_pos
        all_nodes = []
        for (_, _, _, _, _, _, _, nodes, ncol) in rooms:
            for (nlbl, nx, ny) in nodes:
                all_nodes.append((nlbl, nx, ny, ncol))

        # Trunking y level
        ty = 6.65
        for (nlbl, nx, ny, ncol) in all_nodes:
            if 'AP' in nlbl:
                ls = (0, (4, 4))
                lw = 1.2
            elif 'PRN' in nlbl:
                ls = (0, (5, 3))
                lw = 1.0
            else:
                ls = (0, (6, 3))
                lw = 1.5

            if ny > 6.5:
                # Go via trunking (top)
                ax.plot([sw_x, sw_x, nx, nx], [sw_y, ty, ty, ny],
                        color=ncol, lw=lw, linestyle=ls, zorder=3, solid_capstyle='round')
            elif nx < sw_x:
                # Go left
                mid_x = sw_x - (sw_x - 0.1)/2
                ax.plot([sw_x, nx], [sw_y, ny],
                        color=ncol, lw=lw, linestyle=ls, zorder=3,
                        solid_capstyle='round')
            else:
                ax.plot([sw_x, nx], [sw_y, ny],
                        color=ncol, lw=lw, linestyle=ls, zorder=3,
                        solid_capstyle='round')

        ax.set_title(f'{floor}', fontsize=10, fontweight='bold',
                     color=MD, pad=4)

    # Legend
    legend_items = [
        mpatches.Patch(facecolor=MB, label='Kabel Data Cat6 (PC)'),
        mpatches.Patch(facecolor=MP, label='Kabel Pencetak'),
        mpatches.Patch(facecolor=MT, label='Kabel PoE (AP WiFi)'),
        mpatches.Patch(facecolor=MG, label='Fiber / Switch Pusat'),
        mpatches.Patch(facecolor=MR, label='Kabel Resepsi / Bilik C'),
    ]
    fig.legend(handles=legend_items, loc='lower center', ncol=5,
               fontsize=8, frameon=True, fancybox=True,
               facecolor='white', edgecolor='#D0C8BE',
               bbox_to_anchor=(0.5, -0.01))

    fig.suptitle('PELAN LANTAI — RANGKAIAN TOPOLOGI STAR',
                 fontsize=14, fontweight='bold', color=MD, y=1.01)
    fig.tight_layout(rect=[0, 0.06, 1, 0.98])

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────
# DIAGRAM 2: STAR TOPOLOGY LOGICAL (Matplotlib)
# ─────────────────────────────────────────────
def draw_star_topology():
    fig, ax = plt.subplots(figsize=(16, 12))
    fig.patch.set_facecolor('#1a1612')
    ax.set_facecolor('#1a1612')
    ax.set_xlim(-1, 17)
    ax.set_ylim(-1, 14)
    ax.set_aspect('equal')
    ax.axis('off')

    # Grid
    for x in np.arange(0, 17, 1):
        ax.axvline(x, color=(1, 1, 1, 0.04), lw=0.3)
    for y in np.arange(0, 14, 1):
        ax.axhline(y, color=(1, 1, 1, 0.04), lw=0.3)

    # Title
    ax.text(8, 13.5, 'TOPOLOGI STAR — RAJAH LOGIK RANGKAIAN PEJABAT 2 TINGKAT',
            ha='center', va='center', fontsize=11, fontweight='bold',
            color=MG, zorder=10)

    # ── INTERNET ──
    internet = plt.Circle((8, 12.5), 0.8, color=MT, alpha=0.2)
    ax.add_patch(internet)
    ax.add_patch(plt.Circle((8, 12.5), 0.8, color=MT, fill=False, lw=1.5))
    ax.text(8, 12.55, '🌐', ha='center', va='center', fontsize=12)
    ax.text(8, 11.9, 'INTERNET/ISP', ha='center', va='center',
            fontsize=7, color=MT, fontweight='bold')

    # ── FIREWALL ──
    ax.add_patch(mpatches.FancyBboxPatch(
        (7.0, 10.8), 2.0, 0.7, boxstyle='round,pad=0.08',
        facecolor='#3d1a1a', edgecolor=MR, lw=1.5, zorder=3))
    ax.text(8, 11.15, 'FIREWALL / ROUTER', ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=MR, zorder=4)
    ax.plot([8, 8], [11.7, 11.5], color=MT, lw=2, linestyle='--', zorder=3)

    # ── MAIN SWITCH T1 ──
    msw_x, msw_y = 3.5, 6.5
    for r, alpha in [(1.3, 0.08), (1.1, 0.12), (0.9, 0.3)]:
        ax.add_patch(plt.Circle((msw_x, msw_y), r, color=MG,
                                alpha=alpha, zorder=3))
    ax.add_patch(plt.Circle((msw_x, msw_y), 0.85, color='#2c2218',
                             zorder=4))
    ax.add_patch(plt.Circle((msw_x, msw_y), 0.85, color=MG,
                             fill=False, lw=2.5, zorder=5))
    ax.text(msw_x, msw_y + 0.22, 'MAIN', ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=MG, zorder=6)
    ax.text(msw_x, msw_y - 0.05, 'SWITCH', ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=MG, zorder=6)
    ax.text(msw_x, msw_y - 0.38, '24-Port | T1', ha='center', va='center',
            fontsize=5.5, color='#8a7e72', zorder=6)
    ax.text(msw_x, msw_y - 1.4, 'TINGKAT 1', ha='center',
            fontsize=7, color=MG, alpha=0.6, zorder=5)

    # Firewall → Main Switch
    ax.plot([7.3, msw_x + 0.85], [10.95, msw_y + 0.2],
            color=MR, lw=2, linestyle='--', zorder=3)
    ax.text(5.5, 9.0, 'WAN\nUplink', ha='center', fontsize=6.5,
            color=MR, rotation=55, zorder=4)

    # ── DIST SWITCH T2 ──
    dsw_x, dsw_y = 12.5, 6.5
    for r, alpha in [(1.3, 0.08), (1.1, 0.12), (0.9, 0.3)]:
        ax.add_patch(plt.Circle((dsw_x, dsw_y), r, color=MG,
                                alpha=alpha, zorder=3))
    ax.add_patch(plt.Circle((dsw_x, dsw_y), 0.85, color='#2c2218',
                             zorder=4))
    ax.add_patch(plt.Circle((dsw_x, dsw_y), 0.85, color=MG,
                             fill=False, lw=2, zorder=5))
    ax.text(dsw_x, dsw_y + 0.22, 'DIST.', ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=MG, zorder=6)
    ax.text(dsw_x, dsw_y - 0.05, 'SWITCH', ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=MG, zorder=6)
    ax.text(dsw_x, dsw_y - 0.38, '24-Port | T2', ha='center', va='center',
            fontsize=5.5, color='#8a7e72', zorder=6)
    ax.text(dsw_x, dsw_y - 1.4, 'TINGKAT 2', ha='center',
            fontsize=7, color=MG, alpha=0.6, zorder=5)

    # ── FIBER BACKBONE ──
    ax.plot([msw_x + 0.85, dsw_x - 0.85], [msw_y, dsw_y],
            color=MG, lw=4, linestyle=(0, (10, 5)), zorder=3)
    ax.text(8, 6.75, 'FIBER OPTIK — 1 Gbps', ha='center', fontsize=7.5,
            fontweight='bold', color=MG, zorder=4)
    ax.text(8, 6.3, 'LC Duplex Singlemode', ha='center', fontsize=6.5,
            color='#8a7e72', zorder=4)
    ax.annotate('', xy=(dsw_x - 0.85, dsw_y), xytext=(dsw_x - 1.3, dsw_y),
                arrowprops=dict(arrowstyle='->', color=MG, lw=2), zorder=5)
    ax.annotate('', xy=(msw_x + 0.85, msw_y), xytext=(msw_x + 1.3, msw_y),
                arrowprops=dict(arrowstyle='->', color=MG, lw=2), zorder=5)

    # ── NODES TINGKAT 1 ──
    t1_nodes = [
        ('PC-1\n(B.Pengurus)', 0.5, 10.0, MB),
        ('PRN-1\n(Pengurus)', -0.2, 8.0, MP),
        ('PC-2\n(Mesyuarat)', 0.5, 6.5, MGR),
        ('AP-1 WiFi\n(Mesyuarat)', 0.5, 5.0, MT),
        ('PC-3,4\n(Resepsi)', 1.0, 3.5, MR),
        ('PC-5,6\n(Bilik IT)', 2.0, 1.5, MP),
        ('PRN-2\n(Bilik IT)', 3.5, 0.5, MP),
        ('PC-7..10\n(Terbuka T1)', 5.5, 1.5, MG),
        ('AP-2 WiFi\n(Terbuka T1)', 6.5, 3.5, MT),
    ]

    for (lbl, nx, ny, col) in t1_nodes:
        if 'AP' in lbl:
            ax.add_patch(plt.Circle((nx, ny), 0.45, color=col, alpha=0.15,
                                    zorder=3))
            ax.add_patch(plt.Circle((nx, ny), 0.45, color=col,
                                    fill=False, lw=1.5, zorder=4))
            ax.text(nx, ny, '📡', ha='center', va='center',
                    fontsize=8, zorder=5)
        elif 'PRN' in lbl:
            ax.add_patch(mpatches.FancyBboxPatch(
                (nx - 0.5, ny - 0.3), 1.0, 0.6, boxstyle='round,pad=0.06',
                facecolor='#2d1b45', edgecolor=col, lw=1.5, zorder=3))
            ax.text(nx, ny, '🖨️', ha='center', va='center',
                    fontsize=7, zorder=4)
        else:
            ax.add_patch(mpatches.FancyBboxPatch(
                (nx - 0.55, ny - 0.35), 1.1, 0.7, boxstyle='round,pad=0.06',
                facecolor='#1e2833', edgecolor=col, lw=1.5, zorder=3))
            ax.text(nx, ny + 0.05, '🖥️', ha='center', va='center',
                    fontsize=7, zorder=4)
        ax.text(nx, ny - 0.58, lbl, ha='center', va='top',
                fontsize=6, color=col, fontweight='bold', zorder=5)
        # Cable
        ls = (0, (4, 4)) if ('AP' in lbl or 'PRN' in lbl) else '-'
        lw = 1.5 if 'AP' in lbl else (1.2 if 'PRN' in lbl else 2)
        ax.plot([msw_x, nx], [msw_y, ny], color=col, lw=lw,
                linestyle=ls, zorder=2, solid_capstyle='round')

    # ── NODES TINGKAT 2 ──
    t2_nodes = [
        ('PC-11,12\n(Bilik A)', 10.0, 10.0, MB),
        ('PC-13,14\n(Bilik B)', 12.0, 10.5, MGR),
        ('PC-15\n(Bilik C)', 14.5, 10.0, MR),
        ('PRN-3\n(Bilik C)', 15.5, 8.5, MP),
        ('PC-16..18\n(Terbuka T2)', 10.0, 3.5, MP),
        ('AP-3 WiFi\n(Terbuka T2)', 11.5, 2.0, MT),
        ('PC-19,20\n(Bilik D)', 14.5, 3.5, MG),
        ('PRN-4\n(Bilik D)', 15.8, 4.8, MP),
    ]

    for (lbl, nx, ny, col) in t2_nodes:
        if 'AP' in lbl:
            ax.add_patch(plt.Circle((nx, ny), 0.45, color=col, alpha=0.15,
                                    zorder=3))
            ax.add_patch(plt.Circle((nx, ny), 0.45, color=col,
                                    fill=False, lw=1.5, zorder=4))
            ax.text(nx, ny, '📡', ha='center', va='center',
                    fontsize=8, zorder=5)
        elif 'PRN' in lbl:
            ax.add_patch(mpatches.FancyBboxPatch(
                (nx - 0.5, ny - 0.3), 1.0, 0.6, boxstyle='round,pad=0.06',
                facecolor='#2d1b45', edgecolor=col, lw=1.5, zorder=3))
            ax.text(nx, ny, '🖨️', ha='center', va='center',
                    fontsize=7, zorder=4)
        else:
            ax.add_patch(mpatches.FancyBboxPatch(
                (nx - 0.55, ny - 0.35), 1.1, 0.7, boxstyle='round,pad=0.06',
                facecolor='#1e2833', edgecolor=col, lw=1.5, zorder=3))
            ax.text(nx, ny + 0.05, '🖥️', ha='center', va='center',
                    fontsize=7, zorder=4)
        ax.text(nx, ny - 0.58, lbl, ha='center', va='top',
                fontsize=6, color=col, fontweight='bold', zorder=5)
        ls = (0, (4, 4)) if ('AP' in lbl or 'PRN' in lbl) else '-'
        lw = 1.5 if 'AP' in lbl else (1.2 if 'PRN' in lbl else 2)
        ax.plot([dsw_x, nx], [dsw_y, ny], color=col, lw=lw,
                linestyle=ls, zorder=2, solid_capstyle='round')

    # ── SERVER & NAS ──
    ax.add_patch(mpatches.FancyBboxPatch(
        (2.0, -0.7), 1.8, 0.65, boxstyle='round,pad=0.06',
        facecolor='#1a1612', edgecolor=MR, lw=1.5, zorder=3))
    ax.text(2.9, -0.38, '🗄️ SERVER', ha='center', va='center',
            fontsize=7, color=MR, fontweight='bold', zorder=4)
    ax.plot([msw_x, 2.9], [msw_y - 0.85, 0.0],
            color=MR, lw=1.5, linestyle=(0, (5, 3)), zorder=2)

    ax.add_patch(mpatches.FancyBboxPatch(
        (4.0, -0.7), 1.8, 0.65, boxstyle='round,pad=0.06',
        facecolor='#1a1612', edgecolor=MGR, lw=1.5, zorder=3))
    ax.text(4.9, -0.38, '💾 NAS', ha='center', va='center',
            fontsize=7, color=MGR, fontweight='bold', zorder=4)
    ax.plot([msw_x, 4.9], [msw_y - 0.85, 0.0],
            color=MGR, lw=1.5, linestyle=(0, (5, 3)), zorder=2)

    # ── LEGEND ──
    legend_items = [
        mpatches.Patch(facecolor=MB,  label='Kabel Cat6 UTP (PC)'),
        mpatches.Patch(facecolor=MP,  label='Kabel Pencetak'),
        mpatches.Patch(facecolor=MT,  label='Kabel PoE (AP WiFi)'),
        mpatches.Patch(facecolor=MG,  label='Fiber Optik Backbone'),
        mpatches.Patch(facecolor=MR,  label='WAN / Firewall'),
        mpatches.Patch(facecolor='#2c2218', edgecolor=MG, lw=1.5,
                       label='Main / Dist. Switch'),
    ]
    ax.legend(handles=legend_items, loc='upper right',
              fontsize=7, frameon=True, fancybox=True,
              facecolor='#1a1612', edgecolor='#3a3228',
              labelcolor='white', bbox_to_anchor=(0.99, 0.99))

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────
# DIAGRAM 3: CABLE ROUTING CROSS-SECTION
# ─────────────────────────────────────────────
def draw_cable_routing():
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#f0ebe1')
    ax.set_facecolor('#faf7f2')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(7, 6.7, 'SUSUN ATUR & LALUAN KABEL — PANDANGAN KERATAN RENTAS (CROSS-SECTION)',
            ha='center', va='center', fontsize=9, fontweight='bold', color=MD)

    # ── FLOOR / CEILING sections ──
    # Ceiling
    ax.add_patch(plt.Rectangle((0, 5.5), 14, 0.5, color='#bbb', alpha=0.4))
    ax.text(7, 5.75, 'S I L I N G', ha='center', va='center',
            fontsize=8, color='#555', fontweight='bold')
    # Floor
    ax.add_patch(plt.Rectangle((0, 0.1), 14, 0.4, color='#bbb', alpha=0.4))
    ax.text(7, 0.3, 'L A N T A I', ha='center', va='center',
            fontsize=8, color='#555', fontweight='bold')

    # Walls
    ax.add_patch(plt.Rectangle((0, 0.5), 0.25, 5.0, color='#888', alpha=0.5))
    ax.add_patch(plt.Rectangle((4.0, 0.5), 0.25, 5.0, color='#888', alpha=0.5))
    ax.add_patch(plt.Rectangle((8.5, 0.5), 0.25, 5.0, color='#888', alpha=0.5))
    ax.add_patch(plt.Rectangle((13.75, 0.5), 0.25, 5.0, color='#888', alpha=0.5))
    ax.text(2.1, 5.2, 'BILIK PELAYAN', ha='center', fontsize=7.5,
            fontweight='bold', color=MG)
    ax.text(6.3, 5.2, 'BILIK / RUANG KERJA 1', ha='center', fontsize=7.5,
            fontweight='bold', color=MB)
    ax.text(11.1, 5.2, 'BILIK / RUANG KERJA 2', ha='center', fontsize=7.5,
            fontweight='bold', color=MB)

    # ── CABLE TRAY (siling) ──
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.3, 5.1), 13.4, 0.28, boxstyle='round,pad=0.02',
        facecolor=MG, alpha=0.25, edgecolor=MG, lw=1.5))
    ax.text(7, 5.24, '▬ CABLE TRAY / TRUNKING SILING ▬', ha='center',
            va='center', fontsize=7, color=MG, fontweight='bold')

    # ── TRUNKING DINDING kiri ──
    ax.add_patch(plt.Rectangle((0.25, 1.4), 0.3, 3.6, color=MG, alpha=0.3))
    ax.add_patch(plt.Rectangle((0.25, 1.4), 0.3, 3.6, color=MG,
                                fill=False, lw=1.2))
    ax.text(0.4, 3.2, 'T\nR\nU\nN\nK\nI\nN\nG', ha='center', va='center',
            fontsize=5, color=MG, fontweight='bold')

    # ── Patch Panel (bilik pelayan) ──
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.7, 2.5), 2.8, 0.8, boxstyle='round,pad=0.05',
        facecolor=MD, edgecolor=MG, lw=2))
    for i in range(12):
        x = 0.85 + i * 0.2
        col = [MB, MGR, MR, MP, MT, MG][i % 6]
        ax.add_patch(plt.Rectangle((x, 2.65), 0.12, 0.08, color=col))
    ax.text(2.1, 3.45, 'PATCH PANEL 24-Port', ha='center', va='center',
            fontsize=7, color=MG, fontweight='bold')

    # ── Main Switch ──
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.7, 1.5), 2.8, 0.8, boxstyle='round,pad=0.05',
        facecolor=MD, edgecolor=MG, lw=2))
    ax.text(2.1, 1.9, '🔀 MAIN SWITCH', ha='center', va='center',
            fontsize=7.5, color=MG, fontweight='bold')

    # ── UPS ──
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.7, 0.65), 1.2, 0.7, boxstyle='round,pad=0.05',
        facecolor='#1e3a5f', edgecolor=MB, lw=1.5))
    ax.text(1.3, 1.0, 'UPS', ha='center', va='center',
            fontsize=7, color=MB, fontweight='bold')

    # ── PCs in rooms ──
    for xpos, label in [(5.5, 'PC'), (6.8, 'PC'), (10.0, 'PC'), (11.5, 'PC')]:
        ax.add_patch(plt.Rectangle((xpos - 0.3, 0.6), 0.6, 0.45, color=MD))
        ax.add_patch(plt.Circle((xpos, 0.82), 0.12, color=MB, alpha=0.6))
        ax.text(xpos, 0.5, label, ha='center', va='top', fontsize=7,
                color=MB, fontweight='bold')
        # Wall socket
        ax.add_patch(plt.Rectangle((xpos - 0.15, 1.2), 0.3, 0.2,
                                   color='#e2d9cc', ec='#999'))
        ax.text(xpos, 1.45, 'RJ45', ha='center', va='bottom',
                fontsize=5, color='#666')
        # Cable PC → socket → trunking → patch panel
        ax.plot([xpos, xpos, xpos], [1.05, 1.2, 5.1],
                color=MB, lw=2, linestyle='--', zorder=3)
        ax.plot([xpos, 2.1], [5.1, 5.1], color=MB, lw=1.5,
                linestyle='--', zorder=3)
        ax.plot([2.1, 2.1], [5.1, 3.3], color=MB, lw=1.5,
                linestyle='--', zorder=3)

    # Trunking dinding kanan (bilik 2)
    ax.add_patch(plt.Rectangle((8.5, 1.4), 0.3, 3.6, color=MG, alpha=0.3))
    ax.add_patch(plt.Rectangle((8.5, 1.4), 0.3, 3.6, color=MG,
                                fill=False, lw=1.2))

    # AP on ceiling
    for xap, label in [(3.5, 'AP-1'), (9.5, 'AP-2')]:
        ax.add_patch(plt.Circle((xap, 5.0), 0.25, color=MT, alpha=0.3))
        ax.add_patch(plt.Circle((xap, 5.0), 0.25, color=MT, fill=False, lw=1.5))
        ax.text(xap, 5.0, '📡', ha='center', va='center', fontsize=8)
        ax.text(xap, 4.65, label, ha='center', va='top',
                fontsize=6.5, color=MT, fontweight='bold')
        ax.plot([xap, 2.1], [5.0, 5.0], color=MT, lw=1.5,
                linestyle=(0, (4, 3)), zorder=3)
        ax.plot([2.1, 2.1], [5.0, 3.3], color=MT, lw=1.5,
                linestyle=(0, (4, 3)), zorder=3)

    # Labels
    ax.annotate('', xy=(0.8, 2.5), xytext=(2.1, 3.3),
                arrowprops=dict(arrowstyle='->', color=MG, lw=1.5))
    ax.text(1.0, 2.85, 'Ke Switch', fontsize=6, color=MG, rotation=30)

    # Legend
    leg = [
        mpatches.Patch(facecolor=MB, label='Kabel UTP Cat6 (Data)'),
        mpatches.Patch(facecolor=MT, label='Kabel PoE Cat6 (AP)'),
        mpatches.Patch(facecolor=MG, alpha=0.4, label='Trunking / Cable Tray'),
        mpatches.Patch(edgecolor=MG, lw=2,
                       facecolor='none', label='Patch Panel / Switch'),
    ]
    ax.legend(handles=leg, loc='lower right', fontsize=7,
              frameon=True, fancybox=True)

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────
# BUILD WORD DOCUMENT
# ─────────────────────────────────────────────
def build_word():
    doc = Document()

    # Page margins
    for section in doc.sections:
        section.page_width  = Cm(29.7)
        section.page_height = Cm(21.0)
        section.left_margin   = Cm(1.8)
        section.right_margin  = Cm(1.8)
        section.top_margin    = Cm(1.8)
        section.bottom_margin = Cm(1.5)

    styles = doc.styles

    # ── COVER PAGE ──
    doc.add_paragraph()
    cover = doc.add_paragraph()
    cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cover.add_run('PELAN LANTAI & REKABENTUK TOPOLOGI STAR')
    run.font.size = Pt(26)
    run.font.bold = True
    run.font.color.rgb = DARK

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = sub.add_run('Rangkaian Komputer Pejabat 2 Tingkat')
    r2.font.size = Pt(14)
    r2.font.color.rgb = GOLD

    doc.add_paragraph()
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.style = 'Table Grid'
    info = [
        ('Disediakan oleh', 'Jabatan IT / Rangkaian'),
        ('Tarikh', '2 Jun 2026'),
        ('Versi', 'v1.0'),
        ('Jumlah Nod', '20 PC | 4 Pencetak | 3 AP WiFi'),
    ]
    for i, (k, v) in enumerate(info):
        row = meta_table.rows[i]
        kc = row.cells[0]
        vc = row.cells[1]
        set_cell_bg(kc, '1a1612')
        set_cell_bg(vc, '2c2218')
        kp = kc.paragraphs[0]
        kp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        kr = kp.add_run(k)
        kr.font.bold = True
        kr.font.color.rgb = GOLD
        kr.font.size = Pt(10)
        vr = vc.paragraphs[0].add_run(v)
        vr.font.color.rgb = CREAM
        vr.font.size = Pt(10)
    doc.add_page_break()

    # ── SECTION 1: PENGENALAN ──
    def add_section_title(doc, num, title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after  = Pt(4)
        r = p.add_run(f'{num}  {title.upper()}')
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = DARK
        # Gold underline bar
        bar = doc.add_paragraph()
        bar.paragraph_format.space_before = Pt(0)
        bar.paragraph_format.space_after  = Pt(8)
        rb = bar.add_run('─' * 70)
        rb.font.color.rgb = GOLD
        rb.font.size = Pt(8)

    def add_body(doc, text):
        p = doc.add_paragraph(text)
        p.paragraph_format.space_after = Pt(6)
        for run in p.runs:
            run.font.size = Pt(10.5)
            run.font.color.rgb = DARK

    def add_gold_label(doc, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        r = p.add_run(f'▌ {text}')
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = GOLD

    add_section_title(doc, '1.', 'Pengenalan')
    add_body(doc,
        'Dokumen ini menerangkan rekabentuk rangkaian komputer bagi sebuah pejabat dua tingkat '
        'menggunakan topologi bintang (star topology). Topologi star dipilih kerana '
        'kelebihannya dari segi pengurusan, keselamatan, dan kebolehpercayaan rangkaian.')

    add_gold_label(doc, 'Apakah Topologi Star?')
    add_body(doc,
        'Topologi star adalah rekabentuk rangkaian di mana setiap peranti (komputer, pencetak, '
        'access point) disambung terus ke satu suis pusat (central switch). Sambungan berbentuk '
        'seperti bintang — suis di tengah, peranti di hujung setiap "lengan".')

    # Advantages table
    adv_table = doc.add_table(rows=5, cols=2)
    adv_table.style = 'Table Grid'
    adv_table.alignment = WD_TABLE_ALIGNMENT.LEFT
    headers = [('Kelebihan', 'Penerangan')]
    rows_data = [
        ('Satu Pusat Kawalan', 'Semua peranti diurus dari satu suis — mudah pantau dan konfigurasi.'),
        ('Keselamatan Tinggi', 'Kegagalan satu kabel/peranti tidak menjejaskan peranti lain.'),
        ('Mudah Diselenggara', 'Masalah mudah dikesan — hanya satu kabel antara peranti dan suis.'),
        ('Mudah Dikembangkan', 'Tambah peranti baru hanya dengan sambung kabel ke port kosong pada suis.'),
    ]
    for i, (k, v) in enumerate(rows_data):
        row = adv_table.rows[i]
        set_cell_bg(row.cells[0], 'fff8ee')
        kr = row.cells[0].paragraphs[0].add_run(k)
        kr.font.bold = True
        kr.font.size = Pt(9.5)
        kr.font.color.rgb = RGBColor(0xC8, 0x97, 0x3A)
        vr = row.cells[1].paragraphs[0].add_run(v)
        vr.font.size = Pt(9.5)
    doc.add_paragraph()

    # ── SECTION 2: PELAN LANTAI ──
    add_section_title(doc, '2.', 'Pelan Lantai — Susun Atur Pejabat')
    add_body(doc,
        'Pejabat terdiri daripada dua tingkat. Tingkat 1 mengandungi bilik pelayan (server room) '
        'yang merupakan pusat suis utama. Tingkat 2 disambung melalui fiber optik ke suis agihan '
        '(distribution switch). Kabel disusun melalui trunking PVC pada dinding dan cable tray di siling.')

    add_gold_label(doc, 'Susun Atur Bilik')
    room_table = doc.add_table(rows=10, cols=3)
    room_table.style = 'Table Grid'
    room_table.alignment = WD_TABLE_ALIGNMENT.LEFT
    room_headers = [('Bilik / Kawasan', 'Tingkat', 'Peranti Rangkaian')]
    room_data = [
        ('Bilik Pelayan (Server Room)', 'T1', 'Main Switch, Server, NAS, Patch Panel, UPS'),
        ('Bilik Pengurus',              'T1', 'PC-1, Pencetak PRN-1'),
        ('Bilik Mesyuarat',             'T1', 'PC-2, Access Point AP-1'),
        ('Resepsi',                     'T1', 'PC-3, PC-4'),
        ('Bilik IT',                    'T1', 'PC-5, PC-6, Pencetak PRN-2'),
        ('Ruang Kerja Terbuka',         'T1', 'PC-7, PC-8, PC-9, PC-10, Access Point AP-2'),
        ('Bilik Rangkaian',             'T2', 'Distribution Switch, Patch Panel'),
        ('Bilik A & B',                 'T2', 'PC-11, PC-12, PC-13, PC-14'),
        ('Bilik C & D',                 'T2', 'PC-15, PC-19, PC-20, PRN-3, PRN-4'),
        ('Ruang Kerja Terbuka T2',      'T2', 'PC-16, PC-17, PC-18, Access Point AP-3'),
    ]
    # Header row
    hdr = room_table.rows[0]
    for i, (cell, htext) in enumerate(zip(hdr.cells, room_headers[0])):
        set_cell_bg(cell, '1a1612')
        r = cell.paragraphs[0].add_run(htext)
        r.font.bold = True
        r.font.color.rgb = GOLD
        r.font.size = Pt(9)
    for i, (b, t, p) in enumerate(room_data):
        row = room_table.rows[i]
        if i % 2 == 0:
            for cell in row.cells:
                set_cell_bg(cell, 'faf7f2')
        row.cells[0].paragraphs[0].add_run(b).font.size = Pt(9)
        tr = row.cells[1].paragraphs[0].add_run(t)
        tr.font.bold = True
        tr.font.color.rgb = GOLD
        tr.font.size = Pt(9)
        row.cells[2].paragraphs[0].add_run(p).font.size = Pt(9)
    doc.add_paragraph()

    # ── INSERT FLOOR PLAN DIAGRAM ──
    add_gold_label(doc, 'Rajah 1: Pelan Lantai Pejabat (Tingkat 1 & 2)')
    print('  → Menjana gambar pelan lantai...')
    fp_buf = draw_floor_plan()
    doc.add_picture(fp_buf, width=Inches(9.0))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph('Rajah 1: Pelan Lantai & Susun Atur Kabel — Topologi Star')
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in cap.runs:
        r.font.italic = True
        r.font.size = Pt(9)
        r.font.color.rgb = MUTED
    doc.add_paragraph()

    # ── SECTION 3: TOPOLOGI STAR ──
    add_section_title(doc, '3.', 'Rekabentuk Topologi Star — Rajah Logik')
    add_body(doc,
        'Rajah logik menunjukkan hubungan antara semua peranti dalam rangkaian. Setiap peranti '
        'disambung terus ke suis pusat (Main Switch) di Tingkat 1. Suis agihan (Distribution Switch) '
        'di Tingkat 2 disambung ke Main Switch melalui fiber optik kelajuan 1 Gbps.')

    add_body(doc,
        'Semua trafik internet masuk melalui firewall dahulu sebelum diagihkan ke Main Switch. '
        'Ini memastikan keselamatan rangkaian dalaman daripada ancaman luar.')

    print('  → Menjana rajah topologi star...')
    st_buf = draw_star_topology()
    doc.add_picture(st_buf, width=Inches(9.0))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap2 = doc.add_paragraph('Rajah 2: Topologi Star — Rajah Logik Keseluruhan Rangkaian')
    cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in cap2.runs:
        r.font.italic = True
        r.font.size = Pt(9)
        r.font.color.rgb = MUTED

    doc.add_page_break()

    # ── SECTION 4: SUSUN ATUR KABEL ──
    add_section_title(doc, '4.', 'Susun Atur & Laluan Kabel')
    add_body(doc,
        'Kabel disusun mengikut laluan yang terancang menggunakan trunking PVC di dinding '
        'dan cable tray logam di siling. Semua kabel bertemu di patch panel dalam bilik pelayan '
        'sebelum disambung ke suis utama.')

    print('  → Menjana rajah keratan rentas kabel...')
    cr_buf = draw_cable_routing()
    doc.add_picture(cr_buf, width=Inches(9.0))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap3 = doc.add_paragraph('Rajah 3: Keratan Rentas Laluan Kabel (Cross-Section View)')
    cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in cap3.runs:
        r.font.italic = True
        r.font.size = Pt(9)
        r.font.color.rgb = MUTED

    doc.add_paragraph()
    add_gold_label(doc, 'Peraturan Pemasangan Kabel')
    rules = [
        '✦  Kabel UTP Cat6 mesti tidak melebihi 100 meter dari suis ke peranti.',
        '✦  Kabel data (UTP) dipisahkan sekurang-kurangnya 30 cm dari kabel kuasa elektrik.',
        '✦  Setiap kabel dilabel di kedua-dua hujung (contoh: "T1-B.Pengurus-PC1-Port03").',
        '✦  Kabel disusun dalam trunking PVC di dinding, setinggi 30 cm dari lantai atau di siling.',
        '✦  Gunakan cable tie setiap 30 cm untuk menyusun kabel dalam cable tray siling.',
        '✦  Semua kabel berakhir di patch panel — tidak ada kabel yang disambung terus ke suis.',
        '✦  Fiber optik backbone disusun dalam conduit fiber yang berasingan.',
    ]
    for rule in rules:
        p = doc.add_paragraph(rule, style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        for r in p.runs:
            r.font.size = Pt(10)

    doc.add_page_break()

    # ── SECTION 5: JENIS KABEL ──
    add_section_title(doc, '5.', 'Spesifikasi Kabel Yang Digunakan')

    cable_data = [
        ('Jenis Kabel',        'Spesifikasi',                  'Fungsi',                          'Warna Rajah'),
        ('UTP Cat6',           '1 Gbps | 100m | 23 AWG | RJ45','Sambungan PC & Pencetak ke suis', 'Biru / Merah / Hijau'),
        ('Cat6 PoE',           'PoE 802.3af | 15.4W | 1 Gbps', 'Access Point WiFi (data + kuasa)','Teal / Hijau Muda'),
        ('Fiber Singlemode',   'OS2 | 1 Gbps | LC Duplex',     'Backbone antara T1 ↔ T2 switch',  'Emas / Jingga'),
        ('Cat5e (Printer)',    '100 Mbps | 50m | RJ45',         'Pencetak rangkaian berkongsi',    'Ungu'),
        ('WAN / ISP Fiber',    'Mengikut pakej ISP',            'Internet masuk ke firewall',      'Merah'),
    ]
    cable_table = doc.add_table(rows=len(cable_data), cols=4)
    cable_table.style = 'Table Grid'
    cable_table.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, row_data in enumerate(cable_data):
        for j, cell_text in enumerate(row_data):
            cell = cable_table.rows[i].cells[j]
            if i == 0:
                set_cell_bg(cell, '1a1612')
                r = cell.paragraphs[0].add_run(cell_text)
                r.font.bold = True
                r.font.color.rgb = GOLD
                r.font.size = Pt(9)
            else:
                if i % 2 == 0:
                    set_cell_bg(cell, 'faf7f2')
                r = cell.paragraphs[0].add_run(cell_text)
                r.font.size = Pt(9)
                if j == 0:
                    r.font.bold = True

    doc.add_paragraph()

    # ── SECTION 6: SENARAI PERKAKASAN ──
    add_section_title(doc, '6.', 'Senarai Inventori Perkakasan')

    hw_data = [
        ('Bil', 'Perkakasan',               'Model Cadangan',                     'Kuantiti', 'Fungsi Utama'),
        ('1',   'Main Switch 24-Port',       'Cisco SG350-28 / TP-Link TL-SG2428P','1 unit',   'Pusat suis T1 — 24 port Gigabit'),
        ('2',   'Distribution Switch T2',   'TP-Link TL-SG2428 / Netgear GS324T', '1 unit',   'Suis agihan Tingkat 2'),
        ('3',   'Firewall / Router',         'FortiGate 40F / pfSense Mini-PC',    '1 unit',   'Keselamatan & pengurusan internet'),
        ('4',   'Komputer / Workstation',    'Dell OptiPlex / Lenovo ThinkCentre', '20 unit',  'PC pengguna akhir (PC-1 hingga PC-20)'),
        ('5',   'Access Point WiFi 6',       'Ubiquiti UniFi U6 Lite',             '3 unit',   'WiFi coverage T1 (AP-1,2) & T2 (AP-3)'),
        ('6',   'Pencetak Rangkaian',        'HP LaserJet Pro / Canon imageRUNNER','4 unit',   'Pencetak berkongsi (PRN-1 hingga PRN-4)'),
        ('7',   'Pelayan Fail (Server)',     'Dell PowerEdge T40',                 '1 unit',   'DHCP, DNS, fail berkongsi dalaman'),
        ('8',   'NAS Storage',               'Synology DS923+ / QNAP TS-464',      '1 unit',   'Sandaran data & storan berkongsi'),
        ('9',   'Kabel UTP Cat6',            'Belden / Panduit — 305m Roll',       '~500 m',   'Kabel utama semua PC & pencetak'),
        ('10',  'Fiber Optik Singlemode',    'OS2 LC-LC Duplex Patch Cable',       '30 m',     'Backbone T1 ↔ T2 switch'),
        ('11',  'Patch Panel 24-Port',       'Panduit DP24688TGY / AMP Cat6',      '2 unit',   'Pengurusan kabel di bilik pelayan & rangkaian'),
        ('12',  'Trunking PVC / Cable Tray', 'D-Line / Legrand 40×25 mm',          '~80 m',    'Pelindung & penyusun kabel'),
        ('13',  'UPS 1000VA',                'APC Smart-UPS / Eaton 5PX',          '2 unit',   'Perlindungan suis & pelayan dari gangguan kuasa'),
    ]

    hw_table = doc.add_table(rows=len(hw_data), cols=5)
    hw_table.style = 'Table Grid'
    hw_table.alignment = WD_TABLE_ALIGNMENT.LEFT

    col_widths = [Cm(0.9), Cm(4.5), Cm(5.5), Cm(1.8), Cm(6.0)]
    for i, row_data in enumerate(hw_data):
        for j, cell_text in enumerate(row_data):
            cell = hw_table.rows[i].cells[j]
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcW = OxmlElement('w:tcW')
            tcW.set(qn('w:w'), str(int(col_widths[j].emu / 914.4)))
            tcW.set(qn('w:type'), 'dxa')
            tcPr.append(tcW)
            if i == 0:
                set_cell_bg(cell, '1a1612')
                r = cell.paragraphs[0].add_run(cell_text)
                r.font.bold = True
                r.font.color.rgb = GOLD
                r.font.size = Pt(8.5)
            else:
                if i % 2 == 0:
                    set_cell_bg(cell, 'faf7f2')
                r = cell.paragraphs[0].add_run(cell_text)
                r.font.size = Pt(8.5)
                if j == 1:
                    r.font.bold = True

    doc.add_paragraph()

    # ── SECTION 7: KESELAMATAN ──
    add_section_title(doc, '7.', 'Pertimbangan Keselamatan Rangkaian')

    security_items = [
        ('Firewall', 'Semua trafik internet ditapis melalui firewall sebelum masuk ke rangkaian dalaman. '
                     'Peraturan firewall dikonfigurasi untuk menyekat akses tidak dibenarkan.'),
        ('VLAN Segmentation', 'Rangkaian dibahagikan kepada VLAN berbeza mengikut jabatan — '
                               'contohnya VLAN IT, VLAN Pengurusan, VLAN Tetamu (WiFi). '
                               'Ini menghalang peranti dalam VLAN berbeza daripada berkomunikasi secara langsung.'),
        ('Port Security', 'Suis dikonfigurasi dengan port security — setiap port hanya membenarkan '
                          'alamat MAC tertentu. Peranti tidak dibenarkan tidak akan dapat menyambung.'),
        ('Pemantauan Rangkaian', 'Sistem SNMP dan syslog dipasang untuk memantau aktiviti rangkaian '
                                  'secara masa nyata. Amaran dihantar jika ada aktiviti luar biasa.'),
        ('Sandaran Berkala', 'Konfigurasi suis, firewall, dan data disandar setiap malam ke NAS. '
                              'Sandaran disulitkan untuk mengelak akses tidak dibenarkan.'),
    ]

    for title, desc in security_items:
        add_gold_label(doc, title)
        add_body(doc, desc)

    # ── FOOTER NOTE ──
    doc.add_paragraph()
    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    nr = note.add_run('─' * 60)
    nr.font.color.rgb = GOLD
    nr.font.size = Pt(8)

    foot = doc.add_paragraph()
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = foot.add_run('Dokumen ini disediakan oleh DocuMate · Malaysia · 2026')
    fr.font.size = Pt(8)
    fr.font.color.rgb = MUTED

    # ── SAVE ──
    out_path = '/home/user/DocuMate/Pelan_Lantai_Topologi_Star.docx'
    doc.save(out_path)
    print(f'\n✅ Dokumen Word berjaya disimpan: {out_path}')
    return out_path


if __name__ == '__main__':
    print('🔨 Membina dokumen Word...')
    build_word()
