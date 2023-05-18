from firebase_admin import credentials, initialize_app, storage
import os

# Create a credential instance
cred = credentials.Certificate(os.environ.get("FIREBASE_CREDENTIALS"))

# Initialize the app with a service account, granting admin privileges
default_app = initialize_app(
    cred,
    {
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
    },
)


# Create a class to manage the bucket
class FirebaseBucket:
    def __init__(self):
        # Recibe mi bucket
        self.bucket = storage.bucket()

    def upload_file(self, file, filename):
        # blob(filename) -> find or create
        blob = self.bucket.blob(filename)
        blob.upload_from_file(file)
        blob.make_public()
        if blob.public_url:
            return blob.public_url
        else:
            return False

    def delete_file(self, filename):
        blob = self.bucket.blob(filename)
        blob.delete()
        return True


# Instance of the class
firebase_bucket = FirebaseBucket()
