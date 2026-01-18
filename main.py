#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

from visualization.pitch import draw_pitch
from visualization.players import PlayerVisualizer
from data.loader import DataLoader
from data.preprocessor import DataPreprocessor
from utils.theme import Colors
from utils.config import FPS

# Global control variables
is_paused = False
current_frame = 0
anim = None

from visualization.events import EventVisualizer

# ... imports ...

def main():
    # ... setup ...
    print("Initializing Football Race Replay...")
    
    # [Data Loading Omitted for brevity, logic stays same]
    # Re-implementing the data loading part to ensure we strictly follow previous flow
    matches = DataLoader.get_public_matches()
    if matches.empty: return
    match = matches[matches['home_team'] == 'Argentina'].iloc[0]
    match_id = match['match_id']
    print(f"Match: {match['home_team']} vs {match['away_team']}")

    frames = DataLoader.get_match_360_frames(match_id)
    if frames is None: return

    events = DataLoader.get_match_events(match_id)
    events = DataPreprocessor.process_events(events)
    # Ensure raw events have 'pass_outcome' and 'shot_statsbomb_xg' if we want them
    # The preprocessor currently filters columns. We might need to check that.
    
    # 2. Setup Visualization
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(Colors.BACKGROUND)
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
    ax.set_facecolor(Colors.BACKGROUND)
    
    draw_pitch(ax=ax)
    
    player_viz = PlayerVisualizer(ax)
    player_viz.init_players()
    
    event_viz = EventVisualizer(ax) # Initialize Event Viz
    
    title_text = ax.text(60, 82, f"{match['home_team']} vs {match['away_team']}", 
                         ha='center', va='center', fontsize=20, color=Colors.TEXT_COLOR)

    # 3. Animation Loop
    print("Processing tracking data...")
    grouped_frames = [group for _, group in frames.groupby('id', sort=False)]
    total_frames = len(grouped_frames)
    
    # Create a lookup for events by ID to avoid O(N) search every frame
    # events index might not be 'id'. Let's set it.
    events_lookup = events.set_index('id')

    def update(frame_idx):
        global current_frame
        if is_paused:
            return
            
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
        # The 'id' of the frame corresponds to the event_id
        # All rows in frame_data share the same 'id', so take the first one
        event_id = frame_data.iloc[0]['id']
        
        if event_id in events_lookup.index:
            event_row = events_lookup.loc[event_id]
            # Handle duplicate indices if any (unlikely for UUID)
            if isinstance(event_row, pd.DataFrame):
                event_row = event_row.iloc[0]
                
            event_viz.draw_event(event_row)
            
            # Update Title with Event Type
            title_text.set_text(f"{match['home_team']} vs {match['away_team']} - {event_row['type']} ({event_row['minute']}:{event_row['second']:02d})")
        else:
            event_viz.clear()
            title_text.set_text(f"{match['home_team']} vs {match['away_team']}")

        return player_viz.home_dots, player_viz.away_dots

    global anim
    anim = FuncAnimation(fig, update, frames=range(total_frames), 
                         interval=1000/FPS, blit=False, repeat=False)

    # Controls
    def on_key(event):
        global is_paused
        if event.key == ' ':
            is_paused = not is_paused

    fig.canvas.mpl_connect('key_press_event', on_key)

    print("Starting animation...")
    plt.show()

if __name__ == "__main__":
    main()
