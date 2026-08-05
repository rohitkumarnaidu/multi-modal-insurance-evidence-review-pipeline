# Stub for AWS S3 / GCS integration

import boto3
import os

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)

def upload_image_to_cloud(file_bytes: bytes, filename: str) -> str:
    """
    Uploads an image byte stream to the cloud bucket.
    Returns the cloud URI.
    """
    bucket = os.environ.get("IMAGE_BUCKET", "insurance-claims-bucket")
    # s3_client.put_object(Bucket=bucket, Key=filename, Body=file_bytes)
    return f"s3://{bucket}/{filename}"
