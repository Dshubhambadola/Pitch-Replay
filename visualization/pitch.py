from mplsoccer import Pitch
import matplotlib.pyplot as plt
from utils.theme import Colors

def draw_pitch(ax=None):
    """
    Draws a football pitch using mplsoccer with the project's dark theme.
    """
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color=Colors.PITCH_COLOR,
        line_color=Colors.LINE_COLOR,
        goal_type='box',
        linewidth=1.5
    )
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(16, 10))
        fig.set_facecolor(Colors.BACKGROUND)
    
    pitch.draw(ax=ax)
    return pitch, ax
