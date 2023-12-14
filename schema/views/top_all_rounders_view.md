# <h4 align="left"> View Schema: Top Allrounders [ ODI, Test, T20 ] 🏏 </h4>

<hr>

This document provides the schema for the 'top_allrounders_view' in the project. The schema is consistent across all three cricket formats (ODI, Test, T20). SEE [USAGE](#usage)

## Schema

**View Name : top_50_allrounders_view** [Find Schema JSON here](./top_all_rounder_view.json)

- **name** (STRING): Name of the all-rounder.

- **country** (STRING): Country of the all-rounder.

- **matches** (INTEGER): Total matches played by the all-rounder.

- **runs** (INTEGER): Total runs scored by the all-rounder.

- **batting_innings** (INTEGER): Number of innings batted by the player.

- **batting_avg** (FLOAT): Batting average of the all-rounder, calculated as total runs divided by total times dismissed.

- **batting_strike_rate** (FLOAT): Batting strike rate of the all-rounder, representing the number of runs scored per 100 balls faced.

- **hundred** (INTEGER): Total centuries scored by the all-rounder.

- **fifties** (INTEGER): Total half-centuries scored by the all-rounder.

- **best_batting** (INTEGER): Best batting performance by the all-rounder.

- **balls_delivered** (INTEGER): Total number of balls bowled by the all-rounder.

- **wickets** (INTEGER): Total wickets taken by the all-rounder.

- **bowling_innings** (INTEGER): Number of innings bowled by the all-rounder.

- **bowling_avg** (FLOAT): Bowling average of the all-rounder, calculated as total runs conceded divided by total wickets taken.

- **economy_rate** (FLOAT): Bowling economy rate of the all-rounder, calculated as average runs conceded per over bowled.

- **five_fors** (INTEGER): Number of times the all-rounder took five or more wickets in an innings.

- **best_bowling** (INTEGER): Best bowling figures in a single inning by the all-rounder.

## USAGE

- Can be used to **[QUERY](../../sql/DML/top_50_all_rounders.sql)** Top 50 all rounders. **CRITERIA**: POINTS.
