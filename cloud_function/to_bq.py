from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import logging
import smtplib
import threading
from google.cloud import storage, bigquery
import yaml
import os
from datetime import datetime
import csv
import json
from dotenv import load_dotenv
import xmltodict
from google.cloud import secretmanager

# Get the current date and time
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
load_dotenv()

# Configure logging with the current date and time
log_file_name = f'error_log_{current_datetime}.txt'
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Define project_id, dataset_id, and table_id
project_id = os.getenv("PROJECT_ID")
dataset_id = os.getenv("DATASET_ID")

# Formats
formats = ["test", "odi", "t20"]

# Global variables to store existing matches and new match entries
existing_matches_test = []
existing_matches_odi = []
existing_matches_t20 = []
match_entries = []

# List to store error messages for email notification
error_messages = []

file_refactor_threads = []


# List all files in the GCS bucket.
def list_gcs_blobs(format):
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        storage_client = storage.Client(project=project_id)
        # Lists all files inside the bucket/folder
        blobs = storage_client.list_blobs(bucket_name, prefix=format)
        logging.info('Match files fecthed from bucket - %s', format)

        for blob in blobs:
            t = threading.Thread(target=refactor_file, args=[blob, format])
            t.start()
            file_refactor_threads.append(t)

        for thread in file_refactor_threads:
            thread.join()

        if not len(match_entries):
            print("No new matches to add")
            logging.info('No new matches to add')
    except Exception as e:
        logging.error(f"Error listing GCS blobs: {e}")
        error_messages.append(datetime.now().strftime(
            "%Y%m%d_%H%M%S") + f":ERROR: Error listing GCS blobs: {e}")


# Get existing match entries from BigQuery
def get_existing_matches(format):
    try:
        client = bigquery.Client(project=project_id)
        # Perform a query.
        QUERY = (
            f'SELECT DISTINCT `match_id` FROM `sada-seed-2023.cric_stats.{format}_stats` '
        )
        query_job = client.query(QUERY)  # API request
        rows = query_job.result()  # Waits for the query to finish
        existing_matches = globals().get(f"existing_matches_{format}")
        for row in rows:
            existing_matches.append(row.match_id)
    except Exception as e:
        logging.error(f"Error getting existing matches from BigQuery: {e}")
        print(f"Error getting existing matches from BigQuery: {e}")
        error_messages.append(datetime.now().strftime("%Y%m%d_%H%M%S") +
                              f":ERROR: Error getting existing matches from BigQuery: {e}")
        return 0


# Refactor files based on their format (JSON, CSV, XML)
def refactor_file(blob, format):
    try:
        # Detect file type based on the extension
        file_extension = blob.name.split('.')[-1].lower()
        print(blob.name)
        with blob.open('r') as f:
            if not blob.name.endswith('/') and "archive" not in blob.name:
                logging.info("Processing file with filename %s", blob.name)
                if file_extension in ["yaml", "yml"]:
                    match = yaml.safe_load(f)
                elif file_extension == "csv":
                    match = csv.DictReader(f)
                elif file_extension == "xml":
                    match = xmltodict.parse(f.read())
                elif file_extension == "json":
                    match = json.load(f)
                else:
                    logging.error(f"Unsupported file type: {file_extension}")
                    error_messages.append(
                        f"ERROR: Unsupported file type: {file_extension}")
                    return

                match_id = ""
                if not "match_type_number" in match["info"]:
                    match_id = blob.name.split('.')[0].split('/')[1]
                else:
                    match_id = match["info"]["match_type_number"]

                if check_existing_match(match_id, blob.name, format):
                    ball_entries = []
                    for a in match["innings"]:
                        for z, x in a.items():
                            for y in x["deliveries"]:
                                for key, val in y.items():
                                    batsman_country = find_player_country(
                                        match["info"]["players"].items(
                                        ), val["batsman"]
                                    )
                                    bowler_country = find_player_country(
                                        match["info"]["players"].items(
                                        ), val["bowler"]
                                    )
                                    ball_entry = {
                                        "ball": key,
                                        **val,
                                        "batsman_country": batsman_country,
                                        "bowler_country": bowler_country,
                                        "innings": z,
                                    }
                                    ball_entries.append(ball_entry)

                    count = 1
                    playing_teams = {}

                    for key, value in match["info"]["players"].items():
                        playing_teams.update(
                            {"team" + str(count) + "_name": key})
                        playing_teams.update({"team" + str(count): value})
                        count = count + 1
                    dates = []
                    for date in match["info"]["dates"]:
                        dates.append(str(date))
                    match_entry = [{
                        "match_id": match_id,
                        "dates": dates,
                        "playing_11": playing_teams,
                        "ball_data": ball_entries,
                    }]

                    match_entries.append(match_entry)
                    existing_matches = globals().get(
                        f"existing_matches_{format}")
                    existing_matches.append(match_id)
                    load_match_to_bq(match_entry, blob.name, format)

    except Exception as e:
        logging.error(f"Error reading file or refactoring: {e}")
        error_messages.append(datetime.now().strftime(
            "%Y%m%d_%H%M%S") + f":ERROR: Error reading file or refactoring: {e}")


# Checks if match already exists in BigQuery
def check_existing_match(match_id, blob_name, format):
    try:
        existing_matches = globals().get(f"existing_matches_{format}")
        if match_id in existing_matches:
            logging.info(
                "The match_id %s of %s with FileName %s already exists", match_id, format, blob_name)
            print(
                f"The match_id {match_id} of {format} with FileName {blob_name} already exists"
            )
            move_blob_to_archive(blob_name)
            return False
        else:
            return True
    except Exception as e:
        logging.error(f"Error checking existing match: {e}")
        error_messages.append(datetime.now().strftime(
            "%Y%m%d_%H%M%S") + f":ERROR: Error checking existing match: {e}")
        return False


