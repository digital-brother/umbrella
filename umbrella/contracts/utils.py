import shutil
from pathlib import Path

import boto3

from umbrella.config.common import env
from umbrella.core.exceptions import UmbrellaException

LOCAL_ROOT = Path(env('AWS_DOWNLOADS_LOCAL_ROOT'))
BUCKET_NAME = env('AWS_ANALYTICS_BUCKET_NAME')
BUCKET = boto3.resource('s3').Bucket(BUCKET_NAME)


def download_s3_file(aws_file):
    local_file = str(LOCAL_ROOT / aws_file)
    BUCKET.download_file(aws_file, local_file)
    # TODO: Switch from print to logging
    print(f"File '{local_file}' downloaded successfully.")


def dowbload_s3_folder(aws_dir):
    local_dir = LOCAL_ROOT / aws_dir
    shutil.rmtree(local_dir, ignore_errors=True)
    local_dir.mkdir(parents=True, exist_ok=True)
    print(f"Recreated dir {local_dir} successfully.")

    aws_files = BUCKET.objects.filter(Prefix=aws_dir).all()
    if not list(aws_files):
        raise UmbrellaException(f"No data for lease '{aws_dir}'.")

    print(f"Downloading dir '{aws_dir}' from AWS...")
    for aws_file in aws_files:
        download_s3_file(aws_file.key)
    print(f"Dir '{aws_dir}' downloaded successfully.")
