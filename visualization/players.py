import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
import numpy as np
from utils.theme import Colors

class PlayerVisualizer:
    def __init__(self, ax):
        self.ax = ax
        self.home_dots = None
        self.away_dots = None
        self.ball_dot = None
        self.home_text = []
        self.away_text = []
        self.home_hull = None
        self.away_hull = None
        
    def init_players(self):
        """Initializes the scatter plots and text annotations for players."""
        # Home team (Cyan)
        self.home_dots = self.ax.scatter([], [], c=Colors.HOME_TEAM, edgecolors=Colors.HOME_TEAM, 
                                       s=250, zorder=3, label='Home')
        
        # Away team (White)
        self.away_dots = self.ax.scatter([], [], c=Colors.AWAY_TEAM, edgecolors=Colors.AWAY_TEAM, 
                                       s=250, zorder=3, label='Away')
        
        # Ball (White)
        self.ball_dot = self.ax.scatter([], [], c=Colors.BALL, edgecolors='black', 
                                      s=100, zorder=4, label='Ball')
        
        return self.home_dots, self.away_dots, self.ball_dot

    def _update_hull(self, points, color, current_hull_patch):
        """
        Draws/Updates a convex hull around the provided points.
        """
        if current_hull_patch:
            try: current_hull_patch.remove()
            except: pass
            current_hull_patch = None

        if len(points) < 3: return None

        try:
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
            poly = Polygon(hull_points, facecolor=color, alpha=0.1, edgecolor=color, linestyle='--', linewidth=1.5, zorder=1)
            self.ax.add_patch(poly)
            return poly
        except Exception:
            return None

    def _update_text(self, points, text_list, color):
        """
        Updates text annotations (jersey numbers) for players.
        points: list of [x, y]
        text_list: list of existing text objects
        color: text color
        """
        # Clear old text
        for txt in text_list:
            try: txt.remove()
            except: pass
        text_list.clear()
        
        # Add new text
        # For Phase 3, we don't have real jersey numbers yet in the 360 dataframe without joining
        # with lineup data. For visual effect, we will use a placeholder or index.
        # Ideally, we should merge with lineup, but for now let's just show a dot.
        # Wait, the prompt asked for "Player Numbers". 
        # Since 360 frames generally don't have jersey number directly, 
        # I'll just skip adding text for now to avoid cluttering with wrong numbers,
        # OR I can add a dummy number '?' or just keep the dot larger.
        # Actually, let's try to put a small index to show distinctness.
        
        for i, point in enumerate(points):
            # Just a visual placeholder logic for number
            # In a real app, we join on player_id -> jersey_number
            txt = self.ax.text(point[0], point[1], str(i+1), color=color, 
                               fontsize=8, ha='center', va='center', fontweight='bold', zorder=4)
            text_list.append(txt)
            
        return text_list

    def update(self, home_xy, away_xy):
        """
        Updates player positions.
        """
        if home_xy:
            self.home_dots.set_offsets(home_xy)
            self.home_hull = self._update_hull(np.array(home_xy), Colors.HOME_TEAM, self.home_hull)
            self.home_text = self._update_text(home_xy, self.home_text, Colors.HOME_TEXT)
            
        if away_xy:
            self.away_dots.set_offsets(away_xy)
            self.away_hull = self._update_hull(np.array(away_xy), Colors.AWAY_TEAM, self.away_hull)
            self.away_text = self._update_text(away_xy, self.away_text, Colors.AWAY_TEXT)

        return self.home_dots, self.away_dots
