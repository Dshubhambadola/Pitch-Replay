import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.theme import Colors

def draw_pitch(ax, pitch_color=Colors.PITCH_COLOR, line_color=Colors.LINE_COLOR):
    """
    Draws a 120x80 football pitch on the given matplotlib axis.
    Args:
        ax: Matplotlib axes object
        pitch_color: Hex color for background
        line_color: Hex color for lines
    """
    # 0. Background
    ax.set_facecolor(pitch_color)
    
    # 1. Outline and Center Line
    ax.plot([0, 0], [0, 80], color=line_color, lw=2)      # Left
    ax.plot([120, 120], [0, 80], color=line_color, lw=2)  # Right
    ax.plot([0, 120], [0, 0], color=line_color, lw=2)     # Bottom
    ax.plot([0, 120], [80, 80], color=line_color, lw=2)   # Top
    ax.plot([60, 60], [0, 80], color=line_color, lw=2)    # Center Line
    
    # 2. Center Circle
    center_circle = plt.Circle((60, 40), 10, color=line_color, fill=False, lw=2)
    ax.add_patch(center_circle)
    center_spot = plt.Circle((60, 40), 0.8, color=line_color)
    ax.add_patch(center_spot)
    
    # 3. Penalty Areas (18-yard box)
    # Left: [0, 18] x [18, 62] (width 44)
    ax.plot([18, 18], [18, 62], color=line_color, lw=2)
    ax.plot([0, 18],  [62, 62], color=line_color, lw=2)
    ax.plot([0, 18],  [18, 18], color=line_color, lw=2)
    
    # Right: [102, 120] x [18, 62]
    ax.plot([102, 102], [18, 62], color=line_color, lw=2)
    ax.plot([102, 120], [62, 62], color=line_color, lw=2)
    ax.plot([102, 120], [18, 18], color=line_color, lw=2)
    
    # 4. Goal Areas (6-yard box)
    # Left: [0, 6] x [30, 50] (width 20)
    ax.plot([6, 6], [30, 50], color=line_color, lw=2)
    ax.plot([0, 6], [50, 50], color=line_color, lw=2)
    ax.plot([0, 6], [30, 30], color=line_color, lw=2)
    
    # Right
    ax.plot([114, 114], [30, 50], color=line_color, lw=2)
    ax.plot([114, 120], [50, 50], color=line_color, lw=2)
    ax.plot([114, 120], [30, 30], color=line_color, lw=2)
    
    # 5. Goals (Optional, small box outside pitch)
    # Left Goal
    ax.plot([-3, 0], [36, 36], color=line_color, lw=2)
    ax.plot([-3, 0], [44, 44], color=line_color, lw=2)
    ax.plot([-3, -3], [36, 44], color=line_color, lw=2)
    
    # Right Goal
    ax.plot([120, 123], [36, 36], color=line_color, lw=2)
    ax.plot([120, 123], [44, 44], color=line_color, lw=2)
    ax.plot([123, 123], [36, 44], color=line_color, lw=2)
    
    # 6. Penalty Spots
    left_spot = plt.Circle((12, 40), 0.8, color=line_color)
    right_spot = plt.Circle((108, 40), 0.8, color=line_color)
    ax.add_patch(left_spot)
    ax.add_patch(right_spot)
    
    # 7. Arcs
    # Left Arc
    left_arc = patches.Arc((12, 40), 20, 20, theta1=308, theta2=52, color=line_color, lw=2)
    ax.add_patch(left_arc)
    # Right Arc
    right_arc = patches.Arc((108, 40), 20, 20, theta1=128, theta2=232, color=line_color, lw=2)
    ax.add_patch(right_arc)

    # Set limits and aspect
    ax.set_xlim(-5, 125)
    ax.set_ylim(-5, 85)
    ax.set_aspect('equal')
    ax.axis('off')
