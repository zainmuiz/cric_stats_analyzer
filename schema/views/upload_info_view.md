# <h4 align="left"> View Schema: Upload Info - Cric Stat Analyzer 🏏 </h4>

<hr>

This document provides an overview of the schema for the 'upload_info' view within the project. The 'upload_info' table stores crucial information related to the uploading process of cricket match statistics files. The schema details are outlined below.

## Schema Details

**Table Name: upload_info** [Find Schema JSON here](upload_info_view.json)

- **upload_duration_seconds** (NULLABLE FLOAT): Represents the duration of the file upload process in seconds.

- **upload_end_time** (NULLABLE STRING): Indicates the timestamp when the file upload was completed.

- **upload_start_time** (NULLABLE STRING): Denotes the timestamp when the file upload commenced.

- **match_id** (NULLABLE INTEGER): Serves as a unique identifier for the corresponding match.

- **file_name** (NULLABLE STRING): Contains the name of the file uploaded.

## Usage

\*\*[Find View Query Here]()

The 'upload_info' table captures essential metadata about the file upload process, enabling tracking and analysis of the aspects of data ingestion.
