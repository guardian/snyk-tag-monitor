from requests import Response
import requests
from snyk import SnykClient

def _get_snyk_tag_page(snyk_group_id: str, snyk_api_key: str, page_number: int, page_size: int) -> Response:
    snykurl: str = "https://api.snyk.io/api/v1/group/" + snyk_group_id + "/tags?perPage=" + str(page_size) + "&page=" + str(page_number)
    headers: dict[str, str] = {
        'Authorization': f'token {snyk_api_key}',
        'Accept': 'application/json'
    }
    return requests.get(url=snykurl, headers=headers)

def _get_snyk_tags(snyk_group_id: str, snyk_api_key: str, page_number: int, tags: list =[]):
    page_size: int = 1000
    response: Response = _get_snyk_tag_page(snyk_group_id, snyk_api_key, page_number, page_size)

    if(response.status_code != 200):
        print(f'Failed to get page {page_number} of tags from snyk')
        print(f'{response.status_code} : {response.content}')
        raise Exception(f'{response.status_code} : {response.content}')
    else:
        response_json = response.json()
        tags_on_this_page = response_json['tags']
        print(f'page: {page_number}, tags: {len(tags_on_this_page)}')

        if(len(tags_on_this_page) == page_size):
            next_page = page_number + 1
            return tags + _get_snyk_tags(snyk_group_id, snyk_api_key, next_page, tags_on_this_page)
        else:
            return tags + tags_on_this_page

def _delete_tag(tag_dict, group_id, snyk_key):

  delete_tag_url = "https://api.snyk.io/api/v1/group/" + group_id + "/tags/delete"
  json_body = {"key": tag_dict['key'], "value": tag_dict['value'], "force": False}

  response = requests.post(url = delete_tag_url, headers={'Authorization': 'token ' + snyk_key }, json=json_body)
  if response.status_code != 200:
    print("Failed to delete tag")
    print(f'code : {response.status_code}, content: {response.content}')

def _get_owned_tags(snyk_key):

    def deduplicate_dict_list(dict_list):
        return [dict(t) for t in {tuple(d.items()) for d in dict_list}]
    
    client: SnykClient = SnykClient(snyk_key)
    projects: list = client.projects.all()
    nested_tag_list = [project.tags.all() for project in projects]
    flat_list = [item for sublist in nested_tag_list for item in sublist]
    return deduplicate_dict_list(flat_list)

def delete_tags_and_count(snyk_api_key: str, snyk_group_id: str) -> int:

    owned_tags = _get_owned_tags(snyk_api_key)
    initial_tag_list = _get_snyk_tags(snyk_group_id, snyk_api_key, 1)
    print(f"starting tags: {len(initial_tag_list)}")

    orphaned_tags = list(filter(lambda x: x not in owned_tags, initial_tag_list))
    orphaned_tag_count = len(orphaned_tags)
    print(f"orphaned tags: {orphaned_tag_count}")

    for tag in orphaned_tags:
        _delete_tag(tag, snyk_group_id, snyk_api_key)
    
    final_tag_list = _get_snyk_tags(snyk_group_id, snyk_api_key, 1)

    number_of_tags = len(final_tag_list)
    deleted_tag_count = len(initial_tag_list) - len(final_tag_list)
    print(f'deleted tags: {deleted_tag_count}')

    return number_of_tags