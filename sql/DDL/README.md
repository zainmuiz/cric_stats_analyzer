# <h4 align="left"> DDL (Data Definition Language) Folder - Cric Stat Analyzer 🏏 </h4>

<hr>

This folder contains Data Definition Language (DDL) scripts for defining the structure of database objects related to cricket statistics. The DDL scripts are specifically designed for views of three entities: Top Batsmen, Top Bowlers, and Top Allrounders.

## Files:

### 1. [create_top_batsmen_views.sql](./create_top_batsmen_view.sql)

This script defines the schema, analysis and storage information about the top batsmen . It includes details such as the player's name, country, runs, matches played, batting average, and more. [Check Schema Here](../../schema/views/top_batsmen_view.md)

### 2. [create_top_bowlers_views.sql](./create_top_bowlers_view.sql)

This script defines the schema, analysis and storage information about the top bowlers. Key attributes covered include the player's name, country, runs, matches played, bowling average, and other relevant statistics. [Check Schema Here](../../schema/views/top_bowler_view.md)

### 3. [create_top_all_rounders_views.sql](./create_top_all_rounders_views.sql)

This script defines the schema, analysis and storage information about the top bowlers. This includes information about their batting and bowling performances, providing a comprehensive overview of their skills. [Check Schema Here](../../schema/views/top_all_rounder_view.md)

## How to Use:

1. Execute these DDL scripts in your database management system to create the necessary views for storing top batsmen, bowlers, and all-rounders data.

2. Ensure that the database connection parameters within the scripts match your environment.

3. After successful execution, you will have the required views with data to analyze cricket statistics.

Note: These DDL scripts assume the existence of related tables or views, so make sure your database environment is set up accordingly. [Check Dataset Schema Here](../../schema/dataset_schema.md)
