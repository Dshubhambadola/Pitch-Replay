import matplotlib.pyplot as plt
from utils.theme import Colors

class ScreenManager:
    """
    Manages switching between different APPLICATION SCREENS (Dashboard, Match, Tactics).
    """
    def __init__(self, fig):
        self.fig = fig
        self.current_screen = "DASHBOARD" # Default
        self.screens = {}
        self.sidebar_buttons = []
        
    def setup_sidebar(self):
        """Creates the permanent sidebar navigation."""
        # Clean Sidebar Area
        ax = self.fig.add_axes([0.0, 0.0, 0.06, 1.0]) # Thin Left Sidebar
        ax.set_facecolor(Colors.SIDEBAR_BG)
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Logo placeholder
        ax.text(0.5, 0.95, "P", color=Colors.PRIMARY, fontsize=24, fontweight='bold', ha='center', va='center', transform=ax.transAxes)
        
        # Navigation Icons
        # We add a "Pill" indicator for active state
        self.active_indicator = plt.Rectangle((0, 0), 0.1, 0.1, facecolor=Colors.PRIMARY, transform=ax.transAxes, visible=False)
        ax.add_patch(self.active_indicator)
        
        self._add_nav_button(ax, 0.8, "DASH", "DASHBOARD")
        self._add_nav_button(ax, 0.7, "MATCH", "MATCH")
        self._add_nav_button(ax, 0.6, "SQUAD", "TACTICS")
        
        self.nav_ax = ax
        # Initialize default state
        self.switch_to("DASHBOARD")
        
    def _add_nav_button(self, ax, y, label, screen_key):
        """Draws a clickable text button."""
        text = ax.text(0.5, y, label, color='grey', ha='center', va='center', fontsize=9, transform=ax.transAxes, picker=True)
        self.sidebar_buttons.append((text, screen_key, y))
        
    def handle_click(self, event):
        """Checks if a nav button was clicked."""
        if event.inaxes != self.nav_ax: return None
        
        for text, key, y in self.sidebar_buttons:
            # Simple hit test since picker can be finicky in pure matplotlib sub-axes
            # We check Y distance
            if abs(event.ydata - y) < 0.05:
                return key
        return None

    def switch_to(self, screen_key):
        print(f"Switching to {screen_key}...")
        self.current_screen = screen_key
        
        # Update Visuals
        for text, key, y in self.sidebar_buttons:
            if key == screen_key:
                text.set_color('white')
                text.set_fontweight('bold')
                
                # Move indicator
                self.active_indicator.set_y(y - 0.02)
                self.active_indicator.set_height(0.04)
                self.active_indicator.set_width(0.05)
                self.active_indicator.set_visible(True)
            else:
                text.set_color('grey')
                text.set_fontweight('normal')
        
        self.fig.canvas.draw_idle()
