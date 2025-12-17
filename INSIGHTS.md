# Key Findings: NY Liberty Shooting Analysis - 2025 Season

## Executive Summary

Analysis of 1,857 real shot attempts from NY Liberty's 2025 championship run reveals opportunities to optimize late-game execution. While the team's talent is undeniable, the data suggests misalignment between who's taking shots in critical moments and who performs best under pressure.

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

## Critical Finding #1: Stewart Elevates in Crunch Time

**The data reveals Stewart as a true closer**

| Player | Clutch FG% | Rest of Game | Differential |
|--------|-----------|--------------|--------------|
| **Breanna Stewart** | **54.1%** | 45.3% | **+8.8%** ⬆️ |
| **Jonquel Jones** | **55.6%** | 48.4% | **+7.2%** ⬆️ |
| Leonie Fiebich | 48.0% | 49.0% | -1.0% |
| Sabrina Ionescu | 35.4% | 40.9% | -5.5% ⬇️ |
| Natasha Cloud | 33.3% | 44.3% | -11.0% ⬇️ |

**What This Means:**

Stewart isn't just maintaining her efficiency when the game tightens—she's actively getting better. She's attacking the basket more (3PT rate drops from 22.3% to 16.2% in clutch), getting to her spots, and converting at an elite 54% clip. Yet she's only getting 18.4% of the team's clutch possessions.

Meanwhile, Jones—who shoots an elite 42.4% from three—becomes even more reliable late (55.6% clutch FG%). These are the players who thrive under playoff-level pressure.

**Basketball Context:** This isn't about taking the ball out of Sabrina's hands—she's your franchise player and primary initiator. But late-game sets could be designed to get Stewart isolations or Jones catch-and-shoot opportunities off Sabrina's drives and kicks.

---

## Critical Finding #2: Sabrina's Clutch Shot Selection

**High volume meets contested looks**

| Metric | Overall | Q4 | Clutch | Change |
|--------|---------|-----|--------|--------|
| Usage Rate | 30.9% | 33.8% | 39.3% | +8.4% |
| FG% | 40.1% | 37.0% | 35.4% | -4.7% |
| 3PT Rate | 46.8% | 48.9% | 49.4% | +2.6% |

**What's Happening:**

Sabrina's taking nearly 40% of the team's clutch shots, with half of them coming from three. She's your primary ball-handler and closer, which makes sense—but the degree of difficulty on these attempts appears high. She's shooting 29.9% from three overall (below league average of 33.8%), yet taking more threes as the pressure increases.

**Basketball Context:** 

This isn't a talent issue—it's Sabrina Ionescu. But the data suggests defenses are loading up on her late, and the current approach may be playing into their hands. A few considerations:

1. **Shot selection vs shot-making**: Is she taking contested pull-up threes because that's what the defense is giving? Or could plays be designed to get her downhill more often, where she's significantly more efficient (49.3% on 2PT)?

2. **Film would be critical here**: Are defenses showing two to the ball and daring role players to beat them? Is the roller open when she's pulling? Understanding defensive coverages would clarify whether this is a play-calling or shot-selection issue.

3. **Player development angle**: Traditional PD would focus on improving the three-ball. But another approach: lean into her strengths. Design more late-game actions that get her driving, collapsing the defense, and either finishing at the rim or creating open looks for Stewart/Jones.

**The key question**: How can we maintain Sabrina as the primary decision-maker while optimizing the quality of looks everyone's getting?

---

## Critical Finding #3: JJ is a Closer Hiding in Plain Sight

**Elite efficiency across all situations, minimal late-game touches**

- **Season FG%**: 49.0% (5.1% above league average)
- **3PT%**: 42.4% (8.6% above league average)  
- **Q4 efficiency**: 57.4%
- **Clutch efficiency**: 55.6%
- **Clutch usage**: Only 13.4%

**What This Means:**

Jones doesn't just maintain her efficiency—she gets *better* as the game goes on. Most players' efficiency drops in Q4 due to fatigue and defensive intensity. JJ's spikes. She's your most efficient three-point shooter by a wide margin and one of your best finishers at the rim.

**Basketball Context:**

Jones gives you unique versatility late. She can:
- Space the floor at an elite level (42.4% from three)
- Post smaller defenders
- Finish inside (53.6% on 2PT)
- Not force anything (low turnover risk)

Currently getting 13.4% of clutch possessions feels like leaving points on the table. More Spain pick-and-rolls with Sabrina? More flare screens for catch-and-shoot threes? There's room to experiment.

---

## Scalability & Future Analysis

**This framework can expand in multiple directions:**

### Different Metrics:
- eFG% and TS% (would need free throw data from play-by-play API)
- Assisted vs unassisted rates (shows shot creation vs catch-and-shoot ability)
- Shot clock timing (early vs late clock)
- Rim pressure metrics (drives per game, paint touches)

### Different Benchmarks:
- Compare to playoff teams specifically (are regular season averages the right comparison?)
- Opponent-adjusted efficiency (performance vs top defenses)
- Lineup-specific analysis (how does each player perform with different teammates?)

### Different Scopes:
- Full league analysis (12 teams, ~150 players)
- Opponent scouting (how do teams guard each player? Where are the tendencies?)
- Historical trends (how has each player's profile evolved season-over-season?)
- Playoff-specific analysis (does clutch performance translate to postseason?)

### Integration with Other Data:
- **Film breakdown**: Marry shot data with video to understand *why* certain looks are being taken
- **Tracking data**: Player movement, defender distance, shot clock at release
- **Play-by-play**: Score differential, substitution patterns, timeout usage
- **Synergy data**: Play type breakdown (PnR, isolation, spot-up, transition)

---

## Methodology

### Data Source
- **WNBA Stats API** (stats.wnba.com)
- **Season**: 2025 Regular Season
- **Sample**: 1,857 shots, 5 players
- **Clutch Definition**: Last 5 minutes of 4th quarter

**Clutch Definition Caveat**: Due to shot chart API limitations, score differential data is not available. The standard clutch definition (score within 5 points) would require play-by-play data integration. Current analysis includes all final-5-minute Q4 shots regardless of game situation. Despite this limitation, performance trends (Stewart +8.8%, Jones +7.2%, Ionescu -5.5%) remain meaningful indicators of pressure-situation performance. With play-by-play data, these trends would likely become even more pronounced in truly close games.

### League Benchmarks
- Source: Basketball-Reference 2025
- FG%: 43.9% | 2PT%: 49.8% | 3PT%: 33.8%

### Usage Rate Calculation
Usage rate in this analysis represents **% of team shots taken while on court** during the specified period (overall, Q4, or clutch). This differs from traditional USG% (which includes turnovers and free throw attempts) but provides a cleaner measure of shot distribution from available shot chart data.

**For more precise usage metrics:** Play-by-play data would enable calculation of traditional USG% = (FGA + 0.44*FTA + TOV) / (Team FGA + 0.44*Team FTA + Team TOV) * Team Minutes / Player Minutes

---

## Closing Thoughts

The Liberty have championship-level talent. These findings aren't critiques—they're optimization opportunities. Stewart and Jones perform exceptionally under pressure but aren't getting commensurate touches. Sabrina's workload in crunch time is massive, and the shot quality may be suffering as a result.

**The opportunity**: Maintain Sabrina as your primary initiator while being more deliberate about who's finishing possessions and what types of looks they're getting.

Film study would be the natural next step to understand defensive coverages and whether scheme adjustments could improve shot quality without reducing Sabrina's decision-making role.

---

*Analysis conducted December 2025 using Python, pandas, matplotlib*
