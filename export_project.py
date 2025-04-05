import os

output_file = "project_summary.txt"

# Directories and extensions to skip
exclude_dirs = {'.git', '.venv', '__pycache__', '.idea', 'node_modules', 'dist', 'build'}
exclude_exts = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.exe', '.dll', '.pyd', '.pyc',
    '.so', '.zip', '.tar', '.gz', '.pdf', '.db', '.woff', '.woff2', '.ttf'
}

def should_skip(path):
    return any(part in exclude_dirs for part in path.split(os.sep)) or \
           os.path.splitext(path)[1].lower() in exclude_exts

def read_file_safe(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading {file_path}: {e}\n"

summary = []

for root, dirs, files in os.walk(".", topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        rel_path = os.path.relpath(os.path.join(root, file), start=".")
        if should_skip(rel_path):
            continue
        content = read_file_safe(os.path.join(root, file))
        summary.append(f"\n\n# === {rel_path} ===\n\n{content}")

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(summary)

print("✅ Clean summary created as 'project_summary.txt' without .git and binary errors.")
