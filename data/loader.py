from statsbombpy import sb
import pandas as pd
import warnings

# Suppress pandas warnings that sb might trigger
warnings.simplefilter(action='ignore', category=FutureWarning)

class DataLoader:
    """
    Handles loading match data from StatsBomb API.
    """
    
    @staticmethod
    def get_public_matches(competition_id=43, season_id=106):
        """
        Get list of available matches. 
        Default: World Cup 2022 (Comp ID 43, Season ID 106)
        """
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        return matches

    @staticmethod
    def get_match_events(match_id):
        """
        Fetch all events for a specific match.
        """
        print(f"Loading events for match {match_id}...")
        events = sb.events(match_id=match_id)
        return events

    @staticmethod
    def get_match_360_frames(match_id):
        """
        Fetch 360 frames (tracking data) for a match if available.
        Note: Only selected matches have 360 data.
        """
        try:
            # StatsBombPy uses sb.frames for 360 data
            frames = sb.frames(match_id=match_id, fmt="dataframe")
            return frames
        except Exception as e:
            print(f"360 data not available or error loading: {e}")
            return None
