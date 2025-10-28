import os
import threading
from backend.app.services import git_initiation
from backend.app.services.git_manager import auto_commit_and_push

def main():
    git_initiation.main()

    repo_path = os.getcwd()

    thread = threading.Thread(target=auto_commit_and_push, args=(repo_path,))
    thread.daemon = True
    thread.start()

    print("Gideon is running in the background as your live assistant.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n\nExiting Gideon...")
        
if __name__ == "__main__":
    main()