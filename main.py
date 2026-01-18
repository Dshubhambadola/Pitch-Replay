#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

# Original Viz
from visualization.pitch import draw_pitch
from visualization.players import PlayerVisualizer
from visualization.events import EventVisualizer
from visualization.analytics import AnalyticsVisualizer
from data.loader import DataLoader
from data.preprocessor import DataPreprocessor
from utils.theme import Colors
from utils.config import FPS

# New Screens
from screens.manager import ScreenManager
from screens.dashboard import DashboardScreen
from screens.tactics import TacticsScreen

# Global State
is_paused = False
current_frame = 0

def main():
    print("Initializing Stratos Analytics Pro...")
    
    # [Data Loading - Keep existing]
    matches = DataLoader.get_public_matches()
    match = matches[matches['home_team'] == 'Argentina'].iloc[0] if not matches.empty else None
    if match is None: return
    match_id = match['match_id']
    frames = DataLoader.get_match_360_frames(match_id)
    if frames is None: return
    events = DataLoader.get_match_events(match_id)
    events = DataPreprocessor.process_events(events)

    # Setup Figure
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(Colors.BACKGROUND)
    
    # 1. Initialize Screen Manager & Sidebar
    screen_manager = ScreenManager(fig)
    screen_manager.setup_sidebar()
    
    # 2. Initialize Screens
    dashboard_screen = DashboardScreen(fig)
    tactics_screen = TacticsScreen(fig)
    
    # 3. Initialize Match View (The "Live" canvas)
    # This was the old "main ax". We create it but manage its visibility manually via hiding/showing
    # For simplicity, we keep the Axes ALIVE but clear/redraw or overlay on top.
    # Actually, proper way: Main Match View uses specific axes.
    
    # Match View Axes
    ax_match = fig.add_axes([0.1, 0.05, 0.85, 0.9])
    ax_match.set_facecolor(Colors.PITCH_COLOR)
    draw_pitch(ax=ax_match, line_color=Colors.LINE_COLOR, pitch_color=Colors.PITCH_COLOR)
    
    # Visualizers for Match
    player_viz = PlayerVisualizer(ax_match)
    player_viz.init_players()
    event_viz = EventVisualizer(ax_match)
    analytics_viz = AnalyticsVisualizer(ax_match)
    
    # Group Frames
    grouped_frames = [group for _, group in frames.groupby('id', sort=False)]
    total_frames = len(grouped_frames)
    events_lookup = events.set_index('id')

    # --- Screen Switching Logic ---
    def update_screen_visibility():
        curr = screen_manager.current_screen
        
        # 1. Dashboard
        if curr == 'DASHBOARD':
            ax_match.set_visible(False)
            dashboard_screen.show()
            tactics_screen.hide()
        
        # 2. Tactics
        elif curr == 'TACTICS':
            ax_match.set_visible(False)
            dashboard_screen.hide()
            tactics_screen.show()
            
        # 3. Match
        elif curr == 'MATCH':
            dashboard_screen.hide()
            tactics_screen.hide()
            ax_match.set_visible(True)
            
        fig.canvas.draw_idle()

    # Initial State
    update_screen_visibility()

    # --- Interaction Handlers ---
    def on_click_global(event):
        # 1. Check Sidebar
        new_screen = screen_manager.handle_click(event)
        if new_screen:
            screen_manager.switch_to(new_screen)
            update_screen_visibility()
            return

        # 2. If Match Screen Active -> Player Click
        if screen_manager.current_screen == 'MATCH' and event.inaxes == ax_match:
            # Handle player selection (Copied from previous logic)
            click_x, click_y = event.xdata, event.ydata
            if current_frame < len(grouped_frames):
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
                    print(f"Player {selected} clicked")
                    # In Stratos, we might show a popup or specific graphic. 
                    # For now, print to console.

    def on_key_global(event):
        global is_paused
        if event.key == ' ':
            is_paused = not is_paused
        elif event.key == 't':
            analytics_viz.toggle()

    fig.canvas.mpl_connect('button_press_event', on_click_global)
    fig.canvas.mpl_connect('key_press_event', on_key_global)

    # --- Animation Loop ---
    def update(frame_idx):
        global current_frame
        
        # Only update animation if on MATCH screen
        if screen_manager.current_screen != 'MATCH':
            return [] # Do nothing
            
        if is_paused: return []
        
        current_frame = frame_idx
        frame_data = grouped_frames[frame_idx]
        
        # 1. Update Players
        home_xy = []
        away_xy = []
        for _, row in frame_data.iterrows():
            loc = row['location']
            if row['teammate']: home_xy.append(loc)
            else: away_xy.append(loc)
            
        player_viz.update(home_xy, away_xy)
        
        # 2. Update Events
        event_id = frame_data.iloc[0]['id']
        if event_id in events_lookup.index:
            event_row = events_lookup.loc[event_id]
            if isinstance(event_row, pd.DataFrame): event_row = event_row.iloc[0]
            event_viz.draw_event(event_row)
        else:
            event_viz.clear()

        # 3. Analytics
        analytics_viz.draw_defensive_line(home_xy, away_xy)
        analytics_viz.draw_heatmap(home_xy, away_xy)
        analytics_viz.draw_pass_network(home_xy, away_xy)

        return player_viz.home_dots, player_viz.away_dots

    anim = FuncAnimation(fig, update, frames=range(total_frames), 
                         interval=1000/FPS, blit=False, repeat=False)
    
    print("Stratos Analytics Launched.")
    plt.show()

if __name__ == "__main__":
    main()
