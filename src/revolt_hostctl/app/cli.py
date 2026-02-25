import sys
from pathlib import Path
from revolt_hostctl.app.app import App


def build_app() -> App:
    app_root = Path(__file__).resolve().parents[2]
    return App(app_root)


def main():
    app = build_app()
    args = sys.argv[1:]

    if len(args):
        if args[0] == "version":
            print(app.get_version())
        else:
            print("Unknown command")
    else:
        print("No arguments provided")
        sys.exit(0)
