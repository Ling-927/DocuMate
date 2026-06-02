"""Clean Cisco Star Topology diagrams – visual only, minimal text."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc
import numpy as np
import os

OUT = '/home/user/DocuMate/images'
os.makedirs(OUT, exist_ok=True)

CISCO_BLUE = '#00549F'
DARK_BLUE  = '#003D73'
LIGHT_BLUE = '#EBF8FF'
ACCENT     = '#1BA3E8'
GREEN      = '#38A169'
ORANGE     = '#DD6B20'
RED        = '#E53E3E'
GRAY_DARK  = '#2D3748'
GRAY_MID   = '#718096'
GRAY_LIGHT = '#EDF2F7'
WHITE      = '#FFFFFF'
YELLOW     = '#D69E2E'
RACK_BG    = '#1C2433'

plt.rcParams['font.family'] = 'DejaVu Sans'

# ─── Cisco icons ──────────────────────────────────────────────────────────────

def cisco_router(ax, cx, cy, size=0.55, color=CISCO_BLUE, zorder=10):
    r = size
    ax.add_patch(mpatches.Ellipse((cx, cy), r*2, r*0.7,
        fc=color, ec=WHITE, lw=2.5, zorder=zorder))
    ax.add_patch(FancyBboxPatch((cx-r, cy-r*0.62), r*2, r*0.62,
        boxstyle='round,pad=0', fc=color, ec='none', zorder=zorder))
    ax.add_patch(mpatches.Ellipse((cx, cy-r*0.62), r*2, r*0.7,
        fc=color, ec=WHITE, lw=2.5, zorder=zorder))
    ax.add_patch(mpatches.Arc((cx+r*0.25, cy-r*0.3), r*0.55, r*0.55,
        angle=0, theta1=30, theta2=310, color=WHITE, lw=2.2, zorder=zorder+1))
    ax.annotate('', xy=(cx+r*0.52, cy-r*0.16), xytext=(cx+r*0.52, cy-r*0.17),
        arrowprops=dict(arrowstyle='->', color=WHITE, lw=1.8), zorder=zorder+2)
    ax.add_patch(mpatches.Arc((cx-r*0.25, cy-r*0.3), r*0.55, r*0.55,
        angle=0, theta1=230, theta2=150, color=WHITE, lw=2.2, zorder=zorder+1))
    ax.annotate('', xy=(cx-r*0.52, cy-r*0.44), xytext=(cx-r*0.52, cy-r*0.43),
        arrowprops=dict(arrowstyle='->', color=WHITE, lw=1.8), zorder=zorder+2)

def cisco_switch(ax, cx, cy, size=0.45, color=DARK_BLUE, zorder=10):
    w, h = size*2.8, size*0.72
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc=color, ec=WHITE, lw=2.5, zorder=zorder))
    n, gap = 12, w*0.06
    pw = (w - 2*gap - (n-1)*gap/2) / n * 0.9
    px0 = cx - w/2 + gap
    for i in range(n):
        px = px0 + i*(pw + gap/2)
        ax.add_patch(FancyBboxPatch((px, cy-h/2+h*0.15), pw, h*0.3,
            boxstyle='round,pad=0', fc=GREEN, ec='none', zorder=zorder+1))
        ax.add_patch(FancyBboxPatch((px, cy-h/2+h*0.52), pw, h*0.3,
            boxstyle='round,pad=0', fc=GREEN, ec='none', zorder=zorder+1))
    ax.plot(cx-w/2+gap*0.6, cy+h*0.22, 'o', color=GREEN, ms=5, zorder=zorder+2)
    ax.plot(cx-w/2+gap*0.6+0.18, cy+h*0.22, 'o', color=ACCENT, ms=5, zorder=zorder+2)

def cisco_pc(ax, cx, cy, size=0.28, color='#2B6CB0', zorder=10):
    mw, mh = size*2.0, size*1.5
    ax.add_patch(FancyBboxPatch((cx-mw/2, cy), mw, mh,
        boxstyle='round,pad=0,rounding_size=0.06',
        fc=GRAY_DARK, ec=WHITE, lw=1.5, zorder=zorder))
    pad = mw*0.09
    ax.add_patch(FancyBboxPatch((cx-mw/2+pad, cy+pad), mw-2*pad, mh-2*pad,
        boxstyle='round,pad=0,rounding_size=0.04',
        fc=color, ec='none', zorder=zorder+1))
    ax.add_patch(FancyBboxPatch((cx-mw*0.1, cy-mh*0.22), mw*0.2, mh*0.22,
        boxstyle='round,pad=0', fc=GRAY_DARK, ec='none', zorder=zorder))
    ax.add_patch(FancyBboxPatch((cx-mw*0.45, cy-mh*0.32), mw*0.9, mh*0.13,
        boxstyle='round,pad=0,rounding_size=0.04',
        fc='#4A5568', ec=WHITE, lw=0.8, zorder=zorder))

def cisco_cloud(ax, cx, cy, rw=1.4, rh=0.65, color='#DBEAFE', zorder=5):
    for dx, dy, r in [(-0.55,-0.05,0.38),(-.2,0.1,0.46),(0.22,0.15,0.5),
                       (0.58,0.05,0.42),(0.78,-0.12,0.32),(-0.75,-0.12,0.28)]:
        ax.add_patch(mpatches.Circle((cx+dx*rw, cy+dy*rh*2), r*rh*1.3,
            fc=color, ec=ACCENT, lw=2, zorder=zorder))
    ax.add_patch(FancyBboxPatch((cx-rw*0.85, cy-rh*0.6), rw*1.7, rh*0.9,
        boxstyle='round,pad=0', fc=color, ec='none', zorder=zorder))

def cisco_ups(ax, cx, cy, size=0.38, zorder=10):
    w, h = size*1.4, size*2.0
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#1A202C', ec=RED, lw=2.2, zorder=zorder))
    for i, (fc2, frac) in enumerate([(GREEN,0.6),(ORANGE,0.25),(RED,0.15)]):
        bh = h*0.55*frac
        by = cy - h/2 + h*0.12 + sum([h*0.55*[0.6,0.25,0.15][j] for j in range(i)])
        ax.add_patch(FancyBboxPatch((cx-w*0.3, by), w*0.6, bh-0.02,
            boxstyle='round,pad=0,rounding_size=0.02',
            fc=fc2, ec='none', zorder=zorder+1))
    ax.add_patch(FancyBboxPatch((cx-w*0.15, cy+h/2), w*0.3, h*0.06,
        boxstyle='round,pad=0', fc='#4A5568', ec='none', zorder=zorder+1))
    ax.plot(cx, cy+h*0.35, 'o', color=GREEN, ms=6, zorder=zorder+2)


# ══════════════════════════════════════════════════════════════════════════════
#  DIAGRAM 1 – CISCO STAR TOPOLOGY (clean)
# ══════════════════════════════════════════════════════════════════════════════

def draw_star():
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_xlim(-1, 21); ax.set_ylim(-1, 21)
    ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('#F0F4F8')

    # subtle grid
    for v in np.arange(-1, 21, 2):
        ax.axvline(v, color='#CBD5E0', lw=0.3, alpha=0.4, zorder=0)
        ax.axhline(v, color='#CBD5E0', lw=0.3, alpha=0.4, zorder=0)

    # ── Title ──
    ax.add_patch(FancyBboxPatch((-1, 19.5), 22, 1.5,
        boxstyle='round,pad=0,rounding_size=0.2',
        fc=DARK_BLUE, ec='none', zorder=20))
    ax.text(10, 20.38, 'TOPOLOGI BINTANG (STAR TOPOLOGY)',
        ha='center', va='center', fontsize=18, fontweight='bold', color=WHITE, zorder=21)
    ax.text(10, 20.05, 'Cisco Packet Tracer  |  25 PC Pelajar + 1 PC Pengajar  |  Makmal Rangkaian DKM',
        ha='center', va='center', fontsize=11.5, color='#90CDF4', zorder=21)

    # ── Internet ──
    cisco_cloud(ax, 10, 18.2, rw=1.6, rh=0.75, zorder=5)
    ax.text(10, 18.22, 'INTERNET / ISP',
        ha='center', va='center', fontsize=10, fontweight='bold', color=DARK_BLUE, zorder=8)

    # WAN link
    ax.plot([10,10],[17.55,16.12], color=ORANGE, lw=3, zorder=4, solid_capstyle='round')
    ax.plot([10],[16.12], 'v', color=ORANGE, ms=10, zorder=5)
    ax.text(10.35, 16.85, 'WAN', fontsize=9, color=ORANGE, va='center', fontweight='bold')

    # ── Router ──
    ax.add_patch(mpatches.Circle((10,15.2), 1.05,
        fc='#00549F22', ec='#00549F55', lw=2, zorder=6))
    cisco_router(ax, 10, 15.2, size=0.65, color=CISCO_BLUE, zorder=10)
    ax.add_patch(FancyBboxPatch((7.8,13.55), 4.4, 0.92,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc=CISCO_BLUE, ec=DARK_BLUE, lw=1.5, zorder=9))
    ax.text(10, 14.18, 'CISCO 1941 ROUTER',
        ha='center', va='center', fontsize=11, fontweight='bold', color=WHITE, zorder=10)
    ax.text(10, 13.88, '192.168.1.254  |  Fa0/0 (LAN)  |  Fa0/1 (WAN)',
        ha='center', va='center', fontsize=8.5, color='#BEE3F8', zorder=10)

    # Router → Switch
    ax.plot([10,10],[13.55,11.9], color=CISCO_BLUE, lw=4, zorder=4, solid_capstyle='round')
    ax.plot([10],[13.55], 'o', color=CISCO_BLUE, ms=9, zorder=5)
    ax.plot([10],[11.9], 'o', color=CISCO_BLUE, ms=9, zorder=5)
    ax.text(10.45, 12.72, 'GE0/1\nTrunk', fontsize=8.5, color=CISCO_BLUE,
        va='center', fontweight='bold', linespacing=1.3)

    # ── UPS ──
    cisco_ups(ax, 13.8, 15.2, size=0.42, zorder=10)
    ax.add_patch(FancyBboxPatch((12.6,13.55), 2.4, 0.58,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#1A202C', ec=RED, lw=1.5, zorder=9))
    ax.text(13.8, 13.86, 'UPS 1000VA',
        ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, zorder=10)
    ax.plot([12.6,10.7],[15.0,15.0], color=RED, lw=2, ls='--', zorder=4)

    # ── Switch (STAR CENTER) ──
    # star burst rays
    for ang in range(0, 360, 12):
        r2 = np.radians(ang)
        ax.plot([10, 10+5.0*np.cos(r2)], [10.5, 10.5+5.0*np.sin(r2)],
            color='#E2E8F0', lw=0.7, alpha=0.6, zorder=1)

    ax.add_patch(mpatches.Circle((10,10.5), 1.35,
        fc='#003D7322', ec='#003D7355', lw=3, zorder=6))
    cisco_switch(ax, 10, 10.5, size=0.6, color=DARK_BLUE, zorder=10)
    ax.add_patch(FancyBboxPatch((7.5,9.1), 5.0, 0.92,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc=DARK_BLUE, ec='#1A3A5C', lw=1.5, zorder=9))
    ax.text(10, 9.73, 'CISCO CATALYST 2960-24TT  ★  PUSAT BINTANG',
        ha='center', va='center', fontsize=10.5, fontweight='bold', color=WHITE, zorder=10)
    ax.text(10, 9.43, '24 × FastEthernet  +  2 × GigabitEthernet  |  VLAN 10 / 20 / 99',
        ha='center', va='center', fontsize=8.5, color='#90CDF4', zorder=10)

    # ── 26 PCs radiating in star ──
    n      = 26
    radius = 6.5
    start  = 130
    span   = 300

    angles = [start + i*span/(n-1) for i in range(n)]

    for i, ang in enumerate(angles):
        rad = np.radians(ang)
        px  = 10 + radius*np.cos(rad)
        py  = 10.5 + radius*np.sin(rad)

        is_teacher = (i == 0)
        pc_col  = CISCO_BLUE  if is_teacher else '#2B6CB0'
        lc      = '#B7791F'   if is_teacher else '#276749'
        lw2     = 3.0         if is_teacher else 2.0
        vlan_fc = '#FFF9E6'   if is_teacher else LIGHT_BLUE
        vlan_ec = ORANGE      if is_teacher else '#90CDF4'
        vlan_tx = 'VLAN 20'   if is_teacher else 'VLAN 10'
        port_tx = 'Fa0/24'    if is_teacher else f'Fa0/{i}'

        # cable from switch edge to PC
        stub = 1.5
        sx = 10 + stub*np.cos(rad);  sy = 10.5 + stub*np.sin(rad)
        ax.plot([sx, px], [sy, py], color=lc, lw=lw2,
            solid_capstyle='round', zorder=3)
        # port dot on switch
        ax.plot(sx, sy, 'o', color=lc, ms=5, zorder=4)

        # port label (mid-cable)
        mid_f = 0.35
        mx = sx + (px-sx)*mid_f;  my = sy + (py-sy)*mid_f
        ax.text(mx, my, port_tx, ha='center', va='center', fontsize=6,
            color=GRAY_DARK, zorder=7,
            bbox=dict(fc=WHITE+'EE', ec='#CBD5E0', pad=1.2,
                      boxstyle='round,pad=0.2'))

        # PC icon
        cisco_pc(ax, px, py, size=0.25, color=pc_col, zorder=10)

        # label (name + IP + VLAN)
        la  = rad + np.pi
        lo  = 0.4
        lx2 = np.clip(px + lo*np.cos(la), 0.3, 19.7)
        ly2 = np.clip(py + lo*np.sin(la), 0.2, 19.8)

        lbw, lbh = 1.72, 0.82
        ax.add_patch(FancyBboxPatch((lx2-lbw/2, ly2-lbh/2), lbw, lbh,
            boxstyle='round,pad=0,rounding_size=0.1',
            fc=vlan_fc, ec=vlan_ec, lw=1.4, zorder=9))

        name = 'PC PENGAJAR' if is_teacher else f'PC-{i:02d}'
        ip   = '192.168.1.1' if is_teacher else f'192.168.1.{9+i}'

        ax.text(lx2, ly2+0.22, name,
            ha='center', va='center', fontsize=7.5, fontweight='bold',
            color=DARK_BLUE, zorder=11)
        ax.text(lx2, ly2-0.02, ip,
            ha='center', va='center', fontsize=7.2, color=GRAY_DARK, zorder=11)
        ax.add_patch(FancyBboxPatch((lx2-0.4, ly2-0.36), 0.8, 0.22,
            boxstyle='round,pad=0,rounding_size=0.07',
            fc=ORANGE if is_teacher else GREEN+'44', ec='none', zorder=10))
        ax.text(lx2, ly2-0.24, vlan_tx,
            ha='center', va='center', fontsize=6.5,
            color=WHITE if is_teacher else DARK_BLUE,
            fontweight='bold', zorder=11)

    fig.tight_layout(pad=0.2)
    fig.savefig(f'{OUT}/CISCO_star_topology_clean.png',
        dpi=180, bbox_inches='tight', facecolor='#F0F4F8')
    plt.close(fig)
    print('  star topology done')


# ══════════════════════════════════════════════════════════════════════════════
#  DIAGRAM 2 – FLOOR PLAN (clean)
# ══════════════════════════════════════════════════════════════════════════════

def draw_floor():
    fig, ax = plt.subplots(figsize=(18, 14))
    ax.set_xlim(0, 18); ax.set_ylim(0, 14)
    ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('#F0F4F8')

    # ── Room ──
    ax.add_patch(FancyBboxPatch((0.5,0.5), 17.0, 13.0,
        boxstyle='round,pad=0,rounding_size=0.3',
        fc='#FAFAFA', ec=GRAY_DARK, lw=5, zorder=1))

    # front wall stripe
    ax.add_patch(FancyBboxPatch((0.5,12.5), 17.0, 1.0,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#EBF5FF', ec=CISCO_BLUE, lw=1.5, zorder=2))
    ax.text(9, 13.0, 'DINDING HADAPAN',
        ha='center', va='center', fontsize=10, color=CISCO_BLUE, fontweight='bold', zorder=3)

    # title
    ax.add_patch(FancyBboxPatch((0.5,13.5), 17.0, 0.5,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc=DARK_BLUE, ec='none', zorder=10))
    ax.text(9, 13.75, 'PELAN SUSUN ATUR FIZIKAL MAKMAL RANGKAIAN  –  TOPOLOGI BINTANG',
        ha='center', va='center', fontsize=13, fontweight='bold', color=WHITE, zorder=11)

    # projector screen
    ax.add_patch(FancyBboxPatch((2.5,12.52), 8.5, 0.35,
        boxstyle='round,pad=0,rounding_size=0.05',
        fc='#E2E8F0', ec=GRAY_DARK, lw=2, zorder=4))
    ax.text(6.75, 12.7, '[ SKRIN PROJEKTOR ]',
        ha='center', va='center', fontsize=9, color=GRAY_DARK, fontweight='bold', zorder=5)

    # ── Network Rack (back-right) ──
    rx, ry = 14.8, 9.6
    ax.add_patch(FancyBboxPatch((rx, ry), 2.7, 3.2,
        boxstyle='round,pad=0,rounding_size=0.15',
        fc=RACK_BG, ec='#4A5568', lw=3, zorder=6))
    ax.add_patch(FancyBboxPatch((rx+0.12,ry+0.12), 2.46, 2.96,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#141921', ec='#4A5568', lw=1.2, zorder=7))
    for ri2, (rfc2, rlbl2) in enumerate([
        (CISCO_BLUE,'PATCH PANEL'),
        (DARK_BLUE, 'CISCO 2960 SW'),
        (CISCO_BLUE,'CISCO 1941 RT'),
        ('#9B2C2C', 'UPS 1000VA'),
        ('#1A202C', 'PDU / PSU'),
    ]):
        ry2 = ry + 0.22 + ri2*0.53
        ax.add_patch(FancyBboxPatch((rx+0.18,ry2), 2.34, 0.46,
            boxstyle='round,pad=0,rounding_size=0.05',
            fc=rfc2, ec='#4A5568', lw=0.8, zorder=8))
        ax.plot(rx+0.32, ry2+0.23, 'o', color=GREEN, ms=4.5, zorder=9)
        ax.text(rx+1.35, ry2+0.23, rlbl2,
            ha='center', va='center', fontsize=7.5, fontweight='bold',
            color=WHITE, zorder=9)
    ax.text(rx+1.35, ry+2.92, 'NETWORK RACK 12U',
        ha='center', va='center', fontsize=8.5, fontweight='bold',
        color=WHITE, zorder=8)
    cisco_switch(ax, rx+1.35, ry+2.58, size=0.22, color=DARK_BLUE, zorder=10)

    # ── Teacher desk ──
    tx, ty = 5.4, 10.3
    ax.add_patch(FancyBboxPatch((tx, ty), 3.8, 1.8,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc=LIGHT_BLUE, ec=CISCO_BLUE, lw=2.5, zorder=5))
    cisco_pc(ax, tx+1.9, ty+0.75, size=0.3, color=CISCO_BLUE, zorder=8)
    ax.text(tx+1.9, ty+0.26, 'PC PENGAJAR', ha='center', va='center',
        fontsize=9, fontweight='bold', color=CISCO_BLUE, zorder=9)
    ax.text(tx+1.9, ty-0.2, '192.168.1.1  |  VLAN 20  |  Fa0/24',
        ha='center', va='center', fontsize=7.5, color=GRAY_MID, zorder=9)

    # ── 25 Student PCs 5×5 ──
    cols = [1.3, 3.7, 6.1, 8.5, 10.9]
    rows = [8.5, 6.7, 4.9, 3.1, 1.4]
    row_labels = ['Baris 1','Baris 2','Baris 3','Baris 4','Baris 5']

    sw_cx = rx + 1.35
    sw_cy = ry + 1.3

    pc_n = 1
    for ri2, (ry3, rn) in enumerate(zip(rows, row_labels)):
        ax.text(0.82, ry3+0.75, rn, ha='center', va='center',
            fontsize=8, color=GRAY_MID, fontstyle='italic')
        for ci2, cx in enumerate(cols):
            # cable → tray → rack
            ax.plot([cx+0.7, 12.5], [ry3+0.75, ry3+0.75],
                color='#CBD5E0', lw=1.2, ls='--', zorder=2, alpha=0.7)
            ax.plot([12.5, 12.5], [ry3+0.75, sw_cy],
                color='#CBD5E0', lw=1.2, ls='--', zorder=2, alpha=0.7)
            ax.plot([12.5, sw_cx], [sw_cy, sw_cy],
                color='#CBD5E0', lw=1.2, ls='--', zorder=2, alpha=0.7)

            cisco_pc(ax, cx+0.7, ry3+0.5, size=0.27, color='#2B6CB0', zorder=7)

            ax.add_patch(FancyBboxPatch((cx, ry3-0.18), 1.4, 0.62,
                boxstyle='round,pad=0,rounding_size=0.08',
                fc=LIGHT_BLUE, ec='#90CDF4', lw=1, zorder=6))
            ax.text(cx+0.7, ry3+0.12, f'PC-{pc_n:02d}',
                ha='center', va='center',
                fontsize=8, fontweight='bold', color=DARK_BLUE, zorder=7)
            ax.text(cx+0.7, ry3-0.07, f'192.168.1.{9+pc_n}',
                ha='center', va='center', fontsize=6.8, color=GRAY_MID, zorder=7)
            pc_n += 1

    # Teacher cable
    ax.plot([tx+1.9, 12.5], [ty+0.75, ty+0.75],
        color='#B7791F', lw=2, ls='--', zorder=4)
    ax.plot([12.5, sw_cx], [ty+0.75, sw_cy],
        color='#B7791F', lw=2, ls='--', zorder=4)

    # ── Cable tray ──
    ax.add_patch(FancyBboxPatch((12.3, 1.2), 0.4, 10.5,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='none', ec=YELLOW, lw=2.5, ls='--', zorder=5))
    ax.text(12.5, 6.5, 'CABLE\nTRAY\nCat6',
        ha='center', va='center', fontsize=7.5, color=YELLOW,
        fontweight='bold', linespacing=1.4,
        bbox=dict(fc=WHITE+'CC', ec=YELLOW, pad=2, boxstyle='round'), zorder=6)

    # ── Door ──
    ax.add_patch(mpatches.Arc((1.3, 0.5), 1.9, 1.9,
        angle=0, theta1=0, theta2=90,
        color=GRAY_DARK, lw=2, ls='--', zorder=3))
    ax.plot([1.3,1.3],[0.5,1.45], color=GRAY_DARK, lw=3, zorder=3)
    ax.text(1.6, 0.28, 'PINTU', ha='center', fontsize=8, color=GRAY_MID)

    # ── Dimensions ──
    ax.annotate('', xy=(17.75,0.5), xytext=(17.75,13.5),
        arrowprops=dict(arrowstyle='<->', color=GRAY_MID, lw=1.5))
    ax.text(17.93, 7.0, '8 m', va='center', fontsize=9, color=GRAY_MID,
        rotation=90, fontweight='bold')
    ax.annotate('', xy=(0.5,0.15), xytext=(17.5,0.15),
        arrowprops=dict(arrowstyle='<->', color=GRAY_MID, lw=1.5))
    ax.text(9.0, -0.12, '10 meter', ha='center', fontsize=9,
        color=GRAY_MID, fontweight='bold')

    # ── Legend ──
    leg = [(CISCO_BLUE,'PC Pengajar'),(DARK_BLUE,'PC Pelajar (25)'),
           (RACK_BG,'Rack 12U'),(YELLOW,'Cable Tray')]
    for li, (lc, ll) in enumerate(leg):
        lx3 = 0.65 + (li%2)*2.1
        ly3 = 1.35 - (li//2)*0.5
        ax.add_patch(FancyBboxPatch((lx3,ly3), 0.28, 0.28,
            boxstyle='round,pad=0', fc=lc, ec='none', zorder=10))
        ax.text(lx3+0.38, ly3+0.14, ll, va='center',
            fontsize=7.5, color=GRAY_DARK, zorder=10)

    fig.tight_layout(pad=0.2)
    fig.savefig(f'{OUT}/CISCO_floor_plan_clean.png',
        dpi=180, bbox_inches='tight', facecolor='#F0F4F8')
    plt.close(fig)
    print('  floor plan done')


# ══════════════════════════════════════════════════════════════════════════════
#  DIAGRAM 3 – CISCO PACKET TRACER VIEW (clean dark)
# ══════════════════════════════════════════════════════════════════════════════

def draw_pt_view():
    fig, ax = plt.subplots(figsize=(20, 15))
    ax.set_xlim(0, 20); ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor('#2D333B')

    # background
    ax.add_patch(FancyBboxPatch((0,0), 20, 15,
        boxstyle='round,pad=0', fc='#2D333B', ec='none', zorder=0))

    # PT grid
    for gx in np.arange(0, 20, 1):
        ax.axvline(gx, color='#3D434B', lw=0.45, zorder=0)
    for gy in np.arange(0, 15, 1):
        ax.axhline(gy, color='#3D434B', lw=0.45, zorder=0)

    # ── Top toolbar ──
    ax.add_patch(FancyBboxPatch((0,14.3), 20, 0.7,
        boxstyle='round,pad=0', fc='#161B22', ec='none', zorder=20))
    ax.text(0.5, 14.65, 'Cisco Packet Tracer 8.x',
        va='center', fontsize=11, fontweight='bold', color='#58A6FF', zorder=21)
    for ti, item in enumerate(['File','Edit','Options','View','Tools','Extensions','Help']):
        ax.text(4.5+ti*1.6, 14.65, item, va='center', fontsize=9,
            color='#C9D1D9', zorder=21)

    # ── Bottom mode bar ──
    ax.add_patch(FancyBboxPatch((0,0), 20, 0.65,
        boxstyle='round,pad=0', fc='#161B22', ec='none', zorder=20))
    ax.add_patch(FancyBboxPatch((14.3,0.08), 2.3, 0.5,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#58A6FF', ec='#58A6FF', lw=1.5, zorder=21))
    ax.text(15.45, 0.33, 'Realtime', ha='center', va='center',
        fontsize=9.5, fontweight='bold', color=WHITE, zorder=22)
    ax.add_patch(FancyBboxPatch((16.8,0.08), 2.5, 0.5,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#30363D', ec='#3FB950', lw=1.5, zorder=21))
    ax.text(18.05, 0.33, 'Simulation', ha='center', va='center',
        fontsize=9.5, color='#8B949E', zorder=22)

    # ── Devices ──
    # Internet
    cisco_cloud(ax, 10, 13.3, rw=1.3, rh=0.6, color='#1C2D4A', zorder=5)
    ax.text(10, 13.3, 'Internet', ha='center', va='center',
        fontsize=9.5, fontweight='bold', color='#58A6FF', zorder=8)

    # Router
    cisco_router(ax, 10, 11.4, size=0.54, color='#00549F', zorder=10)
    ax.add_patch(FancyBboxPatch((8.65,10.45), 2.7, 0.58,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#1C2D4A', ec='#30363D', lw=1, zorder=9))
    ax.text(10, 10.85, 'Router0', ha='center', va='center',
        fontsize=10, fontweight='bold', color='#58A6FF', zorder=10)
    ax.text(10, 10.62, 'Cisco 1941  |  192.168.1.254',
        ha='center', va='center', fontsize=8, color='#8B949E', zorder=10)

    # Switch
    cisco_switch(ax, 10, 8.0, size=0.54, color=DARK_BLUE, zorder=10)
    ax.add_patch(FancyBboxPatch((8.35,7.07), 3.3, 0.58,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#1C2D4A', ec='#30363D', lw=1, zorder=9))
    ax.text(10, 7.47, 'Switch0', ha='center', va='center',
        fontsize=10, fontweight='bold', color='#3FB950', zorder=10)
    ax.text(10, 7.24, 'Cisco 2960-24TT  ★  PUSAT BINTANG',
        ha='center', va='center', fontsize=8, color='#8B949E', zorder=10)

    # UPS
    cisco_ups(ax, 13.8, 11.4, size=0.36, zorder=10)
    ax.text(13.8, 10.62, 'UPS 1000VA',
        ha='center', va='center', fontsize=9, fontweight='bold',
        color='#FC8181', zorder=10)

    # ── Links ──
    # Internet → Router
    ax.plot([10,10],[12.7,11.95], color='#4D8BD4', lw=3.5, zorder=4, solid_capstyle='round')
    for y in [12.7, 11.95]:
        ax.plot(10, y, 'o', color='#4D8BD4', ms=8, zorder=5)

    # Router → Switch
    ax.plot([10,10],[10.45,8.28], color='#58A6FF', lw=4, zorder=4, solid_capstyle='round')
    for y in [10.45, 8.28]:
        ax.plot(10, y, 'o', color='#58A6FF', ms=8, zorder=5)
    ax.text(10.38, 9.36, 'GE0/1', fontsize=8.5, color='#58A6FF',
        va='center', fontweight='bold')

    # UPS → Router (power, dashed)
    ax.plot([12.8,10.55],[11.4,11.4], color='#FC8181', lw=2, ls='--', zorder=4)

    # ── 26 PCs radiating (star) ──
    n      = 26
    radius = 5.2
    start  = 135
    span   = 310

    for i, ang in enumerate([start + j*span/(n-1) for j in range(n)]):
        rad = np.radians(ang)
        px  = np.clip(10 + radius*np.cos(rad), 0.6, 19.4)
        py  = np.clip(8.0 + radius*np.sin(rad), 0.8, 13.9)

        is_t = (i == 0)
        lc2  = '#B7791F' if is_t else '#4D8BD4'
        pc_c = CISCO_BLUE if is_t else '#2B6CB0'
        nc   = '#F6AD55'  if is_t else '#58A6FF'
        vc   = '#F6AD55'  if is_t else '#3FB950'

        # cable
        ax.plot([10, px], [8.0, py], color=lc2, lw=2.0, zorder=3, alpha=0.9)
        ax.plot(px, py, 'o', color=lc2, ms=5, zorder=4)

        # PC icon
        cisco_pc(ax, px, py, size=0.20, color=pc_c, zorder=10)

        # label
        la  = rad + np.pi
        lo  = 0.42
        lx2 = np.clip(px + lo*np.cos(la), 0.4, 19.0)
        ly2 = np.clip(py + lo*np.sin(la), 0.75, 14.0)

        nm  = 'PC-Pengajar' if is_t else f'PC-{i:02d}'
        ip2 = '192.168.1.1' if is_t else f'192.168.1.{9+i}'
        vl  = 'VLAN 20'     if is_t else 'VLAN 10'
        pt  = 'Fa0/24'      if is_t else f'Fa0/{i}'

        ax.text(lx2, ly2+0.18, nm, ha='center', va='center',
            fontsize=7, fontweight='bold', color=nc, zorder=11)
        ax.text(lx2, ly2-0.02, ip2, ha='center', va='center',
            fontsize=6.2, color='#8B949E', zorder=11)
        ax.text(lx2, ly2-0.20, vl, ha='center', va='center',
            fontsize=5.8, color=vc, fontweight='bold', zorder=11)
        ax.text(lx2, ly2-0.36, pt, ha='center', va='center',
            fontsize=5.5, color='#6E7681', zorder=11)

    # ── Star label at center ──
    ax.add_patch(FancyBboxPatch((7.5,7.68), 5.0, 0.38,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#003D73BB', ec='#58A6FF', lw=1.5, zorder=13))
    ax.text(10, 7.87, '★  PUSAT BINTANG – 26 peranti disambung ke Switch  ★',
        ha='center', va='center', fontsize=9, fontweight='bold',
        color='#58A6FF', zorder=14)

    fig.tight_layout(pad=0.1)
    fig.savefig(f'{OUT}/CISCO_packet_tracer_clean.png',
        dpi=180, bbox_inches='tight', facecolor='#2D333B')
    plt.close(fig)
    print('  packet tracer view done')


# ─── Run ──────────────────────────────────────────────────────────────────────
print('Generating clean Cisco diagrams...')
draw_star()
draw_floor()
draw_pt_view()
print('Done.')
