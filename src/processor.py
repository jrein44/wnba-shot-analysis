"""
Process and analyze WNBA shot data.

This module handles data cleaning, aggregation, and statistical analysis of shot data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import os


class ShotDataProcessor:
    """Process and analyze shot data for visualization and insights."""
    
    def __init__(self, liberty_file: str, league_file: str):
        """
        Initialize processor with data files.
        
        Args:
            liberty_file: Path to Liberty shots CSV
            league_file: Path to league average shots CSV
        """
        self.liberty_data = pd.read_csv(liberty_file)
        self.league_data = pd.read_csv(league_file)
        
    def calculate_shooting_efficiency_by_zone(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate FG% by shot zone.
        
        Args:
            df: Shot data DataFrame
            
        Returns:
            DataFrame with zone-level statistics
        """
        zone_stats = df.groupby('shot_zone').agg({
            'shot_made': ['sum', 'count', 'mean'],
            'shot_distance': 'mean'
        }).reset_index()
        
        zone_stats.columns = ['shot_zone', 'makes', 'attempts', 'fg_pct', 'avg_distance']
        zone_stats['fg_pct'] = zone_stats['fg_pct'].round(3)
        zone_stats = zone_stats.sort_values('attempts', ascending=False)
        
        return zone_stats
    
    def calculate_player_efficiency(self, player_name: str) -> Dict:
        """
        Calculate comprehensive shooting stats for a player.
        
        Args:
            player_name: Name of the player
            
        Returns:
            Dictionary with player statistics
        """
        player_data = self.liberty_data[self.liberty_data['player_name'] == player_name]
        
        if len(player_data) == 0:
            raise ValueError(f"Player {player_name} not found in dataset")
        
        # Overall stats
        total_shots = len(player_data)
        makes = player_data['shot_made'].sum()
        fg_pct = makes / total_shots
        
        # 2PT vs 3PT
        two_pt = player_data[player_data['shot_type'] == '2PT']
        three_pt = player_data[player_data['shot_type'] == '3PT']
        
        two_pt_pct = two_pt['shot_made'].mean() if len(two_pt) > 0 else 0
        three_pt_pct = three_pt['shot_made'].mean() if len(three_pt) > 0 else 0
        
        # Zone breakdown
        zone_stats = self.calculate_shooting_efficiency_by_zone(player_data)
        
        # Distance analysis
        avg_distance = player_data['shot_distance'].mean()
        
        return {
            'player_name': player_name,
            'total_attempts': total_shots,
            'total_makes': int(makes),
            'fg_pct': round(fg_pct, 3),
            'two_pt_pct': round(two_pt_pct, 3),
            'three_pt_pct': round(three_pt_pct, 3),
            'two_pt_attempts': len(two_pt),
            'three_pt_attempts': len(three_pt),
            'avg_shot_distance': round(avg_distance, 1),
            'zone_breakdown': zone_stats
        }
    
    def compare_to_league_average(self, player_name: str) -> pd.DataFrame:
        """
        Compare player's shooting to league averages by zone.
        
        Args:
            player_name: Name of the player
            
        Returns:
            DataFrame comparing player to league average
        """
        player_data = self.liberty_data[self.liberty_data['player_name'] == player_name]
        
        player_zones = self.calculate_shooting_efficiency_by_zone(player_data)
        league_zones = self.calculate_shooting_efficiency_by_zone(self.league_data)
        
        # Merge and calculate difference
        comparison = player_zones.merge(
            league_zones[['shot_zone', 'fg_pct', 'attempts']],
            on='shot_zone',
            how='outer',
            suffixes=('_player', '_league')
        )
        
        comparison['fg_pct_diff'] = (
            comparison['fg_pct_player'] - comparison['fg_pct_league']
        ).round(3)
        
        comparison['efficiency_vs_league'] = comparison['fg_pct_diff'].apply(
            lambda x: 'Above Average' if x > 0.02 else 
                     ('Below Average' if x < -0.02 else 'Average')
        )
        
        return comparison.sort_values('attempts_player', ascending=False)
    
    def get_shot_chart_data(self, player_name: str = None) -> pd.DataFrame:
        """
        Get shot location data formatted for visualization.
        
        Args:
            player_name: Optional player name to filter. If None, returns all Liberty shots.
            
        Returns:
            DataFrame with shot locations and outcomes
        """
        data = self.liberty_data.copy()
        
        if player_name:
            data = data[data['player_name'] == player_name]
        
        # Add color coding for made/missed
        data['outcome'] = data['shot_made'].map({1: 'Made', 0: 'Missed'})
        
        return data[['player_name', 'loc_x', 'loc_y', 'shot_distance', 
                     'shot_zone', 'shot_made', 'outcome', 'shot_type']]
    
    def generate_heat_map_data(self, player_name: str, grid_size: int = 10) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate heat map data for shooting efficiency across the court.
        
        Args:
            player_name: Name of the player
            grid_size: Size of grid cells (in feet)
            
        Returns:
            Tuple of (x_grid, y_grid, efficiency_grid)
        """
        player_data = self.liberty_data[self.liberty_data['player_name'] == player_name]
        
        # Create grid
        x_bins = np.arange(-25, 26, grid_size)
        y_bins = np.arange(0, 31, grid_size)
        
        # Digitize shot locations
        x_idx = np.digitize(player_data['loc_x'], x_bins)
        y_idx = np.digitize(player_data['loc_y'], y_bins)
        
        # Calculate efficiency for each grid cell
        efficiency_grid = np.zeros((len(y_bins), len(x_bins)))
        shot_counts = np.zeros((len(y_bins), len(x_bins)))
        
        for i in range(len(player_data)):
            xi = x_idx.iloc[i]
            yi = y_idx.iloc[i]
            made = player_data.iloc[i]['shot_made']
            
            if 0 <= xi < len(x_bins) and 0 <= yi < len(y_bins):
                efficiency_grid[yi, xi] += made
                shot_counts[yi, xi] += 1
        
        # Calculate percentages (avoid division by zero)
        mask = shot_counts > 0
        efficiency_grid[mask] = efficiency_grid[mask] / shot_counts[mask]
        efficiency_grid[~mask] = np.nan  # Set cells with no shots to NaN
        
        return x_bins, y_bins, efficiency_grid
    
    def generate_team_summary(self) -> pd.DataFrame:
        """
        Generate summary statistics for all Liberty players.
        
        Returns:
            DataFrame with team-wide shooting statistics
        """
        summaries = []
        
        for player in self.liberty_data['player_name'].unique():
            stats = self.calculate_player_efficiency(player)
            summaries.append({
                'Player': stats['player_name'],
                'Attempts': stats['total_attempts'],
                'Makes': stats['total_makes'],
                'FG%': stats['fg_pct'],
                '2P%': stats['two_pt_pct'],
                '3P%': stats['three_pt_pct'],
                'Avg Distance': stats['avg_shot_distance']
            })
        
        summary_df = pd.DataFrame(summaries)
        summary_df = summary_df.sort_values('Attempts', ascending=False)
        
        return summary_df


def main():
    """Process data and generate analysis outputs."""
    print("Processing WNBA shot data...")
    
    # Initialize processor
    processor = ShotDataProcessor(
        liberty_file='data/raw/liberty_shots_2024.csv',
        league_file='data/raw/league_average_shots.csv'
    )
    
    # Create processed data directory
    os.makedirs('data/processed', exist_ok=True)
    
    # Generate team summary
    print("\n--- Team Summary ---")
    team_summary = processor.generate_team_summary()
    print(team_summary.to_string(index=False))
    team_summary.to_csv('data/processed/team_summary.csv', index=False)
    
    # Analyze each player vs league average
    print("\n--- Player Comparisons to League Average ---")
    for player in processor.liberty_data['player_name'].unique():
        print(f"\n{player}:")
        comparison = processor.compare_to_league_average(player)
        print(comparison[['shot_zone', 'fg_pct_player', 'fg_pct_league', 
                         'fg_pct_diff', 'efficiency_vs_league']].to_string(index=False))
        
        # Save comparison
        comparison.to_csv(
            f'data/processed/{player.replace(" ", "_")}_comparison.csv',
            index=False
        )
    
    print("\n✓ Data processing complete!")


if __name__ == '__main__':
    main()
