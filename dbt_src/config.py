# Import required modules
from pathlib import Path
from sqlmesh.dbt.loader import sqlmesh_config
from sqlmesh.integrations.github.cicd.config import GithubCICDBotConfig, MergeMethod
from sqlmesh.core.config import AutoCategorizationMode, CategorizerConfig

def get_active_git_branch_name():

    head_dir = Path(".") / ".git" / "HEAD"
    with head_dir.open("r") as f: content = f.read().splitlines()

    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]

# Set the PR environment name prefix
pr_environment_name = "stage_pr"

# Load the dbt project configuration to be used by SQLMesh
config = sqlmesh_config(Path(__file__).parent)

# Configure the CICD bot
config.cicd_bot = GithubCICDBotConfig(
    invalidate_environment_after_deploy=True, # Indicates if the PR environment created should be automatically invalidated after changes are deployed. Invalidated environments are cleaned up automatically by the Janitor. Default: True
    enable_deploy_command=True, # Indicates if the /deploy command should be enabled in order to allowed synchronized deploys to production. Default: False
    merge_method=MergeMethod.SQUASH, # The merge method to use when automatically merging a PR after deploying to prod. Defaults to None meaning automatic merge is not done. Options: merge, squash, rebase
    command_namespace=None, # The namespace to use for SQLMesh commands. For example if you provide #SQLMesh as a value then commands will be expected in the format of #SQLMesh/<command>. Default: None meaning no namespace is used.
    auto_categorize_changes=CategorizerConfig( # Auto categorization behavior to use for the bot. If not provided then the project-wide categorization behavior is used. See Auto-categorize model changes for details.
        external=AutoCategorizationMode.FULL,
        python=AutoCategorizationMode.FULL,
        sql=AutoCategorizationMode.FULL,
        seed=AutoCategorizationMode.FULL,
    ),
    default_pr_start=None, # Default start when creating PR environment plans. Defaults to None meaning the start date is set to the earliest model's start or to 1 day ago if data previews need to be computed.
    skip_pr_backfill=False, # Indicates if the bot should skip backfilling models in the PR environment. Default: True	
    run_on_deploy_to_prod=False, # Indicates whether to run latest intervals when deploying to prod. If set to false, the deployment will backfill only the changed models up to the existing latest interval in production, ignoring any missing intervals beyond this point. Default: True
    pr_environment_name=pr_environment_name, # The name of the PR environment to create for which a PR number will be appended to. Defaults to the repo name if not provided. Note: The name will be normalized to alphanumeric + underscore and lowercase.

)
