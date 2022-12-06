from aws_helpers import parameter_store, record_tag_count
from snyk_helpers import delete_tags_and_count

app_name = 'snyk-tag-monitor'
snyk_api_key = parameter_store.get_parameter(Name = f"/INFRA/security/{app_name}/snyk-api-key", WithDecryption=True)['Parameter']['Value']
snyk_group_id = parameter_store.get_parameter(Name = f"/INFRA/security/{app_name}/snyk-group-id")['Parameter']['Value']

def handler(event = None, context = None):
    tag_count: int = delete_tags_and_count(snyk_api_key, snyk_group_id)
    record_tag_count(tag_count, app_name)

if __name__ == "__main__":
    handler()
    