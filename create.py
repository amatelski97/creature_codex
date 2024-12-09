import os

# Define the base directory for your project
base_dir = "/home/tcc/tccodex/restructure/V2"  # Change this to your desired folder name

# Define the structure as a dictionary
structure = {
    "core": ["__init__.py", "config.py", "startup.py", "middleware.py", "dependencies.py"],
    "routers": ["__init__.py", "animal_profiles.py", "uploads.py"],
    "services": ["__init__.py", "animal_profiles.py", "uploads.py"],
    "repositories": ["__init__.py", "animal_profiles.py"],
    "utils": ["__init__.py", "csv_handler.py", "media_handler.py"],
    "schemas": ["__init__.py", "animal_profiles.py"],
    "": ["database.py", "models.py", "main.py", "__init__.py"],
}

# Create the folder and file structure
def create_structure(base_path, structure):
    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, "w") as f:
                # Add a placeholder comment in each file
                f.write(f"# Placeholder for {file}")

# Run the function
if __name__ == "__main__":
    create_structure(base_dir, structure)
    print(f"Structure created in '{base_dir}'!")
