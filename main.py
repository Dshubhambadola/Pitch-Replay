#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

from visualization.pitch import draw_pitch
from visualization.players import PlayerVisualizer
from visualization.events import EventVisualizer
from visualization.ui import UIManager
from visualization.analytics import AnalyticsVisualizer
from data.loader import DataLoader
from data.preprocessor import DataPreprocessor
from utils.theme import Colors
from utils.config import FPS

# Global control variables
is_paused = False
current_frame = 0
anim = None

def main():
    print("Initializing Football Race Replay...")
    
    # [Data Loading]
    matches = DataLoader.get_public_matches()
    if matches.empty: return
    match = matches[matches['home_team'] == 'Argentina'].iloc[0] # Keeping Argentina match for data
    match_id = match['match_id']
    
    frames = DataLoader.get_match_360_frames(match_id)
    if frames is None: return

    events = DataLoader.get_match_events(match_id)
    events = DataPreprocessor.process_events(events)
    
    # 2. Setup Visualization
    # Adust Figure Layout for Sidebar
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(Colors.BACKGROUND)
    
    # Create Sidebar UI
    ui_manager = UIManager(fig)
    ui_manager.setup_ui()
    
    # Main Pitch Area (shifted right to make room for sidebar)
    # [left, bottom, width, height]
    ax = fig.add_axes([0.28, 0.05, 0.7, 0.9])
    ax.set_facecolor(Colors.BACKGROUND)
    
    draw_pitch(ax=ax)
    
    # Init Visualizers
    player_viz = PlayerVisualizer(ax)
    player_viz.init_players()
    
    event_viz = EventVisualizer(ax)
    analytics_viz = AnalyticsVisualizer(ax)
    
    # Title
    title_text = ax.text(60, 82, f"{match['home_team']} (Red) vs {match['away_team']} (Blue)", 
                         ha='center', va='center', fontsize=20, color=Colors.TEXT_COLOR)

    # 3. Animation Loop
    grouped_frames = [group for _, group in frames.groupby('id', sort=False)]
    total_frames = len(grouped_frames)
    events_lookup = events.set_index('id')

    def update(frame_idx):
        global current_frame
        if is_paused: return
        current_frame = frame_idx
        frame_data = grouped_frames[frame_idx]
        
        # 1. Update Players
        home_xy = []
        away_xy = []
        for _, row in frame_data.iterrows():
            loc = row['location']
            is_teammate = row['teammate']
            if is_teammate: home_xy.append(loc)
            else: away_xy.append(loc)
            
        player_viz.update(home_xy, away_xy)
        
        # 2. Update Events
        event_id = frame_data.iloc[0]['id']
        if event_id in events_lookup.index:
            event_row = events_lookup.loc[event_id]
            if isinstance(event_row, pd.DataFrame): event_row = event_row.iloc[0]
            event_viz.draw_event(event_row)
            title_text.set_text(f"{match['home_team']} vs {match['away_team']} - {event_row['type']} ({event_row['minute']}:{event_row['second']:02d})")
        else:
            event_viz.clear()
            title_text.set_text(f"{match['home_team']} vs {match['away_team']}")

        # 3. Update Analytics
        analytics_viz.draw_defensive_line(home_xy, away_xy)
        analytics_viz.draw_heatmap(home_xy, away_xy)
        analytics_viz.draw_pass_network(home_xy, away_xy)

        return player_viz.home_dots, player_viz.away_dots

    global anim
    anim = FuncAnimation(fig, update, frames=range(total_frames), 
                         interval=1000/FPS, blit=False, repeat=False)

    # Controls
    def on_key(event):
        global is_paused
        if event.key == ' ':
            is_paused = not is_paused
        elif event.key == 't': # Toggle Analytics
            analytics_viz.toggle()
            print(f"Analytics: {analytics_viz.show_analytics}")

    def on_click(event):
        """Handle mouse clicks to select players."""
        if event.inaxes != ax: return # Only clicks on pitch
        
        click_x, click_y = event.xdata, event.ydata
        
        if current_frame >= len(grouped_frames): return
        
        frame_data = grouped_frames[current_frame]
        
        min_dist = 5.0 
        selected = None
        
        idx_counter = 1
        for _, row in frame_data.iterrows():
            px, py = row['location']
            dist = ((px - click_x)**2 + (py - click_y)**2)**0.5
            
            if dist < min_dist:
                min_dist = dist
                team = "Home" if row['teammate'] else "Away"
                selected = (team, idx_counter, (px, py))
            
            idx_counter += 1
            
        if selected:
            team, idx, loc = selected
            print(f"Clicked: {team} #{idx}")
            ui_manager.draw_player_card(team, idx, loc)

    fig.canvas.mpl_connect('key_press_event', on_key)
    fig.canvas.mpl_connect('button_press_event', on_click)

    print("Starting animation...")
    print("Press 'SPACE' to Pause/Play")
    print("Press 'T' to Toggle Analytics (Defensive Lines)")
    plt.show()

if __name__ == "__main__":
    main()
