# clean_cache.py
import os
import shutil
import sys

print("🧹 Cleaning Python cache files...")

# Find and remove all __pycache__ directories
for root, dirs, files in os.walk('.'):
    for dir_name in dirs:
        if dir_name == '__pycache__':
            cache_dir = os.path.join(root, dir_name)
            try:
                shutil.rmtree(cache_dir)
                print(f"✅ Removed: {cache_dir}")
            except Exception as e:
                print(f"⚠️  Could not remove {cache_dir}: {e}")

# Remove .pyc files
for root, dirs, files in os.walk('.'):
    for file_name in files:
        if file_name.endswith('.pyc'):
            pyc_file = os.path.join(root, file_name)
            try:
                os.remove(pyc_file)
                print(f"✅ Removed: {pyc_file}")
            except Exception as e:
                print(f"⚠️  Could not remove {pyc_file}: {e}")

print("\n✅ Cleanup complete!")
print("\nNow run: python run.py")