# <h4 align="left"> View Schema: Top Batsmen [ ODI, Test, T20 ] 🏏 </h4>

<hr>

This document provides the schema for the 'top_50_batsmen_view' in the project. The schema is consistent across all three cricket formats (ODI, Test, T20). SEE [USAGE](#usage)

## Schema

**View Name : top_50_batsmen_view** [Find Schema JSON here](./top_batsmen_view.json)

- **name** (STRING): Name of the batsman.

- **country** (STRING): Country of the batsman.

- **runs** (INTEGER): Total runs scored by the batsman.

- **matches** (INTEGER): Total matches played by the batsman.

- **batting_innings** (INTEGER): Number of innings the batsman has batted.

- **batting_avg** (FLOAT): Batting average of the batsman.

- **batting_strike_rate** (FLOAT): Batting strike rate of the batsman.

- **hundred** (INTEGER): Number of centuries scored by the batsman.

- **fifties** (INTEGER): Number of half-centuries scored by the batsman.

- **best_batting** (INTEGER): Highest score in a single inning by the batsman.

## USAGE

- Can be used to **[QUERY](../../sql/DML/top_50_batsmen.sql** Top 50 batsman. **CRITERIA** : RUNS.
