"""
Convert real WNBA Stats API JSON data to CSV format for analysis.

This script takes the JSON response from stats.wnba.com and converts it
to the CSV format expected by our analysis pipeline.
"""

import json
import pandas as pd
from pathlib import Path


def convert_wnba_json_to_csv(json_file: str, output_csv: str):
    """
    Convert WNBA Stats API JSON to clean CSV format.
    
    Args:
        json_file: Path to the JSON file from stats.wnba.com
        output_csv: Path where CSV should be saved
    """
    print(f"📖 Reading JSON from {json_file}")
    
    # Load JSON
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract shot chart data
    shot_data = data['resultSets'][0]
    headers = shot_data['headers']
    rows = shot_data['rowSet']
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)
    
    print(f"✓ Found {len(df)} shots")
    print(f"✓ Player: {df['PLAYER_NAME'].iloc[0]}")
    print(f"✓ Team: {df['TEAM_NAME'].iloc[0]}")
    print(f"✓ Date range: {df['GAME_DATE'].min()} to {df['GAME_DATE'].max()}")
    
    # Calculate shooting percentages
    total_shots = len(df)
    made_shots = df['SHOT_MADE_FLAG'].sum()
    fg_pct = made_shots / total_shots if total_shots > 0 else 0
    
    two_pt_shots = df[df['SHOT_TYPE'] == '2PT Field Goal']
    two_pt_made = two_pt_shots['SHOT_MADE_FLAG'].sum()
    two_pt_pct = two_pt_made / len(two_pt_shots) if len(two_pt_shots) > 0 else 0
    
    three_pt_shots = df[df['SHOT_TYPE'] == '3PT Field Goal']
    three_pt_made = three_pt_shots['SHOT_MADE_FLAG'].sum()
    three_pt_pct = three_pt_made / len(three_pt_shots) if len(three_pt_shots) > 0 else 0
    
    print(f"\n📊 Season Stats:")
    print(f"   FG%: {fg_pct:.1%} ({made_shots}/{total_shots})")
    print(f"   2PT%: {two_pt_pct:.1%} ({two_pt_made}/{len(two_pt_shots)})")
    print(f"   3PT%: {three_pt_pct:.1%} ({three_pt_made}/{len(three_pt_shots)})")
    
    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"\n✓ Saved to {output_csv}")
    
    return df


def convert_all_players(input_dir: str = "data/raw/json", output_dir: str = "data/raw"):
    """
    Convert all JSON files in a directory to CSV.
    
    Args:
        input_dir: Directory containing JSON files
        output_dir: Directory where CSVs should be saved
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    json_files = list(input_path.glob("*.json"))
    
    if not json_files:
        print(f"❌ No JSON files found in {input_dir}")
        return
    
    print(f"🔍 Found {len(json_files)} JSON files\n")
    
    for json_file in json_files:
        # Create output filename
        output_csv = output_path / json_file.name.replace('.json', '_shots.csv')
        
        try:
            convert_wnba_json_to_csv(str(json_file), str(output_csv))
            print()
        except Exception as e:
            print(f"❌ Error processing {json_file.name}: {e}\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Single file mode
        json_file = sys.argv[1]
        output_csv = sys.argv[2] if len(sys.argv) > 2 else json_file.replace('.json', '_shots.csv')
        convert_wnba_json_to_csv(json_file, output_csv)
    else:
        # Batch mode - convert all JSONs in data/raw/json/
        print("🏀 WNBA JSON to CSV Converter")
        print("=" * 70)
        convert_all_players()
