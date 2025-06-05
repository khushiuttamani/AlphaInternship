import os
import shutil

# Define categories and their extensions
FILE_CATEGORIES = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    "Documents": ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx'],
    "Audio": ['.mp3', '.wav', '.m4a'],
    "Videos": ['.mp4', '.mov', '.avi', '.mkv'],
    "Archives": ['.zip', '.rar', '.tar', '.gz'],
    "Scripts": ['.py', '.js', '.html', '.css', '.ipynb'],
    "Executables": ['.exe', '.msi'],
    "Others": []
}

def get_category(extension): #function for getting the category
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def organize_directory(directory): #function for organizing the directory
    if not os.path.exists(directory):
        print("The specified directory does not exist.") #check if the directory exists
        return

    print(f"📁 Organizing files in: {directory}\n")

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        _, ext = os.path.splitext(file)
        category = get_category(ext)

        category_folder = os.path.join(directory, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # Move the file
        new_path = os.path.join(category_folder, file)
        shutil.move(file_path, new_path)
        print(f"Moved: {file} → {category}/")

    print("\n File organization complete!")

if __name__ == "__main__":
    #input the path of the directory you want to organize
    target_directory = input("Enter the path of the directory to organize: ").strip()
    organize_directory(target_directory)
