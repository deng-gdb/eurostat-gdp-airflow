import subprocess



if __name__ == "__main__":
    # create Prefect blocks
    subprocess.run("python setup/blocks/create_blocks.py", shell=True)
