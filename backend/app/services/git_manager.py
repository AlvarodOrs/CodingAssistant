import git
import os
import subprocess
import threading
from datetime import datetime

def auto_commit_and_push(repo_path: str, commit_message: str = None):
    """
    Automatically stages and commits specified files to the git repository.

    :param repo_path: Path to the git repository.
    :param file_paths: List of file paths to stage and commit.
    :param commit_message: Commit message for the commit.
    """
    try:
        def ask_for_message():
            nonlocal commit_message
            try: 
                commit_message = input("Enter commit message: ").strip()
            except Exception as e:
                print(f"Error getting commit message: {e}")
                commit_message = None

        # If no commit message is provided, ask the user in a separate thread
        if not commit_message:
            print("No commit message provided. You can enter one now or wait for the default message.")
            thread = threading.Thread(target=ask_for_message)
            thread.start()
            thread.join(timeout=30)  # Wait for 30 seconds for user input

            # If still no message, use default
            if not commit_message:
                commit_message = f"Auto-update on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                print(f"No commit message entered. Using default: {commit_message}")
        try:
            subprocess.run(['git', '-C', repo_path, "add", "."], check=True)
            subprocess.run(['git', '-C', repo_path, "commit", "-m", commit_message], check=True)
            subprocess.run(['git', '-C', repo_path, "push"], check=True)
            print("Gideon committed and pushed successfully.")
        except subprocess.CompletedProcessError as e:
            print(f"An error occurred during git execution: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")