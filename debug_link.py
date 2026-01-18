from statsbombpy import sb
import pandas as pd

try:
    match_id = 3869151
    print("Loading frames...")
    frames = sb.frames(match_id=match_id, fmt='dataframe')
    print("Loading events...")
    events = sb.events(match_id=match_id)
    
    print("\nFrames IDs (First 5):")
    print(frames['id'].unique()[:5])
    
    print("\nEvent IDs (First 5):")
    print(events['id'].head().tolist())
    
    # Check intersection
    frame_ids = set(frames['id'].unique())
    event_ids = set(events['id'])
    common = frame_ids.intersection(event_ids)
    
    print(f"\nUnique Frame IDs: {len(frame_ids)}")
    print(f"Unique Event IDs: {len(event_ids)}")
    print(f"Common IDs: {len(common)}")
    
    if len(common) > 0:
        print("CONFIRMED: Frames are linked to Events by 'id'.")
    else:
        print("WARNING: No ID overlap found.")

except Exception as e:
    print(f"Error: {e}")
