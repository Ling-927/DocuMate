"""
CU6 – 2 gambar untuk laporan:
  cu6_tajuk2_floor_plan.png  → Tajuk 2: Pelan lantai + susun atur kabel bintang
  cu6_tajuk5_packet_tracer.png → Tajuk 5: Cisco Packet Tracer star topology
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch
import numpy as np
import os

OUT = '/home/user/DocuMate/images'
os.makedirs(OUT, exist_ok=True)

# ── colours ───────────────────────────────────────────────────────────────────
C_BLUE   = '#00549F'
C_DARK   = '#003D73'
C_LIGHT  = '#EBF8FF'
C_GREEN  = '#276749'
C_LGREEN = '#C6F6D5'
C_ORANGE = '#DD6B20'
C_RED    = '#E53E3E'
C_RACK   = '#1C2433'
C_GRAY   = '#2D3748'
C_MID    = '#718096'
C_GLITE  = '#EDF2F7'
C_YELL   = '#D69E2E'
WHITE    = '#FFFFFF'

plt.rcParams['font.family'] = 'DejaVu Sans'

# ─── shared icon helpers ──────────────────────────────────────────────────────

def router_icon(ax, cx, cy, r=0.48, color=C_BLUE, z=10):
    ax.add_patch(mpatches.Ellipse((cx,cy), r*2, r*0.68,
        fc=color, ec=WHITE, lw=2.2, zorder=z))
    ax.add_patch(FancyBboxPatch((cx-r, cy-r*0.6), r*2, r*0.62,
        boxstyle='round,pad=0', fc=color, ec='none', zorder=z))
    ax.add_patch(mpatches.Ellipse((cx,cy-r*0.6), r*2, r*0.68,
        fc=color, ec=WHITE, lw=2.2, zorder=z))
    ax.add_patch(mpatches.Arc((cx+r*0.25,cy-r*0.28), r*0.52, r*0.52,
        angle=0, theta1=35, theta2=310, color=WHITE, lw=2, zorder=z+1))
    ax.annotate('',xy=(cx+r*0.50,cy-r*0.14),xytext=(cx+r*0.50,cy-r*0.15),
        arrowprops=dict(arrowstyle='->',color=WHITE,lw=1.6),zorder=z+2)
    ax.add_patch(mpatches.Arc((cx-r*0.25,cy-r*0.28), r*0.52, r*0.52,
        angle=0, theta1=230, theta2=145, color=WHITE, lw=2, zorder=z+1))
    ax.annotate('',xy=(cx-r*0.50,cy-r*0.42),xytext=(cx-r*0.50,cy-r*0.41),
        arrowprops=dict(arrowstyle='->',color=WHITE,lw=1.6),zorder=z+2)

def switch_icon(ax, cx, cy, w=1.2, h=0.38, color=C_DARK, z=10):
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2), w, h,
        boxstyle='round,pad=0,rounding_size=0.07',
        fc=color, ec=WHITE, lw=2, zorder=z))
    n=10; gap=w*0.06; pw=(w-2*gap-(n-1)*gap/1.8)/n*0.85; px0=cx-w/2+gap
    for i in range(n):
        px=px0+i*(pw+gap/1.8)
        ax.add_patch(FancyBboxPatch((px,cy-h/2+h*0.14),pw,h*0.3,
            boxstyle='round,pad=0',fc='#48BB78',ec='none',zorder=z+1))
        ax.add_patch(FancyBboxPatch((px,cy-h/2+h*0.52),pw,h*0.3,
            boxstyle='round,pad=0',fc='#48BB78',ec='none',zorder=z+1))
    ax.plot(cx-w/2+gap*0.5,cy+h*0.22,'o',color='#48BB78',ms=5,zorder=z+2)

def pc_icon(ax, cx, cy, sz=0.22, color=C_BLUE, z=10):
    mw,mh = sz*2.0, sz*1.5
    ax.add_patch(FancyBboxPatch((cx-mw/2,cy),mw,mh,
        boxstyle='round,pad=0,rounding_size=0.05',
        fc=C_GRAY, ec=WHITE, lw=1.3, zorder=z))
    pad=mw*0.09
    ax.add_patch(FancyBboxPatch((cx-mw/2+pad,cy+pad),mw-2*pad,mh-2*pad,
        boxstyle='round,pad=0,rounding_size=0.03',
        fc=color, ec='none', zorder=z+1))
    ax.add_patch(FancyBboxPatch((cx-mw*0.1,cy-mh*0.22),mw*0.2,mh*0.22,
        boxstyle='round,pad=0',fc=C_GRAY,ec='none',zorder=z))
    ax.add_patch(FancyBboxPatch((cx-mw*0.42,cy-mh*0.32),mw*0.84,mh*0.12,
        boxstyle='round,pad=0,rounding_size=0.03',
        fc='#4A5568',ec=WHITE,lw=0.7,zorder=z))

def cloud_icon(ax, cx, cy, rw=1.1, rh=0.55, z=5):
    for dx,dy,r in [(-0.5,-0.05,0.32),(-.18,0.1,0.4),(0.2,0.14,0.44),
                     (0.52,0.04,0.36),(0.68,-0.1,0.28),(-0.65,-0.1,0.26)]:
        ax.add_patch(mpatches.Circle((cx+dx*rw,cy+dy*rh*2),r*rh*1.3,
            fc='#DBEAFE',ec='#63B3ED',lw=1.8,zorder=z))
    ax.add_patch(FancyBboxPatch((cx-rw*0.82,cy-rh*0.55),rw*1.64,rh*0.82,
        boxstyle='round,pad=0',fc='#DBEAFE',ec='none',zorder=z))


# ══════════════════════════════════════════════════════════════════════════════
#  TAJUK 2 — PELAN LANTAI (landscape A4-ish, 25 PC)
# ══════════════════════════════════════════════════════════════════════════════

def draw_floor_plan():
    # landscape: 22 wide × 16 tall (world units)
    fig, ax = plt.subplots(figsize=(22,16))
    ax.set_xlim(0,22); ax.set_ylim(0,16)
    ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('#F0F4F8')

    # ── title bar ──
    ax.add_patch(FancyBboxPatch((0,15.2),22,0.8,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc=C_DARK,ec='none',zorder=30))
    ax.text(11,15.62,
        'TAJUK 2 – PELAN LANTAI MAKMAL RANGKAIAN  |  TOPOLOGI BINTANG (STAR TOPOLOGY)  |  25 PC',
        ha='center',va='center',fontsize=13.5,fontweight='bold',color=WHITE,zorder=31)

    # ── room outline ──
    ax.add_patch(FancyBboxPatch((0.5,0.5),21,14.55,
        boxstyle='round,pad=0,rounding_size=0.25',
        fc='#FAFAFA',ec=C_GRAY,lw=5,zorder=1))

    # front wall shading
    ax.add_patch(FancyBboxPatch((0.5,13.8),21,1.25,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#EBF5FF',ec=C_BLUE,lw=1.5,zorder=2))
    ax.text(11,14.43,'DINDING HADAPAN  /  FRONT WALL',
        ha='center',va='center',fontsize=9,color=C_BLUE,fontweight='bold',zorder=3)

    # projector screen
    ax.add_patch(FancyBboxPatch((3.5,13.82),9.5,0.38,
        boxstyle='round,pad=0,rounding_size=0.05',
        fc='#E2E8F0',ec=C_GRAY,lw=2,zorder=4))
    ax.text(8.25,14.02,'[ SKRIN PROJEKTOR / SMARTBOARD  120" ]',
        ha='center',va='center',fontsize=9,color=C_GRAY,fontweight='bold',zorder=5)

    # ── network rack (back-right) ──
    rack_x,rack_y = 17.6,10.4
    ax.add_patch(FancyBboxPatch((rack_x,rack_y),3.3,3.8,
        boxstyle='round,pad=0,rounding_size=0.2',
        fc=C_RACK,ec='#4A5568',lw=3,zorder=8))
    ax.add_patch(FancyBboxPatch((rack_x+0.14,rack_y+0.14),3.02,3.52,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc='#141921',ec='#4A5568',lw=1.2,zorder=9))

    rack_units=[
        (C_BLUE,     'PATCH PANEL  Cat6  24-port'),
        (C_DARK,     'CISCO 2960-24TT  SWITCH  ★'),
        (C_BLUE,     'CISCO 1941  ROUTER'),
        ('#9B2C2C',  'UPS  APC  1000VA / 700W'),
        ('#1A202C',  'PDU / PSU  16A  8×C13'),
        ('#1A202C',  'FAN TRAY  1U'),
    ]
    for ri,(rfc,rlbl) in enumerate(rack_units):
        ry2=rack_y+0.2+ri*0.56
        ax.add_patch(FancyBboxPatch((rack_x+0.18,ry2),2.94,0.5,
            boxstyle='round,pad=0,rounding_size=0.06',
            fc=rfc,ec='#4A5568',lw=0.8,zorder=10))
        ax.plot(rack_x+0.32,ry2+0.25,'o',
            color='#48BB78' if ri<3 else (C_ORANGE if ri==3 else '#4A5568'),
            ms=5,zorder=11)
        ax.text(rack_x+1.65,ry2+0.25,rlbl,
            ha='center',va='center',fontsize=6.8,fontweight='bold',
            color=WHITE,zorder=11)
    ax.text(rack_x+1.65,rack_y+3.6,'NETWORK RACK  12U',
        ha='center',va='center',fontsize=8.5,fontweight='bold',
        color=WHITE,zorder=10)

    # rack label
    ax.add_patch(FancyBboxPatch((rack_x,rack_y-0.65),3.3,0.55,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc=C_DARK,ec='none',zorder=8))
    ax.text(rack_x+1.65,rack_y-0.37,'ZON PENGKABELAN',
        ha='center',va='center',fontsize=8,fontweight='bold',
        color=WHITE,zorder=9)

    # ── teacher desk ──
    td_x,td_y=5.0,11.4
    ax.add_patch(FancyBboxPatch((td_x,td_y),4.5,2.1,
        boxstyle='round,pad=0,rounding_size=0.15',
        fc=C_LIGHT,ec=C_BLUE,lw=2.5,zorder=5))
    pc_icon(ax,td_x+2.25,td_y+0.9,sz=0.28,color=C_BLUE,z=8)
    ax.text(td_x+2.25,td_y+0.42,'KOMPUTER PENGAJAR',
        ha='center',va='center',fontsize=8.5,fontweight='bold',color=C_BLUE,zorder=9)
    ax.text(td_x+2.25,td_y+0.15,'IP: 192.168.1.1 | VLAN 20 | Fa0/24',
        ha='center',va='center',fontsize=7,color=C_MID,zorder=9)
    ax.text(td_x+2.25,td_y-0.25,'MEJA PENGAJAR',
        ha='center',va='center',fontsize=7.5,color=C_DARK,fontweight='bold',zorder=9)

    # ── cable tray (vertical, right wall) ──
    tray_x = 16.6
    ax.add_patch(FancyBboxPatch((tray_x-0.12,0.8),0.26,12.6,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='none',ec=C_YELL,lw=2.5,ls='--',zorder=6))
    ax.text(tray_x,7.1,'CABLE\nTRAY\nCat6',
        ha='center',va='center',fontsize=7.5,color=C_YELL,
        fontweight='bold',linespacing=1.4,
        bbox=dict(fc=WHITE+'CC',ec=C_YELL,pad=2,boxstyle='round'),zorder=7)

    # ── 25 student PCs (5 rows × 5 cols) ──
    # desk columns (x-center of each desk cluster)
    cols = [1.6, 4.0, 6.4, 8.8, 11.2]
    # row y-positions (from top to bottom = row1..row5)
    rows = [10.2, 8.2, 6.2, 4.2, 2.2]
    row_lbl = ['Baris 1','Baris 2','Baris 3','Baris 4','Baris 5']

    # switch connection point (rack switch)
    sw_cx = rack_x+1.65; sw_cy = rack_y+1.42

    pc_n = 1
    for ri,(ry,rn) in enumerate(zip(rows,row_lbl)):
        # row label
        ax.text(0.88,ry+0.75,rn,ha='center',va='center',
            fontsize=7.5,color=C_MID,fontstyle='italic',zorder=5)
        for ci,cx in enumerate(cols):
            ip_end = 9+pc_n

            # ── cable path: PC → horizontal → vertical tray → rack ──
            # horizontal to tray
            ax.plot([cx+0.7,tray_x],[ry+0.75,ry+0.75],
                color='#A0AEC0',lw=1.0,ls=':',zorder=3,alpha=0.8)
            # vertical tray already drawn; just mark entry dot
            ax.plot(tray_x,ry+0.75,'o',color=C_YELL,ms=4,zorder=4)

        # tray→rack horizontal segment (one per row at rack entry)
        ax.plot([tray_x,sw_cx],[ry+0.75,ry+0.75],
            color='#A0AEC0',lw=1.0,ls=':',zorder=3,alpha=0.5)

        for ci,cx in enumerate(cols):
            ip_end=9+pc_n
            # desk background
            ax.add_patch(FancyBboxPatch((cx-0.05,ry-0.22),1.5,1.15,
                boxstyle='round,pad=0,rounding_size=0.1',
                fc=C_GLITE,ec='#CBD5E0',lw=1.2,zorder=5))
            # PC icon
            pc_icon(ax,cx+0.7,ry+0.38,sz=0.24,color='#2B6CB0',z=8)
            # PC number
            ax.text(cx+0.7,ry+0.12,f'PC-{pc_n:02d}',
                ha='center',va='center',fontsize=8,fontweight='bold',
                color=C_DARK,zorder=9)
            ax.text(cx+0.7,ry-0.1,f'192.168.1.{ip_end}',
                ha='center',va='center',fontsize=6.8,color=C_MID,zorder=9)
            pc_n+=1

    # teacher cable → tray
    ax.plot([td_x+4.5,tray_x],[td_y+0.75,td_y+0.75],
        color=C_ORANGE,lw=1.8,ls='--',zorder=5)
    ax.plot(tray_x,td_y+0.75,'o',color=C_ORANGE,ms=5,zorder=6)
    ax.plot([tray_x,sw_cx],[td_y+0.75,td_y+0.75],
        color=C_ORANGE,lw=1.8,ls='--',zorder=5)

    # ── dimension arrows ──
    ax.annotate('',xy=(21.8,0.5),xytext=(21.8,15.0),
        arrowprops=dict(arrowstyle='<->',color=C_MID,lw=1.5))
    ax.text(21.96,7.75,'8 m',va='center',fontsize=9,color=C_MID,
        rotation=90,fontweight='bold')
    ax.annotate('',xy=(0.5,0.18),xytext=(21.5,0.18),
        arrowprops=dict(arrowstyle='<->',color=C_MID,lw=1.5))
    ax.text(11,0.02,'10 meter',ha='center',fontsize=9,color=C_MID,fontweight='bold')

    # ── door ──
    ax.add_patch(mpatches.Arc((1.4,0.5),2.0,2.0,
        angle=0,theta1=0,theta2=90,color=C_GRAY,lw=2,ls='--',zorder=3))
    ax.plot([1.4,1.4],[0.5,1.5],color=C_GRAY,lw=3,zorder=3)
    ax.text(1.7,0.28,'PINTU',ha='center',fontsize=8,color=C_MID)

    # ── legend ──
    ax.add_patch(FancyBboxPatch((0.6,0.6),5.5,1.5,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc=WHITE,ec='#CBD5E0',lw=1.2,zorder=20))
    legend=[
        (C_BLUE,   'PC Pengajar (1 unit)'),
        ('#2B6CB0','PC Pelajar (25 unit)'),
        (C_RACK,   'Network Rack 12U'),
        (C_YELL,   'Cable Tray Cat6 UTP'),
        ('#A0AEC0','Kabel UTP Cat6 (titik)'),
        (C_ORANGE, 'Kabel Pengajar'),
    ]
    for li,(lc,ll) in enumerate(legend):
        lx2=0.78+(li%2)*2.75; ly2=1.85-(li//2)*0.52
        ax.add_patch(FancyBboxPatch((lx2,ly2-0.02),0.3,0.28,
            boxstyle='round,pad=0',fc=lc,ec='none',zorder=21))
        ax.text(lx2+0.38,ly2+0.12,ll,va='center',fontsize=7.3,
            color=C_GRAY,zorder=21)

    fig.tight_layout(pad=0.2)
    path=f'{OUT}/cu6_tajuk2_floor_plan.png'
    fig.savefig(path,dpi=180,bbox_inches='tight',facecolor='#F0F4F8')
    plt.close(fig)
    print(f'  Saved: {path}')


# ══════════════════════════════════════════════════════════════════════════════
#  TAJUK 5 — CISCO PACKET TRACER  (star topology, 25 PC)
# ══════════════════════════════════════════════════════════════════════════════

def draw_packet_tracer():
    fig, ax = plt.subplots(figsize=(22,20))
    ax.set_xlim(0,22); ax.set_ylim(0,20)
    ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('#2D333B')

    # PT workspace dark bg
    ax.add_patch(FancyBboxPatch((0,0),22,20,
        boxstyle='round,pad=0',fc='#2D333B',ec='none',zorder=0))

    # grid
    for gx in np.arange(0,22,1):
        ax.axvline(gx,color='#3D434B',lw=0.4,zorder=0)
    for gy in np.arange(0,20,1):
        ax.axhline(gy,color='#3D434B',lw=0.4,zorder=0)

    # ── top toolbar ──
    ax.add_patch(FancyBboxPatch((0,19.2),22,0.8,
        boxstyle='round,pad=0',fc='#161B22',ec='none',zorder=30))
    ax.text(0.5,19.6,'Cisco Packet Tracer 8.x',va='center',
        fontsize=12,fontweight='bold',color='#58A6FF',zorder=31)
    for ti,item in enumerate(['File','Edit','Options','View','Tools','Extensions','Help']):
        ax.text(5.5+ti*1.8,19.6,item,va='center',fontsize=9.5,color='#C9D1D9',zorder=31)
    ax.text(19,19.6,'LAPORAN CU6  |  TAJUK 5',va='center',ha='right',
        fontsize=9,color='#8B949E',zorder=31)

    # ── bottom bar ──
    ax.add_patch(FancyBboxPatch((0,0),22,0.7,
        boxstyle='round,pad=0',fc='#161B22',ec='none',zorder=30))
    for mi,(mode,mc,act) in enumerate([
        ('Realtime','#58A6FF',True),('Simulation','#3FB950',False)]):
        bx=16+mi*2.8
        ax.add_patch(FancyBboxPatch((bx,0.1),2.5,0.5,
            boxstyle='round,pad=0,rounding_size=0.08',
            fc=mc if act else '#30363D',ec=mc,lw=1.5,zorder=31))
        ax.text(bx+1.25,0.35,mode,ha='center',va='center',
            fontsize=9.5,fontweight='bold',
            color=WHITE if act else '#8B949E',zorder=32)

    # ══ DEVICES ══════════════════════════════════════════════════════════

    # Internet cloud
    cloud_icon(ax,11,18.0,rw=1.4,rh=0.6,z=5)
    ax.text(11,18.0,'Internet / ISP',ha='center',va='center',
        fontsize=9.5,fontweight='bold',color='#58A6FF',zorder=8)

    # WAN line Internet→Router
    ax.plot([11,11],[17.35,16.05],color='#F6AD55',lw=3,solid_capstyle='round',zorder=4)
    for y in [17.35,16.05]: ax.plot(11,y,'o',color='#F6AD55',ms=8,zorder=5)
    ax.text(11.3,16.7,'WAN',fontsize=8.5,color='#F6AD55',va='center',fontweight='bold')

    # Router
    router_icon(ax,11,15.1,r=0.55,color='#00549F',z=10)
    ax.add_patch(FancyBboxPatch((9.3,13.85),3.4,0.65,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#1C2D4A',ec='#30363D',lw=1,zorder=9))
    ax.text(11,14.29,'Router0',ha='center',va='center',
        fontsize=10.5,fontweight='bold',color='#58A6FF',zorder=10)
    ax.text(11,14.06,'Cisco 1941  |  192.168.1.254',
        ha='center',va='center',fontsize=8.5,color='#8B949E',zorder=10)

    # Router→Switch line
    ax.plot([11,11],[13.85,12.15],color='#58A6FF',lw=4,solid_capstyle='round',zorder=4)
    for y in [13.85,12.15]: ax.plot(11,y,'o',color='#58A6FF',ms=9,zorder=5)
    ax.text(11.45,13.0,'GE0/1\nTrunk',fontsize=8,color='#58A6FF',
        va='center',fontweight='bold',linespacing=1.3)

    # Switch (STAR CENTER)
    # star burst
    for a in range(0,360,12):
        rad=np.radians(a)
        ax.plot([11,11+6.0*np.cos(rad)],[10.8,10.8+6.0*np.sin(rad)],
            color='#3D434B',lw=0.7,alpha=0.6,zorder=1)

    ax.add_patch(mpatches.Circle((11,10.8),1.5,
        fc='#003D7333',ec='#003D7366',lw=3,zorder=6))
    switch_icon(ax,11,10.8,w=2.0,h=0.62,color='#003D73',z=10)
    ax.add_patch(FancyBboxPatch((8.9,9.55),4.2,0.72,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#1C2D4A',ec='#30363D',lw=1,zorder=9))
    ax.text(11,10.02,'Switch0  ★  PUSAT BINTANG',
        ha='center',va='center',fontsize=10.5,fontweight='bold',
        color='#3FB950',zorder=10)
    ax.text(11,9.76,'Cisco Catalyst 2960-24TT  |  VLAN 10 / 20 / 99',
        ha='center',va='center',fontsize=8,color='#8B949E',zorder=10)

    # UPS (right of router)
    ux,uy=15.5,15.1
    ax.add_patch(FancyBboxPatch((ux-0.55,uy-0.9),1.1,1.55,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#1A202C',ec=C_RED,lw=2,zorder=9))
    # battery bars
    for bi,(bfc,bfrac) in enumerate(
        [('#48BB78',0.55),('#ED8936',0.25),('#FC8181',0.15)]):
        bh=1.0*bfrac
        by=uy-0.82+sum([1.0*[0.55,0.25,0.15][j] for j in range(bi)])
        ax.add_patch(FancyBboxPatch((ux-0.28,by),0.56,bh-0.02,
            boxstyle='round,pad=0',fc=bfc,ec='none',zorder=10))
    ax.plot(ux,uy+0.52,'o',color='#48BB78',ms=6,zorder=11)
    ax.add_patch(FancyBboxPatch((ux-0.14,uy+0.65),0.28,0.08,
        boxstyle='round,pad=0',fc='#4A5568',ec='none',zorder=10))
    ax.add_patch(FancyBboxPatch((ux-0.7,uy-1.3),1.4,0.35,
        boxstyle='round,pad=0,rounding_size=0.08',
        fc='#1C2D4A',ec=C_RED,lw=1,zorder=9))
    ax.text(ux,uy-1.12,'UPS-1000VA',ha='center',va='center',
        fontsize=8.5,fontweight='bold',color='#FC8181',zorder=10)
    ax.plot([ux-0.55,11.55],[uy-0.1,uy-0.1],
        color='#FC8181',lw=1.8,ls='--',zorder=4)

    # ══ 26 PCs (25 pelajar + 1 pengajar) in star ══════════════════════════

    n      = 26
    radius = 7.0
    start  = 128
    span   = 304

    angles = [start + i*span/(n-1) for i in range(n)]

    for i,ang in enumerate(angles):
        rad = np.radians(ang)
        px  = np.clip(11 + radius*np.cos(rad), 0.7, 21.3)
        py  = np.clip(10.8 + radius*np.sin(rad), 0.9, 18.8)

        is_t   = (i==0)
        lc2    = '#F6AD55' if is_t else '#4D8BD4'
        pc_col = '#00549F' if is_t else '#2B6CB0'
        nc     = '#F6AD55' if is_t else '#58A6FF'
        vc     = '#F6AD55' if is_t else '#3FB950'
        nm     = 'PC-Pengajar' if is_t else f'PC-{i:02d}'
        ip2    = '192.168.1.1' if is_t else f'192.168.1.{9+i}'
        vl     = 'VLAN 20'    if is_t else 'VLAN 10'
        pt     = 'Fa0/24'     if is_t else f'Fa0/{i}'

        # cable switch→PC
        stub=1.62
        sx=11+stub*np.cos(rad); sy=10.8+stub*np.sin(rad)
        ax.plot([sx,px],[sy,py],color=lc2,lw=2.2,
            solid_capstyle='round',zorder=3,alpha=0.9)
        ax.plot(sx,sy,'o',color=lc2,ms=5.5,zorder=4)

        # port label near switch
        plx=11+(stub+1.1)*np.cos(rad)
        ply=10.8+(stub+1.1)*np.sin(rad)
        ax.text(plx,ply,pt,ha='center',va='center',fontsize=5.8,
            color='#C9D1D9',zorder=6,
            bbox=dict(fc='#2D333B',ec='#4A5568',pad=1,boxstyle='round,pad=0.15'))

        # PC icon
        pc_icon(ax,px,py,sz=0.22,color=pc_col,z=10)

        # label box
        la=rad+np.pi; lo=0.46
        lx2=np.clip(px+lo*np.cos(la),0.4,21.0)
        ly2=np.clip(py+lo*np.sin(la),0.75,19.3)

        ax.add_patch(FancyBboxPatch((lx2-0.88,ly2-0.45),1.76,0.86,
            boxstyle='round,pad=0,rounding_size=0.1',
            fc='#1C2D4A',ec=lc2,lw=1.3,zorder=9))
        ax.text(lx2,ly2+0.24,nm,ha='center',va='center',
            fontsize=7.5,fontweight='bold',color=nc,zorder=11)
        ax.text(lx2,ly2+0.04,ip2,ha='center',va='center',
            fontsize=7,color='#8B949E',zorder=11)
        ax.add_patch(FancyBboxPatch((lx2-0.42,ly2-0.34),0.84,0.22,
            boxstyle='round,pad=0,rounding_size=0.07',
            fc='#3FB950' if not is_t else '#D69E2E',
            ec='none',zorder=10))
        ax.text(lx2,ly2-0.22,vl,ha='center',va='center',
            fontsize=6.5,fontweight='bold',
            color=WHITE,zorder=11)

    # center label
    ax.add_patch(FancyBboxPatch((8.6,9.28),4.8,0.38,
        boxstyle='round,pad=0,rounding_size=0.1',
        fc='#003D73BB',ec='#58A6FF',lw=1.5,zorder=13))
    ax.text(11,9.47,'★  SWITCH PUSAT – 26 PERANTI DISAMBUNG (TOPOLOGI BINTANG)  ★',
        ha='center',va='center',fontsize=9,fontweight='bold',
        color='#58A6FF',zorder=14)

    # ── PT info box ──
    ax.add_patch(FancyBboxPatch((0.2,0.8),5.2,3.4,
        boxstyle='round,pad=0,rounding_size=0.12',
        fc='#161B22',ec='#30363D',lw=1.5,zorder=20))
    ax.text(2.8,4.0,'MAKLUMAT FAIL',ha='center',fontsize=9.5,
        fontweight='bold',color='#58A6FF',zorder=21)
    ax.plot([0.3,5.3],[3.8,3.8],color='#30363D',lw=1,zorder=21)
    pt_info=[
        ('Fail',     'Makmal-Rangkaian.pkt'),
        ('Versi',    'Cisco Packet Tracer 8.x'),
        ('Topologi', 'Star (Bintang)'),
        ('Router',   'Cisco 1941  – 1 unit'),
        ('Switch',   'Cisco 2960-24TT – 1 unit'),
        ('PC Total', '26 unit (25 + 1 Pengajar)'),
        ('Kabel',    'Copper Straight-Through'),
        ('Subnet',   '192.168.1.0 / 24'),
    ]
    for ji,(k2,v2) in enumerate(pt_info):
        yy2=3.55-ji*0.38
        ax.text(0.4,yy2,k2+':',fontsize=7.8,color='#8B949E',va='center',zorder=21)
        ax.text(5.3,yy2,v2,fontsize=7.8,color='#C9D1D9',
            va='center',ha='right',zorder=21)

    fig.tight_layout(pad=0.1)
    path=f'{OUT}/cu6_tajuk5_packet_tracer.png'
    fig.savefig(path,dpi=180,bbox_inches='tight',facecolor='#2D333B')
    plt.close(fig)
    print(f'  Saved: {path}')


# ─── run ──────────────────────────────────────────────────────────────────────
print('Generating CU6 diagrams...')
draw_floor_plan()
draw_packet_tracer()
print('Done.')
