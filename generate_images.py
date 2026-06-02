"""Generate 4 professional diagrams for the DKM Network Lab report."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import matplotlib.patheffects as pe
import numpy as np
import os

OUT = '/home/user/DocuMate/images'
os.makedirs(OUT, exist_ok=True)

# ── Shared theme ──────────────────────────────────────────────────────────────
CISCO_BLUE  = '#00549F'
DARK_BLUE   = '#003D73'
LIGHT_BLUE  = '#EBF8FF'
ACCENT      = '#1BA3E8'
GREEN       = '#38A169'
ORANGE      = '#DD6B20'
RED         = '#E53E3E'
GRAY_DARK   = '#2D3748'
GRAY_MID    = '#718096'
GRAY_LIGHT  = '#EDF2F7'
WHITE       = '#FFFFFF'
RACK_BG     = '#1C2433'
RACK_UNIT   = '#2D3748'
YELLOW      = '#D69E2E'

plt.rcParams.update({
    'font.family':   'DejaVu Sans',
    'figure.facecolor': WHITE,
    'axes.facecolor':   WHITE,
})


def shadow_box(ax, x, y, w, h, fc, ec, lw=1.5, radius=0.3, zorder=3):
    # shadow
    ax.add_patch(FancyBboxPatch((x+0.06, y-0.06), w, h,
        boxstyle=f'round,pad=0,rounding_size={radius}',
        fc='#00000033', ec='none', zorder=zorder-1))
    # main
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f'round,pad=0,rounding_size={radius}',
        fc=fc, ec=ec, lw=lw, zorder=zorder))


# ══════════════════════════════════════════════════════════════════════════════
#  IMAGE 1 – PHYSICAL FLOOR PLAN
# ══════════════════════════════════════════════════════════════════════════════

def draw_floor_plan():
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16); ax.set_ylim(0, 12)
    ax.set_aspect('equal'); ax.axis('off')

    # ── Room outline ──
    room = FancyBboxPatch((0.4, 0.4), 15.2, 11.2,
        boxstyle='round,pad=0,rounding_size=0.2',
        fc='#F7FAFC', ec=GRAY_DARK, lw=4, zorder=1)
    ax.add_patch(room)

    # Title banner
    ax.add_patch(FancyBboxPatch((0.4, 11.15), 15.2, 0.45,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc=DARK_BLUE, ec='none', zorder=5))
    ax.text(8, 11.4, 'PELAN SUSUN ATUR MAKMAL RANGKAIAN KOMPUTER',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=WHITE, zorder=6)

    # ── Projector screen (front wall) ──
    ax.add_patch(FancyBboxPatch((2.0, 10.2), 7.0, 0.5,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#E2E8F0', ec=GRAY_DARK, lw=2, zorder=4))
    ax.text(5.5, 10.45, '▬  SKRIN PROJEKTOR  ▬',
        ha='center', va='center', fontsize=9, color=GRAY_DARK, fontweight='bold', zorder=5)

    # ── Teacher desk ──
    shadow_box(ax, 4.5, 8.8, 4.0, 1.1, LIGHT_BLUE, CISCO_BLUE, lw=2.5, zorder=4)
    # Monitor icon
    ax.add_patch(FancyBboxPatch((5.8, 8.95), 1.6, 0.8,
        boxstyle='round,pad=0,rounding_size=0.05', fc=GRAY_DARK, ec='none', zorder=5))
    ax.add_patch(FancyBboxPatch((5.9, 9.0), 1.4, 0.65,
        boxstyle='round,pad=0,rounding_size=0.03', fc=CISCO_BLUE, ec='none', zorder=6))
    # PC tower
    ax.add_patch(FancyBboxPatch((5.1, 8.95), 0.45, 0.7,
        boxstyle='round,pad=0,rounding_size=0.05', fc=GRAY_DARK, ec='none', zorder=5))
    ax.plot(5.32, 9.18, 'o', color=GREEN, ms=5, zorder=6)
    ax.text(6.5, 9.32, 'PC PENGAJAR', ha='center', va='center',
        fontsize=7, fontweight='bold', color=WHITE, zorder=7)
    ax.text(6.5, 9.1, '192.168.1.1', ha='center', va='center',
        fontsize=6.5, color='#BEE3F8', zorder=7)
    ax.text(6.5, 8.72, 'KOMPUTER PENGAJAR (VLAN 20)',
        ha='center', va='center', fontsize=8, fontweight='bold', color=CISCO_BLUE, zorder=5)

    # ── Network Rack ──
    shadow_box(ax, 13.0, 8.5, 2.0, 2.4, RACK_BG, '#4A5568', lw=2, radius=0.2, zorder=4)
    ax.add_patch(FancyBboxPatch((13.1, 8.6), 1.8, 2.2,
        boxstyle='round,pad=0,rounding_size=0.1', fc='#141921', ec='#4A5568', lw=1, zorder=5))
    # Rack units
    unit_colors = [CISCO_BLUE, DARK_BLUE, '#2D3748', RACK_UNIT, RACK_UNIT]
    unit_labels = ['PATCH\nPANEL','CISCO\n2960 SW','CISCO\n1941 RT','UPS\n1000VA','PDU\nPSU']
    for i, (uc, ul) in enumerate(zip(unit_colors, unit_labels)):
        uy = 8.65 + i * 0.43
        ax.add_patch(FancyBboxPatch((13.15, uy), 1.7, 0.38,
            boxstyle='round,pad=0,rounding_size=0.05', fc=uc, ec='#4A5568', lw=0.8, zorder=6))
        ax.plot(13.22, uy+0.19, 'o', color=GREEN if i < 3 else (ORANGE if i==3 else GREEN),
            ms=4, zorder=7)
        ax.text(14.0, uy+0.19, ul, ha='center', va='center',
            fontsize=5.5, color=WHITE, fontweight='bold', zorder=7)
    ax.text(14.0, 8.42, 'NETWORK RACK 12U', ha='center', va='center',
        fontsize=7.5, fontweight='bold', color=WHITE, zorder=5)

    # ── UPS box ──
    shadow_box(ax, 13.0, 7.2, 2.0, 0.85, '#1A202C', RED, lw=2, radius=0.15, zorder=4)
    ax.add_patch(FancyBboxPatch((13.1, 7.25), 0.55, 0.3,
        boxstyle='round,pad=0,rounding_size=0.05', fc=GREEN, ec='none', zorder=5))
    ax.text(14.0, 7.62, 'UPS 1000VA', ha='center', va='center',
        fontsize=8, fontweight='bold', color=WHITE, zorder=5)
    ax.text(14.0, 7.4, 'APC Smart-UPS', ha='center', va='center',
        fontsize=6.5, color='#FC8181', zorder=5)

    # ── Cable tray (horizontal top + vertical right) ──
    # Horizontal tray
    ax.add_patch(mpatches.FancyArrowPatch(
        (1.0, 8.6), (12.8, 8.6), arrowstyle='-',
        color=YELLOW, lw=5, linestyle='dashed', zorder=3, alpha=0.7))
    ax.text(7.0, 8.45, '═══ CABLE TRAY Cat6 UTP ═══', ha='center', va='center',
        fontsize=7, color=YELLOW, fontweight='bold', zorder=4)
    # Vertical tray
    ax.plot([12.8, 12.8], [8.6, 0.8], color=YELLOW, lw=5, ls='dashed', zorder=3, alpha=0.7)

    # ── Student PCs (5 rows × 5 cols) ──
    pc_cols = [1.2, 3.2, 5.2, 7.2, 9.2]
    pc_rows = [7.2, 6.0, 4.8, 3.6, 2.4]
    row_labels = ['Baris 1', 'Baris 2', 'Baris 3', 'Baris 4', 'Baris 5']
    pc_num = 1

    for ri, (ry, rl) in enumerate(zip(pc_rows, row_labels)):
        ax.text(0.55, ry + 0.4, rl, ha='center', va='center',
            fontsize=7, color=GRAY_MID, rotation=0, fontstyle='italic')
        for ci, cx in enumerate(pc_cols):
            ip_last = 9 + pc_num
            # desk
            ax.add_patch(FancyBboxPatch((cx, ry), 1.5, 0.85,
                boxstyle='round,pad=0,rounding_size=0.08',
                fc=GRAY_LIGHT, ec='#4A5568', lw=1.2, zorder=3))
            # monitor
            ax.add_patch(FancyBboxPatch((cx+0.35, ry+0.18), 0.8, 0.52,
                boxstyle='round,pad=0,rounding_size=0.04',
                fc=GRAY_DARK, ec='none', zorder=4))
            ax.add_patch(FancyBboxPatch((cx+0.38, ry+0.21), 0.74, 0.44,
                boxstyle='round,pad=0,rounding_size=0.02',
                fc=CISCO_BLUE, ec='none', zorder=5))
            # pc tower
            ax.add_patch(FancyBboxPatch((cx+0.08, ry+0.2), 0.22, 0.44,
                boxstyle='round,pad=0,rounding_size=0.04',
                fc=GRAY_DARK, ec='none', zorder=4))
            ax.plot(cx+0.19, ry+0.37, 'o', color=GREEN, ms=3, zorder=5)
            # IP text
            ax.text(cx+0.75, ry+0.43, f'.{ip_last}', ha='center', va='center',
                fontsize=5.5, color=WHITE, fontweight='bold', zorder=6)
            # label
            ax.text(cx+0.75, ry+0.07, f'PC-{pc_num:02d}',
                ha='center', va='center', fontsize=7, fontweight='bold',
                color=DARK_BLUE, zorder=4)
            # cable to tray
            ax.plot([cx+0.75, cx+0.75, 12.8], [ry+0.85, 8.6, 8.6],
                color='#718096', lw=0.6, ls=':', zorder=2, alpha=0.5)
            pc_num += 1

    # ── Door ──
    ax.add_patch(mpatches.Arc((1.2, 0.4), 1.6, 1.6, angle=0, theta1=0, theta2=90,
        color=GRAY_DARK, lw=1.5, linestyle='dashed', zorder=3))
    ax.plot([1.2, 1.2], [0.4, 1.2], color=GRAY_DARK, lw=2, zorder=3)
    ax.text(1.5, 0.22, 'PINTU', ha='center', fontsize=7, color=GRAY_MID, zorder=3)

    # ── Dimension arrows ──
    ax.annotate('', xy=(15.6, 0.4), xytext=(15.6, 11.2),
        arrowprops=dict(arrowstyle='<->', color=GRAY_MID, lw=1.5))
    ax.text(15.85, 5.8, '~8 m', va='center', fontsize=8, color=GRAY_MID, rotation=90)
    ax.annotate('', xy=(0.4, 0.15), xytext=(15.6, 0.15),
        arrowprops=dict(arrowstyle='<->', color=GRAY_MID, lw=1.5))
    ax.text(8.0, -0.08, '~10 meter', ha='center', fontsize=8, color=GRAY_MID)

    # ── Legend ──
    legend_items = [
        mpatches.Patch(fc=CISCO_BLUE, ec='none', label='Komputer Pengajar (1 unit)'),
        mpatches.Patch(fc=GRAY_LIGHT, ec='#4A5568', label='PC Pelajar (25 unit)'),
        mpatches.Patch(fc=RACK_BG, ec='#4A5568', label='Network Rack 12U'),
        mpatches.Patch(fc=YELLOW, ec='none', label='Cable Tray Cat6', alpha=0.7),
    ]
    ax.legend(handles=legend_items, loc='lower right', fontsize=8,
        framealpha=0.95, edgecolor=GRAY_MID, bbox_to_anchor=(0.99, 0.01))

    fig.tight_layout(pad=0.3)
    path = f'{OUT}/01_floor_plan.png'
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print(f'  Saved: {path}')


# ══════════════════════════════════════════════════════════════════════════════
#  IMAGE 2 – LOGICAL NETWORK TOPOLOGY
# ══════════════════════════════════════════════════════════════════════════════

def arrow(ax, x0, y0, x1, y1, color='#4A5568', lw=2, style='-', zorder=3):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(arrowstyle='->', color=color, lw=lw,
            connectionstyle='arc3,rad=0.0'),
        zorder=zorder)

def dbl_arrow(ax, x0, y0, x1, y1, color='#4A5568', lw=2):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(arrowstyle='<->', color=color, lw=lw), zorder=3)

def draw_topology():
    fig, ax = plt.subplots(figsize=(16, 13))
    ax.set_xlim(0, 16); ax.set_ylim(0, 13)
    ax.set_aspect('equal'); ax.axis('off')

    # Background
    ax.add_patch(FancyBboxPatch((0,0), 16, 13,
        boxstyle='round,pad=0,rounding_size=0.3',
        fc='#F7FAFC', ec='none', zorder=0))

    # Title
    ax.add_patch(FancyBboxPatch((0, 12.2), 16, 0.8,
        boxstyle='round,pad=0,rounding_size=0.1', fc=DARK_BLUE, ec='none', zorder=5))
    ax.text(8, 12.6, 'TOPOLOGI RANGKAIAN LOGIK – MAKMAL RANGKAIAN DKM',
        ha='center', va='center', fontsize=13, fontweight='bold', color=WHITE, zorder=6)

    # ── Internet Cloud ──
    ellipse = mpatches.Ellipse((8, 11.2), 3.5, 1.1,
        fc='#DBEAFE', ec=ACCENT, lw=2.5, zorder=4)
    ax.add_patch(ellipse)
    ax.text(8, 11.2, '☁  INTERNET / ISP', ha='center', va='center',
        fontsize=10, fontweight='bold', color=DARK_BLUE, zorder=5)

    # cloud puffs
    for cx, cy, r in [(6.8,11.4,0.45),(7.35,11.55,0.5),(8,11.65,0.55),
                       (8.65,11.55,0.5),(9.2,11.4,0.45)]:
        ax.add_patch(mpatches.Circle((cx,cy), r, fc='#DBEAFE', ec=ACCENT, lw=1.5, zorder=3))

    # WAN line
    ax.plot([8, 8], [10.65, 10.35], color=GRAY_DARK, lw=2.5, zorder=3)
    ax.plot(8, 10.5, 'v', color=GRAY_DARK, ms=8, zorder=4)
    ax.text(8.25, 10.5, 'WAN / DHCP', va='center', fontsize=8, color=GRAY_MID)

    # ── Router ──
    shadow_box(ax, 6.2, 9.1, 3.6, 1.2, CISCO_BLUE, DARK_BLUE, lw=2.5, radius=0.25, zorder=4)
    # router icon (circle with lines)
    ax.add_patch(mpatches.Circle((7.0, 9.72), 0.38, fc='none', ec=WHITE, lw=2, zorder=5))
    ax.plot([6.62,7.38],[9.72,9.72], color=WHITE, lw=1.5, zorder=6)
    ax.plot([7.0,7.0],[9.34,10.1], color=WHITE, lw=1.5, zorder=6)
    ax.plot([6.72,7.27],[9.45,9.99], color=WHITE, lw=1, zorder=6, alpha=0.7)
    ax.text(7.85, 9.85, 'CISCO 1941 ROUTER', ha='left', va='center',
        fontsize=10, fontweight='bold', color=WHITE, zorder=5)
    ax.text(7.85, 9.55, 'Fa0/0: 192.168.1.254  (LAN)', ha='left', va='center',
        fontsize=8, color='#BEE3F8', zorder=5)
    ax.text(7.85, 9.3, 'Fa0/1: DHCP  (WAN / ISP)', ha='left', va='center',
        fontsize=8, color='#BEE3F8', zorder=5)

    # LAN line
    ax.plot([8, 8], [9.1, 8.55], color=GRAY_DARK, lw=3, zorder=3)
    ax.text(8.15, 8.83, 'GigabitEthernet', va='center', fontsize=7.5, color=GRAY_MID)

    # ── Switch ──
    shadow_box(ax, 5.8, 7.6, 4.4, 0.9, DARK_BLUE, '#1A3A5C', lw=2.5, radius=0.2, zorder=4)
    # port dots
    for i in range(24):
        px = 6.0 + i * 0.155
        ax.plot(px, 8.12, 's', color=GREEN, ms=4.5, zorder=5)
    ax.plot(9.85, 8.12, 's', color=ACCENT, ms=5, zorder=5)
    ax.plot(10.0, 8.12, 's', color=ACCENT, ms=5, zorder=5)
    ax.text(8.0, 7.82, 'CISCO CATALYST 2960-24TT',
        ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, zorder=5)
    ax.text(8.0, 7.65, '24× FastEthernet  |  2× GigabitEthernet Uplink',
        ha='center', va='center', fontsize=7.5, color='#90CDF4', zorder=5)

    # patch panel label
    ax.add_patch(FancyBboxPatch((5.8, 8.52), 4.4, 0.35,
        boxstyle='round,pad=0,rounding_size=0.1', fc='#2D3748', ec='#4A5568', lw=1, zorder=4))
    ax.text(8.0, 8.7, 'PATCH PANEL 24-port Cat6 (1U)',
        ha='center', va='center', fontsize=8, color='#E2E8F0', fontweight='bold', zorder=5)

    # ── Fan-out lines ──
    branch_x = [2.0, 5.5, 10.5, 13.5]
    branch_labels = ['PC PENGAJAR\n(VLAN 20)', 'PC PELAJAR 01–10\n(VLAN 10)',
                     'PC PELAJAR 11–20\n(VLAN 10)', 'PC PELAJAR 21–25\n(VLAN 10)']
    branch_ips    = ['192.168.1.1', '192.168.1.10 – .19',
                     '192.168.1.20 – .29', '192.168.1.30 – .34']
    branch_fc     = [LIGHT_BLUE, '#F0FFF4', '#F0FFF4', '#F0FFF4']
    branch_ec     = [CISCO_BLUE, GREEN, GREEN, GREEN]
    branch_ports  = ['Fa0/24', 'Fa0/1–Fa0/10', 'Fa0/11–Fa0/20', 'Fa0/21–Fa0/25']

    sw_bottom_y = 7.6
    for bx, bl, bip, bfc, bec, bport in zip(branch_x, branch_labels, branch_ips,
                                              branch_fc, branch_ec, branch_ports):
        # Line from switch to group
        ax.plot([bx, bx, 8], [5.2, sw_bottom_y-0.02, sw_bottom_y-0.02],
            color='#4A5568', lw=2, ls='--', zorder=2, alpha=0.8)
        ax.plot(bx, 5.2, 'v', color='#4A5568', ms=7, zorder=3)

        # Group box
        shadow_box(ax, bx-1.4, 2.3, 2.8, 2.7, bfc, bec, lw=2.5, radius=0.25, zorder=4)

        # PC icons inside box
        for i in range(min(3, 3)):
            px = bx - 0.8 + i * 0.8
            ax.add_patch(FancyBboxPatch((px-0.28, 4.5), 0.56, 0.42,
                boxstyle='round,pad=0,rounding_size=0.06',
                fc=GRAY_DARK, ec='none', zorder=5))
            ax.add_patch(FancyBboxPatch((px-0.25, 4.53), 0.5, 0.34,
                boxstyle='round,pad=0,rounding_size=0.03',
                fc=CISCO_BLUE if 'PENGAJAR' in bl else '#2B6CB0', ec='none', zorder=6))
            ax.add_patch(FancyBboxPatch((px-0.14, 4.92), 0.28, 0.08,
                boxstyle='round,pad=0,rounding_size=0.03',
                fc='#718096', ec='none', zorder=6))

        ax.text(bx, 4.3, bl, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=bec, zorder=5,
            multialignment='center')
        ax.text(bx, 3.8, bip, ha='center', va='center',
            fontsize=8, color=GRAY_DARK, zorder=5)
        ax.text(bx, 3.45, f'GW: 192.168.1.254', ha='center', va='center',
            fontsize=7.5, color=GRAY_MID, zorder=5)
        ax.text(bx, 3.1, f'Port: {bport}', ha='center', va='center',
            fontsize=7, color=GRAY_MID, zorder=5, fontstyle='italic')
        ax.text(bx, 2.7, f'DNS: 8.8.8.8 / 8.8.4.4', ha='center', va='center',
            fontsize=7, color=GRAY_MID, zorder=5)

    # ── UPS box (right) ──
    shadow_box(ax, 12.3, 9.1, 3.2, 1.1, '#FFF5F5', RED, lw=2, radius=0.2, zorder=4)
    ax.text(13.9, 9.72, 'UPS – APC Smart-UPS 1000VA', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#9B2C2C', zorder=5)
    ax.text(13.9, 9.42, 'Bekalan kuasa sandaran ~15 min', ha='center', va='center',
        fontsize=8, color=GRAY_MID, zorder=5)
    ax.text(13.9, 9.22, 'AVR | Lead-Acid VRLA Battery', ha='center', va='center',
        fontsize=7.5, color=GRAY_MID, zorder=5)
    ax.plot([12.3, 9.8], [9.65, 9.65], color=RED, lw=1.5, ls='--', zorder=3)
    ax.text(11.0, 9.78, 'Bekalan kuasa', fontsize=7, color=RED, ha='center', zorder=4)

    # ── VLAN legend ──
    ax.add_patch(FancyBboxPatch((0.3, 0.2), 15.4, 0.7,
        boxstyle='round,pad=0,rounding_size=0.1', fc='#EDF2F7', ec='#CBD5E0', lw=1, zorder=4))
    ax.text(0.7, 0.55, 'VLAN:', fontsize=9, fontweight='bold', color=GRAY_DARK, va='center', zorder=5)
    vlan_items = [
        (GREEN,    'VLAN 10 – PELAJAR     (192.168.10.0/24)',  1.8),
        (CISCO_BLUE,'VLAN 20 – PENGAJAR  (192.168.20.0/24)',  6.5),
        (ORANGE,   'VLAN 99 – PENGURUSAN (192.168.99.0/24)', 11.2),
    ]
    for vc, vl, vx in vlan_items:
        ax.add_patch(FancyBboxPatch((vx, 0.33), 0.45, 0.45,
            boxstyle='round,pad=0', fc=vc, ec='none', zorder=5))
        ax.text(vx+0.6, 0.55, vl, fontsize=8.5, va='center', color=GRAY_DARK, zorder=5)

    fig.tight_layout(pad=0.3)
    path = f'{OUT}/02_network_topology.png'
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print(f'  Saved: {path}')


# ══════════════════════════════════════════════════════════════════════════════
#  IMAGE 3 – NETWORK RACK 12U
# ══════════════════════════════════════════════════════════════════════════════

def draw_rack():
    fig, ax = plt.subplots(figsize=(14, 16))
    ax.set_xlim(0, 14); ax.set_ylim(0, 16)
    ax.axis('off')

    # Background
    ax.add_patch(FancyBboxPatch((0,0),14,16,
        boxstyle='round,pad=0,rounding_size=0.2', fc='#EDF2F7', ec='none', zorder=0))

    # Title
    ax.add_patch(FancyBboxPatch((0, 15.2), 14, 0.8,
        boxstyle='round,pad=0,rounding_size=0.1', fc=DARK_BLUE, ec='none', zorder=5))
    ax.text(7, 15.6, 'REKABENTUK NETWORK RACK 12U – MAKMAL RANGKAIAN DKM',
        ha='center', va='center', fontsize=13, fontweight='bold', color=WHITE, zorder=6)

    # ── Rack outer frame ──
    rack_x, rack_y, rack_w, rack_h = 3.5, 0.8, 7.0, 14.2
    # shadow
    ax.add_patch(FancyBboxPatch((rack_x+0.15, rack_y-0.15), rack_w, rack_h,
        boxstyle='round,pad=0,rounding_size=0.3',
        fc='#00000055', ec='none', zorder=1))
    # frame
    ax.add_patch(FancyBboxPatch((rack_x, rack_y), rack_w, rack_h,
        boxstyle='round,pad=0,rounding_size=0.3',
        fc='#1A202C', ec='#718096', lw=4, zorder=2))
    # inner frame
    ax.add_patch(FancyBboxPatch((rack_x+0.3, rack_y+0.3), rack_w-0.6, rack_h-0.6,
        boxstyle='round,pad=0,rounding_size=0.2',
        fc='#141921', ec='#4A5568', lw=2, zorder=3))

    # Rack title plate
    ax.add_patch(FancyBboxPatch((rack_x+0.35, rack_y+0.35), rack_w-0.7, 0.7,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#2D3748', ec='#4A5568', lw=1, zorder=4))
    ax.text(7.0, rack_y+0.72, '▐  NETWORK RACK 12U  ▌  MAKMAL RANGKAIAN',
        ha='center', va='center', fontsize=9, fontweight='bold', color='#E2E8F0', zorder=5)

    # ── Rack units data ──
    units = [
        # (U, label, sublabel, fc, ec, led_color, port_count, port_color)
        ('1U',    'PATCH PANEL Cat6 24-port',   'Panduit / Legrand / Generic',
         '#374151', '#4A5568', '#63B3ED', 24, '#63B3ED'),
        ('2U–3U', 'CISCO CATALYST 2960-24TT',   '24× FastEthernet  |  2× GigabitEthernet Uplink',
         CISCO_BLUE, DARK_BLUE, GREEN, 26, GREEN),
        ('4U',    'CISCO 1941 ROUTER',           'Fa0/0: LAN 192.168.1.254  |  Fa0/1: WAN/ISP',
         DARK_BLUE, '#001A40', GREEN, 2, ACCENT),
        ('5U',    'CABLE MANAGEMENT 1U',         'D-Ring / Horizontal Manager / Velcro Ties',
         '#1A202C', '#4A5568', '#4A5568', 0, '#4A5568'),
        ('6U',    'RESERVED – Ruang Simpanan',   'Untuk pengembangan masa hadapan (future use)',
         '#1A202C', '#2D3748', '#4A5568', 0, '#4A5568'),
        ('7U',    'RESERVED – Ruang Simpanan',   '',
         '#1A202C', '#2D3748', '#4A5568', 0, '#4A5568'),
        ('8U–9U', 'UPS – APC Smart-UPS 1000VA', '700W  |  Runtime ~15 min  |  AVR Built-in',
         '#1A3A5C', RED, ORANGE, 0, ORANGE),
        ('10U',   'PDU – Power Distribution',    '8× C13 Outlet  |  16A / 250V  |  Surge Protection',
         '#1A202C', '#4A5568', GREEN, 8, GREEN),
        ('11U',   'FAN TRAY 1U',                 '2× 80mm Fan  |  1500 RPM  |  Rack Cooling',
         '#1A202C', '#4A5568', ACCENT, 0, ACCENT),
        ('12U',   'BLANK PANEL',                 '1U Filler Panel',
         '#141921', '#2D3748', '#2D3748', 0, '#2D3748'),
    ]

    # Heights per logical unit
    unit_heights = [0.8, 1.6, 0.8, 0.8, 0.8, 0.8, 1.6, 0.8, 0.8, 0.8]
    start_y = rack_y + 1.1

    for (u, label, sub, fc, ec, lc, nports, pc), uh in zip(units, unit_heights):
        ux = rack_x + 0.35
        uw = rack_w - 0.7
        # unit background
        ax.add_patch(FancyBboxPatch((ux, start_y), uw, uh-0.06,
            boxstyle='round,pad=0,rounding_size=0.08',
            fc=fc, ec=ec, lw=1.5, zorder=4))

        # LED
        ax.plot(ux+0.18, start_y+uh/2-0.03, 'o', color=lc, ms=8, zorder=5)
        if lc != '#4A5568' and lc != '#2D3748':
            ax.plot(ux+0.18, start_y+uh/2-0.03, 'o',
                color=lc, ms=14, alpha=0.3, zorder=4)  # glow

        # U label
        ax.text(ux+0.45, start_y+uh/2-0.03, u,
            va='center', fontsize=8, fontweight='bold', color='#718096', zorder=5)

        # Main label
        ax.text(ux+1.15, start_y+(uh*0.65 if sub else uh/2)-0.03,
            label, va='center', fontsize=10, fontweight='bold', color='#E2E8F0', zorder=5)

        # Sub-label
        if sub:
            ax.text(ux+1.15, start_y+uh*0.28-0.03, sub,
                va='center', fontsize=7.5, color='#A0AEC0', zorder=5)

        # Ports
        if nports > 0:
            port_start = ux + uw - 0.25 - nports * 0.18
            for i in range(min(nports, 26)):
                px2 = port_start + i * 0.18
                ax.add_patch(FancyBboxPatch((px2, start_y+uh/2-0.12), 0.13, 0.08,
                    boxstyle='round,pad=0,rounding_size=0.02',
                    fc=pc, ec='#141921', lw=0.5, zorder=6, alpha=0.9))

        # Divider line after each unit
        ax.plot([ux, ux+uw], [start_y, start_y], color='#4A5568', lw=0.8, zorder=5)

        start_y += uh

    # Rack rails (decorative side strips)
    for rx in [rack_x+0.3, rack_x+rack_w-0.3]:
        ax.add_patch(FancyBboxPatch((rx-0.05, rack_y+1.0), 0.1, rack_h-1.4,
            boxstyle='round,pad=0,rounding_size=0.05',
            fc='#4A5568', ec='none', zorder=3))
        # Screw holes
        for sy in np.arange(rack_y+1.3, rack_y+rack_h-0.5, 0.8):
            ax.plot(rx, sy, 's', color='#718096', ms=4, zorder=4)

    # ── Right panel: specs ──
    spec_x = 11.0
    specs = [
        ('DIMENSI RAK',   '600mm × 600mm × 600mm'),
        ('KAPASITI',      '12U (Unit Rak)'),
        ('BERAT MAKS',    '60 kilogram'),
        ('JENIS',         'Wall-Mount / Free-Stand'),
        ('BAHAN',         'Steel Powder-Coated'),
        ('WARNA',         'Hitam (RAL 9005)'),
        ('VENTILASI',     'Fan Tray 2× 80mm'),
        ('BEKALAN KUASA', 'UPS 1000VA + PDU 16A'),
        ('LOKASI',        'Sudut belakang kanan'),
    ]
    ax.add_patch(FancyBboxPatch((spec_x-0.3, 2.5), 3.0, 12.0,
        boxstyle='round,pad=0,rounding_size=0.2',
        fc=WHITE, ec='#CBD5E0', lw=1.5, zorder=3))
    ax.text(spec_x+1.15, 14.2, 'SPESIFIKASI RAK', ha='center', va='center',
        fontsize=10, fontweight='bold', color=DARK_BLUE, zorder=4)
    divider_y = 14.05
    ax.plot([spec_x-0.25, spec_x+2.65], [divider_y, divider_y],
        color=CISCO_BLUE, lw=2, zorder=4)

    for i, (k, v) in enumerate(specs):
        sy = 13.5 - i * 1.18
        ax.add_patch(FancyBboxPatch((spec_x-0.25, sy-0.25), 2.9, 1.0,
            boxstyle='round,pad=0,rounding_size=0.1',
            fc='#EBF5FF' if i%2==0 else WHITE, ec='#E2E8F0', lw=0.8, zorder=4))
        ax.text(spec_x+0.05, sy+0.48, k, va='center', fontsize=7.5,
            fontweight='bold', color=CISCO_BLUE, zorder=5)
        ax.text(spec_x+0.05, sy+0.18, v, va='center', fontsize=8.5,
            color=GRAY_DARK, zorder=5)

    fig.tight_layout(pad=0.3)
    path = f'{OUT}/03_network_rack.png'
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='#EDF2F7')
    plt.close(fig)
    print(f'  Saved: {path}')


# ══════════════════════════════════════════════════════════════════════════════
#  IMAGE 4 – CAT6 TIA-568B WIRING DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════

def draw_cabling():
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16); ax.set_ylim(0, 12)
    ax.axis('off')

    # Background
    ax.add_patch(FancyBboxPatch((0,0),16,12,
        boxstyle='round,pad=0,rounding_size=0.3', fc='#F7FAFC', ec='none', zorder=0))

    # Title
    ax.add_patch(FancyBboxPatch((0, 11.2), 16, 0.8,
        boxstyle='round,pad=0,rounding_size=0.1', fc=DARK_BLUE, ec='none', zorder=5))
    ax.text(8, 11.6, 'SPESIFIKASI KABEL UTP CAT6 – PIAWAIAN EIA/TIA-568B',
        ha='center', va='center', fontsize=13, fontweight='bold', color=WHITE, zorder=6)

    # ── 568B Pin-colour table (left) ──
    pin_colors = [
        ('#FF8C00', '#FFFFFF', 'Putih / Oren',  'TX+  (Transmit +)'),
        ('#FF6600', '#FFFFFF', 'Oren',           'TX-  (Transmit -)'),
        ('#90EE90', '#000000', 'Putih / Hijau',  'RX+  (Receive +)'),
        ('#0000CD', '#FFFFFF', 'Biru',           'Tidak digunakan'),
        ('#ADD8E6', '#000000', 'Putih / Biru',   'Tidak digunakan'),
        ('#228B22', '#FFFFFF', 'Hijau',           'RX-  (Receive -)'),
        ('#DEB887', '#000000', 'Putih / Coklat', 'Tidak digunakan'),
        ('#8B4513', '#FFFFFF', 'Coklat',         'Tidak digunakan'),
    ]

    table_x, table_y = 0.4, 2.0
    ax.add_patch(FancyBboxPatch((table_x-0.1, table_y-0.1), 7.5, 8.9,
        boxstyle='round,pad=0,rounding_size=0.2', fc=WHITE, ec='#CBD5E0', lw=1.5, zorder=3))
    ax.text(table_x+3.65, table_y+8.6, 'JADUAL SUSUNAN WARNA PIN – TIA-568B',
        ha='center', va='center', fontsize=10, fontweight='bold', color=DARK_BLUE, zorder=4)
    ax.plot([table_x-0.1, table_x+7.4], [table_y+8.38, table_y+8.38],
        color=CISCO_BLUE, lw=2, zorder=4)

    # Header
    for hx, ht, hw in [(table_x, 'PIN', 0.55), (table_x+0.65, 'WARNA', 0.55),
                        (table_x+1.9, 'NAMA WARNA', 2.2), (table_x+4.3, 'FUNGSI', 3.0)]:
        ax.add_patch(FancyBboxPatch((hx, table_y+7.9), hw+0.1 if ht=='FUNGSI' else hw, 0.42,
            boxstyle='round,pad=0,rounding_size=0.05',
            fc=CISCO_BLUE, ec='none', zorder=4))
        ax.text(hx+0.3, table_y+8.11, ht, va='center', fontsize=9,
            fontweight='bold', color=WHITE, zorder=5)

    for i, (bg, fg, name, func) in enumerate(pin_colors):
        row_y = table_y + 7.15 - i * 0.97
        row_bg = '#EBF5FF' if i % 2 == 0 else WHITE
        ax.add_patch(FancyBboxPatch((table_x-0.05, row_y-0.05), 7.4, 0.85,
            boxstyle='round,pad=0,rounding_size=0.08', fc=row_bg, ec='#E2E8F0', lw=0.8, zorder=4))
        # pin number
        ax.add_patch(mpatches.Circle((table_x+0.25, row_y+0.38), 0.28,
            fc=DARK_BLUE, ec='none', zorder=5))
        ax.text(table_x+0.25, row_y+0.38, str(i+1), ha='center', va='center',
            fontsize=9, fontweight='bold', color=WHITE, zorder=6)
        # color swatch
        ax.add_patch(FancyBboxPatch((table_x+0.62, row_y+0.1), 0.52, 0.55,
            boxstyle='round,pad=0,rounding_size=0.07', fc=bg, ec='#4A5568', lw=1.2, zorder=5))
        # stripe (white/orange etc)
        if 'Putih' in name:
            ax.add_patch(FancyBboxPatch((table_x+0.62, row_y+0.3), 0.52, 0.15,
                boxstyle='round,pad=0,rounding_size=0', fc='white', ec='none', zorder=6, alpha=0.7))
        ax.text(table_x+0.7, row_y+0.38, '', ha='center', va='center', fontsize=9, color=fg, zorder=7)
        # name
        ax.text(table_x+2.0, row_y+0.38, name, va='center', fontsize=9, color=GRAY_DARK, zorder=5)
        # function
        ax.text(table_x+4.35, row_y+0.38, func, va='center', fontsize=9, color=GRAY_DARK, zorder=5)

    # ── RJ-45 connector diagram (center-right) ──
    cj_x, cj_y = 8.5, 5.5
    # connector body
    ax.add_patch(FancyBboxPatch((cj_x, cj_y), 3.8, 4.5,
        boxstyle='round,pad=0,rounding_size=0.3', fc='#374151', ec='#718096', lw=2.5, zorder=4))
    ax.add_patch(FancyBboxPatch((cj_x+0.15, cj_y+0.15), 3.5, 4.2,
        boxstyle='round,pad=0,rounding_size=0.25', fc='#D1D5DB', ec='none', zorder=5))
    # pin channels
    pin_w = 0.28; pin_gap = 0.16
    total_w = 8*pin_w + 7*pin_gap
    start_px = cj_x + (3.8 - total_w) / 2

    pin_bg_colors = ['#FF8C00','#FF6600','#90EE90','#0000CD',
                     '#ADD8E6','#228B22','#DEB887','#8B4513']

    for i, (bg, _,_,_) in enumerate(pin_colors):
        px = start_px + i * (pin_w + pin_gap)
        # pin channel (gray)
        ax.add_patch(FancyBboxPatch((px, cj_y+0.35), pin_w, 3.5,
            boxstyle='round,pad=0,rounding_size=0.05', fc='#9CA3AF', ec='#6B7280', lw=0.8, zorder=6))
        # wire colour
        ax.add_patch(FancyBboxPatch((px+0.03, cj_y+0.4), pin_w-0.06, 3.3,
            boxstyle='round,pad=0,rounding_size=0.04', fc=bg, ec='none', zorder=7))
        # stripe
        if 'Putih' in pin_colors[i][2]:
            for sy in [cj_y+1.0, cj_y+1.8, cj_y+2.6]:
                ax.add_patch(FancyBboxPatch((px+0.03, sy), pin_w-0.06, 0.15,
                    fc=WHITE, ec='none', zorder=8, alpha=0.65))
        # pin number label
        ax.text(px+pin_w/2, cj_y+0.22, str(i+1), ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=GRAY_DARK, zorder=8)

    ax.text(cj_x+1.9, cj_y+4.35, 'KONEKTOR RJ-45 (8P8C)',
        ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, zorder=6)

    # ── Twisted pair cross-section ──
    tp_x, tp_y = 8.5, 1.0
    ax.add_patch(mpatches.Circle((tp_x+1.5, tp_y+1.8), 1.7,
        fc='#F3F4F6', ec='#4A5568', lw=2.5, zorder=4))
    # 4 pairs
    pairs = [
        ((tp_x+1.0, tp_y+2.5), '#FF6600', '#FF8C00', 'Pasangan Oren'),
        ((tp_x+2.0, tp_y+2.5), '#228B22', '#90EE90', 'Pasangan Hijau'),
        ((tp_x+1.0, tp_y+1.1), '#0000CD', '#ADD8E6', 'Pasangan Biru'),
        ((tp_x+2.0, tp_y+1.1), '#8B4513', '#DEB887', 'Pasangan Coklat'),
    ]
    for (px2,py2), c1, c2, lbl in pairs:
        ax.add_patch(mpatches.Circle((px2, py2), 0.36, fc=c1, ec='#2D3748', lw=1.5, zorder=5))
        ax.add_patch(mpatches.Circle((px2+0.36, py2), 0.36, fc=c2, ec='#2D3748', lw=1.5, zorder=5))
    ax.text(tp_x+1.5, tp_y+0.25, 'Keratan Rentas Cat6\n(4 Pasangan Terpiuh)',
        ha='center', va='center', fontsize=8.5, color=GRAY_DARK, multialignment='center', zorder=5)

    # ── Specs table (right) ──
    st_x, st_y = 12.0, 1.0
    ax.add_patch(FancyBboxPatch((st_x-0.2, st_y-0.2), 4.0, 10.2,
        boxstyle='round,pad=0,rounding_size=0.2', fc=WHITE, ec='#CBD5E0', lw=1.5, zorder=3))
    ax.text(st_x+1.8, st_y+9.85, 'SPESIFIKASI CAT6',
        ha='center', fontsize=10, fontweight='bold', color=DARK_BLUE, zorder=4)
    ax.plot([st_x-0.2, st_x+3.8], [st_y+9.6, st_y+9.6], color=CISCO_BLUE, lw=2, zorder=4)

    cat6_specs = [
        ('Kategori',     'Category 6 (Cat6)'),
        ('Kelajuan',     '1000 Mbps (Gigabit)'),
        ('Lebar Jalur',  '250 MHz'),
        ('Panjang Maks', '100 meter'),
        ('Konektor',     'RJ-45 (8P8C)'),
        ('Piawaian',     'EIA/TIA-568B'),
        ('Jenis',        'UTP (Unshielded)'),
        ('Pasangan',     '4 Pasangan Terpiuh'),
        ('Wiring',       'Straight-Through'),
        ('Pelabelan',    'TIA-606-B'),
    ]
    for i, (k, v) in enumerate(cat6_specs):
        sy2 = st_y + 8.9 - i * 0.96
        row_bg = '#EBF5FF' if i % 2 == 0 else WHITE
        ax.add_patch(FancyBboxPatch((st_x-0.15, sy2-0.08), 3.9, 0.85,
            boxstyle='round,pad=0,rounding_size=0.08', fc=row_bg, ec='#E2E8F0', lw=0.8, zorder=4))
        ax.text(st_x+0.05, sy2+0.45, k, va='center', fontsize=8.5,
            fontweight='bold', color=CISCO_BLUE, zorder=5)
        ax.text(st_x+0.05, sy2+0.2, v, va='center', fontsize=9, color=GRAY_DARK, zorder=5)

    fig.tight_layout(pad=0.3)
    path = f'{OUT}/04_cabling_568B.png'
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='#F7FAFC')
    plt.close(fig)
    print(f'  Saved: {path}')


# ══════════════════════════════════════════════════════════════════════════════
#  IMAGE 5 – IP ADDRESSING SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

def draw_ip_table():
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 16); ax.set_ylim(0, 11)
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((0,0),16,11,
        boxstyle='round,pad=0,rounding_size=0.2', fc='#F7FAFC', ec='none', zorder=0))
    ax.add_patch(FancyBboxPatch((0,10.2),16,0.8,
        boxstyle='round,pad=0,rounding_size=0.1', fc=DARK_BLUE, ec='none', zorder=5))
    ax.text(8, 10.6, 'JADUAL PENGALAMATAN IP – MAKMAL RANGKAIAN DKM',
        ha='center', va='center', fontsize=13, fontweight='bold', color=WHITE, zorder=6)

    # ── Summary boxes ──
    summaries = [
        (CISCO_BLUE,  '192.168.1.0/24', 'Subnet LAN Utama',          'Subnet Mask: 255.255.255.0'),
        (DARK_BLUE,   '192.168.1.254',  'Default Gateway (Router)',   'Interface: Fa0/0'),
        (GREEN,       '192.168.1.1',    'Komputer Pengajar',          'VLAN 20 | Port: Fa0/24'),
        ('#9B2C2C',   '8.8.8.8',        'DNS Primer (Google)',        'DNS Sekunder: 8.8.4.4'),
    ]
    for i, (fc2, ip, lbl, sub) in enumerate(summaries):
        bx = 0.4 + i * 3.9
        shadow_box(ax, bx, 8.8, 3.5, 1.1, fc2, 'none', radius=0.2, zorder=4)
        ax.text(bx+1.75, 9.65, ip, ha='center', va='center',
            fontsize=12, fontweight='bold', color=WHITE, zorder=5)
        ax.text(bx+1.75, 9.3, lbl, ha='center', va='center',
            fontsize=8.5, color='#BEE3F8', zorder=5)
        ax.text(bx+1.75, 9.05, sub, ha='center', va='center',
            fontsize=7.5, color='#90CDF4', zorder=5)

    # ── IP address table ──
    headers = ['Peranti', 'Port Switch', 'IP Address', 'VLAN', 'Fungsi']
    col_x   = [0.3, 4.3, 7.0, 9.6, 11.0]
    col_w   = [4.0, 2.7, 2.6, 1.4, 4.8]

    tbl_top = 8.5
    # header row
    for hdr, cx, cw in zip(headers, col_x, col_w):
        ax.add_patch(FancyBboxPatch((cx, tbl_top-0.55), cw-0.05, 0.55,
            boxstyle='round,pad=0,rounding_size=0.05',
            fc=CISCO_BLUE, ec='none', zorder=4))
        ax.text(cx+cw/2-0.025, tbl_top-0.27, hdr, ha='center', va='center',
            fontsize=9, fontweight='bold', color=WHITE, zorder=5)

    rows = [
        ('Cisco 1941 Router (LAN)',  'GE uplink',  '192.168.1.254',  '—',  'Default Gateway', LIGHT_BLUE),
        ('Cisco 2960 Switch (SVI)',  'VLAN 99',    '192.168.99.1',   '99', 'Pengurusan Switch', '#EFF0F7'),
        ('PC Pengajar',             'Fa0/24',      '192.168.1.1',    '20', 'Stesen Pengajar', LIGHT_BLUE),
        ('PC Pelajar 01',           'Fa0/1',       '192.168.1.10',   '10', 'Stesen Pelajar', '#F0FFF4'),
        ('PC Pelajar 02',           'Fa0/2',       '192.168.1.11',   '10', 'Stesen Pelajar', WHITE),
        ('PC Pelajar 03–05',        'Fa0/3–Fa0/5', '192.168.1.12–14','10', 'Stesen Pelajar', '#F0FFF4'),
        ('PC Pelajar 06–10',        'Fa0/6–Fa0/10','192.168.1.15–19','10', 'Stesen Pelajar', WHITE),
        ('PC Pelajar 11–15',        'Fa0/11–15',   '192.168.1.20–24','10', 'Stesen Pelajar', '#F0FFF4'),
        ('PC Pelajar 16–20',        'Fa0/16–20',   '192.168.1.25–29','10', 'Stesen Pelajar', WHITE),
        ('PC Pelajar 21–25',        'Fa0/21–25',   '192.168.1.30–34','10', 'Stesen Pelajar', '#F0FFF4'),
    ]

    row_h = 0.72
    for i, (dev, port, ip, vlan, func, bg) in enumerate(rows):
        ry = tbl_top - 0.57 - (i+1)*row_h
        vals = [dev, port, ip, vlan, func]
        for val, cx, cw in zip(vals, col_x, col_w):
            ax.add_patch(FancyBboxPatch((cx, ry), cw-0.05, row_h-0.04,
                boxstyle='round,pad=0,rounding_size=0.04',
                fc=bg, ec='#E2E8F0', lw=0.8, zorder=4))
            ax.text(cx+cw/2-0.025, ry+row_h/2-0.02, val, ha='center', va='center',
                fontsize=8.5, color=GRAY_DARK, zorder=5)

    # ── VLAN colour legend ──
    ax.add_patch(FancyBboxPatch((0.3, 0.2), 15.4, 0.75,
        boxstyle='round,pad=0,rounding_size=0.1', fc=WHITE, ec='#CBD5E0', lw=1, zorder=4))
    ax.text(0.7, 0.58, 'Petunjuk VLAN:', fontsize=9, fontweight='bold',
        color=GRAY_DARK, va='center', zorder=5)
    for vc, vl, vx in [
        (GREEN,      'VLAN 10 – Pelajar',     2.2),
        (CISCO_BLUE, 'VLAN 20 – Pengajar',    6.5),
        (ORANGE,     'VLAN 99 – Pengurusan', 10.8),
    ]:
        ax.add_patch(FancyBboxPatch((vx, 0.3), 0.4, 0.45,
            boxstyle='round,pad=0,rounding_size=0.05', fc=vc, ec='none', zorder=5))
        ax.text(vx+0.55, 0.52, vl, fontsize=9, va='center', color=GRAY_DARK, zorder=5)

    fig.tight_layout(pad=0.3)
    path = f'{OUT}/05_ip_addressing.png'
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='#F7FAFC')
    plt.close(fig)
    print(f'  Saved: {path}')


# ── Run all ───────────────────────────────────────────────────────────────────
print('Generating diagrams...')
draw_floor_plan()
draw_topology()
draw_rack()
draw_cabling()
draw_ip_table()
print('All 5 images generated successfully.')
