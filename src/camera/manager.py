from src.camera.discover import discover_cameras
from src.config.config import save_config

def select_camera():

    cameras = discover_cameras()

    print("\nDetected Cameras\n")

    recommended = None
    
    for cam in cameras:

        text = f"[{cam.index}] {cam.card_type}"

        if  cam.is_ir and recommended is None:
            recommended = cam.index
            text += " (Recommended)" 

        print(text)

    print()

    choice = input(f"select camera [{recommended}]: ").strip()

    if choice =="":
        choice = recommended
    else:
        choice = int(choice)

    selected = None

    for cam in cameras:
        if cam.index == choice:
            selected = cam
            break

    save_config({
        "camera_index": selected.index,
        "camera_name": selected.card_type
    })

    print(
        f"\nSaved camera: {selected.device}"
    )

    return selected