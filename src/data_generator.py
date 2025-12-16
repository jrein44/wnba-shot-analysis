"""
Generate realistic WNBA shot data for analysis.

This module creates synthetic but realistic shot data based on actual WNBA shooting patterns,
including Liberty players and league averages.
"""

import pandas as pd
import numpy as np
from typing import List, Dict
import os


class WNBAShotGenerator:
    """Generate realistic WNBA shot data based on typical shooting patterns."""
    
    def __init__(self, seed: int = 42):
        """Initialize the generator with a random seed for reproducibility."""
        np.random.seed(seed)
        
        # WNBA court dimensions (feet)
        self.court_length = 94
        self.court_width = 50
        self.hoop_x = 0  # Center of court
        self.hoop_y = 0  # Baseline (we'll shift coordinates)
        
        # Define shot zones with typical WNBA FG%
        self.shot_zones = {
            'Restricted Area': {'fg_pct': 0.58, 'weight': 0.25},
            'Paint (Non-RA)': {'fg_pct': 0.42, 'weight': 0.15},
            'Mid-Range': {'fg_pct': 0.38, 'weight': 0.20},
            'Corner 3': {'fg_pct': 0.37, 'weight': 0.15},
            'Above Break 3': {'fg_pct': 0.34, 'weight': 0.25}
        }
        
    def generate_player_data(self, player_name: str, team: str, position: str, 
                            num_shots: int = 500) -> pd.DataFrame:
        """
        Generate shot data for a single player.
        
        Args:
            player_name: Player's full name
            team: Team name
            position: Player position (Guard, Forward, Center)
            num_shots: Number of shots to generate
            
        Returns:
            DataFrame with shot data
        """
        shots = []
        
        # Adjust shot distribution based on position
        zone_weights = self._adjust_weights_by_position(position)
        
        for _ in range(num_shots):
            # Select zone based on weights
            zone = np.random.choice(
                list(self.shot_zones.keys()),
                p=zone_weights
            )
            
            # Generate shot location based on zone
            x, y, distance = self._generate_shot_location(zone)
            
            # Determine if shot was made (with some randomness around zone average)
            zone_fg_pct = self.shot_zones[zone]['fg_pct']
            # Add player-specific variance (±5%)
            player_variance = np.random.uniform(-0.05, 0.05)
            shot_made = np.random.random() < (zone_fg_pct + player_variance)
            
            shots.append({
                'player_name': player_name,
                'team': team,
                'position': position,
                'shot_zone': zone,
                'loc_x': x,
                'loc_y': y,
                'shot_distance': distance,
                'shot_made': int(shot_made),
                'shot_type': '3PT' if distance >= 22 else '2PT'
            })
            
        return pd.DataFrame(shots)
    
    def _adjust_weights_by_position(self, position: str) -> List[float]:
        """Adjust shot zone weights based on player position."""
        weights = [zone['weight'] for zone in self.shot_zones.values()]
        
        if position == 'Guard':
            # Guards take more 3s, fewer restricted area shots
            weights[0] *= 0.7  # Restricted Area
            weights[3] *= 1.2  # Corner 3
            weights[4] *= 1.3  # Above Break 3
        elif position == 'Center':
            # Centers take more shots at rim, fewer 3s
            weights[0] *= 1.5  # Restricted Area
            weights[1] *= 1.2  # Paint
            weights[3] *= 0.3  # Corner 3
            weights[4] *= 0.3  # Above Break 3
        # Forwards stay close to default
        
        # Normalize weights to sum to 1
        weights = np.array(weights)
        return weights / weights.sum()
    
    def _generate_shot_location(self, zone: str) -> tuple:
        """
        Generate x, y coordinates for a shot based on zone.
        
        Returns:
            (x, y, distance) tuple in feet from hoop
        """
        if zone == 'Restricted Area':
            # Within 4 feet of basket
            distance = np.random.uniform(0, 4)
            angle = np.random.uniform(0, 2 * np.pi)
            
        elif zone == 'Paint (Non-RA)':
            # 4-8 feet from basket
            distance = np.random.uniform(4, 8)
            angle = np.random.uniform(-np.pi/2, np.pi/2)  # Front of basket
            
        elif zone == 'Mid-Range':
            # 8-22 feet, avoid corners
            distance = np.random.uniform(10, 21)
            angle = np.random.uniform(-np.pi/3, np.pi/3)
            
        elif zone == 'Corner 3':
            # 22+ feet in corners
            distance = 22 + np.random.uniform(0, 2)
            # Corners are at ±22 feet on x-axis
            corner_side = np.random.choice([-1, 1])
            x = corner_side * 22
            y = np.random.uniform(0, 5)  # Close to baseline
            return x, y, distance
            
        else:  # Above Break 3
            # 22-28 feet, above the break
            distance = np.random.uniform(22, 28)
            angle = np.random.uniform(-np.pi/4, np.pi/4)
        
        # Convert polar to cartesian
        x = distance * np.sin(angle)
        y = distance * np.cos(angle)
        
        return x, y, distance


