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

        if cmd == "-add":
            app.add_cmd(args)

        elif cmd == "-get":
            app.get_cmd(args)

        elif cmd == "-update":
            app.update_cmd(args)

        elif cmd == "-remove":
            app.remove_cmd(args)

        elif cmd == "-list":
            app.list_cmd(args)

        elif cmd == "-clean":
            app.clean_cmd()

        elif cmd == "-version":
            app.version_cmd()

        elif cmd in ["-h", "-help"]:
            print_help()

        else:
            raise Exception(f"Unknown command: {cmd}")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


def print_help():
    print(
        "Usage: revolt-hostctl <command> [options]\n"
        "\n"
        "Commands:\n"
        "  -add <obj_type> <params>      Add a new <obj_type> object\n"
        "  -get <obj_type> <params>      Get an <obj_type> object by ID\n"
        "  -update <obj_type> <params>   Update an existing <obj_type> object\n"
        "  -remove <obj_type> <id=>      Remove an <obj_type> object by ID\n"
        "  -list <obj_type>              List all <obj_type> objects\n"
        "  -clean                        Delete all objects\n"
        "  -version                      Show version information\n"
        "  -help, -h                     Show this help message\n"
        "\n"
        "_______\n"
        "Object types: network, host"
    )