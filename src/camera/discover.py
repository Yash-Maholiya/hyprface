from pathlib import Path
import subprocess
from dataclasses import dataclass

@dataclass
class CameraInfo:
    index: int
    device: str
    card_type: str
    is_ir: bool

def get_card_type(device):
    try:
        output = subprocess.check_output(
            ["v4l2-ctl", "-d", device, "--all"],
            stderr=subprocess.DEVNULL,
            text=True,
        )

        for line in output.splitlines():
            if "Card type" in line:
                return line.split(":", 1)[1].strip()

    except Exception:
        pass

    return "Unknown"

def discover_cameras():
    cameras = []

    for dev in sorted(Path("/dev").glob("video*")):
        
        index = int(dev.name.replace("video", ""))
        
        card_type = get_card_type(str(dev))

        cameras.append(
            CameraInfo(
                index=index,
                device=str(dev),
                card_type=card_type,
                is_ir="ir" in card_type.lower(),
            )
        )

    return cameras  

'''
def find_preferred_camera():
    cameras = discover_cameras()

    # Prefer IR camera
    for cam in cameras:
        if cam.is_ir:
            return cam

    # Fallback to first available camera
    if cameras:
            return cameras[0]

    return None
'''

if __name__ == "__main__":

    cams = discover_cameras()

    for cam in cams:
        print(cam)

'''
    print("\nDetected Cameras\n")

    for cam in cameras:
        print(f"Device      : {cam.device}")
        print(f"Card Type   : {cam.card_type}")
        print(f"IR Camera   : {cam.is_ir}")
        print("-" * 40)

    preferred = find_preferred_camera()

    if preferred:
        print("\nSelected Camera")
        print(f"Device      : {preferred.device}")
        print(f"Card Type   : {preferred.card_type}")
    else:
        print("No camera dound.")   
''' 