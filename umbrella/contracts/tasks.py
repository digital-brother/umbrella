from umbrella.contracts.utils import download_s3_folder, parse_clause


def load_aws_analytics_jsons_to_db(contract_uuid):
    s3_folder = str(contract_uuid).upper()
    downloaded_files = download_s3_folder(s3_folder)

    for clause_json_file_path in downloaded_files:
        parse_clause(clause_json_file_path)

    return downloaded_files
