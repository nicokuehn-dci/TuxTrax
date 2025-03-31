import subprocess
import sys

def launch_electron_app():
    try:
        subprocess.run(["npm", "start"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching Electron app: {e}")
        sys.exit(1)

def main():
    launch_electron_app()

if __name__ == "__main__":
    main()
