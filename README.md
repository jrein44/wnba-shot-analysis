# WNBA Shot Analysis Portfolio

**End-to-end basketball analytics project using real WNBA API data**

Built by: Jess Reinhardt
Contact: www.linkedin.com/in/jessica-reinhardt | jess.reinhardt44@gmail.com

---

## 🏀 Project Overview

This project demonstrates professional basketball analytics skills through comprehensive shot analysis of NY Liberty players' 2025 season performance. Using real data from the official WNBA Stats API, I built a complete analytics pipeline that mirrors workflows used by professional basketball operations teams.

**Key Features:**
- Real shot-level data collection from stats.wnba.com API
- Clutch performance analysis (last 5 minutes of 4th quarter)
- Quarter-by-quarter efficiency trends
- Automated professional player report generation
- League average benchmarking

---

## 📊 Sample Outputs

### Shot Charts
Clean, professional visualizations with accurate WNBA court dimensions:

![Sabrina Ionescu Shot Chart](outputs/shot_charts/real/Ionescu_2025_CLEAN_shotchart.png)

### Clutch Performance Dashboard
Multi-panel analysis showing usage patterns, efficiency, and situational performance:

![Clutch Analysis Dashboard](outputs/clutch_analysis/comprehensive_dashboard.png)

### Professional Player Reports
Automated Word document generation with statistics, visualizations, and development recommendations:
- [Sabrina Ionescu 2025 Season Report](outputs/player_reports/Ionescu_2025_Season_Report.docx)
- [Breanna Stewart 2025 Season Report](outputs/player_reports/Stewart_2025_Season_Report.docx)
- [Jonquel Jones 2025 Season Report](outputs/player_reports/Jones_2025_Season_Report.docx)

---

## 🔍 Key Insights

**Clutch Performance Analysis:**
- **Breanna Stewart** shoots **+8.8%** better in clutch situations (54.1% vs 45.3% rest of game)
- **Sabrina Ionescu** handles 39.3% of clutch possessions but efficiency drops -5.5%
- **Jonquel Jones** shoots 55.6% in clutch moments despite only 13.4% usage rate

*Clutch = last 5 minutes of Q4. Note: Score differential data not available in shot chart API; standard definition (within 5 points) would require play-by-play integration.*

**Actionable Recommendations:**
- Consider increasing Stewart's clutch usage given her +8.8% efficiency boost
- Explore shot selection optimizations for Ionescu's high-volume clutch attempts
- Leverage Jones' elite efficiency (49.0% FG overall, 42.4% from 3) more strategically

---

## 🛠️ Technical Stack

**Data Collection:**
- Browser developer tools (F12 → Network → XHR) to capture stats.wnba.com API requests
- JSON to CSV data pipeline
- Python data processing (pandas, numpy)

**Analysis:**
- Statistical analysis: shooting efficiency by situation, usage patterns, quarter trends
- Clutch performance definition: Last 5 minutes of Q4
- Benchmarking vs 2025 WNBA league averages (43.9% FG, 49.8% 2PT, 33.8% 3PT)

**Visualization:**
- matplotlib & seaborn for shot charts and analytics dashboards
- Precise WNBA court dimensions (22.15 ft three-point arc)
- Color-coded efficiency visualizations

**Automation:**
- docx-js for automated Word report generation
- Professional formatting with NY Liberty branding
- Embedded shot chart visualizations

---

## 📁 Project Structure

```
wnba-shot-analysis/
├── data/
│   ├── raw/                    # Real shot data from WNBA API
│   │   ├── ionescu_shots_2025.csv
│   │   ├── stewart_shots_2025.csv
│   │   └── jones_shots_2025.csv
│   └── processed/              # Analysis outputs
├── src/
│   ├── convert_real_data.py    # JSON → CSV conversion
│   ├── clutch_analysis.py      # Clutch performance calculations
│   ├── clutch_visualizations.py # Charts and dashboards
│   ├── create_clean_shot_charts.py # Shot chart generation
│   └── generate_player_report.js # Automated report creation
├── outputs/
│   ├── shot_charts/            # Player shot visualizations
│   ├── clutch_analysis/        # Performance dashboards
│   └── player_reports/         # Word documents
├── notebooks/
│   └── analysis.ipynb          # Exploratory analysis
└── README.md
```

## 📈 Skills Demonstrated

✅ **Data Engineering:** API data extraction, JSON parsing, data pipeline development  
✅ **Statistical Analysis:** Performance metrics, situational analysis, benchmarking  
✅ **Data Visualization:** Shot charts, multi-panel dashboards, professional formatting  
✅ **Automation:** Programmatic report generation, reproducible workflows  
✅ **Domain Knowledge:** Basketball analytics, WNBA rules, court dimensions  
✅ **Communication:** Executive summaries, actionable recommendations, visual storytelling

---

## 📊 Data Sources

- **Shot Data:** stats.wnba.com official API
- **League Averages:** Basketball-Reference.com 2025 WNBA season
- **Court Dimensions:** Official WNBA specifications (22.15 ft three-point line)

All data represents the 2025 WNBA regular season.

---

## 🎯 Future Enhancements

- [ ] **Integrate play-by-play data for true clutch filtering** (score within 5 points)
- [ ] Expand to full league-wide dataset (all 12 teams)
- [ ] Add assisted vs. unassisted shot analysis
- [ ] Incorporate defensive matchup data
- [ ] Build interactive dashboard (Streamlit/Dash)
- [ ] Add shot clock timing analysis
- [ ] Create opponent scouting reports

---

## 📫 Contact

Interested in discussing this project or basketball analytics opportunities?

- **LinkedIn:** www.linkedin.com/in/jessica-reinhardt
- **Email:** jess.reinhardt44@gmail.com
- **GitHub:** https://github.com/jrein44

---

## 📝 License

This project is for portfolio demonstration purposes. Data sourced from publicly available WNBA statistics.

---

*Last Updated: December 2025*

## 🔄 Player Comparisons

Example comparison analysis demonstrating ability to evaluate players side-by-side:

**Stewart vs. Ionescu - Clutch Performance:**
- Stewart: 54.1% clutch FG% (+8.8% vs rest of game)
- Ionescu: 35.4% clutch FG% (-5.5% vs rest of game)
- **Recommendation**: Increase Stewart's clutch usage

**Jones vs. League - 3PT Efficiency:**
- Jones: 42.4% from 3PT
- League Avg: 33.8% from 3PT
- **+8.6 percentage points** above average
- Elite floor spacer

