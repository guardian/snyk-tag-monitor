import boto3
from botocore.config import Config
import os
import datetime

_stage = os.environ.get("STAGE", "DEV")

_client_config = Config(
    region_name='eu-west-1',
)


def _send_tag_count_to_cloudwatch(number_of_tags: int, app_name: str):

    cloudwatch = boto3.client('cloudwatch', config=_client_config)

    metric_data = [
        {
            'MetricName': 'snykTagCount',
            'Timestamp': datetime.datetime.now(),
            'Dimensions': [
                {
                    'Name': 'Stage',
                    'Value': _stage
                },
            ],
            'Value': number_of_tags,
        },
    ]

    cloudwatch.put_metric_data(Namespace=app_name, MetricData=metric_data)


parameter_store = boto3.client('ssm', config=_client_config)


def _send_notification(sns_topic_arn: str, message: str, stage: str):
    if (stage == "INFRA"):
        boto3.client('sns').publish(
            TargetArn=sns_topic_arn,
            Message=message,
            Subject="Approaching snyk tag limit - action required"
        )
    else:
        print("Local environment detected. Not attempting to publish")


def record_tag_count(number_of_tags: int, app_name: str):
    sns_topic_arn: str = os.environ.get("SNS_TOPIC_ARN", None)

    _send_tag_count_to_cloudwatch(number_of_tags, app_name)
    print("sent tag count to cloudwatch")
    tag_warning_limit = 4500
    tag_hard_limit = 5000

    if (number_of_tags > tag_warning_limit):
        msg = f'There are currently {number_of_tags} Snyk tags. Snyk has a limit of {tag_hard_limit} tags. Go do something about it...'
        _send_notification(sns_topic_arn, msg, _stage)
        print("sent sns notification")
