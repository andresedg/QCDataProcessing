import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

def select_folder():
    """Function to select a folder using PyQt5."""
    app = QApplication.instance()  # Check if there's already a QApplication instance
    if app is None:
        app = QApplication(sys.argv)  # Create a new application if none exists

    folder = QFileDialog.getExistingDirectory(None, "Select Folder")
    
    if not folder:  # Check if no folder was selected (user canceled)
        print("Folder selection canceled.")
        return None

    app.exit()  # Close the application
    return folder


def select_file():
    """Function to select a file using PyQt5."""
    app = QApplication.instance()  # Check if there's already a QApplication instance
    if app is None:
        app = QApplication(sys.argv)  # Create a new application if none exists

    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly  # Optional: make the file dialog read-only
    file, _ = QFileDialog.getOpenFileName(None, "Select File", "", ".xyz (*.xyz);;All Files (*)", options=options)

    if not file:  # Check if no file was selected (user canceled)
        print("File selection canceled.")
        return None

    app.exit()  # Close the application
    return file


# Testing the functions
if __name__ == "__main__":
    folder = select_folder()
    if folder:
        print(f"Folder selected: {folder}")
    else:
        print("Folder selection canceled.\n")

    file = select_file()
    if file:
        print(f"File selected: {file}")
    else:
        print("File selection canceled.\n")