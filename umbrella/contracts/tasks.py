from umbrella.contracts.utils import download_s3_folder


def load_aws_analytics_jsons_to_db(contract_uuid):
    s3_folder = str(contract_uuid).upper()
    downloaded_files = download_s3_folder(s3_folder)
    return downloaded_files
