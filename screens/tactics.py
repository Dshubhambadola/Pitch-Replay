import matplotlib.pyplot as plt
from visualization.pitch import draw_pitch
from utils.theme import Colors

class TacticsScreen:
    def __init__(self, fig):
        self.fig = fig
        self.axes = []
        
    def show(self):
        self.hide()
        
        # Header
        ax_header = self.fig.add_axes([0.1, 0.9, 0.8, 0.08])
        ax_header.set_facecolor(Colors.BACKGROUND)
        ax_header.text(0.0, 0.5, "Tactical Formation: 4-3-3", color='white', fontsize=24, fontweight='bold', va='center')
        ax_header.text(0.35, 0.5, "Phase: Attacking Organization", color=Colors.PRIMARY, fontsize=14, va='center')
        ax_header.axis('off')
        self.axes.append(ax_header)
        
        # Pitch
        ax_pitch = self.fig.add_axes([0.15, 0.1, 0.7, 0.8])
        ax_pitch.set_facecolor(Colors.PITCH_COLOR)
        draw_pitch(ax_pitch, line_color=Colors.LINE_COLOR, pitch_color=Colors.PITCH_COLOR)
        self.axes.append(ax_pitch)
        
        # Draw Players in 4-3-3
        # GK
        self._draw_player(ax_pitch, 5, 40, "GK", "1")
        # Defense
        self._draw_player(ax_pitch, 25, 10, "LB", "3")
        self._draw_player(ax_pitch, 25, 30, "CB", "4")
        self._draw_player(ax_pitch, 25, 50, "CB", "5")
        self._draw_player(ax_pitch, 25, 70, "RB", "2")
        # Midfield
        self._draw_player(ax_pitch, 50, 40, "CDM", "6")
        self._draw_player(ax_pitch, 70, 20, "CM", "8")
        self._draw_player(ax_pitch, 70, 60, "CM", "10")
        # Attack
        self._draw_player(ax_pitch, 90, 15, "LW", "11")
        self._draw_player(ax_pitch, 100, 40, "ST", "9")
        self._draw_player(ax_pitch, 90, 65, "RW", "7")
        
    def _draw_player(self, ax, x, y, role, num):
        # Circle
        circle = plt.Circle((x, y), 3, color=Colors.PRIMARY, alpha=0.8, zorder=3)
        ax.add_patch(circle)
        # Number
        ax.text(x, y, num, color='black', ha='center', va='center', fontweight='bold', zorder=4)
        # Role Label
        ax.text(x, y-5, role, color='white', ha='center', fontsize=8, zorder=4)
        
    def hide(self):
        for ax in self.axes:
            ax.remove()
        self.axes = []
