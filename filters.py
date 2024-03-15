from enum import Enum


class FilterOperator(Enum):
    IS = 1
    IS_NOT = 2
    CONTAINS = 3
    DOES_NOT_CONTAIN = 4
    IS_EMPTY = 5
    IS_NOT_EMPTY = 6
    GT = 7
    LT = 8
    GTEQ = 9
    LTEQ = 10
    IS_BEFORE = 11
    IS_AFTER = 12

    def __str__(self):
        return ["is", "is-not", "contains", "does-not-contain", "is-empty", "is-not-empty", "gt", "lt", "gteq", "lteq",
                "is-before", "is-after"][self.value - 1]


class Filter:
    def __init__(self, filter_operator: FilterOperator, value: str):
        self.operator = filter_operator
        self.value = value


class ModuleFilterType(Enum):
    NAME = 0
    SOURCE = 1
    VERSION = 2
    WORKSPACE_COUNT = 3
    WORKSPACES = 4

    def __str__(self):
        return ["name", "source", "version", "workspace-count", "workspaces"][self.value]


class ModuleFilter(Filter):
    def __init__(self, filter_type: ModuleFilterType, filter_operator: FilterOperator, value: str):
        super().__init__(filter_operator, value)
        self.type = filter_type


class ProviderFilterType(Enum):
    NAME = 0
    SOURCE = 1
    VERSION = 2
    REGISTRY_TYPE = 3
    WORKSPACE_COUNT = 4
    WORKSPACES = 5

    def __str__(self):
        return ["name", "source", "version", "registry-type", "workspace-count", "workspaces"][self.value]


class ProviderFilter(Filter):
    def __init__(self, filter_type: ProviderFilterType, filter_operator: FilterOperator, value: str):
        super().__init__(filter_operator, value)
        self.type = filter_type


class TFVersionFilterType(Enum):
    VERSION = 0
    WORKSPACE_COUNT = 1
    WORKSPACES = 2

    def __str__(self):
        return ["version", "workspace-count", "workspaces"][self.value]


class TFVersionFilter(Filter):
    def __init__(self, filter_type: TFVersionFilterType, filter_operator: FilterOperator, value: str):
        super().__init__(filter_operator, value)
        self.type = filter_type


class WorkspaceFilterType(Enum):
    WORKSPACE_ALL_CHECKS_SUCCEEDED = 0
    WORKSPACE_CHECKS_ERRORED = 1
    WORKSPACE_CHECKS_FAILED = 2
    WORKSPACE_CHECKS_PASSED = 3
    WORKSPACE_CHECKS_UNKNOWN = 4
    WORKSPACE_CURRENT_RUN_APPLIED_AT = 5
    WORKSPACE_CURRENT_RUN_EXTERNAL_ID = 6
    WORKSPACE_CURRENT_RUN_STATUS = 7
    WORKSPACE_DRIFTED = 8
    WORKSPACE_EXTERNAL_ID = 9
    WORKSPACE_MODULE_COUNT = 10
    WORKSPACE_MODULES_IN_WORKSPACE = 11
    WORKSPACE_ORGANIZATION_NAME = 12
    WORKSPACE_PROJECT_EXTERNAL_ID = 13
    WORKSPACE_PROJECT_NAME = 14
    WORKSPACE_PROVIDER_COUNT = 15
    WORKSPACE_PROVIDERS = 16
    WORKSPACE_RESOURCES_DRIFTED = 17
    WORKSPACE_RESOURCES_UNDRIFTED = 18
    WORKSPACE_STATE_VERSION_TERRAFORM_VERSION = 19
    WORKSPACE_VCS_REPO_IDENTIFIER = 20
    WORKSPACE_CREATED_AT = 21
    WORKSPACE_NAME = 22
    WORKSPACE_TERRAFORM_VERSION = 23
    WORKSPACE_UPDATED_AT = 24

    def __str__(self):
        return ["all-checks-succeeded", "checks-errored", "checks-failed", "checks-passed", "checks-unknown",
                "current-run-applied-at", "current-run-external-id", "current-run-status", "drifted", "external-id",
                "module-count", "modules-in-workspace", "organization-name", "project-external-id", "project-name",
                "provider-count", "providers", "resources-drifted", "resources-undrifted",
                "state-version-terraform-version", "vcs-repo-identifier", "created-at", "name", "terraform-version",
                "updated-at"][self.value]


class WorkspaceFilter(Filter):
    def __init__(self, filter_type: WorkspaceFilterType, filter_operator: FilterOperator, value: str):
        super().__init__(filter_operator, value)
        self.type = filter_type
