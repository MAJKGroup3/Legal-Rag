import boto3
from app.core.config import Config

class S3Manager:
    def __init__(self):
        #credentials from config
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION,
        )


    def create_buckets(self):
        for bucket_name in [Config.RAW_BUCKET, Config.PROCESSED_BUCKET]:
            try:
                #check if exists
                self.s3_client.head_bucket(Bucket=bucket_name)
            except Exception:
                try:
                    #create if doesnt exist
                    if Config.AWS_REGION == "us-east-1":
                        self.s3_client.create_bucket(Bucket=bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=bucket_name,
                            CreateBucketConfiguration={
                                "LocationConstraint": Config.AWS_REGION
                            },
                        )
                except Exception as e:
                    print(f"Error creating bucket {bucket_name}: {e}")


    def upload_file(self, bucket: str, key: str, data: bytes, content_type: str):
        self.s3_client.put_object(
            Bucket=bucket, Key=key, Body=data, ContentType=content_type
        )


    def list_objects(self, bucket: str, prefix: str = ""):
        try:
            #list all objects in bucket, with optional prefix
            response = self.s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            return response.get("Contents", [])
        except Exception:
            return []


    def delete_object(self, bucket: str, key: str):
        self.s3_client.delete_object(Bucket=bucket, Key=key)
