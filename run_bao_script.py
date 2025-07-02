import subprocess

def run_script(command: str):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(f"Error:\n{result.stderr}")
    if result.returncode != 0:
        print(f"Script failed with exit code {result.returncode}. Stopping.")
        exit(result.returncode)

def trans_to_next(db='imdb'):
    # 1️⃣ 删除旧模型
    print("Deleting old Bao model...", flush=True)
    subprocess.run("rm -rf /app/source/baselines/Bao/bao_server/bao_default_model", shell=True, check=True)
    subprocess.run("rm -rf /app/source/baselines/Bao/bao_server/bao_previous_model", shell=True, check=True)

    # 2️⃣ 修改 bao.cfg
    cfg_path = "/app/source/baselines/Bao/bao_server/bao.cfg"
    print(f"Modifying {cfg_path}...", flush=True)

    with open(cfg_path, "r") as f:
        lines = f.readlines()

    with open(cfg_path, "w") as f:
        for line in lines:
            if line.strip().startswith("PostgreSQLConnectString"):
                f.write(f"PostgreSQLConnectString = dbname='{db}' user='postgres' password='postgres' host='pg1'\n")
            else:
                f.write(line)

    # 3️⃣ restart_bao_server
    # Step 1: Kill existing bao-server screen if it exists
    result = subprocess.run("screen -ls | grep bao-server", shell=True, stdout=subprocess.PIPE)
    if result.stdout:
        print("Existing bao-server screen found, terminating it...", flush=True)
        subprocess.run("screen -S bao-server -X quit", shell=True, check=True)
    else:
        print("No existing bao-server screen found, proceeding to start.", flush=True)

    # Step 2: Start bao-server in detached screen
    print("Starting bao-server in detached screen...", flush=True)
    subprocess.run(
        "screen -dmS bao-server bash -c 'cd /app/source/baselines/Bao/bao_server && python main.py'",
        shell=True,
        check=True
    )

if __name__ == "__main__":
    command_list = [
        (
            'python run_queries.py '
            '--database_name imdb '
            '--query_dir /app/source/BiSplit/data/job-static/job-static.txt '
            '--output_file train__bao__job_static.txt'
        ),
        (
            'python run_queries.py '
            '--database_name imdb '
            '--query_dir /app/source/BiSplit/data/job-dynamic/job-dynamic.txt '
            '--output_file train__bao__job_dynamic.txt'
        ),
    ]

    db_list = ['stack', 'stack']
    for idx, command in enumerate(command_list):
        trans_to_next(db=db_list[idx])
        run_script(command)
