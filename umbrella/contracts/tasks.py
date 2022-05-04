from celery import shared_task

from umbrella.contracts.utils import parse_aws_clause


@shared_task
def load_aws_analytics_jsons_to_db(contract_uuid, file_name):
    parse_aws_clause(contract_uuid, file_name)
    return str(contract_uuid)
