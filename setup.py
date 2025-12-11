import os

libraries = [
    "requests",
    "comtypes",
    "pillow",
    "selenium",
    "colorama",
    "soundcard",
    "soundfile",
    "pycaw",
    "requests"
    "pywin32"
]

for library in libraries:
    print(f"Installing {library}...")
    os.system(f"pip install {library}")
    print(f"{library} installation finished.\n")
