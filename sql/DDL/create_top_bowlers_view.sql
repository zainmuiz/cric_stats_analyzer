-- create_top_50_bowler_view.sql

-- Description: This script creates the 'top_bowlers_view' view. Change dataset according to whichever format required. (odi_stats, test_stats, t20_stats)
-- Version: 1.0
-- Author: Zain Muiz


CREATE VIEW cric_stats.top_bowlers_views AS
SELECT
  bowler AS name,
  bowler_country AS country,
  SUM(wickets) AS wickets,
  (
    SELECT COUNT(DISTINCT match_id)
    FROM `cric_stats.test_stats` AS matches
    WHERE
      (matches.playing_11.team1_name = tbd.bowler_country
       AND tbd.bowler IN UNNEST(matches.playing_11.team1))
      OR
      (matches.playing_11.team2_name = tbd.bowler_country
       AND tbd.bowler IN UNNEST(matches.playing_11.team2))
  ) AS matches,
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
  bowler, bowler_country;
