"""
Create shot chart visualizations on basketball court diagrams.

This module generates publication-quality shot charts with court overlays,
heat maps, and comparative analysis visualizations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, Rectangle, Arc, Polygon
import os


class BasketballCourt:
    """Draw a basketball court on a matplotlib figure."""
    
    def __init__(self, ax=None, color='black', lw=2):
        """
        Initialize court drawer.
        
        Args:
            ax: Matplotlib axes object
            color: Line color for court
            lw: Line width
        """
        if ax is None:
            ax = plt.gca()
        self.ax = ax
        self.color = color
        self.lw = lw
        
    def draw(self, half_court=True):
        """
        Draw the basketball court with proper NBA/WNBA dimensions.
        Based on official court specifications.
        
        Args:
            half_court: If True, only draw half court
        """
        # Court dimensions (in feet)
        width = 50
        height = 47
        key_height = 19
        inner_key_width = 12
        outer_key_width = 16
        backboard_width = 6
        backboard_offset = 4
        neck_length = 0.5
        hoop_radius = 0.75
        hoop_center_y = backboard_offset + neck_length + hoop_radius
        three_point_radius = 23.75
        three_point_side_radius = 22
        three_point_side_height = 14
        
        # Outer perimeter
        if half_court:
            self.ax.plot([width/2, width/2, -width/2, -width/2, width/2],
                        [0, height, height, 0, 0],
                        color=self.color, linewidth=self.lw)
        
        # Paint (the key)
        self.ax.plot([outer_key_width/2, outer_key_width/2, -outer_key_width/2, -outer_key_width/2],
                    [0, key_height, key_height, 0],
                    color=self.color, linewidth=self.lw)
        
        # Free throw circle (top arc solid, bottom dashed)
        ft_circle = Circle((0, key_height), radius=inner_key_width/2, 
                          linewidth=self.lw, color=self.color, fill=False)
        self.ax.add_patch(ft_circle)
        
        # Bottom arc of free throw circle (dashed)
        theta_bottom = np.linspace(-np.pi, 0, 50)
        x_bottom = (inner_key_width/2) * np.cos(theta_bottom)
        y_bottom = key_height + (inner_key_width/2) * np.sin(theta_bottom)
        self.ax.plot(x_bottom, y_bottom, color=self.color, linewidth=self.lw, 
                    linestyle='--', dashes=(5, 5))
        
        # Hoop
        hoop = Circle((0, hoop_center_y), radius=hoop_radius, 
                     linewidth=self.lw, color=self.color, fill=False)
        self.ax.add_patch(hoop)
        
        # Backboard
        self.ax.plot([-backboard_width/2, backboard_width/2], 
                    [backboard_offset, backboard_offset],
                    color=self.color, linewidth=self.lw+1)
        
        # Restricted area arc
        restricted = Arc((0, hoop_center_y), 8, 8, theta1=0, theta2=180,
                        linewidth=self.lw, color=self.color)
        self.ax.add_patch(restricted)
        
        # Three point line - side lines
        self.ax.plot([three_point_side_radius, three_point_side_radius], 
                    [0, three_point_side_height],
                    color=self.color, linewidth=self.lw)
        self.ax.plot([-three_point_side_radius, -three_point_side_radius], 
                    [0, three_point_side_height],
                    color=self.color, linewidth=self.lw)
        
        # Three point arc
        # Calculate where arc should start (at y = three_point_side_height)
        # Using circle equation: y = hoop_center_y + sqrt(r^2 - x^2)
        # Solve for theta when y = three_point_side_height
        y_diff = three_point_side_height - hoop_center_y
        if y_diff < three_point_radius:
            theta_start = np.arcsin(y_diff / three_point_radius)
            theta_arc = np.linspace(theta_start, np.pi - theta_start, 100)
            x_arc = three_point_radius * np.cos(theta_arc)
            y_arc = hoop_center_y + three_point_radius * np.sin(theta_arc)
            self.ax.plot(x_arc, y_arc, color=self.color, linewidth=self.lw)
        
        # Set axis limits
        self.ax.set_xlim(-27, 27)
        self.ax.set_ylim(-2, 50)
        
        # Remove axis ticks and set aspect
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('white')


class ShotChartVisualizer:
    """Create shot chart visualizations."""
    
    def __init__(self, output_dir: str = 'outputs/shot_charts'):
        """
        Initialize visualizer.
        
        Args:
            output_dir: Directory to save output images
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("white")
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.size'] = 10
        
    def plot_shot_chart(self, shot_data: pd.DataFrame, player_name: str,
                       save: bool = True):
        """
        Create a shot chart for a player.
        
        Args:
            shot_data: DataFrame with shot locations
            player_name: Player name for title
            save: Whether to save the figure
        """
        fig, ax = plt.subplots(figsize=(12, 11))
        
        # Draw court
        court = BasketballCourt(ax)
        court.draw()
        
        # Plot shots
        made_shots = shot_data[shot_data['shot_made'] == 1]
        missed_shots = shot_data[shot_data['shot_made'] == 0]
        
        # Plot misses first (so makes are on top)
        ax.scatter(missed_shots['loc_x'], missed_shots['loc_y'],
                  c='#d62728', marker='x', s=80, linewidths=2, 
                  alpha=0.6, label='Miss')
        
        ax.scatter(made_shots['loc_x'], made_shots['loc_y'],
                  c='#2ca02c', marker='o', s=80, linewidths=1.5,
                  edgecolors='darkgreen', alpha=0.7, label='Make')
        
        # Add statistics
        total_shots = len(shot_data)
        makes = shot_data['shot_made'].sum()
        fg_pct = makes / total_shots * 100
        
        two_pt = shot_data[shot_data['shot_type'] == '2PT']
        three_pt = shot_data[shot_data['shot_type'] == '3PT']
        two_pt_pct = two_pt['shot_made'].mean() * 100 if len(two_pt) > 0 else 0
        three_pt_pct = three_pt['shot_made'].mean() * 100 if len(three_pt) > 0 else 0
        
        # Title and stats
        plt.title(f'{player_name} - Shot Chart', 
                 fontsize=18, fontweight='bold', pad=20)
        
        stats_text = (f'FG: {makes}/{total_shots} ({fg_pct:.1f}%)\n'
                     f'2PT: {two_pt_pct:.1f}% | 3PT: {three_pt_pct:.1f}%')
        
        ax.text(0, 52, stats_text, ha='center', fontsize=12,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.legend(loc='upper right', fontsize=11)
        
        plt.tight_layout()
        
        if save:
            filename = f"{player_name.replace(' ', '_')}_shot_chart.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight', 
                       facecolor='white')
            print(f"✓ Saved shot chart: {filepath}")
        
        return fig, ax
    
    def plot_heat_map(self, shot_data: pd.DataFrame, player_name: str,
                     grid_size: int = 3, save: bool = True):
        """
        Create a heat map showing shooting efficiency by location.
        
        Args:
            shot_data: DataFrame with shot locations
            player_name: Player name for title
            grid_size: Size of grid cells in feet
            save: Whether to save the figure
        """
        fig, ax = plt.subplots(figsize=(12, 11))
        
        # Create grid
        x_bins = np.arange(-25, 26, grid_size)
        y_bins = np.arange(0, 48, grid_size)
        
        # Calculate efficiency in each cell
        efficiency_grid = np.zeros((len(y_bins)-1, len(x_bins)-1))
        shot_counts = np.zeros((len(y_bins)-1, len(x_bins)-1))
        
        for _, shot in shot_data.iterrows():
            x_idx = np.digitize(shot['loc_x'], x_bins) - 1
            y_idx = np.digitize(shot['loc_y'], y_bins) - 1
            
            if 0 <= x_idx < len(x_bins)-1 and 0 <= y_idx < len(y_bins)-1:
                efficiency_grid[y_idx, x_idx] += shot['shot_made']
                shot_counts[y_idx, x_idx] += 1
        
        # Calculate percentages
        mask = shot_counts > 2  # Only show cells with 3+ shots
        efficiency_pct = np.zeros_like(efficiency_grid)
        efficiency_pct[mask] = efficiency_grid[mask] / shot_counts[mask] * 100
        efficiency_pct[~mask] = np.nan
        
        # Draw court first
        court = BasketballCourt(ax)
        court.draw()
        
        # Overlay heat map
        im = ax.imshow(efficiency_pct, extent=[-25, 25, 0, 47],
                      origin='lower', cmap='RdYlGn', alpha=0.7,
                      vmin=0, vmax=70, aspect='auto', zorder=1)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Field Goal %', rotation=270, labelpad=20)
        
        # Title
        plt.title(f'{player_name} - Shooting Heat Map',
                 fontsize=18, fontweight='bold', pad=20)
        
        # Add note
        ax.text(0, 52, 'Heat map shows FG% in areas with 3+ shot attempts',
               ha='center', fontsize=10, style='italic')
        
        plt.tight_layout()
        
        if save:
            filename = f"{player_name.replace(' ', '_')}_heat_map.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight',
                       facecolor='white')
            print(f"✓ Saved heat map: {filepath}")
        
        return fig, ax
    
    def plot_zone_comparison(self, player_stats: pd.DataFrame, player_name: str,
                           save: bool = True):
        """
        Create bar chart comparing player efficiency to league average by zone.
        
        Args:
            player_stats: DataFrame with zone-level comparison
            player_name: Player name for title
            save: Whether to save the figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data
        zones = player_stats['shot_zone'].values
        player_fg = player_stats['fg_pct_player'].values * 100
        league_fg = player_stats['fg_pct_league'].values * 100
        
        x = np.arange(len(zones))
        width = 0.35
        
        # Create bars
        bars1 = ax.bar(x - width/2, player_fg, width, label=player_name,
                      color='#1f77b4', alpha=0.8)
        bars2 = ax.bar(x + width/2, league_fg, width, label='League Average',
                      color='#ff7f0e', alpha=0.8)
        
        # Customize
        ax.set_xlabel('Shot Zone', fontsize=12, fontweight='bold')
        ax.set_ylabel('Field Goal %', fontsize=12, fontweight='bold')
        ax.set_title(f'{player_name} vs League Average by Zone',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(zones, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%',
                       ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        if save:
            filename = f"{player_name.replace(' ', '_')}_zone_comparison.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved zone comparison: {filepath}")
        
        return fig, ax


def main():
    """Generate all visualizations."""
    from processor import ShotDataProcessor
    
    print("Generating shot chart visualizations...")
    
    # Initialize processor and visualizer
    processor = ShotDataProcessor(
        liberty_file='data/raw/liberty_shots_2024.csv',
        league_file='data/raw/league_average_shots.csv'
    )
    viz = ShotChartVisualizer()
    
    # Generate charts for each player
    players = processor.liberty_data['player_name'].unique()
    
    for player in players:
        print(f"\nGenerating charts for {player}...")
        
        # Get player data
        shot_data = processor.get_shot_chart_data(player)
        
        # Shot chart
        viz.plot_shot_chart(shot_data, player)
        
        # Heat map
        viz.plot_heat_map(shot_data, player)
        
        # Zone comparison
        comparison = processor.compare_to_league_average(player)
        viz.plot_zone_comparison(comparison, player)
    
    print("\n✓ All visualizations complete!")
    print(f"Charts saved to: {viz.output_dir}")


if __name__ == '__main__':
    main()
