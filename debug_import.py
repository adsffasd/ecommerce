import sys
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

try:
    print(f"Current working directory: {os.getcwd()}")
    print(f"sys.path: {sys.path}")
    import app
    print("Imported app successfully")
    import app.main
    print("Imported app.main successfully")
    from app.main import app as fastapi_app
    print(f"Imported app object: {fastapi_app}")
except Exception as e:
    print(f"Error importing: {e}")
    import traceback
    traceback.print_exc()
