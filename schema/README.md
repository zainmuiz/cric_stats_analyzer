# <h3 align="left"> Schema Folder - Cric Stat Analyzer 🏏 </h3>

<hr>

The "schema" folder in this repository contains crucial information about the dataset, table, and view schemas used in the Cric Stat Analyzer project. This information is essential for understanding the structure and organization of the data in Google BigQuery. Below is a detailed guide to the contents of this folder.

## Dataset Schema

The dataset schema provides an overview of the structure of the datasets used in Cric Stat Analyzer. Each dataset corresponds to a specific category or type of cricket match data. The dataset schema documentation outlines the purpose and organization of the datasets.

- [**Dataset Schema Documentation**](./dataset_schema.md)

## Table Schemas

Table schemas define the structure of individual tables within the datasets. These tables store specific types of cricket match statistics and related information. The table schema documentation provides details about the columns, data types, and descriptions of each field in the tables.

### List of Table Schemas:

1. [**Stats Table Schema**](./tables/stats_table_schema.md)
   - Schema for the primary stats table containing cricket match statistics.
   - Distinct tables exist for each format (ODI, Test, T20), sharing the same schema.
2. [**Upload Info Table Schema**](./tables/upload_info_table_schema.md)
   - Schema for the table storing information about each uploaded match file, such as duration and timestamps.

### Note:

The same schema is maintained across all three formats (ODI, Test, T20) for the corresponding tables.

## View Schemas

View schemas define the structure of virtual views created in BigQuery. These views offer aggregated or specialized perspectives on the raw match data stored in the tables. The view schema documentation outlines the purpose and structure of each view.

### List of View Schemas:

1. [**Top Batsmen View Schema**](./views/top_batsmen_view_schema.md)

   - Schema for the view displaying statistics of the top batsmen respective to each format.
   - Fields include player name, country, runs, matches, batting average, and more.

2. [**Top Bowlers View Schema**](./views/top_bowlers_view_schema.md)

   - Schema for the view showcasing statistics of the top 50 bowlers respective to each format.
   - Fields include player name, country, runs, matches, bowling average, and more.

3. [**Top Allrounders View Schema**](./views/top_allrounders_view_schema.md)
   - Schema for the view presenting statistics of the top 50 all-rounders respective to each format.
   - Fields encompass player name, country, runs, matches, batting average, bowling average, and more.

### Note:

The same schema is maintained across all three formats (ODI, Test, T20) for the corresponding views.

This documentation provides comprehensive insights into the structure and organization of the datasets, tables, and views in Cric Stat Analyzer's BigQuery environment.
