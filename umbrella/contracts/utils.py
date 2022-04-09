import json
import shutil
from pathlib import Path

import boto3

from config.settings.common import env
from umbrella.contracts.models import Lease, Node, CLAUSE_TYPE_KDP_TYPES_MAPPING
from umbrella.core.exceptions import UmbrellaError

LOCAL_ROOT = Path(env('AWS_DOWNLOADS_LOCAL_ROOT'))
BUCKET_NAME = env('AWS_ANALYTICS_BUCKET_NAME')
BUCKET = boto3.resource('s3').Bucket(BUCKET_NAME)


def download_s3_file(aws_file):
    local_file = str(LOCAL_ROOT / aws_file)
    BUCKET.download_file(aws_file, local_file)
    # TODO: Switch from print to logging
    print(f"File '{local_file}' downloaded successfully.")
    return local_file


def download_s3_folder(aws_dir):
    local_dir = LOCAL_ROOT / aws_dir
    shutil.rmtree(local_dir, ignore_errors=True)
    local_dir.mkdir(parents=True, exist_ok=True)
    print(f"Recreated dir {local_dir} successfully.")

    aws_files = BUCKET.objects.filter(Prefix=aws_dir).all()
    if not list(aws_files):
        raise UmbrellaError(f"No data for lease '{aws_dir}'.")

    print(f"Downloading dir '{aws_dir}' from AWS...")
    downloaded_files = []
    for aws_file in aws_files:
        downloaded_file = download_s3_file(aws_file.key)
        downloaded_files.append(downloaded_file)
    print(f"Dir '{aws_dir}' downloaded successfully.")
    return downloaded_files


def parse_kdp_item(kdp_name, parent_kdp_name, list_obj, lease):
    node = Node.create(
        type=kdp_name,
        content=list_obj,
    )

    clause_types = CLAUSE_TYPE_KDP_TYPES_MAPPING.keys()
    if kdp_name in clause_types:
        node.lease = lease

    para_id = list_obj["paraId"]
    clause = Node.objects.filter(type=parent_kdp_name, lease=lease, content__paraId=para_id).first()
    node.clause = clause

    node.save()


def parse_kdp_item_list(json_data, lease):
    parent_kdp_name = ""
    for kdp_name, kdp_items in json_data.items():
        if not parent_kdp_name:
            parent_kdp_name = kdp_name
        for list_obj in kdp_items:
            parse_kdp_item(kdp_name, parent_kdp_name, list_obj, lease)


def parse_json(file_path):
    path = Path(file_path)
    upper_uuid = file_path.split("/")[-2]
    lease_uuid = upper_uuid.lower()
    lease = Lease.objects.filter(id=lease_uuid).first()
    if not lease:
        raise UmbrellaError(f"No Contracts with id: {lease_uuid}")

    with path.open(mode="rb") as f:
        json_data = json.load(f)
        parse_kdp_item_list(json_data, lease)
