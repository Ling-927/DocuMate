import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

# Case dimensions
W, D, H = 110, 140, 80
T = 3  # wall thickness

def box_faces(x0, y0, z0, x1, y1, z1, color, alpha=1.0):
    """Return Poly3DCollection for a solid box."""
    verts = [
        # bottom
        [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)],
        # top
        [(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],
        # front
        [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],
        # back
        [(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],
        # left
        [(x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1)],
        # right
        [(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],
    ]
    poly = Poly3DCollection(verts, alpha=alpha)
    poly.set_facecolor(color)
    poly.set_edgecolor('#1a1a1a')
    poly.set_linewidth(0.4)
    return poly

def cylinder_ring(cx, cy, z0, z1, r, color, alpha=1.0, n=20):
    """Return Poly3DCollection for a cylinder (side only)."""
    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    faces = []
    for i in range(n):
        t0, t1 = theta[i], theta[(i+1) % n]
        x0, y0 = cx + r*np.cos(t0), cy + r*np.sin(t0)
        x1, y1 = cx + r*np.cos(t1), cy + r*np.sin(t1)
        faces.append([(x0,y0,z0),(x1,y1,z0),(x1,y1,z1),(x0,y0,z1)])
    # top cap
    top = [(cx+r*np.cos(t), cy+r*np.sin(t), z1) for t in theta]
    faces.append(top)
    poly = Poly3DCollection(faces, alpha=alpha)
    poly.set_facecolor(color)
    poly.set_edgecolor('#333')
    poly.set_linewidth(0.3)
    return poly

fig = plt.figure(figsize=(12, 9), facecolor='#1a1a2e')
ax = fig.add_subplot(111, projection='3d', facecolor='#1a1a2e')

# Shift so origin = bottom-left-back corner
ox, oy, oz = -W/2, -D/2, -H/2

# ── MAIN BODY (6 walls, hollow) ──────────────────────────────────────────────
wall_color = '#4a7fa5'
wall_alpha = 0.82

# Bottom wall
ax.add_collection3d(box_faces(ox, oy, oz, ox+W, oy+D, oz+T, wall_color, wall_alpha))
# Top wall
ax.add_collection3d(box_faces(ox, oy, oz+H-T, ox+W, oy+D, oz+H, wall_color, wall_alpha))
# Front wall (y = oy)
ax.add_collection3d(box_faces(ox, oy, oz+T, ox+W, oy+T, oz+H-T, wall_color, wall_alpha))
# Back wall (y = oy+D) — with camera window cut-out visual hint
ax.add_collection3d(box_faces(ox, oy+D-T, oz+T, ox+W, oy+D, oz+H-T, wall_color, wall_alpha))
# Left wall
ax.add_collection3d(box_faces(ox, oy+T, oz+T, ox+T, oy+D-T, oz+H-T, wall_color, wall_alpha))
# Right wall
ax.add_collection3d(box_faces(ox+W-T, oy+T, oz+T, ox+W, oy+D-T, oz+H-T, wall_color, wall_alpha))

# ── CAMERA WINDOW (front face, bright cutout) ────────────────────────────────
# On back wall (y near oy+D), centered, at z=15 above centre
cw_cx = 0  # world-centred
cw_cz = 15  # z offset from centre
win = box_faces(cw_cx-15, oy+D-T-0.5, oz+H/2+cw_cz-10,
                cw_cx+15, oy+D+0.5, oz+H/2+cw_cz+10, '#e0f0ff', 0.95)
ax.add_collection3d(win)

# ── COOLING VENTS – louvres on right wall ────────────────────────────────────
for i in range(-2, 3):
    yc = oy + D/2 + i*15
    zc = oz + H/2 + 10
    louver = box_faces(ox+W-T-3, yc-4, zc-1, ox+W+1, yc+4, zc+1, '#7ec8e3', 0.9)
    ax.add_collection3d(louver)

# ── COOLING VENTS – louvres on left wall ────────────────────────────────────
for i in range(-2, 3):
    yc = oy + D/2 + i*15
    zc = oz + H/2 + 10
    louver = box_faces(ox-1, yc-4, zc-1, ox+T+3, yc+4, zc+1, '#7ec8e3', 0.9)
    ax.add_collection3d(louver)

# ── POWER CABLE HOLE (bottom) ────────────────────────────────────────────────
ax.add_collection3d(cylinder_ring(0, oy+20, oz-1, oz+T+2, 7, '#0a0a0a', 1.0))

# ── PI 4 STANDOFFS (4 cylinders) ────────────────────────────────────────────
standoff_positions = [(-29,-24.5),(29,-24.5),(-29,24.5),(29,24.5)]
for sx, sy in standoff_positions:
    ax.add_collection3d(cylinder_ring(sx, sy, oz+T, oz+T+15, 2.5, '#c8973a', 1.0))

# ── CAMERA BRACKET ───────────────────────────────────────────────────────────
bx0, bx1 = -20, 20
by0, by1 = oy+D-15-1, oy+D-15+1
bz0, bz1 = oz+H/2, oz+H/2+40
bracket = box_faces(bx0, by0, bz0, bx1, by1, bz1, '#e8b96a', 0.9)
ax.add_collection3d(bracket)
# Lens hole hint (dark square in middle of bracket)
lens = box_faces(-7.5, by0-0.2, oz+H/2+12.5, 7.5, by1+0.2, oz+H/2+27.5, '#111', 1.0)
ax.add_collection3d(lens)

# ── BREADBOARD GHOST ─────────────────────────────────────────────────────────
bb = box_faces(-27.5, oy+D/2-30-42.5, oz+T+2,
               27.5, oy+D/2-30+42.5, oz+T+7, '#2d7a4f', 0.35)
ax.add_collection3d(bb)

# ── Axis / view ──────────────────────────────────────────────────────────────
margin = 20
ax.set_xlim(ox-margin, ox+W+margin)
ax.set_ylim(oy-margin, oy+D+margin)
ax.set_zlim(oz-margin, oz+H+margin)
ax.set_box_aspect([W, D, H])
ax.view_init(elev=22, azim=-45)

ax.set_xlabel('Width (mm)', color='#aaa', fontsize=8)
ax.set_ylabel('Depth (mm)', color='#aaa', fontsize=8)
ax.set_zlabel('Height (mm)', color='#aaa', fontsize=8)
ax.tick_params(colors='#666', labelsize=7)
for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor('#333')
ax.grid(True, color='#333', linewidth=0.4)

# ── Legend ───────────────────────────────────────────────────────────────────
from matplotlib.patches import Patch
legend_items = [
    Patch(facecolor='#4a7fa5', label='Case body (110×140×80 mm)'),
    Patch(facecolor='#e0f0ff', label='Camera window'),
    Patch(facecolor='#7ec8e3', label='Cooling vents (louvres)'),
    Patch(facecolor='#0a0a0a', edgecolor='#555', label='Power cable hole ⌀14 mm'),
    Patch(facecolor='#c8973a', label='Pi 4 standoffs ×4'),
    Patch(facecolor='#e8b96a', label='Camera mount (−15°)'),
    Patch(facecolor='#2d7a4f', alpha=0.5, label='Breadboard footprint (ghost)'),
]
ax.legend(handles=legend_items, loc='upper left', fontsize=7,
          facecolor='#12122a', edgecolor='#444', labelcolor='#ccc',
          framealpha=0.85)

fig.suptitle('Raspberry Pi 4 + Cam V3 — Outdoor Case', color='#e8b96a',
             fontsize=13, fontweight='bold', y=0.97)

plt.tight_layout()
plt.savefig('/home/user/DocuMate/case_render.png', dpi=160, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print("Saved case_render.png")
