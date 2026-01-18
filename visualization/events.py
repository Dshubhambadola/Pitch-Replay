from utils.theme import Colors
import matplotlib.patches as patches

class EventVisualizer:
    def __init__(self, ax):
        self.ax = ax
        self.current_overlays = []

    def clear(self):
        """Remove all current overlays."""
        for artist in self.current_overlays:
            try:
                artist.remove()
            except:
                pass
        self.current_overlays = []

    def draw_event(self, event_row):
        """
        Draws the visualization for a specific event.
        """
        self.clear()
        
        event_type = event_row['type']
        
        if event_type == 'Pass':
            self._draw_pass(event_row)
        elif event_type == 'Shot':
            self._draw_shot(event_row)
            
    def _draw_pass(self, event):
        """Draws a pass arrow."""
        start = event['location']
        end = event['pass_end_location']
        
        if not isinstance(start, (list, tuple)) or not isinstance(end, (list, tuple)):
            return

        # Determine color based on outcome (not strictly available in reduced columns yet, 
        # but let's assume Teal for now or check if we have 'pass_outcome')
        # Ideally we check event['pass_outcome'].NaN means complete.
        
        color = Colors.HIGHLIGHT # Cyan
        if 'pass_outcome' in event and isinstance(event['pass_outcome'], str):
             # Failures in Red
             color = Colors.ACCENT_RED
             
        arrow = patches.FancyArrowPatch(
            (start[0], start[1]), 
            (end[0], end[1]),
            arrowstyle='-|>',
            mutation_scale=20,
            color=color,
            linewidth=2,
            zorder=2,
            alpha=0.8
        )
        
        self.ax.add_patch(arrow)
        self.current_overlays.append(arrow)

    def _draw_shot(self, event):
        """Draws a shot marker (Star or Circle)."""
        loc = event['location']
        if not isinstance(loc, (list, tuple)):
            return
            
        # Draw a "Goal" text or just a marker
        # Using a star for shots
        marker = self.ax.scatter(
            loc[0], loc[1],
            s=300,
            marker='*',
            color=Colors.HIGHLIGHT,
            edgecolors='white',
            linewidth=2,
            zorder=5 # On top of everything
        )
        self.current_overlays.append(marker)
        
        # Add xG text if available (mock logic for now if column missing)
        xg = 0.0
        if 'shot_statsbomb_xg' in event:
             xg = event['shot_statsbomb_xg']
             
        text = self.ax.text(
            loc[0], loc[1] + 2,
            f"Shot\nxG: {xg:.2f}",
            color='white',
            fontsize=10,
            ha='center',
            bbox=dict(facecolor='black', alpha=0.7, edgecolor=Colors.BORDER)
        )
        self.current_overlays.append(text)
