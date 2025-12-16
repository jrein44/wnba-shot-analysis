"""
Generate improved shot charts with cleaner court rendering.
Uses precise WNBA dimensions and better visual styling.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import Circle, Arc
import sys

def draw_clean_court(ax, color='black', lw=1.5):
    """
    Draw a clean, professional basketball court.
    Based on official WNBA dimensions.
    """
    # Court dimensions (in feet, matching stats.wnba.com coordinates /10)
    # API uses tenths of feet, so divide by 10 for actual feet
    
    # Outer boundary
    ax.plot([-25, 25, 25, -25, -25], [0, 0, 47, 47, 0], 
            color=color, linewidth=lw, zorder=1)
    
    # Paint/key (16 feet wide, 19 feet long)
    ax.plot([-8, 8], [0, 0], color=color, linewidth=lw, zorder=1)
    ax.plot([-8, -8], [0, 19], color=color, linewidth=lw, zorder=1)
    ax.plot([8, 8], [0, 19], color=color, linewidth=lw, zorder=1)
    ax.plot([-8, 8], [19, 19], color=color, linewidth=lw, zorder=1)
    
    # Free throw circle (12 ft diameter = 6 ft radius)
    # Top half solid
    theta_top = np.linspace(0, np.pi, 50)
    x_top = 6 * np.cos(theta_top)
    y_top = 19 + 6 * np.sin(theta_top)
    ax.plot(x_top, y_top, color=color, linewidth=lw, zorder=1)
    
    # Bottom half dashed
    theta_bottom = np.linspace(np.pi, 2*np.pi, 50)
    x_bottom = 6 * np.cos(theta_bottom)
    y_bottom = 19 + 6 * np.sin(theta_bottom)
    ax.plot(x_bottom, y_bottom, color=color, linewidth=lw, 
            linestyle='--', dashes=(3, 3), zorder=1)
    
    # Hoop (0.75 ft radius, center at y = 5.25)
    hoop_center_y = 5.25  # 4 ft backboard + 0.5 ft neck + 0.75 ft radius
    hoop = Circle((0, hoop_center_y), 0.75, fill=False, 
                  color=color, linewidth=lw, zorder=1)
    ax.add_patch(hoop)
    
    # Backboard (6 ft wide at y = 4)
    ax.plot([-3, 3], [4, 4], color=color, linewidth=lw+0.5, zorder=1)
    
    # Restricted area (4 ft radius semicircle)
    restricted = Arc((0, hoop_center_y), 8, 8, theta1=0, theta2=180,
                     color=color, linewidth=lw, zorder=1)
    ax.add_patch(restricted)
    
    # Three-point line
    # WNBA uses FIBA distance (adopted in 2013)
    # 22 feet 1.75 inches (22.146 ft) at the arc
    # ~21 feet 8 inches (~21.65 ft) in the corners
    
    three_radius = 22.146  # Distance from hoop center to top of arc (6.75m)
    
    # In WNBA/FIBA, the three-point line is 3 feet from the sideline
    # Court is 50 ft wide, so sideline is at x = ±25
    # Three-point line is 3 ft from sideline: x = ±22
    corner_distance = 22
    
    # Calculate where the arc reaches x = ±22 (this gives us the y-coordinate)
    # Using circle equation: x² + (y - hoop_center_y)² = r²
    corner_y = hoop_center_y + np.sqrt(three_radius**2 - corner_distance**2)
    
    # Corner three lines (from baseline to where arc naturally intersects)
    ax.plot([-corner_distance, -corner_distance], [0, corner_y], 
            color=color, linewidth=lw, zorder=1)
    ax.plot([corner_distance, corner_distance], [0, corner_y], 
            color=color, linewidth=lw, zorder=1)
    
    # Three-point arc - only draw where |x| <= 22
    # This ensures smooth connection to corner lines
    theta_start = np.arcsin((corner_y - hoop_center_y) / three_radius)
    theta_arc = np.linspace(theta_start, np.pi - theta_start, 150)
    x_arc = three_radius * np.cos(theta_arc)
    y_arc = hoop_center_y + three_radius * np.sin(theta_arc)
    ax.plot(x_arc, y_arc, color=color, linewidth=lw, zorder=1)
    
    # Styling
    ax.set_xlim(-27, 27)
    ax.set_ylim(-2, 49)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#f5f5f5')  # Light gray background
    

def create_clean_shot_chart(csv_path, player_name, output_path):
    """Generate a clean, professional shot chart."""
    
    # Load data
    df = pd.read_csv(csv_path)
    
    # Calculate stats
    total = len(df)
    made = df[df['SHOT_MADE_FLAG'] == 1]
    missed = df[df['SHOT_MADE_FLAG'] == 0]
    fg_pct = (len(made) / total * 100) if total > 0 else 0
    
    two_pt = df[df['SHOT_TYPE'] == '2PT Field Goal']
    three_pt = df[df['SHOT_TYPE'] == '3PT Field Goal']
    two_pct = (two_pt['SHOT_MADE_FLAG'].sum() / len(two_pt) * 100) if len(two_pt) > 0 else 0
    three_pct = (three_pt['SHOT_MADE_FLAG'].sum() / len(three_pt) * 100) if len(three_pt) > 0 else 0
    
    # Create figure with white background
    fig, ax = plt.subplots(figsize=(12, 11), facecolor='white')
    
    # Draw court
    draw_clean_court(ax, color='#333333', lw=1.5)
    
    # Convert API coordinates (tenths of feet) to feet
    made_x = made['LOC_X'] / 10
    made_y = made['LOC_Y'] / 10
    missed_x = missed['LOC_X'] / 10
    missed_y = missed['LOC_Y'] / 10
    
    # Plot shots - misses first (underneath)
    ax.scatter(missed_x, missed_y, 
               c='#E74C3C', marker='x', s=60, linewidths=2, 
               alpha=0.5, label='Miss', zorder=2)
    
    ax.scatter(made_x, made_y, 
               c='#27AE60', marker='o', s=60, 
               edgecolors='#1E8449', linewidth=0.8,
               alpha=0.7, label='Make', zorder=3)
    
    # Title with stats
    title = f'{player_name} - 2025 Season Shot Chart'
    subtitle = f'{total} shots | {fg_pct:.1f}% FG | {two_pct:.1f}% 2PT | {three_pct:.1f}% 3PT'
    
    ax.text(0, 51, title, ha='center', va='bottom',
            fontsize=16, fontweight='bold', color='#2C3E50')
    ax.text(0, 48.5, subtitle, ha='center', va='top',
            fontsize=12, color='#34495E', style='italic')
    
    # Legend with cleaner styling
    legend = ax.legend(loc='upper right', frameon=True, 
                      fancybox=True, shadow=False,
                      fontsize=10, markerscale=1.5)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.9)
    legend.get_frame().set_edgecolor('#CCCCCC')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f'✓ Saved clean shot chart: {output_path}')
    plt.close()


if __name__ == '__main__':
    # Generate clean shot charts for all players
    players = [
        ('Sabrina Ionescu', 'data/raw/ionescu_shots_2025.csv', 
         'outputs/shot_charts/real/Ionescu_2025_CLEAN_shotchart.png'),
        ('Breanna Stewart', 'data/raw/stewart_shots_2025.csv',
         'outputs/shot_charts/real/Stewart_2025_CLEAN_shotchart.png'),
        ('Jonquel Jones', 'data/raw/jones_shots_2025.csv',
         'outputs/shot_charts/real/Jones_2025_CLEAN_shotchart.png'),
        ('Natasha Cloud', 'data/raw/nc_shots_2025.csv',
         'outputs/shot_charts/real/Cloud_2025_CLEAN_shotchart.png'),
        ('Leonie Fiebich', 'data/raw/lf_shots_2025.csv',
         'outputs/shot_charts/real/Fiebich_2025_CLEAN_shotchart.png'),
    ]
    
    for name, csv_path, output_path in players:
        create_clean_shot_chart(csv_path, name, output_path)
    
    print('\n✅ All clean shot charts generated!')
