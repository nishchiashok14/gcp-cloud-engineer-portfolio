
from google.cloud import storage

# 1. Connect to Google Cloud
client = storage.Client()

# 2. Enter your bucket name
BUCKET_NAME = "YOUR_BUCKET_NAME"

# 3. Select the local file
FILE_PATH = "sample.txt"

# 4. Select the name for the uploaded file
DESTINATION_NAME = "sample.txt"

# 5. Get the Cloud Storage bucket
bucket = client.bucket(BUCKET_NAME)

# 6. Create an object reference
blob = bucket.blob(DESTINATION_NAME)

# 7. Upload the file
blob.upload_from_filename(FILE_PATH)

print("Backup uploaded successfully!")

