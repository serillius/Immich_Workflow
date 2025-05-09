import os
import sys
import subprocess

def load_api_key(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, sep, value = line.partition('=')
                if sep:
                    os.environ[key.strip()] = value.strip()

if __name__ == '__main__':
    current_dir = os.getcwd()
    env_path = current_dir + '/.env'
    immich_go_path = current_dir + '/immich-go'

    load_api_key(env_path)
    api_key = os.getenv("IMMICH_API_KEY")
    immich_server = os.getenv("IMMICH_SERVER")
    upload_path = sys.argv[1]

    if not api_key:
        print("Error: IMMICH_API_KEY is not set in the .env file")
        sys.exit(1)
    if not immich_server:
        print("Error: IMMICH_SERVER is not set in the .env file")
        sys.exit(1)
    if not os.path.isfile(immich_go_path):
        print("Error: immich-go executable not found")
        sys.exit(1)

    cmd = [
        f"{immich_go_path}",
        "upload",
        "from-folder",
        f"--server={immich_server}",
        f"--api-key={api_key}",
        "--into-album=Ingested",
        "--manage-raw-jpeg=StackCoverJPG",
        f"{upload_path}",
    ]
    print("Uploading pictures to IMMICH")
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)
