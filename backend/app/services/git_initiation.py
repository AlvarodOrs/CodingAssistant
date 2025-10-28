import os
import subprocess
import backend.app.config as config

def check_git_installed() -> bool:
    """
    Check if Git is installed on the system.

    :return: True if Git is installed, False otherwise.
    """
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        print("Git is installed.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Git is not installed.")
        return False

def initialize_git_repo(repo_path: str) -> None:
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        try:
            subprocess.run(['git', '-C', repo_path, 'init'], check=True)
            print(f"Initialized a new Git repository in {repo_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to initialize Git repository: {e}")
    else:
        print(f"Git repository already exists in {repo_path}")

def check_git_user_config() -> bool:
    """Check if Git global username and email are configured."""
    try:
        username_proc = subprocess.run(
            ['git', 'config', '--global', 'user.name'],
            capture_output=True,
            text=True,
            encoding='utf-8',  # force UTF-8
            errors='ignore',   # ignore bad characters
            check=False
        )
        email_proc = subprocess.run(
            ['git', 'config', '--global', 'user.email'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            check=False
        )

        username = username_proc.stdout.strip() if username_proc.stdout else ""
        email = email_proc.stdout.strip() if email_proc.stdout else ""

        if username and email:
            print(f"Git user.name and user.email are configured to {username} & {email}")
            return True
        else:
            print("Git user.name and/or user.email are not configured.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Failed to check Git configuration: {e}")
        return False
    
def configure_git_user() -> None:
    """
    Configure git global username/email from config.py and print them.
    """
    if not config.GIT_USERNAME or not config.GIT_EMAIL:
        print("❌ Git username/email not set in config.py")
        return
    try:
        subprocess.run(['git', 'config', '--global', 'user.name', config.GIT_USERNAME], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', config.GIT_EMAIL], check=True)
        # Print what is being used
        print(f"✅ Git global user set to: {config.GIT_USERNAME} <{config.GIT_EMAIL}>")
    except subprocess.CalledProcessError as e:
        print(f"Failed to configure Git user: {e}")
        return

def main():
    repo_path = os.path.dirname(os.path.abspath(__file__))

    if not check_git_installed():
        return

    initialize_git_repo(repo_path)

    if not check_git_user_config():
        configure_git_user()
    
if __name__ == "__main__":
    main()

