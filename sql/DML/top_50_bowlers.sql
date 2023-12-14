-- top_50_bowlers.sql

-- Description: This script queries the 'top_50_bowlers' from 'top_bowler_view'. Change dataset according to whichever format required. (odi_stats, test_stats, t20_stats)
-- Pre-Requisites: Ensure you have the top_batsman_view setup. DDL can be found at '../DDL/'
-- Version: 1.0
-- Author: Zain Muiz



SELECT
   *
FROM
   `cric_stats.top_bowlers_views`
ORDER BY
   wickets DESC
LIMIT 50;
