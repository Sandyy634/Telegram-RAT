import os
import sys
import shutil

def add_to_startup():
    try:
        # Get startup folder path
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        script_path = os.path.abspath(sys.argv[0])
        dest = os.path.join(startup_folder, os.path.basename(script_path))

        if not os.path.exists(dest):
            shutil.copy(script_path, dest)
        return True
    except Exception as e:
        return False
