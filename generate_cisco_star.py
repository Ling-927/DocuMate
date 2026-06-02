"""
Generate professional Cisco-style Star Topology diagrams for DKM report.
All devices use authentic Cisco icon shapes.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe
import numpy as np
import os

OUT = '/home/user/DocuMate/images'
os.makedirs(OUT, exist_ok=True)

# ── Colour palette ──────────────────────────────────────────────────────────
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
YELLOW      = '#D69E2E'
RACK_BG     = '#1C2433'
BLACK       = '#000000'

plt.rcParams['font.family'] = 'DejaVu Sans'

# ════════════════════════════════════════════════════════════════════════════
#  Cisco icon drawing functions
# ════════════════════════════════════════════════════════════════════════════

def cisco_router(ax, cx, cy, size=0.55, color=CISCO_BLUE, zorder=10):
    """Cisco router – cylinder body with two curved arrows."""
    r = size
    # cylinder body (ellipse top)
    body = mpatches.Ellipse((cx, cy), r*2, r*0.7,
        fc=color, ec=WHITE, lw=2, zorder=zorder)
    ax.add_patch(body)
    # cylinder sides
    rect = FancyBboxPatch((cx-r, cy-r*0.6), r*2, r*0.6,
        boxstyle='round,pad=0,rounding_size=0',
        fc=color, ec='none', zorder=zorder)
    ax.add_patch(rect)
    # bottom ellipse
    bot = mpatches.Ellipse((cx, cy-r*0.6), r*2, r*0.7,
        fc=color, ec=WHITE, lw=2, zorder=zorder)
    ax.add_patch(bot)
    # circular arrow right
    arc1 = Arc((cx+r*0.25, cy-r*0.3), r*0.55, r*0.55,
        angle=0, theta1=30, theta2=300, color=WHITE, lw=2.2, zorder=zorder+1)
    ax.add_patch(arc1)
    ax.annotate('', xy=(cx+r*0.52, cy-r*0.16),
        xytext=(cx+r*0.52, cy-r*0.17),
        arrowprops=dict(arrowstyle='->', color=WHITE, lw=1.8), zorder=zorder+2)
    # circular arrow left
    arc2 = Arc((cx-r*0.25, cy-r*0.3), r*0.55, r*0.55,
        angle=0, theta1=240, theta2=150, color=WHITE, lw=2.2, zorder=zorder+1)
    ax.add_patch(arc2)
    ax.annotate('', xy=(cx-r*0.52, cy-r*0.44),
        xytext=(cx-r*0.52, cy-r*0.43),
        arrowprops=dict(arrowstyle='->', color=WHITE, lw=1.8), zorder=zorder+2)


def cisco_switch(ax, cx, cy, size=0.45, color=DARK_BLUE, zorder=10):
    """Cisco switch – rectangle with port dots."""
    w, h = size*2.6, size*0.75
    # body
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc=color, ec=WHITE, lw=2, zorder=zorder))
    # port squares
    n_ports = 12
    gap = w*0.06
    pw  = (w - 2*gap - (n_ports-1)*gap/2) / n_ports * 0.9
    px0 = cx - w/2 + gap
    for i in range(n_ports):
        px = px0 + i*(pw + gap/2)
        ax.add_patch(FancyBboxPatch((px, cy-h/2+h*0.18), pw, h*0.28,
            boxstyle='round,pad=0,rounding_size=0.02',
            fc=GREEN, ec='none', zorder=zorder+1))
        ax.add_patch(FancyBboxPatch((px, cy-h/2+h*0.52), pw, h*0.28,
            boxstyle='round,pad=0,rounding_size=0.02',
            fc=GREEN, ec='none', zorder=zorder+1))
    # LED
    ax.plot(cx-w/2+gap*0.6, cy+h*0.25, 'o', color=GREEN, ms=5, zorder=zorder+2)
    ax.plot(cx-w/2+gap*0.6+0.18, cy+h*0.25, 'o', color=ACCENT, ms=5, zorder=zorder+2)


def cisco_pc(ax, cx, cy, size=0.28, color='#2B6CB0', zorder=10):
    """Cisco PC – monitor + base + keyboard."""
    mw, mh = size*2.0, size*1.5
    # monitor frame
    ax.add_patch(FancyBboxPatch((cx-mw/2, cy), mw, mh,
        boxstyle='round,pad=0,rounding_size=0.06',
        fc=GRAY_DARK, ec=WHITE, lw=1.4, zorder=zorder))
    # screen
    pad = mw*0.08
    ax.add_patch(FancyBboxPatch((cx-mw/2+pad, cy+pad), mw-2*pad, mh-2*pad,
        boxstyle='round,pad=0,rounding_size=0.04',
        fc=color, ec='none', zorder=zorder+1))
    # stand
    ax.add_patch(FancyBboxPatch((cx-mw*0.1, cy-mh*0.22), mw*0.2, mh*0.22,
        boxstyle='round,pad=0,rounding_size=0.02',
        fc=GRAY_DARK, ec='none', zorder=zorder))
    # keyboard
    ax.add_patch(FancyBboxPatch((cx-mw*0.45, cy-mh*0.32), mw*0.9, mh*0.13,
        boxstyle='round,pad=0,rounding_size=0.04',
        fc='#4A5568', ec=WHITE, lw=0.8, zorder=zorder))


def cisco_cloud(ax, cx, cy, rw=1.4, rh=0.65, color='#DBEAFE', zorder=5):
    """Internet cloud shape."""
    for dx, dy, r in [(-0.55,-0.05,0.38),(-.2,0.1,0.46),(0.22,0.15,0.5),
                       (0.58,0.05,0.42),(0.78,-0.12,0.32),(-0.75,-0.12,0.28)]:
        ax.add_patch(mpatches.Circle((cx+dx*rw, cy+dy*rh*2), r*rh*1.3,
            fc=color, ec=ACCENT, lw=2, zorder=zorder))
    # fill bottom
    ax.add_patch(FancyBboxPatch((cx-rw*0.85, cy-rh*0.6), rw*1.7, rh*0.9,
        boxstyle='round,pad=0,rounding_size=0', fc=color, ec='none', zorder=zorder))


def cisco_ups(ax, cx, cy, size=0.4, zorder=10):
    """UPS – tall box with battery icon."""
    w, h = size*1.4, size*2.0
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#1A202C', ec=RED, lw=2.2, zorder=zorder))
    # battery bar
    for i, (fc, frac) in enumerate([(GREEN,0.6),(ORANGE,0.25),(RED,0.15)]):
        bh = h*0.55*frac
        by = cy - h/2 + h*0.12 + sum([h*0.55*[0.6,0.25,0.15][j] for j in range(i)])
        ax.add_patch(FancyBboxPatch((cx-w*0.3, by), w*0.6, bh-0.02,
            boxstyle='round,pad=0,rounding_size=0.02',
            fc=fc, ec='none', zorder=zorder+1))
    # terminal nub
    ax.add_patch(FancyBboxPatch((cx-w*0.15, cy+h/2), w*0.3, h*0.06,
        boxstyle='round,pad=0,rounding_size=0.02',
        fc='#4A5568', ec='none', zorder=zorder+1))
    # LED
    ax.plot(cx, cy+h*0.35, 'o', color=GREEN, ms=6, zorder=zorder+2)


def draw_link(ax, x0, y0, x1, y1, color='#4A5568', lw=2.0,
              ls='-', label='', label_color=GRAY_MID, zorder=2):
    """Draw a connection line with optional label."""
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=ls,
            solid_capstyle='round', zorder=zorder)
    if label:
        mx, my = (x0+x1)/2, (y0+y1)/2
        angle  = np.degrees(np.arctan2(y1-y0, x1-x0))
        if abs(angle) > 90: angle += 180
        ax.text(mx, my, label, ha='center', va='center',
                fontsize=6.5, color=label_color, rotation=angle,
                bbox=dict(fc=WHITE, ec='none', pad=1), zorder=zorder+1)


def label_device(ax, cx, cy, lines, offsets=(0, -0.55), fontsize=8.5,
                 bold_first=True, color=GRAY_DARK, zorder=12):
    ox, oy = offsets
    for i, line in enumerate(lines):
        ax.text(cx+ox, cy+oy - i*0.28, line, ha='center', va='top',
                fontsize=fontsize if i>0 else fontsize+0.5,
                fontweight='bold' if (i==0 and bold_first) else 'normal',
                color=color, zorder=zorder,
                bbox=dict(fc=WHITE+'CC', ec='none', pad=0.5, boxstyle='round'))


# ════════════════════════════════════════════════════════════════════════════
#  IMAGE 1 – CISCO STAR TOPOLOGY (main diagram)
# ════════════════════════════════════════════════════════════════════════════

def draw_cisco_star():
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_xlim(-1, 21); ax.set_ylim(-1, 21)
    ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('#F0F4F8')

    # ── Title banner ──────────────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((-1, 19.5), 22, 1.5,
        boxstyle='round,pad=0,rounding_size=0.2',
        fc=DARK_BLUE, ec='none', zorder=20))
    ax.text(10, 20.35, 'TOPOLOGI BINTANG (STAR TOPOLOGY) – MAKMAL RANGKAIAN CISCO',
        ha='center', va='center', fontsize=17, fontweight='bold', color=WHITE, zorder=21)
    ax.text(10, 20.0, 'Cisco Packet Tracer  |  25 PC Pelajar + 1 PC Pengajar  |  DKM Teknologi Maklumat',
        ha='center', va='center', fontsize=11, color='#90CDF4', zorder=21)

    # ── Background grid (subtle) ──────────────────────────────────────────
    for gv in np.arange(-1, 21, 2):
        ax.axvline(gv, color='#CBD5E0', lw=0.4, alpha=0.4, zorder=0)
        ax.axhline(gv, color='#CBD5E0', lw=0.4, alpha=0.4, zorder=0)

    # ══════════════════════════════════════════════════════════════════════
    # LAYER 0 – Internet (top-center)
    # ══════════════════════════════════════════════════════════════════════
    inet_x, inet_y = 10, 18.0
    cisco_cloud(ax, inet_x, inet_y, rw=1.6, rh=0.75, zorder=5)
    ax.text(inet_x, inet_y+0.1, 'INTERNET / ISP',
        ha='center', va='center', fontsize=9.5, fontweight='bold',
        color=DARK_BLUE, zorder=8)

    # ══════════════════════════════════════════════════════════════════════
    # LAYER 1 – Router Cisco 1941 (center-upper)
    # ══════════════════════════════════════════════════════════════════════
    rt_x, rt_y = 10, 15.5
    # glow ring
    ax.add_patch(mpatches.Circle((rt_x, rt_y), 1.0,
        fc='#00549F33', ec='#00549F66', lw=2, zorder=6))
    cisco_router(ax, rt_x, rt_y, size=0.62, color=CISCO_BLUE, zorder=10)

    # Router label box
    ax.add_patch(FancyBboxPatch((rt_x-1.9, rt_y-2.2), 3.8, 0.95,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc=CISCO_BLUE, ec=DARK_BLUE, lw=1.5, zorder=9))
    ax.text(rt_x, rt_y-1.55, 'CISCO 1941 ROUTER',
        ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, zorder=10)
    ax.text(rt_x, rt_y-1.85, 'Fa0/0: 192.168.1.254 (LAN) | Fa0/1: WAN/ISP',
        ha='center', va='center', fontsize=8, color='#BEE3F8', zorder=10)

    # WAN line: internet → router
    draw_link(ax, inet_x, inet_y-0.65, rt_x, rt_y+0.65,
        color=ORANGE, lw=2.5, label='WAN Link (ISP)')

    # ══════════════════════════════════════════════════════════════════════
    # LAYER 2 – Switch Cisco 2960 (CENTER of star)
    # ══════════════════════════════════════════════════════════════════════
    sw_x, sw_y = 10, 10.5

    # Star burst background
    for angle in range(0, 360, 15):
        rad = np.radians(angle)
        ax.plot([sw_x, sw_x + 4.5*np.cos(rad)],
                [sw_y, sw_y + 4.5*np.sin(rad)],
                color='#E2E8F0', lw=0.8, alpha=0.5, zorder=1)

    # Switch glow
    ax.add_patch(mpatches.Circle((sw_x, sw_y), 1.3,
        fc='#003D7333', ec='#003D7366', lw=3, zorder=6))
    cisco_switch(ax, sw_x, sw_y, size=0.55, color=DARK_BLUE, zorder=10)

    # Switch label
    ax.add_patch(FancyBboxPatch((sw_x-2.2, sw_y-1.85), 4.4, 1.0,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc=DARK_BLUE, ec='#1A3A5C', lw=1.5, zorder=9))
    ax.text(sw_x, sw_y-1.22, 'CISCO CATALYST 2960-24TT',
        ha='center', va='center', fontsize=10.5, fontweight='bold', color=WHITE, zorder=10)
    ax.text(sw_x, sw_y-1.55, '24× FastEthernet  |  2× GigabitEthernet  |  PUSAT BINTANG',
        ha='center', va='center', fontsize=8, color='#90CDF4', zorder=10)

    # Router → Switch (trunk/uplink)
    draw_link(ax, rt_x, rt_y-0.4, sw_x, sw_y+0.42,
        color=CISCO_BLUE, lw=3.5, label='GigabitEthernet Uplink')
    ax.text(rt_x+0.6, (rt_y-0.4+sw_y+0.42)/2+0.1,
        'Trunk\nVLAN 10,20,99', ha='left', va='center', fontsize=7.5,
        color=CISCO_BLUE, fontweight='bold', zorder=12,
        bbox=dict(fc=WHITE, ec=CISCO_BLUE, pad=2, boxstyle='round'))

    # ══════════════════════════════════════════════════════════════════════
    # LAYER 3 – UPS (right of router)
    # ══════════════════════════════════════════════════════════════════════
    ups_x, ups_y = 14.2, 15.5
    cisco_ups(ax, ups_x, ups_y, size=0.38, zorder=10)
    ax.add_patch(FancyBboxPatch((ups_x-1.1, ups_y-1.62), 2.2, 0.8,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#1A202C', ec=RED, lw=1.5, zorder=9))
    ax.text(ups_x, ups_y-1.12, 'UPS 1000VA',
        ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, zorder=10)
    ax.text(ups_x, ups_y-1.42, 'APC Smart-UPS',
        ha='center', va='center', fontsize=7.5, color='#FC8181', zorder=10)
    # power line to router
    ax.plot([ups_x-1.1, rt_x+0.9], [ups_y-0.3, rt_y-0.3],
        color=RED, lw=1.8, ls='--', zorder=4)
    ax.text((ups_x-1.1+rt_x+0.9)/2, ups_y-0.5, 'Bekalan Kuasa',
        ha='center', fontsize=7, color=RED, fontstyle='italic', zorder=5)

    # ══════════════════════════════════════════════════════════════════════
    # LAYER 4 – 26 PC nodes radiating from switch (STAR)
    # ══════════════════════════════════════════════════════════════════════
    # Place 26 PCs evenly around switch, skipping top sector (where router is)
    # Angles: avoid 60°–120° (top area) to keep router visible
    # Distribute 26 PCs in 300° arc (from 130° to 430° = 130° to 70° going CW)

    n_pcs = 26
    radius = 6.2

    # Define angles: full 360° but skip top 60° (80°–100° reserved for router)
    # Spread 26 devices evenly in 300°, centered at 270° (bottom)
    start_angle = 130   # degrees (measured from positive x-axis, CCW)
    total_arc   = 300
    angles_deg  = [start_angle + i * total_arc / (n_pcs - 1) for i in range(n_pcs)]

    # PC info
    pc_info = [
        ('PC\nPENGAJAR', '192.168.1.1',   'VLAN 20', CISCO_BLUE, '#BEE3F8', 'Fa0/24'),
    ] + [
        (f'PC-{i:02d}', f'192.168.1.{9+i}', 'VLAN 10', '#2B6CB0', '#C6F6D5', f'Fa0/{i}')
        for i in range(1, 26)
    ]

    for i, (angle_deg, (name, ip, vlan, pc_color, vlan_color, port)) in enumerate(
            zip(angles_deg, pc_info)):

        angle = np.radians(angle_deg)
        px = sw_x + radius * np.cos(angle)
        py = sw_y + radius * np.sin(angle)

        # ── Connection line from switch to PC ──
        # Calculate port stub point (closer to switch)
        stub_r = 1.45
        sx = sw_x + stub_r * np.cos(angle)
        sy = sw_y + stub_r * np.sin(angle)

        # Line color: orange for teacher, green for students
        lc = '#B7791F' if i == 0 else '#276749'
        lw2 = 2.5 if i == 0 else 1.8
        draw_link(ax, sx, sy, px, py, color=lc, lw=lw2, zorder=3)

        # Port label along line
        mid_r = stub_r + (radius - stub_r) * 0.28
        mx = sw_x + mid_r * np.cos(angle)
        my = sw_y + mid_r * np.sin(angle)
        ax.text(mx, my, port, ha='center', va='center', fontsize=6,
            color=GRAY_DARK, zorder=7,
            bbox=dict(fc=WHITE+'EE', ec='#CBD5E0', pad=1.5, boxstyle='round,pad=0.2'))

        # ── PC icon ──
        cisco_pc(ax, px, py, size=0.24, color=pc_color, zorder=10)

        # ── PC label box ──
        lbox_w, lbox_h = 1.65, 0.88
        # decide label position (opposite to switch direction)
        la = angle + np.pi  # away from center
        lx = px + 0.38 * np.cos(la)
        ly = py + 0.38 * np.sin(la)

        # frame colour
        fc2 = '#FFF9E6' if i == 0 else LIGHT_BLUE
        ec2 = ORANGE if i == 0 else '#90CDF4'

        ax.add_patch(FancyBboxPatch((lx - lbox_w/2, ly - lbox_h/2), lbox_w, lbox_h,
            boxstyle='round,pad=0,rounding_size=0.1',
            fc=fc2, ec=ec2, lw=1.3, zorder=9))

        # Name (bold)
        nm = name.replace('\n', '/')
        ax.text(lx, ly + 0.22, nm, ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=DARK_BLUE, zorder=11)
        # IP
        ax.text(lx, ly - 0.02, ip, ha='center', va='center',
            fontsize=7, color=GRAY_DARK, zorder=11)
        # VLAN tag
        ax.add_patch(FancyBboxPatch((lx - 0.38, ly - 0.36), 0.76, 0.22,
            boxstyle='round,pad=0,rounding_size=0.08',
            fc=vlan_color, ec='none', zorder=10))
        ax.text(lx, ly - 0.24, vlan, ha='center', va='center',
            fontsize=6.5, color=DARK_BLUE, fontweight='bold', zorder=11)

    # ══════════════════════════════════════════════════════════════════════
    # LEGEND & INFO BOXES
    # ══════════════════════════════════════════════════════════════════════

    # Left info panel
    info_x, info_y = -0.8, 4.0
    ax.add_patch(FancyBboxPatch((info_x, info_y-0.2), 3.8, 6.2,
        boxstyle='round,pad=0,rounding_size=0.2',
        fc=WHITE, ec='#CBD5E0', lw=1.5, zorder=15))
    ax.text(info_x+1.9, info_y+5.82, 'MAKLUMAT RANGKAIAN',
        ha='center', fontsize=9.5, fontweight='bold', color=DARK_BLUE, zorder=16)
    ax.plot([info_x+0.1, info_x+3.7], [info_y+5.58, info_y+5.58],
        color=CISCO_BLUE, lw=1.8, zorder=16)

    net_info = [
        ('Topologi',       'Bintang (Star)'),
        ('Subnet',         '192.168.1.0/24'),
        ('Subnet Mask',    '255.255.255.0'),
        ('Default GW',     '192.168.1.254'),
        ('DNS Primer',     '8.8.8.8'),
        ('DNS Sekunder',   '8.8.4.4'),
        ('VLAN Pelajar',   'VLAN 10'),
        ('VLAN Pengajar',  'VLAN 20'),
        ('VLAN Pengurusan','VLAN 99'),
        ('Kabel',          'UTP Cat6 568B'),
        ('Protokol',       'IEEE 802.3'),
        ('Kelajuan',       '100/1000 Mbps'),
    ]
    for j, (k, v) in enumerate(net_info):
        yy = info_y + 5.28 - j*0.44
        bg = '#EBF5FF' if j % 2 == 0 else WHITE
        ax.add_patch(FancyBboxPatch((info_x+0.05, yy-0.18), 3.7, 0.38,
            boxstyle='round,pad=0,rounding_size=0.05',
            fc=bg, ec='none', zorder=16))
        ax.text(info_x+0.2, yy+0.02, k+':', ha='left', va='center',
            fontsize=8, color=GRAY_MID, zorder=17)
        ax.text(info_x+3.7, yy+0.02, v, ha='right', va='center',
            fontsize=8.5, fontweight='bold', color=DARK_BLUE, zorder=17)

    # Right legend panel
    leg_x, leg_y = 17.0, 4.0
    ax.add_patch(FancyBboxPatch((leg_x-0.2, leg_y-0.2), 4.1, 5.0,
        boxstyle='round,pad=0,rounding_size=0.2',
        fc=WHITE, ec='#CBD5E0', lw=1.5, zorder=15))
    ax.text(leg_x+1.85, leg_y+4.62, 'PETUNJUK',
        ha='center', fontsize=9.5, fontweight='bold', color=DARK_BLUE, zorder=16)
    ax.plot([leg_x-0.1, leg_x+3.9], [leg_y+4.38, leg_y+4.38],
        color=CISCO_BLUE, lw=1.8, zorder=16)

    legend_items = [
        ('CISCO 1941 ROUTER',     CISCO_BLUE, 'circle'),
        ('CISCO 2960 SWITCH',     DARK_BLUE,  'rect'),
        ('PC PELAJAR (25 unit)',  '#2B6CB0',  'monitor'),
        ('PC PENGAJAR (1 unit)',  CISCO_BLUE, 'monitor'),
        ('UPS 1000VA',            RED,        'rect'),
        ('Sambungan Pelajar',     '#276749',  'line'),
        ('Sambungan Pengajar',    ORANGE,     'line'),
        ('WAN/Internet',          ORANGE,     'dash'),
        ('Bekalan Kuasa',         RED,        'dash'),
    ]
    for j, (lbl, lc, ltype) in enumerate(legend_items):
        yy = leg_y + 4.0 - j * 0.44
        lxi = leg_x + 0.15
        if ltype == 'circle':
            ax.add_patch(mpatches.Circle((lxi+0.2, yy+0.05), 0.18, fc=lc, ec=WHITE, lw=1, zorder=16))
        elif ltype == 'rect':
            ax.add_patch(FancyBboxPatch((lxi, yy-0.1), 0.4, 0.3,
                boxstyle='round,pad=0,rounding_size=0.05', fc=lc, ec=WHITE, lw=1, zorder=16))
        elif ltype == 'monitor':
            ax.add_patch(FancyBboxPatch((lxi, yy-0.05), 0.38, 0.28,
                boxstyle='round,pad=0,rounding_size=0.04', fc=GRAY_DARK, ec=WHITE, lw=1, zorder=16))
            ax.add_patch(FancyBboxPatch((lxi+0.04, yy-0.01), 0.3, 0.2,
                boxstyle='round,pad=0,rounding_size=0.02', fc=lc, ec='none', zorder=17))
        elif ltype == 'line':
            ax.plot([lxi, lxi+0.4], [yy+0.07, yy+0.07], color=lc, lw=2.5, zorder=16)
        elif ltype == 'dash':
            ax.plot([lxi, lxi+0.4], [yy+0.07, yy+0.07], color=lc, lw=2, ls='--', zorder=16)
        ax.text(leg_x+0.7, yy+0.07, lbl, ha='left', va='center',
            fontsize=8, color=GRAY_DARK, zorder=17)

    # ── "STAR CENTER" callout ──────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((7.5, 9.0), 5.0, 0.75,
        boxstyle='round,pad=0,rounding_size=0.15',
        fc=DARK_BLUE+'CC', ec=WHITE, lw=1.5, zorder=13))
    ax.text(10.0, 9.38, '★  PUSAT BINTANG – Semua 26 peranti disambung di sini  ★',
        ha='center', va='center', fontsize=9, fontweight='bold',
        color=WHITE, zorder=14)

    fig.tight_layout(pad=0.2)
    path = f'{OUT}/CISCO_star_topology.png'
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='#F0F4F8')
    plt.close(fig)
    print(f'  Saved: {path}')


# ════════════════════════════════════════════════════════════════════════════
#  IMAGE 2 – CISCO STAR FLOOR PLAN (Physical with star lines)
# ════════════════════════════════════════════════════════════════════════════

def draw_cisco_floor_plan():
    fig, ax = plt.subplots(figsize=(18, 14))
    ax.set_xlim(0, 18); ax.set_ylim(0, 14)
    ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('#F0F4F8')

    # ── Title ──
    ax.add_patch(FancyBboxPatch((0, 13.2), 18, 0.8,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc=DARK_BLUE, ec='none', zorder=20))
    ax.text(9, 13.6, 'PELAN LANTAI MAKMAL RANGKAIAN – SUSUN ATUR FIZIKAL (STAR TOPOLOGY)',
        ha='center', va='center', fontsize=13.5, fontweight='bold', color=WHITE, zorder=21)

    # ── Room walls ──
    ax.add_patch(FancyBboxPatch((0.4, 0.4), 17.2, 12.6,
        boxstyle='round,pad=0,rounding_size=0.3',
        fc='#FAFAFA', ec=GRAY_DARK, lw=4, zorder=1))

    # ── Front wall accent ──
    ax.add_patch(FancyBboxPatch((0.4, 12.2), 17.2, 0.8,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#EBF5FF', ec=CISCO_BLUE, lw=1.5, zorder=2))
    ax.text(9, 12.62, '━━━━━  DINDING HADAPAN  ━━━━━',
        ha='center', va='center', fontsize=9, color=CISCO_BLUE, fontweight='bold', zorder=3)

    # ── Projector screen ──
    ax.add_patch(FancyBboxPatch((2.5, 12.22), 8.0, 0.35,
        boxstyle='round,pad=0,rounding_size=0.05',
        fc='#E2E8F0', ec=GRAY_DARK, lw=2, zorder=4))
    ax.text(6.5, 12.4, '[ SKRIN PROJEKTOR – 120 inch ]',
        ha='center', va='center', fontsize=8.5, color=GRAY_DARK, fontweight='bold', zorder=5)

    # ── Network Rack (back-right corner) ──
    rack_x, rack_y = 14.8, 9.8
    ax.add_patch(FancyBboxPatch((rack_x, rack_y), 2.6, 2.6,
        boxstyle='round,pad=0,rounding_size=0.15',
        fc=RACK_BG, ec='#4A5568', lw=3, zorder=8))
    ax.add_patch(FancyBboxPatch((rack_x+0.12, rack_y+0.12), 2.36, 2.36,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#141921', ec='#4A5568', lw=1.5, zorder=9))

    # rack unit strips
    rack_units = [
        (CISCO_BLUE,  'PATCH'),
        (DARK_BLUE,   'SW2960'),
        (CISCO_BLUE,  'RT1941'),
        ('#9B2C2C',   'UPS'),
        ('#1A202C',   'PDU'),
    ]
    for ri, (rfc, rlbl) in enumerate(rack_units):
        ry2 = rack_y + 0.22 + ri * 0.44
        ax.add_patch(FancyBboxPatch((rack_x+0.18, ry2), 2.24, 0.38,
            boxstyle='round,pad=0,rounding_size=0.05',
            fc=rfc, ec='#4A5568', lw=0.8, zorder=10))
        ax.plot(rack_x+0.3, ry2+0.19, 'o', color=GREEN, ms=4, zorder=11)
        ax.text(rack_x+1.3, ry2+0.19, rlbl, ha='center', va='center',
            fontsize=7, fontweight='bold', color=WHITE, zorder=11)
    ax.text(rack_x+1.3, rack_y+2.48, 'NETWORK RACK 12U',
        ha='center', va='center', fontsize=8, fontweight='bold', color=WHITE, zorder=10)

    cisco_switch(ax, rack_x+1.3, rack_y+2.2, size=0.25, color=DARK_BLUE, zorder=12)

    # ── Teacher desk (front center) ──
    td_x, td_y = 5.8, 10.5
    ax.add_patch(FancyBboxPatch((td_x, td_y), 3.4, 1.5,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc=LIGHT_BLUE, ec=CISCO_BLUE, lw=2.5, zorder=5))
    cisco_pc(ax, td_x+1.7, td_y+0.6, size=0.28, color=CISCO_BLUE, zorder=8)
    ax.text(td_x+1.7, td_y+0.18, 'KOMPUTER PENGAJAR', ha='center', va='center',
        fontsize=8, fontweight='bold', color=CISCO_BLUE, zorder=9)
    ax.text(td_x+1.7, td_y-0.18, 'IP: 192.168.1.1 | VLAN 20 | Fa0/24',
        ha='center', va='center', fontsize=7.5, color=GRAY_MID, zorder=9)

    # ══════════════════════════════════════════════════════════════════════
    # 25 Student PCs in 5×5 grid
    # ══════════════════════════════════════════════════════════════════════
    col_x = [1.2, 3.6, 6.0, 8.4, 10.8]
    row_y = [8.5, 6.8, 5.1, 3.4, 1.7]
    row_names = ['Baris 1', 'Baris 2', 'Baris 3', 'Baris 4', 'Baris 5']

    # Switch position (rack center)
    sw_cx = rack_x + 1.3
    sw_cy = rack_y + 1.3

    pc_num = 1
    for ri, (ry, rn) in enumerate(zip(row_y, row_names)):
        ax.text(0.7, ry+0.75, rn, ha='center', va='center',
            fontsize=7.5, color=GRAY_MID, fontstyle='italic', rotation=0)
        for ci, cx in enumerate(col_x):
            ip_end = 9 + pc_num

            # ── Star cable: PC → Rack ──
            # Route via cable tray (right wall tray at x=12.6, horizontal tray at y=9.6)
            # Horizontal segment to tray
            ax.plot([cx+0.7, 12.6], [ry+0.75, ry+0.75],
                color='#CBD5E0', lw=1.2, ls='--', zorder=2, alpha=0.7)
            # Vertical segment up tray
            ax.plot([12.6, 12.6], [ry+0.75, sw_cy],
                color='#CBD5E0', lw=1.2, ls='--', zorder=2, alpha=0.7)
            # To rack
            ax.plot([12.6, sw_cx], [sw_cy, sw_cy],
                color='#CBD5E0', lw=1.2, ls='--', zorder=2, alpha=0.7)

            # ── PC icon ──
            cisco_pc(ax, cx+0.7, ry+0.5, size=0.26, color='#2B6CB0', zorder=8)

            # ── Label ──
            ax.add_patch(FancyBboxPatch((cx, ry-0.15), 1.4, 0.6,
                boxstyle='round,pad=0,rounding_size=0.08',
                fc=LIGHT_BLUE, ec='#90CDF4', lw=1, zorder=7))
            ax.text(cx+0.7, ry+0.12, f'PC-{pc_num:02d}', ha='center', va='center',
                fontsize=7.5, fontweight='bold', color=DARK_BLUE, zorder=8)
            ax.text(cx+0.7, ry-0.05, f'.{ip_end}', ha='center', va='center',
                fontsize=6.5, color=GRAY_MID, zorder=8)

            pc_num += 1

    # ── Cable tray indicators ──
    # Vertical tray (right wall)
    ax.add_patch(FancyBboxPatch((12.45, 1.4), 0.3, 9.0,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='none', ec=YELLOW, lw=2.5, ls='--', zorder=6))
    ax.text(12.6, 5.9, 'CABLE\nTRAY\nCat6', ha='center', va='center',
        fontsize=7, color=YELLOW, fontweight='bold',
        bbox=dict(fc=WHITE+'CC', ec=YELLOW, pad=2, boxstyle='round'), zorder=7)

    # Teacher cable
    ax.plot([td_x+1.7, 12.6], [td_y+0.6, td_y+0.6],
        color='#B7791F', lw=2, ls='--', zorder=5)
    ax.plot([12.6, sw_cx], [td_y+0.6, sw_cy],
        color='#B7791F', lw=2, ls='--', zorder=5)

    # ── Door ──
    ax.add_patch(Arc((1.2, 0.4), 1.8, 1.8, angle=0, theta1=0, theta2=90,
        color=GRAY_DARK, lw=1.8, ls='--', zorder=3))
    ax.plot([1.2, 1.2], [0.4, 1.3], color=GRAY_DARK, lw=2.5, zorder=3)
    ax.text(1.5, 0.22, 'PINTU', ha='center', fontsize=8, color=GRAY_MID, zorder=3)

    # ── Dimension labels ──
    ax.annotate('', xy=(17.8, 0.4), xytext=(17.8, 13.0),
        arrowprops=dict(arrowstyle='<->', color=GRAY_MID, lw=1.5))
    ax.text(17.95, 6.7, '~8 meter', va='center', fontsize=8, color=GRAY_MID,
        rotation=90, fontweight='bold')
    ax.annotate('', xy=(0.4, 0.15), xytext=(17.6, 0.15),
        arrowprops=dict(arrowstyle='<->', color=GRAY_MID, lw=1.5))
    ax.text(9.0, -0.12, '~10 meter', ha='center', fontsize=8, color=GRAY_MID,
        fontweight='bold')

    # ── Legend ──
    ax.add_patch(FancyBboxPatch((0.4, 0.4), 4.0, 1.2,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc=WHITE, ec='#CBD5E0', lw=1.2, zorder=15))
    leg_items = [
        (CISCO_BLUE, 'PC Pengajar (1 unit)'),
        ('#2B6CB0',  'PC Pelajar (25 unit)'),
        (RACK_BG,    'Network Rack 12U'),
        (YELLOW,     'Cable Tray Cat6'),
    ]
    for li, (lc, ll) in enumerate(leg_items):
        lx2 = 0.6 + (li % 2) * 2.0
        ly2 = 1.35 - (li // 2) * 0.55
        ax.add_patch(FancyBboxPatch((lx2, ly2), 0.28, 0.28,
            boxstyle='round,pad=0', fc=lc, ec='none', zorder=16))
        ax.text(lx2+0.35, ly2+0.14, ll, va='center', fontsize=7.2,
            color=GRAY_DARK, zorder=16)

    fig.tight_layout(pad=0.2)
    path = f'{OUT}/CISCO_floor_plan.png'
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='#F0F4F8')
    plt.close(fig)
    print(f'  Saved: {path}')


# ════════════════════════════════════════════════════════════════════════════
#  IMAGE 3 – CISCO PACKET TRACER SIMULATION VIEW
# ════════════════════════════════════════════════════════════════════════════

def draw_packet_tracer_view():
    """Mimics actual Cisco Packet Tracer workspace look."""
    fig, ax = plt.subplots(figsize=(20, 14))
    ax.set_xlim(0, 20); ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor('#1E2329')  # dark PT background

    # PT workspace background
    ax.add_patch(FancyBboxPatch((0, 0), 20, 14,
        boxstyle='round,pad=0,rounding_size=0',
        fc='#2D333B', ec='none', zorder=0))

    # PT-style grid
    for gx in np.arange(0, 20, 1):
        ax.axvline(gx, color='#3D434B', lw=0.5, zorder=0)
    for gy in np.arange(0, 14, 1):
        ax.axhline(gy, color='#3D434B', lw=0.5, zorder=0)

    # ── Top toolbar simulation ──
    ax.add_patch(FancyBboxPatch((0, 13.3), 20, 0.7,
        boxstyle='round,pad=0,rounding_size=0', fc='#161B22', ec='none', zorder=20))
    ax.text(1.5, 13.65, '  Cisco Packet Tracer 8.x',
        va='center', fontsize=11, fontweight='bold', color='#58A6FF', zorder=21)
    toolbar_items = ['File','Edit','Options','View','Tools','Extensions','Help']
    for ti, item in enumerate(toolbar_items):
        ax.text(4.5 + ti*1.6, 13.65, item, va='center', fontsize=9,
            color='#C9D1D9', zorder=21)

    # Mode bar bottom
    ax.add_patch(FancyBboxPatch((0, 0), 20, 0.7,
        boxstyle='round,pad=0,rounding_size=0', fc='#161B22', ec='none', zorder=20))
    mode_items = [
        ('Realtime', '#58A6FF', True),
        ('Simulation', '#3FB950', False),
    ]
    for mi, (mode, mc, active) in enumerate(mode_items):
        bx = 14.5 + mi * 2.5
        ax.add_patch(FancyBboxPatch((bx, 0.1), 2.2, 0.5,
            boxstyle='round,pad=0,rounding_size=0.08',
            fc=mc if active else '#30363D', ec=mc, lw=1.5, zorder=21))
        ax.text(bx+1.1, 0.35, mode, ha='center', va='center',
            fontsize=9, fontweight='bold',
            color=WHITE if active else '#8B949E', zorder=22)

    # ══════════════════════════════════════════════════════════════════════
    #  DEVICES on workspace
    # ══════════════════════════════════════════════════════════════════════

    # Internet (top)
    cisco_cloud(ax, 10, 12.2, rw=1.3, rh=0.6, color='#1C2D4A', zorder=5)
    ax.text(10, 12.2, 'Internet', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#58A6FF', zorder=8)

    # Router
    cisco_router(ax, 10, 10.4, size=0.52, color='#00549F', zorder=10)
    # PT-style label under router
    ax.add_patch(FancyBboxPatch((8.8, 9.5), 2.4, 0.55,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#1C2D4A', ec='#30363D', lw=1, zorder=9))
    ax.text(10, 9.78, 'Router0', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#58A6FF', zorder=10)
    ax.text(10, 9.58, 'Cisco 1941', ha='center', va='center',
        fontsize=7.5, color='#8B949E', zorder=10)

    # Switch (center of star)
    cisco_switch(ax, 10, 7.5, size=0.50, color=DARK_BLUE, zorder=10)
    ax.add_patch(FancyBboxPatch((8.6, 6.65), 2.8, 0.55,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#1C2D4A', ec='#30363D', lw=1, zorder=9))
    ax.text(10, 6.93, 'Switch0', ha='center', va='center',
        fontsize=9, fontweight='bold', color='#3FB950', zorder=10)
    ax.text(10, 6.73, 'Cisco 2960-24TT  [PUSAT BINTANG]',
        ha='center', va='center', fontsize=7.5, color='#8B949E', zorder=10)

    # Link: Internet → Router
    ax.plot([10, 10], [11.55, 10.95], color='#4D8BD4', lw=3, zorder=4,
        solid_capstyle='round')
    ax.plot(10, 11.55, 'o', color='#4D8BD4', ms=7, zorder=5)
    ax.plot(10, 10.95, 'o', color='#4D8BD4', ms=7, zorder=5)

    # Link: Router → Switch
    ax.plot([10, 10], [9.85, 7.85], color='#4D8BD4', lw=3.5, zorder=4,
        solid_capstyle='round')
    ax.plot(10, 9.85, 'o', color='#58A6FF', ms=7, zorder=5)
    ax.plot(10, 7.85, 'o', color='#58A6FF', ms=7, zorder=5)
    ax.text(10.25, 8.85, 'GE0/1', fontsize=7, color='#58A6FF', va='center', zorder=6)

    # UPS (right of router)
    cisco_ups(ax, 13.5, 10.4, size=0.35, zorder=10)
    ax.text(13.5, 9.62, 'UPS-1000VA', ha='center', va='center',
        fontsize=8.5, fontweight='bold', color='#FC8181', zorder=10)
    ax.plot([12.8, 10.55], [10.4, 10.4], color='#FC8181', lw=2, ls='--', zorder=4)

    # ── 26 PCs arranged in star ──
    n_pcs = 26
    star_r = 4.5
    start_a = 135
    total_a = 310

    angles = [start_a + i * total_a / (n_pcs - 1) for i in range(n_pcs)]

    for i, ang in enumerate(angles):
        rad = np.radians(ang)
        px  = 10 + star_r * np.cos(rad)
        py  = 7.5 + star_r * np.sin(rad)

        # clamp to workspace
        px = np.clip(px, 0.7, 19.3)
        py = np.clip(py, 0.9, 12.8)

        # connection line (PT copper straight-through style)
        lc2 = '#B7791F' if i == 0 else '#4D8BD4'
        ax.plot([10, px], [7.5, py], color=lc2, lw=1.8, zorder=3, alpha=0.85)
        # connection dots (PT style)
        ax.plot(px, py, 'o', color=lc2, ms=5, zorder=4)

        # PC icon
        pc_col = CISCO_BLUE if i == 0 else '#2B6CB0'
        cisco_pc(ax, px, py, size=0.20, color=pc_col, zorder=10)

        # PT label
        name = 'PC-Pengajar' if i == 0 else f'PC-{i:02d}'
        ip   = '192.168.1.1' if i == 0 else f'192.168.1.{9+i}'
        vlan = 'VLAN 20' if i == 0 else 'VLAN 10'
        vc   = '#F6AD55' if i == 0 else '#58A6FF'

        la = rad + np.pi
        lo = 0.45
        lx = px + lo * np.cos(la)
        ly = py + lo * np.sin(la)
        lx = np.clip(lx, 0.5, 18.8)
        ly = np.clip(ly, 0.8, 12.9)

        ax.text(lx, ly+0.16, name, ha='center', va='center',
            fontsize=6.8, fontweight='bold', color=vc, zorder=11)
        ax.text(lx, ly-0.06, ip, ha='center', va='center',
            fontsize=6, color='#8B949E', zorder=11)
        ax.text(lx, ly-0.24, vlan, ha='center', va='center',
            fontsize=5.5, color='#3FB950' if i > 0 else '#F6AD55', zorder=11)

    # ── "TOPOLOGI BINTANG" annotation ──
    ax.add_patch(FancyBboxPatch((7.5, 6.55), 5.0, 0.55,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc='#003D73CC', ec='#58A6FF', lw=1.5, zorder=13))
    ax.text(10, 6.83, '★  STAR TOPOLOGY – Switch sebagai PUSAT  ★',
        ha='center', va='center', fontsize=9, fontweight='bold',
        color='#58A6FF', zorder=14)

    # ── PT file info box ──
    ax.add_patch(FancyBboxPatch((0.2, 0.75), 4.0, 2.8,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc='#161B22', ec='#30363D', lw=1.5, zorder=15))
    ax.text(2.2, 3.35, 'FILE INFO', ha='center', fontsize=9,
        fontweight='bold', color='#58A6FF', zorder=16)
    pt_info = [
        ('Fail', 'Makmal-Rangkaian.pkt'),
        ('Versi', 'Packet Tracer 8.x'),
        ('Mode', 'Realtime Mode'),
        ('Protokol', 'IEEE 802.3u/ab'),
        ('Peranti', '28 (Router+SW+26PC)'),
        ('Kabel', 'Copper Straight-Through'),
    ]
    for ji, (k2, v2) in enumerate(pt_info):
        yy2 = 3.05 - ji * 0.38
        ax.text(0.4, yy2, k2+':', fontsize=7.5, color='#8B949E',
            va='center', zorder=16)
        ax.text(4.1, yy2, v2, fontsize=7.5, color='#C9D1D9',
            va='center', ha='right', zorder=16)

    fig.tight_layout(pad=0.1)
    path = f'{OUT}/CISCO_packet_tracer_view.png'
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='#2D333B')
    plt.close(fig)
    print(f'  Saved: {path}')


# ── Run ───────────────────────────────────────────────────────────────────────
print('Generating Cisco Star Topology diagrams...')
draw_cisco_star()
draw_cisco_floor_plan()
draw_packet_tracer_view()
print('Done! 3 Cisco diagrams generated.')
