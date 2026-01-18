import pandas as pd
import numpy as np
from utils.config import PITCH_LENGTH, PITCH_WIDTH

class DataPreprocessor:
    """
    Standardizes data coordinate systems and prepares for animation.
    StatsBomb coordinates: X (0-120), Y (0-80).
    Origin is top-left (0,0) -> (120, 80).
    """

    @staticmethod
    def process_events(events_df):
        """
        Clean and format event data.
        """
        if events_df is None or events_df.empty:
            return pd.DataFrame()

        # Filter for relevant columns
        cols = ['id', 'index', 'period', 'timestamp', 'minute', 'second', 
                'type', 'player', 'team', 'location', 'pass_end_location',
                'pass_outcome', 'shot_statsbomb_xg', 'shot_outcome']
        
        # Keep only existing columns
        events = events_df[[c for c in cols if c in events_df.columns]].copy()
        
        # Separate X, Y coordinates
        # Location is usually a list [x, y]
        events['x'] = events['location'].apply(lambda loc: loc[0] if isinstance(loc, (list, tuple)) else np.nan)
        events['y'] = events['location'].apply(lambda loc: loc[1] if isinstance(loc, (list, tuple)) else np.nan)
        
        return events

    @staticmethod
    def process_360_frames(frames_df):
        """
        Process 360 tracking frame data.
        Frames contain a list of 'freeze_frame' objects with player positions.
        """
        if frames_df is None or frames_df.empty:
            return None
            
        # 360 data needs to be flattened: one row per player per frame
        # This can be expensive, so we might return it raw or optimized later
        # For now, let's keep it as is and parse during animation loop for performance
        return frames_df
