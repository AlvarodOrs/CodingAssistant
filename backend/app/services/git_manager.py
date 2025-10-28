import git
from datetime import datetime

def auto_commit_and_push(repo_path: str, commit_message: str = None):
    """
    Automatically stages and commits specified files to the git repository.

    :param repo_path: Path to the git repository.
    :param file_paths: List of file paths to stage and commit.
    :param commit_message: Commit message for the commit.
    """
    try:
        repo = git.Repo(repo_path)
        if repo.is_dirty(untracked_files=True):
            repo.git.add(all=True)
            if not commit_message:
                commit_message = f"Auto-update on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            origin.push()
            print("Gideon committed and pushed successfully.")
        else:
            print("No changes to commit.")
    except Exception as e:
        print(f"An error occurred during git operations: {e}")