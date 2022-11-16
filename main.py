import os
import requests
from requests import Response
import boto3

group_id =  os.environ.get("SNYK_GROUP_ID", None)
snyk_api_key =  os.environ.get("SNYK_API_KEY", None)
sns_topic_arn = os.environ.get("SNS_TOPIC_ARN", None)
stage = os.environ.get("STAGE", "DEV")
page_size = 100
tag_warning_limit = 900
tag_hard_limit = 1000

def send_notification(sns_topic_arn: str, message: str, stage: str):
    if (stage == "INFRA"):
        client = boto3.client('sns')
        client.publish(
            TargetArn = sns_topic_arn,
            Message = message,
            Subject = "Approaching snyk tag limit - action required"
        )
    else:
        print("Local environment detected. Not attempting to publish")

def get_snyk_tag_page(group_id: str, snyk_api_key: str, page_number: int, page_size: int) -> Response:
    snykurl = "https://api.snyk.io/api/v1/group/" + group_id + "/tags?perPage=" + str(page_size) + "&page=" + str(page_number)
    headers = {
        'Authorization': 'token ' + snyk_api_key,
        'Accept': 'application/json'
    }
    return requests.get(url=snykurl, headers=headers)

def get_snyk_tags(group_id: str, snyk_api_key: str, page_number, tags=[]):
    print(f'{len(tags)} tags on page {page_number}')
    response = get_snyk_tag_page(group_id, snyk_api_key, page_number, page_size)
    
    if(response.status_code != 200):
        print("Failed to make request to Snyk")
        print(response.text)
        raise Exception(f'{response.status_code} : {response.content}')
    else:
        response_json = response.json()
        tags_on_this_page = response_json['tags']
        print(f'tags on this page: {len(tags_on_this_page)}')

        if(len(tags_on_this_page) == page_size):
            next_page = page_number + 1
            print(f'Getting page {next_page}')
            return tags + get_snyk_tags(group_id, snyk_api_key, next_page, tags_on_this_page)
        else:
            return tags + tags_on_this_page
        
def handler(event = None, context = None):
    if(isinstance(group_id, str) and isinstance(snyk_api_key, str) and isinstance(sns_topic_arn, str)):
        all_tags = get_snyk_tags(group_id, snyk_api_key, 1)
        number_of_tags = len(all_tags)
        if(number_of_tags > tag_warning_limit):
            send_notification(sns_topic_arn, f'There are currently {number_of_tags} Snyk tags. Snyk has a limit of {tag_hard_limit} tags. Go do something about it...')
    else:
        raise Exception("Config missing!")

if __name__ == "__main__":
    handler()