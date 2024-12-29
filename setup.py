import os

# لیست تمام کتابخانه‌هایی که نیاز دارید
libraries = [
    "requests",
    "comtypes",
    "pillow",
    "selenium",
    "colorama",
    "soundcard",
    "soundfile",
    "pycaw",
    "pywin32"
]

# نصب هر کتابخانه
for library in libraries:
    print(f"Installing {library}...")
    os.system(f"pip install {library}")
    print(f"{library} installation finished.\n")
