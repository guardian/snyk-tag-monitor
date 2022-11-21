import os
import requests
from requests import Response
import boto3
from botocore.config import Config
import datetime

app_name = 'snyk-tag-monitor'

def get_secret_value_from_arn(arn_env_var, secret_client) -> str:
    arn_value: str | None = os.environ.get(arn_env_var, None)
    secret_value = secret_client.get_secret_value(SecretId=arn_value)
    return secret_value['SecretString']

def send_notification(sns_topic_arn: str, message: str, stage: str):
    if (stage == "INFRA"):
        boto3.client('sns').publish(
            TargetArn = sns_topic_arn,
            Message = message,
            Subject = "Approaching snyk tag limit - action required"
        )
    else:
        print("Local environment detected. Not attempting to publish")

def get_snyk_tag_page(snyk_group_id: str, snyk_api_key: str, page_number: int, page_size: int) -> Response:
    snykurl: str = "https://api.snyk.io/api/v1/group/" + snyk_group_id + "/tags?perPage=" + str(page_size) + "&page=" + str(page_number)
    headers: dict[str, str] = {
        'Authorization': f'token {snyk_api_key}',
        'Accept': 'application/json'
    }
    return requests.get(url=snykurl, headers=headers)

def get_snyk_tags(snyk_group_id: str, snyk_api_key: str, page_number: int, tags: list =[]):
    page_size: int = 1000
    response: Response = get_snyk_tag_page(snyk_group_id, snyk_api_key, page_number, page_size)

    if(response.status_code != 200):
        print("Failed to make request to Snyk")
        print(response.text)
        raise Exception(f'{response.status_code} : {response.content}')
    else:
        response_json = response.json()
        tags_on_this_page = response_json['tags']
        print('{' + f'app: {app_name}, page: {page_number}, tags: {len(tags_on_this_page)}' + '}')

        if(len(tags_on_this_page) == page_size):
            next_page = page_number + 1
            return tags + get_snyk_tags(snyk_group_id, snyk_api_key, next_page, tags_on_this_page)
        else:
            return tags + tags_on_this_page

def handler(event = None, context = None):
    print(f"The {app_name} is starting.")

    client_config = Config(
    region_name = 'eu-west-1',
    )

    tag_warning_limit = 4500
    tag_hard_limit = 5000
    stage = os.environ.get("STAGE", "DEV")
    parameter_store = boto3.client('ssm', config = client_config)
    cloudwatch = boto3.client('cloudwatch', config = client_config)
    snyk_api_key = parameter_store.get_parameter(Name = f"/INFRA/security/{app_name}/snyk-api-key", WithDecryption=True)['Parameter']['Value']
    snyk_group_id = parameter_store.get_parameter(Name = f"/INFRA/security/{app_name}/snyk-group-id")['Parameter']['Value']
    sns_topic_arn: str = os.environ.get("SNS_TOPIC_ARN", None)

    all_tags = get_snyk_tags(snyk_group_id, snyk_api_key, 1)
    number_of_tags = len(all_tags)

    metric_data = [
        {
            'MetricName': 'snykTagCount',
            'Timestamp': datetime.datetime.now(),
            'Dimensions': [
               {
                   'Name': 'Stage',
                   'Value': stage
               },
           ],
            'Value': number_of_tags,
        },
    ]

    cloudwatch.put_metric_data(Namespace = app_name, MetricData = metric_data)
    if(number_of_tags > tag_warning_limit):
        msg = f'There are currently {number_of_tags} Snyk tags. Snyk has a limit of {tag_hard_limit} tags. Go do something about it...'
        send_notification(sns_topic_arn, msg, stage)

    print(f"Done. The {app_name} completed successfully.")

if __name__ == "__main__":
    handler()
