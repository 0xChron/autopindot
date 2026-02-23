import subprocess
import shutil
import sys
import os

APP_NAME = "Autopindot"
ENTRY_FILE = "main.py"
ICON_PATH = "assets/favicon.ico"
ADD_DATA = "assets;assets" 


def run(cmd: list[str]):
    print(">>>", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def clean():
    for folder in ["build", "dist", f"{APP_NAME}.spec"]:
        if os.path.exists(folder):
            print(f"Removing {folder}...")
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            else:
                os.remove(folder)


def build(onefile=True):
    cmd = [
        "pyinstaller",
        "--windowed",
        "--name", APP_NAME,
        "--icon", ICON_PATH,
        "--add-data", ADD_DATA,
    ]

    if onefile:
        cmd.append("--onefile")

    cmd.append(ENTRY_FILE)

    run(cmd)


if __name__ == "__main__":
    mode = "--onedir" if "--onedir" in sys.argv else "--onefile"

    clean()

    if mode == "--onedir":
        build(onefile=False)
    else:
        build(onefile=True)

    print("\nbuild complete.")