"""
Clutch shooting and usage pattern analysis for WNBA players.

This module analyzes:
1. Quarter-by-quarter usage patterns
2. Late-game (Q4 final 5 min) efficiency vs rest of game
3. Shot selection changes throughout game
4. Fatigue effects on shooting efficiency
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def load_player_data(data_dir='data/raw'):
    """Load all player shot data into a single DataFrame."""
    data_path = Path(data_dir)
    all_data = []
    
    player_files = {
        'ionescu_shots_2025.csv': 'Sabrina Ionescu',
        'stewart_shots_2025.csv': 'Breanna Stewart',
        'jones_shots_2025.csv': 'Jonquel Jones',
        'nc_shots_2025.csv': 'Natasha Cloud',
        'lf_shots_2025.csv': 'Leonie Fiebich'
    }
    
    for filename, player_name in player_files.items():
        file_path = data_path / filename
        if file_path.exists():
            df = pd.read_csv(file_path)
            all_data.append(df)
            print(f"✓ Loaded {player_name}: {len(df)} shots")
    
    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n📊 Total shots loaded: {len(combined)}")
    return combined


def calculate_time_remaining(df):
    """Calculate total seconds remaining in game for each shot."""
    # WNBA has 4 quarters of 10 minutes each (40 total minutes)
    df = df.copy()
    
    # Calculate seconds remaining in current period
    df['seconds_in_period'] = df['MINUTES_REMAINING'] * 60 + df['SECONDS_REMAINING']
    
    # Calculate total seconds remaining in game
    # Period 1 = 3 quarters + current time left
    # Period 2 = 2 quarters + current time left
    # Period 3 = 1 quarter + current time left
    # Period 4 = current time left only
    quarters_remaining = (4 - df['PERIOD']).clip(lower=0)
    df['total_seconds_remaining'] = (quarters_remaining * 600) + df['seconds_in_period']
    
    return df


def define_game_situations(df):
    """Add categorical columns for different game situations."""
    df = calculate_time_remaining(df)
    
    # Quarter labels
    df['quarter'] = 'Q' + df['PERIOD'].astype(str)
    
    # Clutch time: Last 5 minutes of Q4 (300 seconds or less remaining)
    df['is_clutch'] = (df['PERIOD'] == 4) & (df['total_seconds_remaining'] <= 300)
    
    # Late game: All of Q4
    df['is_q4'] = df['PERIOD'] == 4
    
    # Time segments within quarters (early/mid/late)
    df['period_segment'] = pd.cut(
        df['seconds_in_period'],
        bins=[0, 200, 400, 600],
        labels=['Late', 'Mid', 'Early'],
        include_lowest=True
    )
    
    return df


def calculate_player_usage(df):
    """Calculate usage patterns by player and situation."""
    
    # Overall usage
    total_shots = len(df)
    player_usage = df.groupby('PLAYER_NAME').size()
    player_usage_pct = (player_usage / total_shots * 100).round(1)
    
    # Q4 usage
    q4_shots = df[df['is_q4']]
    q4_usage = q4_shots.groupby('PLAYER_NAME').size()
    q4_usage_pct = (q4_usage / len(q4_shots) * 100).round(1)
    
    # Clutch usage (last 5 min of Q4)
    clutch_shots = df[df['is_clutch']]
    if len(clutch_shots) > 0:
        clutch_usage = clutch_shots.groupby('PLAYER_NAME').size()
        clutch_usage_pct = (clutch_usage / len(clutch_shots) * 100).round(1)
    else:
        clutch_usage_pct = pd.Series()
    
    # Combine into summary
    usage_summary = pd.DataFrame({
        'Total_Shots': player_usage,
        'Usage_Pct': player_usage_pct,
        'Q4_Shots': q4_usage,
        'Q4_Usage_Pct': q4_usage_pct,
        'Clutch_Shots': clutch_usage if len(clutch_shots) > 0 else 0,
        'Clutch_Usage_Pct': clutch_usage_pct if len(clutch_shots) > 0 else 0
    }).fillna(0)
    
    return usage_summary.sort_values('Usage_Pct', ascending=False)


def calculate_shooting_efficiency(df, group_cols=['PLAYER_NAME']):
    """Calculate shooting efficiency metrics by specified grouping."""
    
    if len(group_cols) == 0:
        # No grouping - calculate overall stats
        fga = df['SHOT_ATTEMPTED_FLAG'].sum()
        fgm = df['SHOT_MADE_FLAG'].sum()
        fg_pct = (fgm / fga * 100) if fga > 0 else 0
        
        result = pd.DataFrame({
            'FGA': [fga],
            'FGM': [fgm],
            'FG_PCT': [round(fg_pct, 1)]
        })
        
        # Add 2PT and 3PT splits
        for shot_type in ['2PT Field Goal', '3PT Field Goal']:
            type_df = df[df['SHOT_TYPE'] == shot_type]
            prefix = '2PT' if '2PT' in shot_type else '3PT'
            
            if len(type_df) > 0:
                type_fga = type_df['SHOT_ATTEMPTED_FLAG'].sum()
                type_fgm = type_df['SHOT_MADE_FLAG'].sum()
                type_pct = (type_fgm / type_fga * 100) if type_fga > 0 else 0
                
                result[f'{prefix}_FGA'] = type_fga
                result[f'{prefix}_FGM'] = type_fgm
                result[f'{prefix}_PCT'] = round(type_pct, 1)
            else:
                result[f'{prefix}_FGA'] = 0
                result[f'{prefix}_FGM'] = 0
                result[f'{prefix}_PCT'] = 0
        
        return result
    
    # With grouping
    grouped = df.groupby(group_cols).agg({
        'SHOT_ATTEMPTED_FLAG': 'sum',  # Total shots
        'SHOT_MADE_FLAG': 'sum',        # Made shots
    }).reset_index()
    
    grouped.columns = list(group_cols) + ['FGA', 'FGM']
    grouped['FG_PCT'] = (grouped['FGM'] / grouped['FGA'] * 100).round(1)
    
    # Add 2PT and 3PT splits
    for shot_type in ['2PT Field Goal', '3PT Field Goal']:
        type_df = df[df['SHOT_TYPE'] == shot_type]
        if len(type_df) > 0:
            type_grouped = type_df.groupby(group_cols).agg({
                'SHOT_ATTEMPTED_FLAG': 'sum',
                'SHOT_MADE_FLAG': 'sum',
            }).reset_index()
            
            prefix = '2PT' if '2PT' in shot_type else '3PT'
            type_grouped.columns = list(group_cols) + [f'{prefix}_FGA', f'{prefix}_FGM']
            type_grouped[f'{prefix}_PCT'] = (type_grouped[f'{prefix}_FGM'] / type_grouped[f'{prefix}_FGA'] * 100).round(1)
            
            grouped = grouped.merge(type_grouped, on=group_cols, how='left')
    
    return grouped.fillna(0)


def analyze_clutch_performance(df):
    """Compare clutch vs non-clutch shooting for each player."""
    
    results = []
    
    for player in df['PLAYER_NAME'].unique():
        player_df = df[df['PLAYER_NAME'] == player]
        
        # Non-clutch stats
        non_clutch = player_df[~player_df['is_clutch']]
        non_clutch_stats = calculate_shooting_efficiency(non_clutch, [])
        
        # Clutch stats
        clutch = player_df[player_df['is_clutch']]
        if len(clutch) > 0:
            clutch_stats = calculate_shooting_efficiency(clutch, [])
        else:
            clutch_stats = pd.DataFrame({'FGA': [0], 'FGM': [0], 'FG_PCT': [0]})
        
        results.append({
            'Player': player,
            'Non_Clutch_FGA': int(non_clutch_stats['FGA'].iloc[0]),
            'Non_Clutch_FG_PCT': float(non_clutch_stats['FG_PCT'].iloc[0]),
            'Clutch_FGA': int(clutch_stats['FGA'].iloc[0]),
            'Clutch_FG_PCT': float(clutch_stats['FG_PCT'].iloc[0]),
            'Clutch_Diff': float(clutch_stats['FG_PCT'].iloc[0] - non_clutch_stats['FG_PCT'].iloc[0])
        })
    
    return pd.DataFrame(results).sort_values('Clutch_FGA', ascending=False)


def analyze_quarter_trends(df):
    """Analyze efficiency trends across quarters."""
    
    quarter_stats = []
    
    for player in df['PLAYER_NAME'].unique():
        player_df = df[df['PLAYER_NAME'] == player]
        
        for quarter in [1, 2, 3, 4]:
            q_df = player_df[player_df['PERIOD'] == quarter]
            if len(q_df) > 0:
                stats = calculate_shooting_efficiency(q_df, [])
                quarter_stats.append({
                    'Player': player,
                    'Quarter': f'Q{quarter}',
                    'FGA': int(stats['FGA'].iloc[0]),
                    'FG_PCT': float(stats['FG_PCT'].iloc[0])
                })
    
    return pd.DataFrame(quarter_stats)


def analyze_shot_selection_by_time(df):
    """Analyze how shot selection changes throughout the game."""
    
    shot_selection = []
    
    for player in df['PLAYER_NAME'].unique():
        player_df = df[df['PLAYER_NAME'] == player]
        
        # Q1-Q3 shot selection
        early_game = player_df[player_df['PERIOD'] <= 3]
        early_3pt_rate = (early_game['SHOT_TYPE'] == '3PT Field Goal').sum() / len(early_game) * 100 if len(early_game) > 0 else 0
        
        # Q4 shot selection
        q4 = player_df[player_df['PERIOD'] == 4]
        q4_3pt_rate = (q4['SHOT_TYPE'] == '3PT Field Goal').sum() / len(q4) * 100 if len(q4) > 0 else 0
        
        # Clutch shot selection
        clutch = player_df[player_df['is_clutch']]
        clutch_3pt_rate = (clutch['SHOT_TYPE'] == '3PT Field Goal').sum() / len(clutch) * 100 if len(clutch) > 0 else 0
        
        shot_selection.append({
            'Player': player,
            'Q1_Q3_3PT_Rate': round(early_3pt_rate, 1),
            'Q4_3PT_Rate': round(q4_3pt_rate, 1),
            'Clutch_3PT_Rate': round(clutch_3pt_rate, 1),
            'Q1_Q3_Shots': len(early_game),
            'Q4_Shots': len(q4),
            'Clutch_Shots': len(clutch)
        })
    
    return pd.DataFrame(shot_selection)


def print_analysis_summary(df):
    """Print comprehensive analysis summary."""
    
    print("\n" + "="*80)
    print("NY LIBERTY CLUTCH SHOOTING & USAGE ANALYSIS - 2025 Season")
    print("="*80)
    
    # Usage patterns
    print("\n📊 USAGE PATTERNS")
    print("-" * 80)
    usage = calculate_player_usage(df)
    print(usage.to_string())
    
    # Clutch performance
    print("\n🔥 CLUTCH PERFORMANCE (Last 5 min of Q4)")
    print("-" * 80)
    clutch_perf = analyze_clutch_performance(df)
    print(clutch_perf.to_string(index=False))
    
    # Quarter trends
    print("\n📈 QUARTER-BY-QUARTER EFFICIENCY")
    print("-" * 80)
    quarter_trends = analyze_quarter_trends(df)
    pivot = quarter_trends.pivot(index='Player', columns='Quarter', values='FG_PCT')
    print(pivot.round(1).to_string())
    
    # Shot selection
    print("\n🎯 SHOT SELECTION BY GAME SITUATION")
    print("-" * 80)
    shot_selection = analyze_shot_selection_by_time(df)
    print(shot_selection.to_string(index=False))
    
    print("\n" + "="*80)


if __name__ == "__main__":
    # Load data
    df = load_player_data()
    
    # Add game situation columns
    df = define_game_situations(df)
    
    # Print analysis
    print_analysis_summary(df)
