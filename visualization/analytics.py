import numpy as np
from scipy.stats import gaussian_kde
from utils.theme import Colors

class AnalyticsVisualizer:
    def __init__(self, ax):
        self.ax = ax
        self.defensive_lines = []
        self.show_analytics = False
        
    def toggle(self):
        self.show_analytics = not self.show_analytics
        if not self.show_analytics:
            self.clear()
            
    def clear(self):
        for artist in self.defensive_lines:
            try: 
                # Contours are collections
                if hasattr(artist, 'collections'):
                    for c in artist.collections:
                        c.remove()
                else:
                    artist.remove()
            except: pass
        self.defensive_lines = []
        
    def draw_defensive_line(self, home_xy, away_xy, attacking_team="Home"):
        """
        Draws a vertical line representing the last defender's position.
        """
        if not self.show_analytics: return
        self.clear()
        
        # Calculate Home Defensive Line (Deepest player)
        if home_xy:
            hx = [p[0] for p in home_xy]
            min_h = min(hx)
            line1 = self.ax.axvline(x=min_h, color=Colors.HOME_TEAM, linestyle='--', alpha=0.6)
            self.defensive_lines.append(line1)

        if away_xy:
            ax = [p[0] for p in away_xy]
            max_a = max(ax)
            line3 = self.ax.axvline(x=max_a, color=Colors.AWAY_TEAM, linestyle='--', alpha=0.6)
            self.defensive_lines.append(line3)

    def draw_heatmap(self, home_xy, away_xy):
        """Draws a KDE heatmap for team positioning."""
        if not self.show_analytics: return
        
        # Grid for KDE
        x_grid, y_grid = np.mgrid[0:120:30j, 0:80:20j]
        positions = np.vstack([x_grid.ravel(), y_grid.ravel()])
        
        # Home Heatmap
        if len(home_xy) > 2:
            try:
                values = np.array(home_xy).T
                kernel = gaussian_kde(values)
                z = np.reshape(kernel(positions).T, x_grid.shape)
                c1 = self.ax.contourf(x_grid, y_grid, z, levels=5, cmap='Reds', alpha=0.4, zorder=1)
                self.defensive_lines.append(c1)
            except: pass

        # Away Heatmap
        if len(away_xy) > 2:
            try:
                values = np.array(away_xy).T
                kernel = gaussian_kde(values)
                z = np.reshape(kernel(positions).T, x_grid.shape)
                c2 = self.ax.contourf(x_grid, y_grid, z, levels=5, cmap='Blues', alpha=0.4, zorder=1)
                self.defensive_lines.append(c2)
            except: pass
            
    def draw_pass_network(self, home_xy, away_xy):
        """Draws a visual network connecting teammates (mocking pass links)."""
        if not self.show_analytics: return
        
        # Home Network
        self._draw_network_links(home_xy, Colors.HOME_TEAM)
        # Away Network
        self._draw_network_links(away_xy, Colors.AWAY_TEAM)

    def _draw_network_links(self, positions, color):
        import matplotlib.patches as patches
        if not positions: return
        
        pts = np.array(positions)
        from scipy.spatial.distance import pdist, squareform
        dists = squareform(pdist(pts))
        
        rows, cols = np.where((dists > 0) & (dists < 25))
        seen = set()
        
        for r, c in zip(rows, cols):
            if r >= c: continue
            if (r, c) in seen: continue
            seen.add((r, c))
            
            p1 = pts[r]
            p2 = pts[c]
            
            # Bezier curve for visual flair
            path = patches.Path(
                [p1, (p1+p2)/2 + [2,2], p2], 
                [patches.Path.MOVETO, patches.Path.CURVE3, patches.Path.CURVE3]
            )
            patch = patches.PathPatch(path, facecolor='none', edgecolor=color, alpha=0.15, linewidth=1, zorder=1)
            self.ax.add_patch(patch)
            self.defensive_lines.append(patch)
