import sys
from pathlib import Path
from revolt_hostctl.app.app import App


APP_ROOT = Path(__file__).resolve().parents[2]


def main():
    app = App(APP_ROOT)
    args = sys.argv[1:]

    if len(args):
        if args[0] == "--version":
            print(app.get_version())
        else:
            print("Unknown command")
    else:
        print("No arguments provided")
        sys.exit(0)