# Loads new entries in BQ.
def load_match_to_bq(match, blob_name, format):
    try:
        # Create a BigQuery client
        client = bigquery.Client(project=project_id)
        table_id = str(format) + "_stats"
        # Specify the dataset and table to upload the data
        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        info_table_ref = dataset_ref.table("upload_info")
        upload_file_info = {"file_name": blob_name,
                            "match_id": match[0]["match_id"]}

        # Load the JSON file into BigQuery
        job_config = bigquery.LoadJobConfig()
        job_config.schema_update_options = [
            bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
        ]
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.autodetect = True

        upload_start_time = datetime.now()
        upload_file_info.update(
            {"upload_start_time": upload_start_time.strftime("%Y%m%d_%H%M%S")})

        # Loading to Big Query table from JSON
        job = client.load_table_from_json(
            match, table_ref, job_config=job_config
        )
        # Waiting for the job to complete
        job.result()
        logging.info("Loaded %s rows into %s", job.output_rows, table_id)
        print(f"Loaded {job.output_rows} rows into {table_id}")
        upload_end_time = datetime.now()

        move_blob_to_archive(blob_name)

        upload_file_info.update(
            {"upload_end_time": upload_end_time.strftime("%Y%m%d_%H%M%S")})
        upload_duration = (upload_end_time - upload_start_time).total_seconds()
        upload_file_info.update({"upload_duration_seconds": upload_duration})

        job = client.load_table_from_json(
            [upload_file_info], info_table_ref, job_config=job_config
        )

        job.result()  # Waiting for the job to complete

    except Exception as e:
        logging.error(f"Error loading matches to BigQuery: {e}")
        error_messages.append(datetime.now().strftime(
            "%Y%m%d_%H%M%S") + f":ERROR: Error loading matches to BigQuery: {e}")


# Function for moving files between directories or buckets. it will use GCP's copy function then delete the blob from the old location.
def move_blob_to_archive(blob_name):
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        source_blob = bucket.blob(blob_name)
        if 'odi' in source_blob.name:
            destination_folder = bucket.blob("odi_archive/")
        if 'test' in source_blob.name:
            destination_folder = bucket.blob("test_archive/")
            print("hello")
        if 't20' in source_blob.name:
            destination_folder = bucket.blob("t20_archive/")

        new_blob_name = (
            destination_folder.name + source_blob.name.split('/', 1)[1]
        )  # Split function strips source folder name from the File Name.

        destination_blob = storage_client.bucket(
            bucket_name).blob(new_blob_name)
        if destination_blob.exists():
            # If it exists, generate a new unique name by appending a timestamp or some other identifier
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_blob_name = f"{destination_folder.name}{timestamp}_{source_blob.name.split('/')[-1]}"
        # copy to new destination

        new_blob = bucket.copy_blob(source_blob, bucket, new_blob_name)
        # delete in old destination
        source_blob.delete()

        print(f"File moved from {source_blob} to {new_blob_name}")
        logging.info("File moved from %s to %s", source_blob, new_blob_name)
    except Exception as e:
        logging.error(f"Error moving blob to archive: {e}")
        error_messages.append(datetime.now().strftime("%Y%m%d_%H%M%S")
                              + f":ERROR: Error moving blob to archive: {e}")


# Find batsman country
def find_player_country(players, player):
    try:
        for team_name, player_names in players:
            for player_name in player_names:
                if player in player_name:
                    return team_name
    except Exception as e:
        logging.error(f"Error finding player country: {e}")
        error_messages.append(f"ERROR: Error finding player country: {e}")


# Function to send a consolidated email notification for all errors
def send_email_notification():
    if error_messages:
        try:
            sender_email = os.getenv("SENDER_EMAIL")
            receiver_email = os.getenv("RECEIVER_EMAIL")
            secret_id = os.getenv("SECRET_ID")
            secret_version = os.getenv("SECRET_VERSION")
            password = (access_secret(project_id, secret_id, secret_version))

            msg = MIMEMultipart()
            msg['Subject'] = 'Error Notification : Cric Stat Analyzer'
            msg['From'] = sender_email
            msg['To'] = receiver_email
            error_string = "\n".join(error_messages)

            # Create MIMEApplication using the BytesIO object
            part = MIMEApplication(error_string)

            # After the file is closed
            part.add_header('Content-Disposition', 'attachment',
                            filename='error_file.txt')
            msg.attach(part)

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                logging.info(
                    "Error Notification Email Sent to %s", receiver_email)
                print(f"Error Notification Email Sent to {receiver_email}")
        except Exception as e:
            logging.error(f"Error sending email notification: {e}")
            print(f"Error sending email notification: {e}")


# Check if any errors are logged before sending the email
def check_and_send_email_notification():
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        if len(error_messages):
            client = storage.Client(project_id)
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob("error_logs/" + log_file_name)
            with blob.open(mode='w') as f:
                for line in error_messages:
                    f.write(line)
            send_email_notification()
        else:
            logging.info(
                "Execution successfully completed. No errors found.")
            print("Execution successfully completed. No errors found.")
    except Exception as e:
        logging.error(f"Error checking log file and sending email: {e}")
        print(f"Error checking log file and sending email: {e}")


# Accesing secrets from GCS Secret Manager
def access_secret(project_id, secret_id, version):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, version)
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode('UTF-8')
    return payload


# Cloud Function Entry Point
def to_bq():

    for format in formats:
        get_existing_matches(format)
        list_gcs_blobs(format)

    for thread in file_refactor_threads:
        thread.join()

    check_and_send_email_notification()


to_bq()
