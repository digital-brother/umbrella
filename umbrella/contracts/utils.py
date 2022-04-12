import json
import logging
import shutil
from glob import glob
from pathlib import Path

import boto3
from django.conf import settings
from django.forms import model_to_dict

from config.settings.common import env
from umbrella.contracts.models import Contract, Node, CLAUSE_TYPE_KDP_TYPES_MAPPING
from umbrella.core.exceptions import UmbrellaError

BUCKET_NAME = env('AWS_ANALYTICS_BUCKET_NAME')
BUCKET = boto3.resource('s3').Bucket(BUCKET_NAME)

logger = logging.getLogger('load_aws_analytics_jsons_to_db')


# Download analytics json files
def download_s3_folder(aws_dir):
    local_dir = settings.AWS_DOWNLOADS_LOCAL_ROOT / aws_dir
    shutil.rmtree(local_dir, ignore_errors=True)
    local_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Cleaned dir '{local_dir}'.")

    aws_files = BUCKET.objects.filter(Prefix=aws_dir).all()
    if not list(aws_files):
        raise UmbrellaError(f"No data for contract '{aws_dir}'.")

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


def parse_contract(contract_dir):
    clause_files = list(Path(contract_dir).glob('*.json'))

    contract_nodes = {}
    for clause_file in clause_files:
        clause_nodes = parse_clause_file(clause_file)
        contract_nodes[clause_file.name] = clause_nodes
    return contract_nodes


def parse_clause_file(clause_file):
    contract = _get_contract_from_clause_file_path(clause_file)
    logger.info(f"Parsing '{clause_file}'.")
    with clause_file.open(mode="rb") as f:
        json_data = json.load(f)
        clause_type = _get_clause_type_from_json_data(json_data)

        clause_nodes = {}
        for node_type, nodes_list in json_data.items():
            clause_nodes[node_type] = parse_node_list(node_type, nodes_list, contract, clause_type)

    return clause_nodes


def parse_node_list(node_type, nodes_list, contract, clause_type):
    clause_types = CLAUSE_TYPE_KDP_TYPES_MAPPING.keys()
    is_clause = node_type in clause_types
    handler = parse_clause if is_clause else parse_kdp

    node_list = []
    for node_json in nodes_list:
        node = handler(node_type, node_json, contract, clause_type)
        node_list.append(node)
        logger.info(f"Parsed node {model_to_dict(node)}")

    return node_list


def parse_clause(node_type, node_json, contract, _):
    return Node.create(
        type=node_type,
        content=node_json,
        contract=contract
    )


def parse_kdp(node_type, node_json, contract, clause_type):
    para_id = node_json["paraId"]
    clause = Node.objects.filter(type=clause_type, contract=contract, content__paraId=para_id).first()
    if not clause:
        raise UmbrellaError(f"No '{clause_type}' clause found for '{node_type}' KDP with paraId '{para_id}'.")

    return Node.create(
        type=node_type,
        content=node_json,
        clause=clause,
    )


def _get_contract_from_clause_file_path(clause_file):
    upper_uuid = clause_file.parent.name
    contract_uuid = upper_uuid.lower()
    contract = Contract.objects.filter(id=contract_uuid).first()
    if not contract:
        raise UmbrellaError(f"No Contracts with id: {contract_uuid}")
    return contract


def _get_clause_type_from_json_data(json_data):
    json_keys = set(json_data)
    available_clause_types = set(CLAUSE_TYPE_KDP_TYPES_MAPPING)
    common_clauses = json_keys & available_clause_types
    if len(common_clauses) != 1:
        msg = f"File should contain 1 clause, but contains {len(common_clauses)}: {common_clauses}"
        raise UmbrellaError(msg)
    clause_type = list(common_clauses)[0]
    return clause_type
