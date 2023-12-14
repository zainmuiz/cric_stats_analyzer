-- create_top_batsmen_view.sql

-- Description: This script creates the 'top_batsman_view' view. Change dataset according to whichever format required. (odi_stats, test_stats, t20_stats)
-- Version: 1.0
-- Author: Zain Muiz


CREATE VIEW cric_stats.top_50_batsmen_views AS
SELECT
  batsman AS name,
  batsman_country AS country,
  SUM(runs) AS runs,
  (
    SELECT COUNT(DISTINCT match_id)
    FROM `cric_stats.test_stats` AS matches
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
GROUP BY batsman, batsman_country;