from typing import Optional, List, Dict, Tuple


# RepoInfo class (already defined in the previous script)
class RepoInfo:
    def __init__(self, name: str, version: str, github_url: str, stars: int, forks: int,
                 releases: int, tags: int, age_in_days: int, last_updated_in_days: int,
                 contributors: List[dict], contributor_data: Optional[dict] = None):
        self.name = name
        self.version = version
        self.github_url = github_url
        self.stars = stars
        self.forks = forks
        self.releases = releases
        self.tags = tags
        self.age_in_days = age_in_days
        self.last_updated_in_days = last_updated_in_days
        self.contributors = contributors
        self.contributor_data = contributor_data


# RepoInfoManager class to manage RepoInfo instances
class RepoInfoManager:
    def __init__(self):
        self.repo_info_dict: Dict[Tuple[str, str], RepoInfo] = {}

    def add_repo_info(self, repo_info: RepoInfo):
        """Adds a RepoInfo instance to the manager."""
        key = (repo_info.name, repo_info.version)
        self.repo_info_dict[key] = repo_info

    def get_repo_info(self, package_name: str, package_version: str) -> Optional[RepoInfo]:
        """Retrieves a RepoInfo instance by package name and version."""
        return self.repo_info_dict.get((package_name, package_version))

    def get_all_repo_infos(self) -> List[RepoInfo]:
        """Returns a list of all RepoInfo instances."""
        return list(self.repo_info_dict.values())


# # Example Usage
# # Create an instance of RepoInfoManager
# repo_manager = RepoInfoManager()
#
# # Adding a RepoInfo instance
# repo_info = RepoInfo(
#     name='numpy',
#     version='1.25.1',
#     github_url='https://github.com/numpy/numpy',
#     stars=100000,
#     forks=20000,
#     releases=116,
#     tags=245,
#     age_in_days=5000,
#     last_updated_in_days=50,
#     contributors=[],
#     contributor_data=None
# )
#
# repo_manager.add_repo_info(repo_info)
#
# # Retrieving a RepoInfo instance
# retrieved_info = repo_manager.get_repo_info('numpy', '1.25.1')
# if retrieved_info:
#     print(f"Stars: {retrieved_info.stars}")
#     print(f"Contributors: {len(retrieved_info.contributors)}")
#
# # Get all RepoInfo instances
# all_repos = repo_manager.get_all_repo_infos()
# for repo in all_repos:
#     print(f"Repo: {repo.name}, Version: {repo.version}, Stars: {repo.stars}")
