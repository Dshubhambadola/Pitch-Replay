import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from utils.theme import Colors

class DashboardScreen:
    def __init__(self, fig):
        self.fig = fig
        self.axes = []
        
    def show(self):
        """Renders the Analytics Dashboard with Bento-style containers."""
        self.hide() 
        
        # 1. Header (Top)
        ax_header = self.fig.add_axes([0.1, 0.9, 0.8, 0.08])
        ax_header.set_facecolor(Colors.BACKGROUND)
        ax_header.text(0.0, 0.5, "Kevin De Bruyne", color='white', fontsize=28, fontweight='bold', va='center')
        ax_header.text(0.35, 0.5, "#17 | Manchester City", color=Colors.PRIMARY, fontsize=14, va='center')
        ax_header.axis('off')
        self.axes.append(ax_header)
        
        # Helper to draw rounded panel
        def draw_bento_panel(rect, title):
            # rect: [x, y, w, h]
            ax = self.fig.add_axes(rect)
            ax.set_facecolor(Colors.BACKGROUND) # Transparentish
            
            # Draw Rounded Box
            # In add_axes, coordinates are 0-1 relative to AXES, but we need to draw relative to valid space.
            # Actually, easiest way is to make the AXES the container background.
            ax.set_facecolor(Colors.CHART_BG)
            
            # Rounded FancyBboxPatch as background
            # We add a patch covering the whole axes
            bbox = patches.FancyBboxPatch((0, 0), 1, 1,
                                          boxstyle="round,pad=0,rounding_size=0.05",
                                          facecolor=Colors.CHART_BG,
                                          transform=ax.transAxes,
                                          clip_on=False,
                                          zorder=0)
            ax.add_patch(bbox)
            
            # Title
            if title:
                ax.text(0.05, 0.92, title.upper(), color='grey', fontsize=9, fontweight='bold', transform=ax.transAxes)
            
            ax.axis('off')
            return ax

        # 2. Main Heatmap (Left Large Box) - Grid Location
        ax_heat = draw_bento_panel([0.1, 0.35, 0.45, 0.5], "SEASONAL HEATMAP")
        # Visual styling: Add pitch outline
        self._draw_mini_pitch(ax_heat)
        # Heatmap blobs
        x, y = np.random.normal(loc=60, scale=20, size=1000), np.random.normal(loc=40, scale=15, size=1000)
        ax_heat.hist2d(x, y, bins=30, range=[[0, 120], [0, 80]], cmap='Greens', alpha=0.6, zorder=2)
        self.axes.append(ax_heat)
        
        # 3. Pass Distribution (Right Top Box)
        ax_pass = draw_bento_panel([0.57, 0.55, 0.35, 0.3], "PASS DISTRIBUTION")
        labels = ['Forward', 'Lateral', 'Backward']
        vals = [85, 60, 30] # percents
        y_pos = [2.5, 1.5, 0.5]
        
        # Custom "Progress Bar" chart
        for y, val, label in zip(y_pos, vals, labels):
            # Label
            ax_pass.text(0.05, y/3 + 0.1, label, color='white', fontsize=10, transform=ax_pass.transAxes)
            # Background Track
            rect_bg = patches.Rectangle((0.3, y/3+0.08), 0.6, 0.08, facecolor='#1E3A5F', transform=ax_pass.transAxes)
            ax_pass.add_patch(rect_bg)
            # Fill
            width = 0.6 * (val/100)
            rect_fill = patches.Rectangle((0.3, y/3+0.08), width, 0.08, facecolor=Colors.PRIMARY, transform=ax_pass.transAxes)
            ax_pass.add_patch(rect_fill)
        self.axes.append(ax_pass)
        
        # 4. Network Centrality (Right Middle Box)
        ax_net = draw_bento_panel([0.57, 0.35, 0.35, 0.18], "NETWORK CENTRALITY")
        ax_net.text(0.5, 0.4, "0.84", color='white', fontsize=36, fontweight='bold', ha='center', va='center', transform=ax_net.transAxes)
        # Radial Circles decoration
        c1 = patches.Circle((0.5, 0.45), 0.2, color=Colors.PRIMARY, fill=False, lw=3, alpha=0.3, transform=ax_net.transAxes)
        ax_net.add_patch(c1)
        self.axes.append(ax_net)
        
        # 5. Bottom Stats Matrix (Bottom Strip)
        ax_stats = draw_bento_panel([0.1, 0.1, 0.82, 0.22], "PLAYER PERFORMANCE MATRIX")
        
        # Draw nicer bars
        data = [30, 45, 20, 10, 15, 25, 35, 60, 65, 40]
        n_bars = len(data)
        bar_width = 0.6
        for i, h in enumerate(data):
            # Calculate position in 0-1 range
            x_center = (i + 0.5) / n_bars
            h_norm = h / 100 * 0.7 
            
            # Rounded Top Bar
            # We simulate rounded top by drawing a rect + circle on top? Or just standard bars for now.
            rect = patches.Rectangle((x_center - 0.03, 0.15), 0.06, h_norm, facecolor=Colors.PRIMARY, transform=ax_stats.transAxes)
            ax_stats.add_patch(rect)
            
        self.axes.append(ax_stats)
        
    def _draw_mini_pitch(self, ax):
        # Draw a faint pitch outline inside the axes (0-120, 0-80)
        # Map 0-120 to axes 0.05-0.95
        ax.set_xlim(-5, 125)
        ax.set_ylim(-5, 85)
        
        lc = Colors.BORDER
        ax.plot([0, 120], [0, 0], color=lc, lw=1)
        ax.plot([0, 120], [80, 80], color=lc, lw=1)
        ax.plot([0, 0], [0, 80], color=lc, lw=1)
        ax.plot([120, 120], [0, 80], color=lc, lw=1)
        ax.plot([60, 60], [0, 80], color=lc, lw=1)
        # Center Circle
        c = patches.Circle((60, 40), 10, color=lc, fill=False)
        ax.add_patch(c)
        
    def hide(self):
        for ax in self.axes:
            ax.remove()
        self.axes = []
