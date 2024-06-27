import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, source_folder, destination_folders):
        super().__init__()
        self.source_folder = source_folder
        self.destination_folders = destination_folders

    def on_created(self, event):
        if not event.is_directory:
            filename = event.src_path
            file_extension = os.path.splitext(filename)[1].lower()

            for file_type, extensions in self.destination_folders.items():
                if file_extension in extensions:
                    self.move_file(filename, file_type)
                    break

    def move_file(self, filename, file_type):
        # Check if the file exists (wait a short time for the download to complete)
        max_attempts = 5
        attempt = 0
        while not os.path.exists(filename) and attempt < max_attempts:
            time.sleep(1)
            attempt += 1

        if os.path.exists(filename):
            # Move the file to the destination folder
            basename = os.path.basename(filename)
            destination_folder = self.destination_folders[file_type]
            destination_file_path = os.path.join(destination_folder, basename)

            try:
                shutil.move(filename, destination_file_path)
                print(f"Moved {basename} to {destination_folder}")
            except Exception as e:
                print(f"Error moving {basename}: {e}")
        else:
            print(f"File {filename} not found after download.")

if __name__ == "__main__":
    # Define source and destination folders
    downloads_folder = r"C:\Users\willi\Downloads"  # Adjust with your actual path

    # Define destination folders based on file types
    destination_folders = {
        'Images': ('.png', '.jpg', '.jpeg', '.gif'),
        'Documents': ('.pdf', '.doc', '.docx'),
        'Videos': ('.mp4', '.mov', '.avi'),
        # Add more categories as needed
    }

    # Create the handler and observer
    event_handler = DownloadHandler(downloads_folder, destination_folders)
    observer = Observer()
    observer.schedule(event_handler, downloads_folder, recursive=False)

    # Start monitoring
    observer.start()
    print(f"Monitoring {downloads_folder} for new downloads...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
