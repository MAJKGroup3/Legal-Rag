import boto3
from botocore.exceptions import BotoCoreError, ClientError

class SimpleS3Manager:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name="us-east-1"):
        try:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
            )
        except (BotoCoreError, ClientError) as e:
            print(f"Error initializing S3 client: {e}")
            self.s3_client = None


    def upload_file(self, bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream"):
        if not self.s3_client:
            print("S3 client not initialized.")
            return
        try:
            self.s3_client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
            print(f"Uploaded {key} to bucket {bucket}")
        except (BotoCoreError, ClientError) as e:
            print(f"Error uploading file {key}: {e}")


    def list_objects(self, bucket: str, prefix: str = ""):
        if not self.s3_client:
            print("S3 client not initialized.")
            return []
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            contents = response.get("Contents", [])
            keys = [obj["Key"] for obj in contents]
            print(f"Found {len(keys)} objects in bucket {bucket}")
            return keys
        except (BotoCoreError, ClientError) as e:
            print(f"Error listing objects in bucket {bucket}: {e}")
            return []


    def delete_object(self, bucket: str, key: str):
        if not self.s3_client:
            print("S3 client not initialized.")
            return
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=key)
            print(f"Deleted {key} from bucket {bucket}")
        except (BotoCoreError, ClientError) as e:
            print(f"Error deleting file {key}: {e}")


if __name__ == "__main__":
    AWS_ACCESS_KEY_ID = "XXX"
    AWS_SECRET_ACCESS_KEY = "XXX"
    BUCKET_NAME = "sample-bucket"

    s3 = SimpleS3Manager(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    s3.upload_file(BUCKET_NAME, "test.txt", b"Hello World of S3!", content_type="text/plain")
    keys = s3.list_objects(BUCKET_NAME)
    print("Objects in bucket:", keys)
    s3.delete_object(BUCKET_NAME, "test.txt")
