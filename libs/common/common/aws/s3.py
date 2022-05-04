# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
# https://realpython.com/python-boto3-aws-s3/
import os

import loguru
from botocore.exceptions import ClientError

from common.aws.aws import create_boto3_session


def create_s3_resource(
        aws_access_key_id: str, aws_secret_access_key: str, region_name: str, *, logger=loguru.logger
):
    boto3_session = create_boto3_session(aws_access_key_id, aws_secret_access_key, region_name)
    s3_resource = boto3_session.resource('s3')
    logger.bind(s3_resource=s3_resource).debug("Created s3 resource")
    return s3_resource


def create_s3_client(
        aws_access_key_id: str, aws_secret_access_key: str, region_name: str, *, logger=loguru.logger
):
    boto3_session = create_boto3_session(aws_access_key_id, aws_secret_access_key, region_name)
    s3_client = boto3_session.client('s3')
    logger.bind(s3_resource=s3_client).debug("Created s3 client")
    return s3_client


# Create an Amazon S3 bucket
# Unsafe for use in prod (as currently creates only public bucket)
def create_bucket(
        aws_access_key_id: str, aws_secret_access_key: str, region_name: str, bucket_name: str, *, logger=loguru.logger
):
    try:
        s3_resource = create_s3_resource(aws_access_key_id, aws_secret_access_key, region_name, logger=logger)
        bucket_response = s3_resource.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': f"{region_name}"}
        )
        logger.bind(bucket_response=bucket_response).debug("Created s3 bucket")
        return bucket_response
    except ClientError as e:
        logger.error(f"Failed to create S3 bucket, error: {e}")


# List existing buckets
def list_buckets(
        aws_access_key_id: str, aws_secret_access_key: str, region_name: str, *, logger=loguru.logger
):
    try:
        s3_client = create_s3_client(aws_access_key_id, aws_secret_access_key, region_name, logger=logger)
        bucket_response = s3_client.list_buckets()
        return bucket_response
    except ClientError as e:
        logger.error(f"Failed to create S3 bucket, error: {e}")


# Upload file
def upload_file(
        aws_access_key_id: str, aws_secret_access_key: str, region_name: str,
        file_name: str, bucket: str, object_name=None, *, logger=loguru.logger
) -> bool:
    try:
        s3_client = create_s3_client(aws_access_key_id, aws_secret_access_key, region_name, logger=logger)
        if object_name is None:
            object_name = os.path.basename(file_name)
        is_none = s3_client.upload_file(file_name, bucket, object_name)
        return is_none is None
    except ClientError as e:
        logger.error(f"Failed to upload file, error: {e}")
        return False

# TODO: upload fileobj


# Downloading file
def download_file(
        aws_access_key_id: str, aws_secret_access_key: str, region_name: str,
        bucket: str, object_name: str, file_name: str = None, *, logger=loguru.logger
) -> bool:
    try:
        s3_client = create_s3_client(aws_access_key_id, aws_secret_access_key, region_name, logger=logger)
        if file_name is None:
            file_name = os.path.basename(object_name)
        is_none = s3_client.download_file(bucket, object_name, file_name)
        return is_none is None
    except (ClientError, FileNotFoundError) as e:
        logger.error(f"Failed to download file, error: {e}")
        return False

# TODO: download fileobj

# TODO: File Transfer Configuration
