from statsbombpy import sb
try:
    frames = sb.frames(match_id=3869151, fmt='dataframe')
    print("Columns:", frames.columns.tolist())
    print("First row:", frames.iloc[0])
except Exception as e:
    print(f"Error: {e}")
