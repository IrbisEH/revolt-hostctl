from pathlib import Path
from revolt_hostctl.app.app import App


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parents[2]
    app = App(root_dir)
