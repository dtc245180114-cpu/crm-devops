import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, PathPatch
from matplotlib.path import Path

def draw_diagram():
    fig = plt.figure(figsize=(11, 10), dpi=200)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1100)
    ax.set_ylim(0, 1000)
    ax.axis('off')

    plt.rcParams['font.family'] = 'Segoe UI'

    # Title
    ax.text(550, 965, "Sơ đồ kiến trúc hệ thống CRM Chăm sóc Khách hàng", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#111827')

    # Actor: Người dùng (top right)
    actor_x, actor_y = 850, 890
    # Head
    head = Circle((actor_x, actor_y + 30), 16, edgecolor='#1f2937', facecolor='white', lw=1.8, zorder=5)
    ax.add_patch(head)
    # Body
    ax.plot([actor_x, actor_x], [actor_y + 14, actor_y - 25], color='#1f2937', lw=1.8, zorder=5)
    # Arms
    ax.plot([actor_x - 26, actor_x + 26], [actor_y, actor_y], color='#1f2937', lw=1.8, zorder=5)
    # Legs
    ax.plot([actor_x, actor_x - 22], [actor_y - 25, actor_y - 60], color='#1f2937', lw=1.8, zorder=5)
    ax.plot([actor_x, actor_x + 22], [actor_y - 25, actor_y - 60], color='#1f2937', lw=1.8, zorder=5)
    # Label
    ax.text(actor_x, actor_y - 75, "Người dùng", fontsize=12, fontweight='bold', ha='center', va='top', color='#1f2937')

    # Docker Compose Line
    ax.plot([30, 1070], [755, 755], color='#374151', lw=1.8)
    ax.text(550, 770, "Docker Compose (máy chủ Ubuntu)", fontsize=13, fontweight='bold', ha='center', va='center', color='#1f2937')

    # Arrow from Actor to Nginx
    ax.annotate("", xy=(actor_x, 665), xytext=(actor_x, 805),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.8, mutation_scale=14))
    ax.text(actor_x + 10, 725, "HTTPS", fontsize=11, fontweight='bold', ha='left', va='center', color='#1f2937')

    # Helper for 3D boxes
    def draw_3d_box(x, y, w, h, title):
        # Main box
        rect = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                              edgecolor='#374151', facecolor='white', lw=1.8, zorder=2)
        ax.add_patch(rect)
        # Top-right 3D effect
        d = 12
        ax.plot([x, x + d], [y + h, y + h + d], color='#374151', lw=1.4, zorder=2)
        ax.plot([x + d, x + w + d], [y + h + d, y + h + d], color='#374151', lw=1.4, zorder=2)
        ax.plot([x + w, x + w + d], [y + h, y + h + d], color='#374151', lw=1.4, zorder=2)
        ax.plot([x + w + d, x + w + d], [y + h + d, y + d], color='#374151', lw=1.4, zorder=2)
        ax.plot([x + w, x + w + d], [y, y + d], color='#374151', lw=1.4, zorder=2)
        
        ax.text(x + w/2, y + h - 22, title, fontsize=13, fontweight='bold', ha='center', va='center', color='#111827', zorder=3)

    # Helper for UML components
    def draw_component(x, y, w, h, title, sub=""):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=3",
                              edgecolor='#374151', facecolor='#fafafa', lw=1.4, zorder=3)
        ax.add_patch(rect)
        # Small UML icon in top right
        icon_w, icon_h = 16, 11
        ix, iy = x + w - 24, y + h - 18
        icon_box = FancyBboxPatch((ix, iy), icon_w, icon_h, boxstyle="square,pad=0",
                                  edgecolor='#374151', facecolor='white', lw=1, zorder=4)
        ax.add_patch(icon_box)
        # 2 small tabs
        t_w, t_h = 6, 3
        ax.add_patch(FancyBboxPatch((ix - 3, iy + 6), t_w, t_h, boxstyle="square,pad=0", edgecolor='#374151', facecolor='white', lw=0.8, zorder=5))
        ax.add_patch(FancyBboxPatch((ix - 3, iy + 1), t_w, t_h, boxstyle="square,pad=0", edgecolor='#374151', facecolor='white', lw=0.8, zorder=5))

        if sub:
            ax.text(x + w/2, y + h/2 + 8, title, fontsize=11, fontweight='bold', ha='center', va='center', color='#111827', zorder=4)
            ax.text(x + w/2, y + h/2 - 10, sub, fontsize=9.5, ha='center', va='center', color='#4b5563', zorder=4)
        else:
            ax.text(x + w/2, y + h/2, title, fontsize=11, fontweight='bold', ha='center', va='center', color='#111827', zorder=4)

    # 1. Reverse Proxy Box
    draw_3d_box(650, 520, 400, 145, "Reverse Proxy")
    draw_component(675, 545, 350, 75, "Nginx", "HTTPS + security headers")

    # 2. Ứng dụng Box
    draw_3d_box(650, 275, 400, 165, "Ứng dụng")
    draw_component(675, 305, 160, 85, "Web Python", "(Flask + Gunicorn)")
    draw_component(865, 305, 160, 85, "pgAdmin", "(Quản trị CSDL)")

    # 3. Database Cylinder: PostgreSQL
    db_x, db_y, db_w, db_h = 770, 75, 160, 110
    # Cylinder bottom ellipse
    b_ell = patches.Ellipse((db_x + db_w/2, db_y + 25), db_w, 45, edgecolor='#374151', facecolor='#fafafa', lw=1.6, zorder=2)
    ax.add_patch(b_ell)
    # Cylinder body
    rect_db = FancyBboxPatch((db_x, db_y + 25), db_w, 55, boxstyle="square,pad=0", edgecolor='#374151', facecolor='#fafafa', lw=1.6, zorder=2)
    ax.add_patch(rect_db)
    # Re-cover with white to hide interior seam
    rect_fill = FancyBboxPatch((db_x + 1, db_y + 25), db_w - 2, 55, boxstyle="square,pad=0", edgecolor='none', facecolor='#fafafa', zorder=2.5)
    ax.add_patch(rect_fill)
    b_ell2 = patches.Ellipse((db_x + db_w/2, db_y + 25), db_w - 2, 43, edgecolor='none', facecolor='#fafafa', zorder=2.6)
    ax.add_patch(b_ell2)
    # Bottom arc
    arc = patches.Arc((db_x + db_w/2, db_y + 25), db_w, 45, angle=0, theta1=180, theta2=360, edgecolor='#374151', lw=1.6, zorder=3)
    ax.add_patch(arc)
    # Cylinder top ellipse
    t_ell = patches.Ellipse((db_x + db_w/2, db_y + 80), db_w, 45, edgecolor='#374151', facecolor='white', lw=1.6, zorder=4)
    ax.add_patch(t_ell)
    ax.text(db_x + db_w/2, db_y + 50, "PostgreSQL", fontsize=12, fontweight='bold', ha='center', va='center', color='#111827', zorder=5)

    # 4. Giám sát và log tập trung Box
    draw_3d_box(40, 60, 560, 665, "Giám sát và log tập trung")
    draw_component(245, 590, 150, 70, "Grafana")
    draw_component(75, 415, 140, 70, "Loki")
    draw_component(375, 415, 160, 70, "Prometheus")
    draw_component(65, 120, 200, 95, "Promtail", "(đọc log container)")
    draw_component(335, 120, 230, 95, "Exporters", "(container, web, DB)")

    # ------------------ ARROWS ------------------
    # Nginx -> Grafana (proxy)
    ax.annotate("", xy=(395, 625), xytext=(675, 582),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14))
    ax.text(540, 620, "proxy", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    # Nginx -> Web Python (proxy)
    ax.annotate("", xy=(755, 390), xytext=(800, 545),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14))
    ax.text(760, 465, "proxy", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    # Nginx -> pgAdmin (proxy)
    ax.annotate("", xy=(945, 390), xytext=(890, 545),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14))
    ax.text(935, 465, "proxy", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    # Web Python -> PostgreSQL (SQL)
    ax.annotate("", xy=(810, 185), xytext=(755, 305),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14))
    ax.text(765, 235, "SQL", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    # pgAdmin -> PostgreSQL (SQL)
    ax.annotate("", xy=(890, 185), xytext=(945, 305),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14))
    ax.text(935, 235, "SQL", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    # Grafana -> Loki (log)
    ax.annotate("", xy=(180, 485), xytext=(280, 590),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14))
    ax.text(215, 545, "log", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    # Grafana -> Prometheus (metrics)
    ax.annotate("", xy=(440, 485), xytext=(360, 590),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14))
    ax.text(415, 545, "metrics", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    # Promtail -> Loki (đẩy log)
    ax.annotate("", xy=(145, 415), xytext=(155, 215),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14))
    ax.text(150, 315, "đẩy log", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    # Prometheus -> Exporters (thu metrics)
    ax.annotate("", xy=(450, 215), xytext=(450, 415),
                arrowprops=dict(arrowstyle="-|>", color='#1f2937', lw=1.6, mutation_scale=14,
                                connectionstyle="arc3,rad=-0.35"))
    ax.text(405, 315, "thu metrics", fontsize=10.5, ha='center', va='center', color='#1f2937',
            bbox=dict(boxstyle="square,pad=0.2", facecolor='white', edgecolor='none'))

    plt.tight_layout()
    png_path = r"c:\Users\Dell 9370\Downloads\thi_trienkhai\so_do_kien_truc_crm.png"
    plt.savefig(png_path, dpi=200, bbox_inches='tight', facecolor='white')
    print("PNG created successfully at:", png_path)

if __name__ == '__main__':
    draw_diagram()
