from celery import shared_task

from umbrella.contracts.utils import parse_aws_clause_file


@shared_task
def parse_aws_clause_async(aws_file_path):
    clause_nodes = parse_aws_clause_file(aws_file_path)
    return clause_nodes
