from services.git_manager import auto_commit_and_push
import os

if __name__ == "__main__":
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    auto_commit_and_push(repo_path)
