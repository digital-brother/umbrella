from celery import shared_task

from umbrella.contracts.utils import download_s3_folder, parse_local_contract


@shared_task
def load_aws_analytics_jsons_to_db(contract_uuid):
    s3_folder = str(contract_uuid).upper()
    local_folder = download_s3_folder(s3_folder)
    parse_local_contract(local_folder)
    return str(local_folder)
