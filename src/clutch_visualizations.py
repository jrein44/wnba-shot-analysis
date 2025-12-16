"""
Visualization module for clutch shooting analysis.
Creates compelling charts that tell the story of Liberty's late-game performance.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from clutch_analysis import (
    load_player_data, 
    define_game_situations,
    calculate_player_usage,
    analyze_clutch_performance,
    analyze_quarter_trends,
    analyze_shot_selection_by_time
)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# NY Liberty colors
LIBERTY_COLORS = {
    'primary': '#6ECEB2',      # Liberty Seafoam
    'secondary': '#002B5C',    # Navy
    'accent': '#A1A1A4',       # Gray
    'green': '#2E7D32',        # Made shots
    'red': '#C62828'           # Missed shots
}


def create_usage_comparison_chart(df, output_path):
    """Create chart showing usage patterns: overall vs Q4 vs clutch."""
    
    usage = calculate_player_usage(df)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Prepare data
    players = usage.index.tolist()
    x = np.arange(len(players))
    width = 0.25
    
    # Create bars
    bars1 = ax.bar(x - width, usage['Usage_Pct'], width, 
                   label='Overall Usage', color=LIBERTY_COLORS['accent'], alpha=0.8)
    bars2 = ax.bar(x, usage['Q4_Usage_Pct'], width,
                   label='Q4 Usage', color=LIBERTY_COLORS['primary'], alpha=0.8)
    bars3 = ax.bar(x + width, usage['Clutch_Usage_Pct'], width,
                   label='Clutch Usage (Last 5 min)', color=LIBERTY_COLORS['secondary'], alpha=0.8)
    
    # Customize
    ax.set_ylabel('Usage Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('NY Liberty Shot Distribution: Who Gets The Ball in Crunch Time?', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([name.split()[0] for name in players], fontsize=11)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved usage comparison chart")
    plt.close()


def create_clutch_efficiency_chart(df, output_path):
    """Create chart showing clutch vs non-clutch efficiency."""
    
    clutch_perf = analyze_clutch_performance(df)
    clutch_perf = clutch_perf[clutch_perf['Clutch_FGA'] >= 20]  # Min 20 clutch attempts
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    players = [name.split()[0] for name in clutch_perf['Player']]
    x = np.arange(len(players))
    width = 0.35
    
    # Create bars
    bars1 = ax.bar(x - width/2, clutch_perf['Non_Clutch_FG_PCT'], width,
                   label='Rest of Game', color=LIBERTY_COLORS['accent'], alpha=0.8)
    bars2 = ax.bar(x + width/2, clutch_perf['Clutch_FG_PCT'], width,
                   label='Clutch (Last 5 min Q4)', color=LIBERTY_COLORS['secondary'], alpha=0.8)
    
    # Add difference indicators
    for i, (idx, row) in enumerate(clutch_perf.iterrows()):
        diff = row['Clutch_Diff']
        color = LIBERTY_COLORS['green'] if diff > 0 else LIBERTY_COLORS['red']
        symbol = '▲' if diff > 0 else '▼'
        
        y_pos = max(row['Non_Clutch_FG_PCT'], row['Clutch_FG_PCT']) + 3
        ax.text(i, y_pos, f"{symbol} {abs(diff):.1f}%",
               ha='center', va='bottom', fontsize=10, 
               fontweight='bold', color=color)
    
    # Customize
    ax.set_ylabel('Field Goal %', fontsize=12, fontweight='bold')
    ax.set_title('Who Steps Up in Clutch Time? Efficiency Comparison', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(players, fontsize=11)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(clutch_perf['Clutch_FG_PCT'].max(), 
                       clutch_perf['Non_Clutch_FG_PCT'].max()) + 10)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=8)
    
    # Add note
    ax.text(0.98, 0.02, 'Min. 20 clutch attempts', 
            transform=ax.transAxes, ha='right', va='bottom',
            fontsize=8, style='italic', color='gray')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved clutch efficiency chart")
    plt.close()


def create_quarter_trends_chart(df, output_path):
    """Create line chart showing efficiency trends across quarters."""
    
    quarter_trends = analyze_quarter_trends(df)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot lines for each player
    colors = [LIBERTY_COLORS['secondary'], LIBERTY_COLORS['primary'], 
              LIBERTY_COLORS['accent'], '#FF6B35', '#4ECDC4']
    
    for i, player in enumerate(quarter_trends['Player'].unique()):
        player_data = quarter_trends[quarter_trends['Player'] == player]
        quarters = [int(q[1]) for q in player_data['Quarter']]
        
        ax.plot(quarters, player_data['FG_PCT'], 
               marker='o', linewidth=2.5, markersize=8,
               label=player.split()[0], color=colors[i % len(colors)],
               alpha=0.8)
    
    # Customize
    ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
    ax.set_ylabel('Field Goal %', fontsize=12, fontweight='bold')
    ax.set_title('Fatigue Factor: How Efficiency Changes Throughout the Game', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'], fontsize=11)
    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(30, 60)
    
    # Add 50% reference line
    ax.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(4.1, 50, '50%', va='center', fontsize=9, color='gray')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved quarter trends chart")
    plt.close()


def create_shot_selection_chart(df, output_path):
    """Create chart showing how 3PT rate changes in different situations."""
    
    shot_selection = analyze_shot_selection_by_time(df)
    shot_selection = shot_selection[shot_selection['Clutch_Shots'] >= 20]  # Min 20 clutch shots
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    players = [name.split()[0] for name in shot_selection['Player']]
    x = np.arange(len(players))
    width = 0.25
    
    # Create bars
    bars1 = ax.bar(x - width, shot_selection['Q1_Q3_3PT_Rate'], width,
                   label='Q1-Q3', color=LIBERTY_COLORS['accent'], alpha=0.8)
    bars2 = ax.bar(x, shot_selection['Q4_3PT_Rate'], width,
                   label='Q4', color=LIBERTY_COLORS['primary'], alpha=0.8)
    bars3 = ax.bar(x + width, shot_selection['Clutch_3PT_Rate'], width,
                   label='Clutch', color=LIBERTY_COLORS['secondary'], alpha=0.8)
    
    # Customize
    ax.set_ylabel('3-Point Attempt Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Shot Selection Strategy: Do Players Attack the Rim or Stay Outside in Crunch Time?', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(players, fontsize=11)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.0f}%',
                   ha='center', va='bottom', fontsize=8)
    
    # Add note
    ax.text(0.98, 0.02, 'Min. 20 clutch attempts', 
            transform=ax.transAxes, ha='right', va='bottom',
            fontsize=8, style='italic', color='gray')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved shot selection chart")
    plt.close()


def create_scatter_plot(df, output_path):
    """Create scatter plot: Clutch usage vs clutch efficiency."""
    
    clutch_perf = analyze_clutch_performance(df)
    clutch_perf = clutch_perf[clutch_perf['Clutch_FGA'] >= 10]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create scatter
    scatter = ax.scatter(clutch_perf['Clutch_FGA'], 
                        clutch_perf['Clutch_FG_PCT'],
                        s=300, alpha=0.6, 
                        c=clutch_perf['Clutch_Diff'],
                        cmap='RdYlGn', vmin=-15, vmax=15,
                        edgecolors='black', linewidth=1.5)
    
    # Add player labels
    for idx, row in clutch_perf.iterrows():
        ax.annotate(row['Player'].split()[0], 
                   (row['Clutch_FGA'], row['Clutch_FG_PCT']),
                   fontsize=10, fontweight='bold',
                   ha='center', va='center')
    
    # Add quadrant lines
    clutch_median_fga = clutch_perf['Clutch_FGA'].median()
    clutch_median_pct = clutch_perf['Clutch_FG_PCT'].median()
    
    ax.axvline(x=clutch_median_fga, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=clutch_median_pct, color='gray', linestyle='--', alpha=0.5)
    
    # Add quadrant labels
    ax.text(clutch_median_fga * 1.5, clutch_median_pct * 1.05, 
            'High Volume\nHigh Efficiency', 
            ha='center', va='bottom', fontsize=9, 
            style='italic', color='gray', alpha=0.7)
    ax.text(clutch_median_fga * 0.5, clutch_median_pct * 0.95,
            'Low Volume\nLow Efficiency',
            ha='center', va='top', fontsize=9,
            style='italic', color='gray', alpha=0.7)
    
    # Customize
    ax.set_xlabel('Clutch Shot Attempts (Last 5 min of Q4)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Clutch Field Goal %', fontsize=12, fontweight='bold')
    ax.set_title('The Clutch Matrix: Usage vs Efficiency in Critical Moments', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Clutch Boost\n(vs Rest of Game)', 
                   rotation=270, labelpad=20, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved clutch matrix scatter plot")
    plt.close()


def create_dashboard(df, output_path):
    """Create a comprehensive 4-panel dashboard."""
    
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25)
    
    # Panel 1: Usage comparison
    ax1 = fig.add_subplot(gs[0, 0])
    usage = calculate_player_usage(df)
    players = [name.split()[0] for name in usage.index]
    x = np.arange(len(players))
    width = 0.25
    
    ax1.bar(x - width, usage['Usage_Pct'], width, label='Overall', 
            color=LIBERTY_COLORS['accent'], alpha=0.8)
    ax1.bar(x, usage['Q4_Usage_Pct'], width, label='Q4',
            color=LIBERTY_COLORS['primary'], alpha=0.8)
    ax1.bar(x + width, usage['Clutch_Usage_Pct'], width, label='Clutch',
            color=LIBERTY_COLORS['secondary'], alpha=0.8)
    
    ax1.set_ylabel('Usage %', fontsize=10, fontweight='bold')
    ax1.set_title('Shot Distribution', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(players, fontsize=9)
    ax1.legend(fontsize=8)
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Clutch efficiency
    ax2 = fig.add_subplot(gs[0, 1])
    clutch_perf = analyze_clutch_performance(df)
    clutch_perf = clutch_perf[clutch_perf['Clutch_FGA'] >= 20]
    
    players2 = [name.split()[0] for name in clutch_perf['Player']]
    x2 = np.arange(len(players2))
    width2 = 0.35
    
    ax2.bar(x2 - width2/2, clutch_perf['Non_Clutch_FG_PCT'], width2,
            label='Non-Clutch', color=LIBERTY_COLORS['accent'], alpha=0.8)
    ax2.bar(x2 + width2/2, clutch_perf['Clutch_FG_PCT'], width2,
            label='Clutch', color=LIBERTY_COLORS['secondary'], alpha=0.8)
    
    ax2.set_ylabel('FG %', fontsize=10, fontweight='bold')
    ax2.set_title('Clutch Efficiency (Min. 20 attempts)', fontsize=12, fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(players2, fontsize=9)
    ax2.legend(fontsize=8)
    ax2.grid(axis='y', alpha=0.3)
    
    # Panel 3: Quarter trends
    ax3 = fig.add_subplot(gs[1, 0])
    quarter_trends = analyze_quarter_trends(df)
    colors = [LIBERTY_COLORS['secondary'], LIBERTY_COLORS['primary'], 
              LIBERTY_COLORS['accent'], '#FF6B35', '#4ECDC4']
    
    for i, player in enumerate(quarter_trends['Player'].unique()):
        player_data = quarter_trends[quarter_trends['Player'] == player]
        quarters = [int(q[1]) for q in player_data['Quarter']]
        ax3.plot(quarters, player_data['FG_PCT'], 
                marker='o', linewidth=2, markersize=6,
                label=player.split()[0], color=colors[i % len(colors)], alpha=0.8)
    
    ax3.set_xlabel('Quarter', fontsize=10, fontweight='bold')
    ax3.set_ylabel('FG %', fontsize=10, fontweight='bold')
    ax3.set_title('Quarter-by-Quarter Trends', fontsize=12, fontweight='bold')
    ax3.set_xticks([1, 2, 3, 4])
    ax3.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'], fontsize=9)
    ax3.legend(fontsize=7, ncol=2)
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    # Panel 4: Shot selection
    ax4 = fig.add_subplot(gs[1, 1])
    shot_selection = analyze_shot_selection_by_time(df)
    shot_selection = shot_selection[shot_selection['Clutch_Shots'] >= 20]
    
    players4 = [name.split()[0] for name in shot_selection['Player']]
    x4 = np.arange(len(players4))
    width4 = 0.25
    
    ax4.bar(x4 - width4, shot_selection['Q1_Q3_3PT_Rate'], width4,
            label='Q1-Q3', color=LIBERTY_COLORS['accent'], alpha=0.8)
    ax4.bar(x4, shot_selection['Q4_3PT_Rate'], width4,
            label='Q4', color=LIBERTY_COLORS['primary'], alpha=0.8)
    ax4.bar(x4 + width4, shot_selection['Clutch_3PT_Rate'], width4,
            label='Clutch', color=LIBERTY_COLORS['secondary'], alpha=0.8)
    
    ax4.set_ylabel('3PT Rate %', fontsize=10, fontweight='bold')
    ax4.set_title('Shot Selection by Situation', fontsize=12, fontweight='bold')
    ax4.set_xticks(x4)
    ax4.set_xticklabels(players4, fontsize=9)
    ax4.legend(fontsize=8)
    ax4.grid(axis='y', alpha=0.3)
    
    # Add overall title
    fig.suptitle('NY Liberty 2025 Clutch Performance Dashboard', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved comprehensive dashboard")
    plt.close()


def generate_all_visualizations(output_dir='outputs/clutch_analysis'):
    """Generate all clutch analysis visualizations."""
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*80)
    print("GENERATING CLUTCH ANALYSIS VISUALIZATIONS")
    print("="*80 + "\n")
    
    # Load and prepare data
    df = load_player_data()
    df = define_game_situations(df)
    
    # Generate individual charts
    create_usage_comparison_chart(df, output_path / 'usage_comparison.png')
    create_clutch_efficiency_chart(df, output_path / 'clutch_efficiency.png')
    create_quarter_trends_chart(df, output_path / 'quarter_trends.png')
    create_shot_selection_chart(df, output_path / 'shot_selection.png')
    create_scatter_plot(df, output_path / 'clutch_matrix.png')
    create_dashboard(df, output_path / 'comprehensive_dashboard.png')
    
    print("\n" + "="*80)
    print("✅ ALL VISUALIZATIONS CREATED!")
    print("="*80)
    print(f"\nFiles saved to: {output_path}")


if __name__ == "__main__":
    generate_all_visualizations()
