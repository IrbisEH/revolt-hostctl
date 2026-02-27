import sys
from pathlib import Path
from revolt_hostctl.app.app import App


APP_ROOT = Path(__file__).resolve().parents[2]


def main():
    app = App(APP_ROOT)
    args = sys.argv[1:]

    try:
        if not len(args):
            raise Exception("No command provided")

        cmd = args.pop(0)

        if cmd in ["-h", "--help"]:
            app.help()

        elif cmd == "--add":
            app.add_obj(args)

        elif cmd == "--update":
            app.update_obj(args)

        elif cmd == "--remove":
            app.remove_obj(args)

        elif cmd == "--list":
            app.list_objs(args)

        elif cmd == "--version":
            app.version()

    except Exception as e:
        print(f"Error: {e}")
        exit(1)
