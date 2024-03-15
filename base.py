import sys
import requests
from urllib.parse import urlparse, urlunparse, urlencode
import time
from . import filters
from typing import List

RATELIMIT = 30
RATEBUFFER = 7


class Client:
    def __init__(self, org_name, token):
        self.session = requests.Session()
        self.org_name = org_name
        self.token = token
        self.headers = {'Authorization': f'Bearer {self.token}'}
        self.endpoint = {
            'modules': [],
            'workspaces': [],
            'tf_versions': [],
            'providers': [],
            'registry_modules': []
        }

    def modules(self, module_filters: List[filters.ModuleFilter]) -> list:
        """
        Get the modules for the organization.
        :param module_filters: The filters to apply to the query.
        :return: The modules for the organization.
        """
        url = build_explorer_url(self.org_name)
        params = {'type': 'modules', 'page[size]': 100}

        for i, module_filter in enumerate(module_filters):
            key = f"filter[{i}][{module_filter.type.__str__()}][{module_filter.operator.__str__()}][0]"
            params[key] = module_filter.value

        url = f'{url}?{urlencode(params)}'

        modules = self.get_data(url, 'modules')

        return modules

    def workspaces(self, workspace_filters: List[filters.WorkspaceFilter]) -> list:
        """
        Get the workspaces for the organization.
        :param workspace_filters: The filters to apply to the query.
        :return: The workspaces for the organization.
        """
        url = build_explorer_url(self.org_name)
        params = {'type': 'workspaces', 'page[size]': 100}

        for i, workspace_filter in enumerate(workspace_filters):
            key = f"filter[{i}][{workspace_filter.type.__str__()}][{workspace_filter.operator.__str__()}][0]"
            params[key] = workspace_filter.value

        url = f'{url}?{urlencode(params)}'

        workspaces = self.get_data(url, 'workspaces')

        return workspaces

    def providers(self, provider_filters: List[filters.ProviderFilter]) -> list:
        """
        Get the providers for the organization.
        :param provider_filters: The filters to apply to the query.
        :return: The providers for the organization.
        """
        url = build_explorer_url(self.org_name)
        params = {'type': 'providers', 'page[size]': 100}

        for i, provider_filter in enumerate(provider_filters):
            key = f"filter[{i}][{provider_filter.type.__str__()}][{provider_filter.operator.__str__()}][0]"
            params[key] = provider_filter.value

        url = f'{url}?{urlencode(params)}'

        providers = self.get_data(url, 'providers')

        return providers

    def tf_versions(self, tf_version_filters: List[filters.TFVersionFilter]) -> list:
        """
        Get the Terraform versions for the organization.
        :param tf_version_filters: The filters to apply to the query.
        :return: The Terraform versions for the organization.
        """
        url = build_explorer_url(self.org_name)
        params = {'type': 'tf_versions', 'page[size]': 100}

        for i, tf_version_filter in enumerate(tf_version_filters):
            key = f"filter[{i}][{tf_version_filter.type.__str__()}][{tf_version_filter.operator.__str__()}][0]"
            params[key] = tf_version_filter.value

        url = f'{url}?{urlencode(params)}'

        tf_versions = self.get_data(url, 'tf_versions')

        return tf_versions

    def registry_modules(self) -> list:
        """
        Get the latest version of all modules in an organizations private registry. This is currently used by indexing
        to 0, which as of now is the latest version. No comparison is done to ensure this is the latest version.
        :return: The latest version of all modules for the organization.
        """
        url = build_registry_url(self.org_name)
        params = {'page[size]': 100}

        url = f'{url}?{urlencode(params)}'

        registry_modules = self.get_data(url, 'registry_modules')

        return registry_modules

    def get_data(self, url, endpoint_type: str) -> list:
        """
        Try to make a request and handle any exceptions that occur.
        :param url: The URL to request.
        :param endpoint_type: The type of endpoint being requested. (workspace, module, etc.)
        :return: The data from the request in list format.
        """
        while url:
            try:
                response = self.session.get(url, headers=self.headers)
            except ValueError as e:
                print(f'Error building URL: {e}', file=sys.stderr)
                sys.exit(1)
            except requests.exceptions.RequestException as e:
                print(f'Error fetching modules: {e}', file=sys.stderr)
                sys.exit(1)

            check_status_code(response)
            data = response.json()
            self.endpoint[endpoint_type].extend(data['data'])

            url = data['links']['next'] \
                if data['meta']['pagination']['next-page'] is not None else None

            prevent_rate_limiting(data['meta']['pagination']['total-pages'])

        return self.endpoint[endpoint_type]


class RateLimitExceededException(Exception):
    """Exception raised when the API rate limit is exceeded."""
    pass


def build_explorer_url(org_name: str) -> str:
    """
    Build the URL for the explorer endpoint.
    :param org_name: The name of the organization.
    :return: The URL for the explorer endpoint.
    """
    base_url = urlparse(f'https://app.terraform.io/api/v2/organizations/{org_name}/explorer')
    return str(urlunparse(base_url))


def build_registry_url(org_name: str) -> str:
    """
    Build the URL for the registry modules endpoint.
    :param org_name: The name of the organization.
    :return: The URL for the registry modules endpoint.
    """
    base_url = urlparse(f'https://app.terraform.io/api/v2/organizations/{org_name}/registry-modules')
    return str(urlunparse(base_url))


def check_status_code(response: requests.Response) -> None:
    """
    Check the status code of the response and raise an exception if the rate limit is exceeded.
    :param response: The response object from the request.
    :raises RateLimitExceededException: If the response status code is 429
    """
    if response.status_code == 429:
        limit = response.headers['x-ratelimit-limit']
        raise RateLimitExceededException(f'Rate limit exceeded. Limit: {limit}')
    if response.status_code < 200 or response.status_code >= 300:
        raise requests.exceptions.RequestException(f'Unexpected status code: {response.status_code}')


def prevent_rate_limiting(page_count: int) -> None:
    """
    Prevent rate limiting by sleeping for a short period of time if the page count exceeds the rate limit.
    :param page_count: The total number of pages returned by the API.
    """
    if page_count < RATELIMIT:
        return

    delay = 1000.0 / RATELIMIT + RATEBUFFER
    time.sleep(delay)
