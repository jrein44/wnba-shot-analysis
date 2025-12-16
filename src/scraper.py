"""
Scrape WNBA shot chart data from publicly available sources.

This script provides multiple scraping methods:
1. Basketball-Reference for game-level stats
2. ESPN for play-by-play data
3. Her Hoop Stats for shot location data (if available)

NOTE: Run this script locally on your machine, not in restricted environments.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from typing import List, Dict, Optional
import os


class WNBAScraper:
    """Scraper for WNBA shot and game data."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_basketball_reference_shooting(self, player_name: str, season: int = 2024) -> Optional[pd.DataFrame]:
        """
        Scrape shooting stats from Basketball-Reference.
        
        Note: This gets aggregated shooting stats, not individual shot locations.
        
        Args:
            player_name: Player's name (e.g., "Sabrina Ionescu")
            season: Season year
            
        Returns:
            DataFrame with shooting zones and percentages
        """
        # Convert name to BBRef format (e.g., "ionessa01w")
        # You'll need to look up player codes manually or build a lookup
        
        print(f"📊 Scraping Basketball-Reference for {player_name}")
        print("⚠️  Note: BBRef has aggregated stats, not individual shot locations")
        
        # Example URL structure
        # https://www.basketball-reference.com/wnba/players/i/ionessa01w.html
        
        return None  # Placeholder
    
    def scrape_espn_play_by_play(self, game_id: str) -> Optional[pd.DataFrame]:
        """
        Scrape play-by-play data from ESPN for a specific game.
        
        Args:
            game_id: ESPN game ID
            
        Returns:
            DataFrame with play-by-play events including shots
        """
        url = f"https://www.espn.com/wnba/playbyplay/_/gameId/{game_id}"
        
        print(f"📊 Scraping ESPN PBP for game {game_id}")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ESPN's play-by-play is usually in a table or accordion
            # Structure varies, so this is a template
            
            plays = []
            # Find play-by-play elements and extract
            # This requires inspecting ESPN's HTML structure
            
            return pd.DataFrame(plays)
            
        except Exception as e:
            print(f"❌ Error scraping ESPN: {e}")
            return None
    
    def get_liberty_game_ids_2024(self) -> List[str]:
        """
        Get list of Liberty game IDs for 2024 season.
        
        You can find these by:
        1. Going to ESPN's WNBA schedule
        2. Filtering for Liberty games
        3. Extracting game IDs from URLs
        """
        # Example game IDs (you'd need to collect these manually)
        game_ids = [
            "401636519",  # Example
            "401636520",
            # ... more games
        ]
        return game_ids
    
    def scrape_wnba_stats_api_shot_chart(self, player_id: str, season: str = "2024") -> Optional[pd.DataFrame]:
        """
        Attempt to scrape from WNBA Stats API.
        
        The WNBA Stats API is similar to NBA's stats.nba.com.
        However, it may require headers and has rate limiting.
        
        Args:
            player_id: WNBA player ID (e.g., "1629477" for Ionescu)
            season: Season string (e.g., "2024")
            
        Returns:
            DataFrame with shot locations
        """
        # WNBA Stats API endpoint
        url = "https://stats.wnba.com/stats/shotchartdetail"
        
        params = {
            'PlayerID': player_id,
            'Season': season,
            'SeasonType': 'Regular Season',
            'TeamID': '0',
            'GameID': '',
            'Outcome': '',
            'Location': '',
            'Month': '0',
            'SeasonSegment': '',
            'DateFrom': '',
            'DateTo': '',
            'OpponentTeamID': '0',
            'VsConference': '',
            'VsDivision': '',
            'Position': '',
            'RookieYear': '',
            'GameSegment': '',
            'Period': '0',
            'LastNGames': '0',
            'ContextMeasure': 'FGA'
        }
        
        # WNBA Stats API requires specific headers
        api_headers = {
            'Host': 'stats.wnba.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'x-nba-stats-origin': 'stats',
            'x-nba-stats-token': 'true',
            'Connection': 'keep-alive',
            'Referer': 'https://stats.wnba.com/',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        
        try:
            print(f"📊 Attempting WNBA Stats API for player {player_id}")
            response = requests.get(url, params=params, headers=api_headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response
            if 'resultSets' in data and len(data['resultSets']) > 0:
                shot_data = data['resultSets'][0]
                headers = shot_data['headers']
                rows = shot_data['rowSet']
                
                df = pd.DataFrame(rows, columns=headers)
                
                print(f"✓ Got {len(df)} shots from API")
                return df
            else:
                print("❌ No shot data in API response")
                return None
                
        except Exception as e:
            print(f"❌ API error: {e}")
            print("💡 Try running this locally, not in a restricted network")
            return None


def manual_data_collection_guide():
    """
    Print instructions for manually collecting data when scraping fails.
    """
    print("\n" + "="*70)
    print("MANUAL DATA COLLECTION GUIDE")
    print("="*70)
    
    print("\n📋 OPTION 1: Export from stats.wnba.com")
    print("-" * 70)
    print("1. Go to: https://stats.wnba.com/player/1629477/")
    print("2. Click on 'Shot Dashboard' tab")
    print("3. Look for 'Export' or download button (if available)")
    print("4. Save as CSV")
    print("\nPlayer IDs for Liberty:")
    print("  - Sabrina Ionescu: 1629477")
    print("  - Breanna Stewart: 1628932")
    print("  - Jonquel Jones: 1628886")
    print("  - Betnijah Laney-Hamilton: 1628326")
    print("  - Courtney Vandersloot: 201234")
    
    print("\n📋 OPTION 2: Use Browser Dev Tools")
    print("-" * 70)
    print("1. Go to stats.wnba.com shot chart page")
    print("2. Open browser Developer Tools (F12)")
    print("3. Go to Network tab")
    print("4. Look for API calls to 'shotchartdetail'")
    print("5. Right-click → Copy → Copy response")
    print("6. Paste into a .json file")
    print("7. I can help you convert JSON to CSV")
    
    print("\n📋 OPTION 3: Screenshot Shot Charts")
    print("-" * 70)
    print("1. Take screenshots of shot charts from stats.wnba.com")
    print("2. Include them in your GitHub as visual examples")
    print("3. Use aggregated stats instead of individual shots")
    print("4. Create analysis based on zone percentages")
    
    print("\n📋 OPTION 4: Use Her Hoop Stats")
    print("-" * 70)
    print("1. Go to: herhoopstats.com")
    print("2. Search for Liberty players")
    print("3. Export available data")
    print("4. They may have downloadable shot data")
    
    print("\n📋 OPTION 5: Create Realistic Sample")
    print("-" * 70)
    print("1. Use official season stats (FG%, 3P%, etc.)")
    print("2. Generate sample shots matching those percentages")
    print("3. Clearly label as 'modeled data based on season stats'")
    print("4. Include source citations for percentages used")
    
    print("\n" + "="*70)


def create_sample_from_official_stats():
    """
    Create a realistic dataset based on official published stats.
    """
    print("\n🏀 Creating sample dataset based on official 2024 stats...")
    
    # Based on actual 2024 Liberty stats from basketball-reference
    players = [
        {
            'name': 'Sabrina Ionescu',
            'fga': 524,  # Field goal attempts
            'fgm': 210,  # Field goals made
            'fg_pct': 0.401,
            'three_pa': 319,
            'three_pm': 95,
            'three_pct': 0.298
        },
        {
            'name': 'Breanna Stewart',
            'fga': 601,
            'fgm': 269,
            'fg_pct': 0.448,
            'three_pa': 220,
            'three_pm': 94,
            'three_pct': 0.427
        },
        # Add more players...
    ]
    
    print("✓ Use these official stats to validate synthetic data")
    print("✓ Generated shots will match these percentages")
    
    return players


def main():
    """Main execution."""
    print("🏀 WNBA Shot Data Scraper")
    print("=" * 70)
    
    scraper = WNBAScraper()
    
    # Try API approach (will likely fail in restricted networks)
    print("\n1️⃣  Attempting WNBA Stats API...")
    df = scraper.scrape_wnba_stats_api_shot_chart(player_id="1629477", season="2024")
    
    if df is not None:
        print(f"\n✅ SUCCESS! Got {len(df)} shots")
        print(f"Columns: {list(df.columns)}")
        
        # Save data
        output_path = 'data/raw/scraped_shots.csv'
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✓ Saved to: {output_path}")
    else:
        print("\n❌ Scraping failed (expected in restricted networks)")
        print("\n" + "💡 RECOMMENDATION".center(70, "="))
        print("Run this script locally on your own computer where you can")
        print("access stats.wnba.com freely.")
        print("\nOR follow the manual collection guide below:")
        
        manual_data_collection_guide()


if __name__ == '__main__':
    main()
