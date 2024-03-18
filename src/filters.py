from dataclasses import dataclass
from enum import Enum


class FilterOperator(Enum):
    IS = "is"
    IS_NOT = "is-not"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "does-not-contain"
    IS_EMPTY = "is-empty"
    IS_NOT_EMPTY = "is-not-empty"
    GT = "gt"
    LT = "lt"
    GTEQ = "gteq"
    LTEQ = "lteq"
    IS_BEFORE = "is-before"
    IS_AFTER = "is-after"


class ModuleFilterType(Enum):
    NAME = "name"
    SOURCE = "source"
    VERSION = "version"
    WORKSPACE_COUNT = "workspace-count"
    WORKSPACES = "workspaces"


@dataclass(frozen=True)
class ModuleFilter:
    type: ModuleFilterType
    operator: FilterOperator
    value: str


class ProviderFilterType(Enum):
    NAME = "name"
    SOURCE = "source"
    VERSION = "version"
    REGISTRY_TYPE = "registry-type"
    WORKSPACE_COUNT = "workspace-count"
    WORKSPACES = "workspaces"


@dataclass(frozen=True)
class ProviderFilter:
    type: ProviderFilterType
    operator: FilterOperator
    value: str


class TFVersionFilterType(Enum):
    VERSION = "version"
    WORKSPACE_COUNT = "workspace-count"
    WORKSPACES = "workspaces"


@dataclass(frozen=True)
class TFVersionFilter:
    type: TFVersionFilterType
    operator: FilterOperator
    value: str


class WorkspaceFilterType(Enum):
    ALL_CHECKS_SUCCEEDED = "all-checks-succeeded"
    CHECKS_ERRORED = "checks-errored"
    CHECKS_FAILED = "checks-failed"
    CHECKS_PASSED = "checks-passed"
    CHECKS_UNKNOWN = "checks-unknown"
    CURRENT_RUN_APPLIED_AT = "current-run-applied-at"
    CURRENT_RUN_EXTERNAL_ID = "current-run-external-id"
    CURRENT_RUN_STATUS = "current-run-status"
    DRIFTED = "drifted"
    EXTERNAL_ID = "external-id"
    MODULE_COUNT = "module-count"
    MODULES_IN_WORKSPACE = "modules-in-workspace"
    ORGANIZATION_NAME = "organization-name"
    PROJECT_EXTERNAL_ID = "project-external-id"
    PROJECT_NAME = "project-name"
    PROVIDER_COUNT = "provider-count"
    PROVIDERS = "providers"
    RESOURCES_DRIFTED = "resources-drifted"
    RESOURCES_UNDRIFTED = "resources-undrifted"
    STATE_VERSION_TERRAFORM_VERSION = "state-version-terraform-version"
    VCS_REPO_IDENTIFIER = "vcs-repo-identifier"
    CREATED_AT = "created-at"
    NAME = "name"
    TERRAFORM_VERSION = "terraform-version"
    UPDATED_AT = "updated-at"


@dataclass(frozen=True)
class WorkspaceFilter:
    type: WorkspaceFilterType
    operator: FilterOperator
    value: str
