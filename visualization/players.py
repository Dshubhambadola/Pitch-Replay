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
        self.home_hull = None
        self.away_hull = None
        
    def init_players(self):
        """Initializes the scatter plots for players."""
        # Home team (Neon Teal)
        self.home_dots = self.ax.scatter([], [], c=Colors.HOME_TEAM, edgecolors=Colors.BACKGROUND, 
                                       s=150, zorder=3, label='Home')
        
        # Away team (Hot Pink)
        self.away_dots = self.ax.scatter([], [], c=Colors.AWAY_TEAM, edgecolors=Colors.BACKGROUND, 
                                       s=150, zorder=3, label='Away')
        
        # Ball (White)
        self.ball_dot = self.ax.scatter([], [], c=Colors.BALL, edgecolors='black', 
                                      s=80, zorder=4, label='Ball')
        
        return self.home_dots, self.away_dots, self.ball_dot

    def _update_hull(self, points, color, current_hull_patch):
        """
        Draws/Updates a convex hull around the provided points.
        """
        # Remove old hull
        if current_hull_patch:
            try:
                current_hull_patch.remove()
            except:
                pass
            current_hull_patch = None

        if len(points) < 3:
            return None

        # Calculate Convex Hull
        try:
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
            
            # Draw Polygon
            poly = Polygon(hull_points, facecolor=color, alpha=0.1, edgecolor=color, linestyle='--', linewidth=1.5, zorder=1)
            self.ax.add_patch(poly)
            return poly
        except Exception:
            return None

    def update(self, home_xy, away_xy):
        """
        Updates player positions.
        """
        # Update dots
        if home_xy:
            self.home_dots.set_offsets(home_xy)
            # Update Home Hull
            self.home_hull = self._update_hull(np.array(home_xy), Colors.HOME_TEAM, self.home_hull)
            
        if away_xy:
            self.away_dots.set_offsets(away_xy)
            # Update Away Hull
            self.away_hull = self._update_hull(np.array(away_xy), Colors.AWAY_TEAM, self.away_hull)

        return self.home_dots, self.away_dots, self.ball_dot
