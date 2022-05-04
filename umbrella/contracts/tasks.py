from pathlib import Path

from celery import shared_task

from umbrella.contracts.utils import parse_aws_clause_file


@shared_task
def parse_aws_clause_file_async(aws_file_path_str):
    aws_file_path = Path(aws_file_path_str)
    clause_nodes = parse_aws_clause_file(aws_file_path)
    return clause_nodes
