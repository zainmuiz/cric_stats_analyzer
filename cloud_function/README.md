# <h3 align="left"> Cric Stat Analyzer 🏏 - Cloud Function</h3>

<hr>

Cric Stat Analyzer is a powerful Python script crafted to elegantly process and analyze cricket match statistics from various formats (Test, ODI, T20). This tool seamlessly refactors the data and orchestrates its smooth migration into BigQuery tables for in-depth analysis.

## Introduction

This script serves as a main component within a system, automating the extraction, transformation, and loading (ETL) process for cricket match statistics.

## Prerequisites

Before using Cric Stat Analyzer Script, ensure you have the following essentials:

- **Google Cloud Storage Bucket:** Match Files to be stored in GCS Bucket.
- **BigQuery Dataset and Tables:** Datasets and Tables to ingest data. Check Dataset and Tables Schemea [Here](../schema/dataset_schema.md)
- **Environment Variables:** Set up crucial variables like `PROJECT_ID`, `DATASET_ID`, `BUCKET_NAME`, etc. Find Env Variable Schema [Here](./sample_env.txt)
- **Python Libraries:** Install the required packages listed in [`requirements.txt`](./requirements.txt).

### Libraries Used

Cric Stat Analyzer Cloud Function is built using several Python libraries and frameworks. Here is a list of the key libraries used:

- **google-cloud-storage:** Enables interaction with Google Cloud Storage for managing and accessing files.

- **google-cloud-bigquery:** Facilitates communication with Google BigQuery to perform queries and load data.

- **yaml:** Allows parsing YAML files, which might be used for cricket match data representation.

- **csv:** The built-in CSV module for working with CSV files during data extraction.

- **json:** The built-in JSON module for parsing and processing JSON files containing cricket match data.

- **xmltodict:** Transforms XML data into a Python dictionary for processing cricket match information.

- **datetime:** A built-in module for handling date and time operations, used for timestamping and durations.

- **csv:** The built-in CSV module for reading CSV files during the ETL process.

- **json:** The built-in JSON module for reading and parsing JSON files during data transformation.

- **dotenv:** Allows loading environment variables from a .env file for configuration.

- **logging:** Provides logging capabilities for tracking errors and informational messages.

- **smtplib:** A library for sending emails, used for error notifications.

- **threading:** Used for multi-threading to enhance file processing efficiency.

- **google.cloud.secretmanager:** Interacts with Google Cloud Secret Manager to securely access credentials.

- **os:** A built-in module for interacting with the operating system, used for accessing environment variables and file operations.

- **yaml:** A library for working with YAML files, which might be utilized for representing configuration data.

These libraries collectively empower Cric Stat Analyzer to efficiently process, analyze, and load cricket match statistics into BigQuery.

## Cloud Function Folder Structure

- **to_bq.py:** The script orchestrating the process of retreival, processing and ingestion of match files.
- **sample.env:** A guide to configuring your environment variables.
- **requirements.txt:** A concise list of Python packages used.

## Functions

### `list_gcs_blobs(format: str)`

- **Arguments:**

  - `format`: The format of the cricket match (e.g., "test", "odi", "t20").

- **Description:**
  - Lists all files inside the specified GCS bucket/folder.
  - Starts a new thread for concurrent file refactoring.

### `get_existing_matches(format: str)`

- **Arguments:**

  - `format`: The format of the cricket match (e.g., "test", "odi", "t20").

- **Description:**
  - Queries BigQuery to fetch distinct match IDs for a given format.
  - Populates global variables with existing match IDs.

### `refactor_file(blob: Blob, format: str)`

- **Arguments:**

  - `blob`: The Google Cloud Storage Blob object representing the file.
  - `format`: The format of the cricket match (e.g., "test", "odi", "t20").

- **Description:**
  - Detects file type based on the extension (JSON, CSV, XML).
  - Refactors each file and extracts relevant information.
  - Checks for existing matches and loads new entries into BigQuery.

### `check_existing_match(match_id: str, blob_name: str, format: str)`

- **Arguments:**

  - `match_id`: The unique identifier of the cricket match.
  - `blob_name`: The name of the Google Cloud Storage Blob.
  - `format`: The format of the cricket match (e.g., "test", "odi", "t20").

- **Description:**
  - Checks if a match already exists in BigQuery based on its ID.
  - Moves the file to the archive if it already exists.

### `load_match_to_bq(match: List[Dict[str, Any]], blob_name: str, format: str)`

- **Arguments:**

  - `match`: List of dictionaries representing match information.
  - `blob_name`: The name of the Google Cloud Storage Blob.
  - `format`: The format of the cricket match (e.g., "test", "odi", "t20").

- **Description:**
  - Loads new entries into the specified BigQuery table.
  - Handles schema updates and autodetection of the schema.

### `move_blob_to_archive(blob_name: str)`

- **Arguments:**

  - `blob_name`: The name of the Google Cloud Storage Blob.

- **Description:**
  - Moves files between directories or buckets using GCP's copy function.
  - Appends a timestamp to the filename if it already exists in the destination.

### `find_player_country(players: Iterable[Tuple[str, List[str]]], player: str)`

- **Arguments:**

  - `players`: Iterable of tuples containing team names and player names.
  - `batsman`: The name of the player to get country informations.

- **Description:**
  - Finds the country of a player based on the provided player list.

### `send_email_notification()`

- **Description:**
  - Sends a consolidated email notification for all errors.
  - Attaches an error log file to the email.

### `check_and_send_email_notification()`

- **Description:**
  - Checks if any errors are logged before sending the email.
  - Writes error messages to a file and sends an email notification.

### `access_secret(project_id: str, secret_id: str, version: str)`

- **Arguments:**

  - `project_id`: Google Cloud project ID.
  - `secret_id`: ID of the secret in Google Cloud Secret Manager.
  - `version`: Version of the secret.

- **Description:**
  - Accesses a secret from Google Cloud Secret Manager.

### `to_bq()`

- **Description:**
  - Orchestrates the entire process for different match formats.
  - Calls relevant functions for each format.
  - Checks for errors and sends email notifications.
