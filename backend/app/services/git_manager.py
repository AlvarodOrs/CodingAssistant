import git
import os
import subprocess
import threading
import time
from datetime import datetime
from app import config

def auto_commit_and_push(repo_path: str, commit_message: str = None):
    """
    Automatically stages and commits specified files to the git repository.

    :param repo_path: Path to the git repository.
    :param commit_message: Commit message for the commit.
    """
    def has_changes():
        """
        Check if there are any changes in the repository.
        """
        result = subprocess.run(['git', '-C', repo_path, 'status', '--porcelain'], capture_output=True, text=True)
        return bool(result.stdout.strip())
        
    def commit_and_push():
        nonlocal commit_message
        if not commit_message:
            def ask_for_message():
                nonlocal commit_message
                try:
                    user_input = input("Enter commit message: ").strip()
                    if user_input:
                        commit_message = user_input
                except Exception:
                    commit_message = None

            thread = threading.Thread(target=ask_for_message)
            thread.start()
            thread.join(timeout=config.USER_INPUT_TIMEOUT)

            if not commit_message:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                commit_message = config.DEFAULT_COMMIT_MESSAGE.format(timestamp=timestamp)
                print(f"⏰ No se introdujo mensaje. Usando automático: '{commit_message}'")
        try:
            subprocess.run(['git', '-C', repo_path, "add", "."], check=True)
            subprocess.run(['git', '-C', repo_path, "commit", "-m", commit_message], check=True)
            subprocess.run(['git', '-C', repo_path, "push"], check=True)
            print("Gideon committed and pushed successfully.")
        except subprocess.CompletedProcessError as e:
            print(f"An error occurred during git execution: {e}")

    print(f"Gideon initiated, he will commit changes in the background every {config.AUTO_COMMIT_INTERVAL} seconds.")
    while True:
        if has_changes():
            print("Checking for changes to commit...")
            commit_and_push()
        else:
            print("No changes detected.")
            time.sleep(config.AUTO_COMMIT_INTERVAL)