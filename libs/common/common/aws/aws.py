import boto3


def create_boto3_session(
        aws_access_key_id: str, aws_secret_access_key: str, region_name: str
) -> boto3.session.Session:
    return boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
