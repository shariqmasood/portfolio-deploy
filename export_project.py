import os

# Define file extensions you want to include
valid_extensions = ['.py', '.html', '.css', '.js', '.txt', '.md', '', '.json']

# Define the output file
output_file = "project_summary.txt"

# Walk through all directories and files
with open(output_file, "w", encoding='utf-8') as out:
    for root, dirs, files in os.walk("."):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in valid_extensions and ".venv" not in root and "__pycache__" not in root and ".idea" not in root:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding='utf-8') as f:
                        rel_path = os.path.relpath(full_path, ".")
                        out.write(f"\n\n### FILE: {rel_path} ###\n")
                        out.write(f.read())
                        out.write("\n\n" + "#" * 60 + "\n")
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")

print(f"\n✅ Project exported to: {output_file}")