def generate_liberty_roster() -> pd.DataFrame:
    """Generate shot data for 2024 NY Liberty key players."""
    generator = WNBAShotGenerator(seed=42)
    
    players = [
        {'name': 'Breanna Stewart', 'position': 'Forward', 'shots': 600},
        {'name': 'Sabrina Ionescu', 'position': 'Guard', 'shots': 550},
        {'name': 'Jonquel Jones', 'position': 'Center', 'shots': 450},
        {'name': 'Betnijah Laney-Hamilton', 'position': 'Guard', 'shots': 400},
        {'name': 'Courtney Vandersloot', 'position': 'Guard', 'shots': 350},
    ]
    
    all_shots = []
    for player in players:
        player_shots = generator.generate_player_data(
            player_name=player['name'],
            team='New York Liberty',
            position=player['position'],
            num_shots=player['shots']
        )
        all_shots.append(player_shots)
    
    return pd.concat(all_shots, ignore_index=True)


def generate_league_average() -> pd.DataFrame:
    """Generate league average shooting data for comparison."""
    generator = WNBAShotGenerator(seed=100)
    
    # Generate data for multiple 'average' players to create league baseline
    league_shots = []
    for i in range(20):  # 20 players worth of data
        shots = generator.generate_player_data(
            player_name=f'League Average Player {i}',
            team='League Average',
            position='Forward',  # Use forward as baseline
            num_shots=400
        )
        league_shots.append(shots)
    
    return pd.concat(league_shots, ignore_index=True)


def main():
    """Generate and save all shot data."""
    print("Generating WNBA shot data...")
    
    # Create data directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Generate Liberty data
    print("Generating NY Liberty player data...")
    liberty_data = generate_liberty_roster()
    liberty_data.to_csv('data/raw/liberty_shots_2024.csv', index=False)
    print(f"✓ Generated {len(liberty_data)} Liberty shots")
    
    # Generate league average
    print("Generating league average data...")
    league_data = generate_league_average()
    league_data.to_csv('data/raw/league_average_shots.csv', index=False)
    print(f"✓ Generated {len(league_data)} league average shots")
    
    # Print summary statistics
    print("\n--- Summary Statistics ---")
    print("\nLiberty Team Shooting:")
    for player in liberty_data['player_name'].unique():
        player_data = liberty_data[liberty_data['player_name'] == player]
        fg_pct = player_data['shot_made'].mean()
        three_pt_pct = player_data[player_data['shot_type'] == '3PT']['shot_made'].mean()
        print(f"{player:25s} FG%: {fg_pct:.3f}  3P%: {three_pt_pct:.3f}")
    
    print("\nLeague Average:")
    league_fg_pct = league_data['shot_made'].mean()
    league_three_pct = league_data[league_data['shot_type'] == '3PT']['shot_made'].mean()
    print(f"FG%: {league_fg_pct:.3f}  3P%: {league_three_pct:.3f}")
    
    print("\n✓ Data generation complete!")


if __name__ == '__main__':
    main()
