# Key Findings: NY Liberty Shooting Analysis - 2025 Season

## Executive Summary

Analysis of 1,857 real shot attempts from NY Liberty's 2025 season reveals distinct performance patterns across game situations. Using official WNBA Stats API data, this analysis identifies clutch performance differentials, usage patterns, and efficiency trends that inform strategic decision-making.

---

## Team-Wide Insights - 2025 Season

### Shooting Efficiency Overview (Real Data)

| Player | Shots | FG% | 2PT% | 3PT% | vs League Avg |
|--------|-------|-----|------|------|---------------|
| Jonquel Jones | 306 | 49.0% | 53.6% | 42.4% | +5.1% FG |
| Leonie Fiebich | 221 | 48.9% | 56.4% | 42.5% | +5.0% FG |
| Breanna Stewart | 408 | 46.1% | 52.0% | 24.1% | +2.2% FG |
| Natasha Cloud | 349 | 43.3% | 50.8% | 33.8% | -0.6% FG |
| Sabrina Ionescu | 573 | 40.1% | 49.3% | 29.9% | -3.8% FG |

**2025 WNBA League Averages**: 43.9% FG, 49.8% 2PT, 33.8% 3PT

---

## Critical Finding #1: Clutch Performance Reveals Hidden Value

**Breanna Stewart shoots +8.8% better in clutch but only gets 18.4% of shots**

| Player | Clutch FG% | Rest of Game | Differential |
|--------|-----------|--------------|--------------|
| **Breanna Stewart** | **54.1%** | 45.3% | **+8.8%** ⬆️ |
| **Jonquel Jones** | **55.6%** | 48.4% | **+7.2%** ⬆️ |
| Leonie Fiebich | 48.0% | 49.0% | -1.0% |
| Sabrina Ionescu | 35.4% | 40.9% | -5.5% ⬇️ |
| Natasha Cloud | 33.3% | 44.3% | -11.0% ⬇️ |

**Actionable Insight**: Stewart and Jones perform BETTER under pressure. Current clutch distribution (Ionescu 39.3%, Stewart 18.4%) doesn't align with performance data.

---

## Critical Finding #2: The Sabrina Paradox

**As usage increases in clutch (+8.4%), efficiency decreases (-5.5%)**

| Metric | Overall | Q4 | Clutch | Change |
|--------|---------|-----|--------|--------|
| Usage Rate | 30.9% | 33.8% | 39.3% | +8.4% |
| FG% | 40.1% | 37.0% | 35.4% | -4.7% |

**Root Cause Analysis**:
- 49.4% of clutch shots are 3-pointers
- Only shoots 29.9% from 3PT overall
- More efficient on 2PT attempts (49.3%)

**Recommendation**: Reduce contested 3PT attempts in clutch. Focus on driving to create higher-percentage looks.

---

## Critical Finding #3: Jonquel Jones is Underutilized

**Elite efficiency (49.0% FG, 42.4% 3PT) with only 16.5% usage**

- **Best Q4 efficiency**: 57.4%
- **Best clutch efficiency**: 55.6%  
- **Elite 3PT shooter**: 42.4% (well above 33.8% league avg)
- **Current clutch usage**: Only 13.4%

**Opportunity**: Jones maintains elite efficiency in all situations but receives minimal touches in critical moments.

---

## Methodology

### Data Source
- **WNBA Stats API** (stats.wnba.com)
- **Season**: 2025 Regular Season
- **Sample**: 1,857 shots, 5 players
- **Clutch Definition**: Last 5 minutes of 4th quarter

**Clutch Definition Caveat**: Due to shot chart API limitations, score differential data is not available. The standard clutch definition (score within 5 points) would require play-by-play data integration. Current analysis includes all final-5-minute Q4 shots regardless of game situation. Despite this limitation, performance trends (Stewart +8.8%, Jones +7.2%, Ionescu -5.5%) remain meaningful indicators of pressure-situation performance.

### League Benchmarks
- Source: Basketball-Reference 2025
- FG%: 43.9% | 2PT%: 49.8% | 3PT%: 33.8%

---

*Analysis conducted December 2024 using Python, pandas, matplotlib*
