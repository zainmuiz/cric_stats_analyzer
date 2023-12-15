-- create_top_all_rounders_view.sql

-- Description: This script creates the 'top_all_rounders_view' view. Change dataset according to whichever format required. (odi_stats, test_stats, t20_stats)
-- Version: 1.0
-- Author: Zain Muiz




CREATE VIEW cric_stats.top_all_rounders AS
WITH BatsmanStats AS (
SELECT
  batsman AS name,
  batsman_country AS country,
  SUM(runs) AS runs,
  (
    SELECT COUNT(DISTINCT match_id)
    FROM `cric_stats.${format}_stats` AS matches  -- change ${format} to required Dataset. (odi, test, t20)
    WHERE
      (matches.playing_11.team1_name = tbd.batsman_country
       AND tbd.batsman IN UNNEST(matches.playing_11.team1))
      OR
      (matches.playing_11.team2_name = tbd.batsman_country
       AND tbd.batsman IN UNNEST(matches.playing_11.team2))
  ) AS matches,
  COUNT(DISTINCT CONCAT(match_id, innings)) AS batting_innings,
  COALESCE(ROUND(SUM(runs) * 1.0 / NULLIF(COUNT(DISTINCT CONCAT(match_id, innings)), 0), 2), 0) AS batting_avg,
  COALESCE(ROUND(SUM(runs) * 100.0 / NULLIF(MAX(balls), 0), 2), 0) AS batting_strike_rate,
  SUM(CASE WHEN runs >= 100 THEN 1 ELSE 0 END) AS hundred,
  SUM(CASE WHEN runs >= 50 AND runs < 100 THEN 1 ELSE 0 END) AS fifties,
  MAX(runs) AS best_batting
FROM (
  SELECT
    batsman,
    batsman_country,
    match_id,
    innings,
    SUM(runs.batsman) AS runs,
    MAX(runs.batsman) AS total_runs,
    COUNT(ball_data) AS balls
  FROM
    `cric_stats.${format}_stats`,   -- change ${format} to required Dataset. (odi, test, t20)
    UNNEST(ball_data) AS ball_data
  GROUP BY
    batsman, batsman_country, match_id, innings
) AS tbd
GROUP BY batsman, batsman_country
),

BowlerStats AS (
  SELECT
  bowler AS name,
  bowler_country AS country,
  SUM(wickets) AS wickets,
  (
    SELECT COUNT(DISTINCT match_id)
    FROM `cric_stats.${format}_stats` AS matches   -- change ${format} to required Dataset. (odi, test, t20)
    WHERE
      (matches.playing_11.team1_name = tbd.bowler_country
       AND tbd.bowler IN UNNEST(matches.playing_11.team1))
      OR
      (matches.playing_11.team2_name = tbd.bowler_country
       AND tbd.bowler IN UNNEST(matches.playing_11.team2))
  ) AS matches,
  SUM(tbd.ball) as ball,
  SUM(bowling_innings) AS bowling_innings,
  COALESCE(ROUND(SUM(runs) * 1.0 / NULLIF(SUM(wickets), 0), 2), 0) AS bowling_avg,
  COALESCE(ROUND(SUM(runs) * 6.0 / NULLIF(SUM(ball), 0), 2), 0) AS economy_rate,
  COALESCE(ROUND(SUM(ball) * 1.0 / NULLIF(SUM(wickets), 0), 2), 0) AS bowling_strike_rate,
  SUM(DISTINCT CASE WHEN wickets_innings >= 5 THEN 1 ELSE 0 END) AS five_fors,
  MAX(wickets_innings) AS best_bowling
FROM (
  SELECT
    bowler,
    bowler_country,
    match_id,
    SUM(runs.total) as runs,
    COUNT(DISTINCT CONCAT(match_id, ball_data.innings, ball_data.ball)) AS ball,
    SUM(CASE WHEN ball_data.wicket.kind IS NOT NULL THEN 1 ELSE 0 END) AS wickets,
    COUNT(DISTINCT CONCAT(match_id, ball_data.innings)) AS bowling_innings,
    SUM(CASE WHEN wicket.kind IS NOT NULL THEN 1 ELSE 0 END) AS wickets_innings
  FROM
    `cric_stats.${format}_stats`,   -- change ${format} to required Dataset. (odi, test, t20)
    UNNEST(ball_data) AS ball_data
  GROUP BY
    bowler, bowler_country, match_id, innings
) AS tbd
GROUP BY
  bowler, bowler_country
),

AllRounderStats AS (
  SELECT
    COALESCE(BatsmanStats.name, BowlerStats.name) AS name,
    COALESCE(BatsmanStats.country, BowlerStats.country) AS country,
    COALESCE(BatsmanStats.matches, BowlerStats.matches) AS matches,
    runs,
    batting_innings,
    batting_avg,
    batting_strike_rate,
    hundred,
    fifties,
    best_batting,
    ball AS balls_delivered,
    wickets,
    bowling_innings,
    bowling_avg,
    economy_rate,
    bowling_strike_rate,
    five_fors,
    best_bowling
  FROM
    BatsmanStats
  FULL JOIN
    BowlerStats
  ON
    BatsmanStats.name = BowlerStats.name
    AND BatsmanStats.country = BowlerStats.country
    AND BatsmanStats.matches = BowlerStats.matches
)


SELECT
  name,
  country,
  matches,
  ROUND(
    (runs * (batting_avg / NULLIF(25, 0)) * (batting_strike_rate / NULLIF(60, 0)))
    + (wickets * (35 / NULLIF(bowling_avg, 0)) * (35 / NULLIF(bowling_strike_rate, 0))),
    2
  ) AS points,
  runs,
  batting_innings,
  batting_avg,
  batting_strike_rate,
  hundred,
  fifties,
  best_batting,
  balls_delivered,
  wickets,
  bowling_innings,
  bowling_avg,
  economy_rate,
  five_fors,
  best_bowling,
  
FROM
  AllRounderStats;
