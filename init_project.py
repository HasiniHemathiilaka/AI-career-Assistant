import os
from backend.models.database import init_db, DATABASE_URL

def main():
    print("🚀 Initializing AI Career Assistant Database...")
    
    # 1. Strip the sqlite prefix to get the raw file system path
    db_path = DATABASE_URL.replace("sqlite:///", "")
    print(f"📂 Target database file path: {db_path}")
    
    # 2. Run the SQLAlchemy compilation
    try:
        init_db()
        print("⚙️ SQLAlchemy table metadata generation executed.")
    except Exception as e:
        print(f"❌ Error during init_db execution: {e}")
        return

    # 3. Explicit post-check verification
    if os.path.exists(db_path):
        print(f"✅ System initialized successfully! Check '{db_path}'.")
        print(f"📏 Database file size: {os.path.getsize(db_path)} bytes")
    else:
        print("❌ Critical Error: The database file still does not exist on disk after initialization.")

if __name__ == "__main__":
    main()