import json
import logging
import shutil
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError
from django.conf import settings
from django.forms import model_to_dict

from config.settings.common import env
from umbrella.contracts.models import Contract, Node
from umbrella.core.exceptions import UmbrellaError

BUCKET_NAME = env('AWS_ANALYTICS_BUCKET_NAME')
S3 = boto3.resource('s3')
BUCKET = S3.Bucket(BUCKET_NAME)

logger = logging.getLogger('load_aws_analytics_jsons_to_db')


def get_files_from_aws_dir(aws_dir):
    try:
        aws_files = BUCKET.objects.filter(Prefix=aws_dir).all()
    except BotoCoreError as err:
        raise UmbrellaError(f"Can't get files from aws directory '{aws_dir}'. Error: {err}")
    if not list(aws_files):
        raise UmbrellaError(f"No data for contract '{aws_dir}'.")

    return aws_files


# Download analytics json files
def download_s3_folder(aws_dir):
    local_dir = settings.AWS_DOWNLOADS_LOCAL_ROOT / aws_dir
    shutil.rmtree(local_dir, ignore_errors=True)
    local_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Cleaned dir '{local_dir}'.")

    aws_files = get_files_from_aws_dir(aws_dir)

    downloaded_files = []
    for aws_file in aws_files:
        # To run download only for file, folder is also present in aws_files
        if aws_file.key.endswith('.json'):
            downloaded_file = download_s3_file(aws_file.key)
            downloaded_files.append(downloaded_file)
    return local_dir


def download_s3_file(aws_file):
    local_file = str(settings.AWS_DOWNLOADS_LOCAL_ROOT / aws_file)
    BUCKET.download_file(aws_file, local_file)
    logger.info(f"Downloaded '{local_file}'.")
    return local_file


def parse_local_contract(contract_dir):
    clause_files = list(Path(contract_dir).glob('*.json'))

    contract_nodes = {}
    for clause_file in clause_files:
        clause_nodes = parse_local_clause_file(clause_file)
        contract_nodes[clause_file.name] = clause_nodes
    return contract_nodes


def parse_local_clause_file(clause_file):
    contract = _get_contract_from_clause_file_path(clause_file)
    logger.info(f"Parsing '{clause_file}'.")
    with clause_file.open(mode="rb") as f:
        json_data = json.load(f)
        clause_type = _get_clause_type_from_file_name(f.name)

        clause_nodes = {}
        for node_type, nodes_list in json_data.items():
            clause_nodes[node_type] = parse_node_list(node_type, nodes_list, contract, clause_type)

    return clause_nodes


def parse_aws_contract(contract_id):
    aws_dir = str(contract_id).upper()
    aws_files = get_files_from_aws_dir(aws_dir)

    contract_nodes = {}
    for aws_file in aws_files:
        if not aws_file.key.endswith('.json'):
            continue

        clause_path = Path(aws_file.key)
        clause_nodes = parse_aws_clause_file(clause_path)

        contract_nodes[clause_path.name] = clause_nodes
    return contract_nodes


def parse_aws_clause_file(clause_file):
    contract = _get_contract_from_clause_file_path(clause_file)
    logger.info(f"Parsing '{clause_file}'.")
    try:
        file_data = S3.Object(BUCKET_NAME, str(clause_file)).get()
    except BotoCoreError as err:
        raise UmbrellaError(f"Can't get file '{clause_file.name}' data. Error: {err}")

    encoded_json_data = file_data['Body'].read()
    decoded_json_data = encoded_json_data.decode("utf-8")
    json_data = json.loads(decoded_json_data)

    clause_type = clause_file.stem
    clause_nodes = {}
    for node_type, nodes_list in json_data.items():
        clause_nodes[node_type] = parse_node_list(node_type, nodes_list, contract, clause_type)
    logger.info(f"Parsing done.")
    return clause_nodes


def parse_node_list(node_type, nodes_list, contract, clause_type):
    is_clause = node_type == clause_type
    handler = parse_clause if is_clause else parse_kdp

    node_list = []
    for node_json in nodes_list:
        node = handler(node_type, node_json, contract, clause_type)
        node_list.append(node)
        logger.info(f"Parsed node {node}")

    return node_list


def parse_clause(node_type, node_json, contract, _):
    clause = Node.create(type=node_type, content=node_json, contract=contract)
    return model_to_dict(clause)


def parse_kdp(node_type, node_json, contract, clause_type):
    para_id = node_json["paraId"]
    clause = Node.objects.filter(type=clause_type, contract=contract, content__paraId=para_id).first()
    if not clause:
        raise UmbrellaError(f"No '{clause_type}' clause found for '{node_type}' KDP with paraId '{para_id}'.")

    kdp = Node.create(type=node_type, content=node_json, clause=clause, )
    return model_to_dict(kdp)


def _get_contract_from_clause_file_path(clause_file):
    upper_uuid = clause_file.parent.name
    contract_uuid = upper_uuid.lower()
    # contract = Contract.objects.filter(id=contract_uuid).first()
    contract = Contract.objects.first()
    if not contract:
        raise UmbrellaError(f"No Contracts with id: {contract_uuid}")
    return contract


def _get_clause_type_from_file_name(file_path):
    parsed_path = Path(file_path)
    file_name = parsed_path.stem
    return file_name
