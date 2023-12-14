# <h4 align="left"> View Schema: Top Bowlers [ ODI, Test, T20 ] 🏏 </h4>

<hr>

This document provides the schema for the 'top_50_bowler_view' in the project. The schema is consistent across all three cricket formats (ODI, Test, T20). SEE [USAGE](#usage)

##

**View Name : top_bowlers_view** [Find Schema JSON here](./top_bowlers_view.json)

- **name** (STRING): Name of the bowler.

- **country** (STRING): Country of the bowler.

- **wickets** (INTEGER): Total wickets taken by the bowler.

- **matches** (INTEGER): Total matches played by the bowler.

- **bowling_innings** (INTEGER): Number of innings bowled by the player.

- **bowling_avg** (FLOAT): Bowling average of the bowler, calculated as total runs conceded divided by total wickets taken.

- **economy_rate** (FLOAT): Bowling economy rate of the bowler, calculated as average runs conceded per over bowled.

- **bowling_strike_rate** (FLOAT): Bowling strike rate of the bowler, representing the number of balls bowled per wicket taken.

- **five_fors** (INTEGER): Number of times the bowler took five or more wickets in an innings.

- **best_bowling** (INTEGER): Best bowling figures in a single inning by the bowler.

## USAGE

- Can be used to **[QUERY]**(../../sql/DML/top_50_bowlers.sql) Top 50 bowlers. **CRITERIA**: WICKETS
