import matplotlib.pyplot as plt
from utils.theme import Colors

class UIManager:
    def __init__(self, fig):
        self.fig = fig
        # Create Sidebar immediately
        self.sidebar_ax = self.fig.add_axes([0.0, 0.0, 0.25, 1.0])
        self.sidebar_ax.set_facecolor(Colors.PANEL_BG)
        self.sidebar_ax.set_xticks([])
        self.sidebar_ax.set_yticks([])
        self.text_objects = {}
        
    def setup_ui(self, title="Match Replay"):
        """Creates the UI layout. For MatchViz Pro, we focus on overlays."""
        # Clean Sidebar or Minimal usage
        # We can keep the sidebar for global stats, but it should be dark/minimal.
        pass

    def draw_player_card(self, team, number, location):
        """
        Draws a detailed popup card for the selected player.
        """
        if self.sidebar_ax: self.sidebar_ax.clear()
        
        # Create a new axes for the card if it doesn't exist or reuse
        # Ideally, we draw patches on the MAIN axes for "Popup" effect relative to player,
        # OR we use the sidebar area as a "Detail Panel" which is safer for matplotlib layout.
        # Given the "Popup" requirement, let's try to draw it in the top-right or sidebar area.
        
        # Let's use the sidebar space (left 25%) as the "Detail View" to mimic the card.
        ax = self.sidebar_ax
        if not ax: return
        
        ax.set_facecolor(Colors.PANEL_BG)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        # Avatar / Header
        circle = plt.Circle((0.5, 0.85), 0.1, color=Colors.HIGHLIGHT, alpha=0.2, transform=ax.transAxes)
        ax.add_patch(circle)
        ax.text(0.5, 0.85, f"#{number}", color='white', ha='center', va='center', fontsize=20, fontweight='bold', transform=ax.transAxes)
        
        # Name
        ax.text(0.5, 0.72, f"{team} Player", color='white', ha='center', fontsize=14, fontweight='bold', transform=ax.transAxes)
        ax.text(0.5, 0.68, "Midfielder", color='grey', ha='center', fontsize=10, transform=ax.transAxes)
        
        # Stats Grid (Mock Data)
        self._draw_stat_box(ax, 0.1, 0.5, "DISTANCE", "8.2 km")
        self._draw_stat_box(ax, 0.55, 0.5, "SPRINTS", "12")
        self._draw_stat_box(ax, 0.1, 0.35, "PRECISION", "91%")
        self._draw_stat_box(ax, 0.55, 0.35, "CONTROL", "87")
        
        # Action Button
        rect = plt.Rectangle((0.1, 0.1), 0.8, 0.08, facecolor=Colors.HIGHLIGHT, transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(0.5, 0.14, "VIEW FULL REPORT", color='black', ha='center', fontweight='bold', transform=ax.transAxes)

    def _draw_stat_box(self, ax, x, y, label, value):
        # Background
        rect = plt.Rectangle((x, y), 0.35, 0.12, facecolor='#222b36', edgecolor=Colors.BORDER, transform=ax.transAxes)
        ax.add_patch(rect)
        # Content
        ax.text(x + 0.02, y + 0.08, label, color='grey', fontsize=7, transform=ax.transAxes)
        ax.text(x + 0.02, y + 0.03, value, color='white', fontsize=14, fontweight='bold', transform=ax.transAxes)

    def update_selected_player(self, team_name, player_idx, location):
        """Updates the sidebar with selected player info."""
        # Since we don't have real names, we use Team + Index
        name = f"{team_name} Player {player_idx}"
        role = "Midfielder" # Mock role
        
        # Update Text
        self.text_objects['name'].set_text(name)
        self.text_objects['role'].set_text(role)
        self.text_objects['team'].set_text(team_name)
        
        # Color code name
        if team_name == "Home":
            self.text_objects['name'].set_color(Colors.HOME_TEAM)
        else:
            self.text_objects['name'].set_color(Colors.AWAY_TEAM)
        
        # Add dynamic detail (Position)
        # Refresh the sidebar canvas to show changes if needed, 
        # but usually set_text works with main loop.
