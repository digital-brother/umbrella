from celery import shared_task

from umbrella.contracts.utils import parse_aws_contract


@shared_task
def load_aws_analytics_jsons_to_db(contract_uuid):
    parse_aws_contract(contract_uuid)
    return str(contract_uuid)
