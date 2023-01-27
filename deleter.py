import os
import posixpath
from typing import Tuple
import urllib.parse
import mlflow
from mlflow.entities import ViewType
from mlflow.store.artifact.artifact_repo import ArtifactRepository
from mlflow.store.artifact.artifact_repository_registry import get_artifact_repository
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository
from mlflow.utils.file_utils import path_to_local_file_uri
# from dotenv import load_dotenv


def delete_old_artifacts(experiment_name: str):
    """Delete all artifacts belonging to one experiment in order to to save storage

    Args:
        experiment_name (str): The name of the experiment
    """
    # load mlflow credentials form env variables 
    # load_dotenv()

    experiments = mlflow.search_experiments()

    experiment_id = -1
    for e in experiments:
        if e.name == experiment_name:
            experiment_id = e.experiment_id
    if experiment_id == -1:
        print(f"Could not find the experiment with the name: {experiment_name}")
        return
    _delete_old_artifacts_of_experiment(experiment_id)


def delete_all_old_artifacts():
    """Delete all artifacts belonging to deleted runs to save storage
    """
    # load mlflow credentials form env variables 
    # load_dotenv()
    
    experiments = mlflow.search_experiments()
    for e in experiments:
        _delete_old_artifacts_of_experiment(e.experiment_id)

def _delete_old_artifacts_of_experiment(experiment_id: int):
    """Delete all artifacts belonging to the experiment id

    Args:
        experiment_name (int): The id of the experiment
    """
    # Get all delete runs
    runs = mlflow.search_runs(experiment_ids=[experiment_id], run_view_type=ViewType.DELETED_ONLY)

    for r in runs.to_dict(orient="records"):
        # print(r)
        artifact_repo, artifact_path = _get_artifact_repo(r["artifact_uri"])
        # check if artifacts are not empty
        if artifact_repo.list_artifacts():
            print(f"Deleting all artifacts of the run with the run_id: {r['run_id']}")
            artifact_repo.delete_artifacts(artifact_path)


def _get_artifact_repo(artifact_uri: str) -> Tuple[ArtifactRepository, str]:
    """Adopted _download_artifact_from_uri from mlflow.tracking.artifact_utils to get artifact store

    Args:
        artifact_uri (str): Uri of the model run

    Returns:
        Tuple[ArtifactRepository, str]: repo from the artifact_uri, artifact_path
    """
    if os.path.exists(artifact_uri):
        if os.name != "nt":
            # If we're dealing with local files, just reference the direct pathing.
            # non-nt-based file systems can directly reference path information, while nt-based
            # systems need to url-encode special characters in directory listings to be able to
            # resolve them (i.e., spaces converted to %20 within a file name or path listing)
            root_uri = os.path.dirname(artifact_uri)
            artifact_path = os.path.basename(artifact_uri)
            return get_artifact_repository(artifact_uri=root_uri)
        else:  # if we're dealing with nt-based systems, we need to utilize pathname2url to encode.
            artifact_uri = path_to_local_file_uri(artifact_uri)

    parsed_uri = urllib.parse.urlparse(str(artifact_uri))
    prefix = ""
    if parsed_uri.scheme and not parsed_uri.path.startswith("/"):
        # relative path is a special case, urllib does not reconstruct it properly
        prefix = parsed_uri.scheme + ":"
        parsed_uri = parsed_uri._replace(scheme="")

    # For models:/ URIs, it doesn't make sense to initialize a ModelsArtifactRepository with only
    # the model name portion of the URI, then call download_artifacts with the version info.
    if ModelsArtifactRepository.is_models_uri(artifact_uri):
        root_uri, artifact_path = ModelsArtifactRepository.split_models_uri(artifact_uri)
    else:
        artifact_path = posixpath.basename(parsed_uri.path)
        parsed_uri = parsed_uri._replace(path=posixpath.dirname(parsed_uri.path))
        root_uri = prefix + urllib.parse.urlunparse(parsed_uri)

    return get_artifact_repository(artifact_uri=root_uri), artifact_path


if __name__ == "__main__":
    delete_all_old_artifacts()