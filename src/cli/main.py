import sys

from src.camera.manager import select_camera
from src.camera.capture import start_camera
from src.camera.doctor import doctor
from src.config.config import load_config



def main():

    if len(sys.argv) < 2:
        print(
            "Usage: python -m src.cli.main "
            "[scan|capture|doctor]"
        )
        return

    command = sys.argv[1]

    if command == "scan":
        select_camera()

    elif command == "doctor":
        doctor()

    elif command == "capture":

        config = load_config()

        index = config.get(
            "camera_index"
        )

        if index is None:
            print(
                "Run scan first."
            )
            return

        start_camera(index)

    else:
        print(
            "Unknown command."
        )


if __name__ == "__main__":
    main()