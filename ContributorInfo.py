import requests
from typing import List
from utilities.ApiTokenRotator import ApiTokenRotator


# Model class to store contributor information
class ContributorInfo:
    def __init__(self, username: str, github_id: int, contributions: int, organization: str, location: str):
        self.username = username
        self.github_id = github_id
        self.contributions = contributions
        self.organization = organization
        self.location = location


# Function to fetch additional contributor details
def fetch_contributor_details(headers, contributor) -> ContributorInfo:
    try:
        username = contributor.get('login', 'unknown')
        github_id = contributor.get('id', -1)
        contributions = contributor.get('contributions', 0)

        # Fetch additional details like organization and location
        contributor_url = contributor['url']
        response = requests.get(contributor_url, headers=headers)
        if response.status_code == 200:
            contributor_data = response.json()
            organization = contributor_data.get('company', 'N/A')
            location = contributor_data.get('location', 'N/A')
        else:
            organization = 'N/A'
            location = 'N/A'

        return ContributorInfo(username, github_id, contributions, organization, location)
    except Exception as e:
        print(f"Failed to fetch contributor details: {e}")
        return ContributorInfo(username, github_id, contributions, 'N/A', 'N/A')


# Function to process contributors and link them to package information
def process_contributors(package_name: str, package_version: str, contributors: List[dict]) -> dict:
    contributor_data = []
    token_rotator = ApiTokenRotator()
    headers = {'Authorization': f'token {token_rotator.get_next_token()}'}

    for contributor in contributors:
        contributor_info = fetch_contributor_details(headers, contributor)
        contributor_data.append(contributor_info)

    # Link contributor information to package name and version
    package_contributor_data = {
        'package_name': package_name,
        'package_version': package_version,
        'contributors': contributor_data
    }

    return package_contributor_data
