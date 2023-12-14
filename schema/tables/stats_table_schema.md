# <h4 align="left"> Table Schema: Stats - Cric Stat Analyzer 🏏 </h4>

<hr>

This document outlines the schema for the 'stats' table within the project. The 'stats' table is used to store cricket match statistics for three different formats: ODI, Test, and T20. Despite the variations in cricket formats, all three tables share a consistent schema, which is elucidated below.

## Overview

The 'stats' table captures comprehensive details about cricket matches, including player statistics, match events, and relevant contextual information. The schema provides a structured representation of the stored data.

### Table Schema

**Table Name: {format}\_stats** [Find Schema JSON here](stats_table_schema.json)

- **ball_data** (REPEATED RECORD)

  - wicket (NULLABLE RECORD)
    - player_out (NULLABLE STRING)
    - kind (NULLABLE STRING)
    - fielders (REPEATED STRING)
  - extras (NULLABLE RECORD)
    - noballs (NULLABLE INTEGER)
    - legbyes (NULLABLE INTEGER)
    - wides (NULLABLE INTEGER)
  - bowler_country (NULLABLE STRING)
  - batsman_country (NULLABLE STRING)
  - runs (NULLABLE RECORD)
    - total (NULLABLE INTEGER)
    - extras (NULLABLE INTEGER)
    - batsman (NULLABLE INTEGER)
  - non_striker (NULLABLE STRING)
  - bowler (NULLABLE STRING)
  - innings (NULLABLE STRING)
  - batsman (NULLABLE STRING)
  - ball (NULLABLE FLOAT)
  - replacements (NULLABLE RECORD)
    - role (REPEATED RECORD)
      - role (NULLABLE STRING)
      - reason (NULLABLE STRING)
      - out (NULLABLE STRING)
      - in (NULLABLE STRING)

- **playing_11** (NULLABLE RECORD)

  - team2 (REPEATED STRING)
  - team1 (REPEATED STRING)
  - team2_name (NULLABLE STRING)
  - team1_name (NULLABLE STRING)

- **dates** (REPEATED DATE)
- **match_id** (NULLABLE INTEGER)
