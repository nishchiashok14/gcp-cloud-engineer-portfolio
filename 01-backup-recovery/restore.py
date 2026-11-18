from google.cloud import storage

# Connect to Google Cloud
client = storage.Client()

# GCP bucket name
BUCKET_NAME = "project-04354dfd-b58a-4510-a66-backup"

# File to restore
FILE_NAME = "sample.txt"

# First version's generation ID
GENERATION_ID = 1794989285953264

# Get the bucket
bucket = client.bucket(BUCKET_NAME)

# Select the required file generation
blob = bucket.blob(FILE_NAME, generation=GENERATION_ID)

# Download the old version
blob.download_to_filename("restored_sample.txt")

print("Previous backup version restored successfully!")
