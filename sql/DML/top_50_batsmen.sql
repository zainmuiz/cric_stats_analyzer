-- top_50_batsmen.sql

-- Description: This script queries the 'top_50_batsman' from 'top_batsman_view'. Change dataset according to whichever format required. (odi_stats, test_stats, t20_stats)
-- Pre-Requisites: Ensure you have the top_batsman_view setup. DDL can be found at '../DDL/'
-- Version: 1.0
-- Author: Zain Muiz


SELECT
   *
FROM
   `cric_stats.top_batsmen_views`
ORDER BY
   runs DESC
LIMIT 50;
