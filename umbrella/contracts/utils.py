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


def parse_node(node_type, clause_type, node_content, lease):
    node = Node.create(
        type=node_type,
        content=node_content,
    )

    clause_types = CLAUSE_TYPE_KDP_TYPES_MAPPING.keys()
    if node_type in clause_types:
        node.lease = lease

    para_id = node_content["paraId"]
    clause = Node.objects.filter(type=clause_type, lease=lease, content__paraId=para_id).first()
    node.clause = clause

    node.save()


def parse_node_list(json_data, lease):
    json_keys = json_data.keys()
    clause_type = json_keys[0] if json_keys else None
    for node_type, nodes_list in json_data.items():
        for node in nodes_list:
            parse_node(node_type, clause_type, node, lease)


def parse_json(file_path):
    path = Path(file_path)
    upper_uuid = file_path.split("/")[-2]
    lease_uuid = upper_uuid.lower()
    lease = Lease.objects.filter(id=lease_uuid).first()
    if not lease:
        raise UmbrellaError(f"No Contracts with id: {lease_uuid}")

    with path.open(mode="rb") as f:
        json_data = json.load(f)
        parse_node_list(json_data, lease)
