import json
import re
import requests
from datetime import datetime
from typing import List, Optional
from ContributorInfo import process_contributors
from Models.RepoInfoManager import RepoInfoManager, RepoInfo
from utilities.ApiTokenRotator import ApiTokenRotator
from pathlib import Path

p = Path(__file__).resolve()


# Function to validate and normalize GitHub URL
def is_valid_github_url(url: str) -> Optional[str]:
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)', url)
    if match:
        vendor, product = match.groups()
        # Normalize the URL to ensure it only contains {Vendor}/{Product}
        return f'https://github.com/{vendor}/{product}'
    return None


# Function to handle pagination for GitHub API requests
def fetch_all_pages(api_url: str, headers: {}) -> List[dict]:
    items = []
    page = 1
    while True:
        paginated_url = f"{api_url}?page={page}&per_page=100"
        response = requests.get(paginated_url, headers=headers)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        items.extend(data)
        page += 1
    return items


# Function to fetch GitHub repository information
def fetch_github_info(github_url: str, name: str, version: str) -> Optional[RepoInfo]:
    try:
        headers = {'Authorization': f'token {token_rotator.get_next_token()}'}
        params = {'per_page': 100}
        repo_name = github_url.replace('https://github.com/', '')
        api_url = f'https://api.github.com/repos/{repo_name}'

        response = requests.get(api_url, headers=headers)
        repo_data = response.json()

        if response.status_code != 200:
            return None

        stars = repo_data.get('stargazers_count', 0)
        forks = repo_data.get('forks_count', 0)
        created_at = datetime.strptime(repo_data.get('created_at'), '%Y-%m-%dT%H:%M:%SZ')
        updated_at = datetime.strptime(repo_data.get('updated_at'), '%Y-%m-%dT%H:%M:%SZ')

        age_in_days = (datetime.now() - created_at).days
        last_updated_in_days = (datetime.now() - updated_at).days

        # Get number of releases
        releases_url = f'{api_url}/releases'
        releases = fetch_all_pages(releases_url, headers)
        releases_count = len(releases)

        # Get number of tags
        tags_url = f'{api_url}/tags'
        tags = fetch_all_pages(tags_url, headers)
        tags_count = len(tags)

        # Get contributors
        contributors_url = f'{api_url}/contributors'
        contributors = fetch_all_pages(contributors_url, headers)

        # Process and collect detailed contributor data
        contributor_data = process_contributors(name, version, contributors)

        return RepoInfo(name, version, github_url, stars, forks,
                        releases_count, tags_count, age_in_days, last_updated_in_days, contributors, contributor_data)
    except Exception as e:
        print(f"Failed to fetch GitHub info for {github_url}: {e}")
        return None


# Main function to process the SBOM and additional JSON file
def process_sbom(sbom_path: str, fallback_json_path: str):
    with open(sbom_path, 'r') as sbom_file:
        sbom_data = json.load(sbom_file)

    with open(fallback_json_path, 'r') as fallback_file:
        fallback_data = json.load(fallback_file)

    top_level_refs = []
    # Find the first dependsOn block and extract the refs
    for dependency in sbom_data['dependencies']:
        if dependency['ref'] == sbom_data['metadata']['component']['bom-ref']:
            top_level_refs = dependency['dependsOn']
            break

    repo_data = []

    for component in sbom_data['components']:
        if component['bom-ref'] in top_level_refs:
            name = component['name']
            version = component.get('version', 'unknown')

            github_url = None
            if 'externalReferences' in component:
                for ref in component['externalReferences']:
                    if ref['type'] == 'VCS':
                        valid_url = is_valid_github_url(ref['url'])
                        if valid_url:
                            github_url = valid_url
                            break

            if not github_url and name in fallback_data:
                github_url = fallback_data[name]

            if github_url:
                repo_info = fetch_github_info(github_url, name, version)
                if repo_info:
                    repo_manager.add_repo_info(repo_info)
                else:
                    print(f"No repo info found for package: {name} {version}")
            else:
                print(f"No github URL for package: {name} {version}")

    # Output the gathered repository information
    for repo_info in repo_data:
        print(f"Component: {repo_info.name}, Version: {repo_info.version}")
        print(f"GitHub URL: {repo_info.github_url}")
        print(
            f"Stars: {repo_info.stars}, Forks: {repo_info.forks}, Releases: {repo_info.releases}, Tags: {repo_info.tags}")
        print(f"Repo Age (days): {repo_info.age_in_days}, Last Updated (days): {repo_info.last_updated_in_days}")
        print(f"Contributors: {len(repo_info.contributors)}")
        print("-" * 40)


# Example usage
sbom_path = './sboms/pypi_sbom.json'
fallback_json_path = './github_urls/github_urls_pypi.json'
token_rotator = ApiTokenRotator()
repo_manager = RepoInfoManager()
process_sbom(sbom_path, fallback_json_path)
all_repos = repo_manager.get_all_repo_infos()
print('breakpoint')

