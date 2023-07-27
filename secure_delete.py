import os
import getpass
import subprocess

def secure_delete(path):
    """
    Securely delete a file or directory at a specified path
    """
    # The 'shred' command overwrites a file with random data multiple times, making it hard to recover
    # '-u' option deletes the file after overwriting
    # '-v' option shows progress
    if os.path.isfile(path):
        subprocess.run(['shred', '-u', '-v', path])
    elif os.path.isdir(path):
        delete = input(f"{path} is a directory. Do you want to delete the entire directory? [yes/no]: ")
        if delete.lower() == "yes":
            # Recursively delete all files in a directory
            for dirpath, dirnames, filenames in os.walk(path, topdown=False):
                for name in filenames:
                    file_path = os.path.join(dirpath, name)
                    subprocess.run(['shred', '-u', '-v', file_path])
            # Finally, delete the directory itself
            os.rmdir(path)
        else:
            print("The directory was not deleted.")
    else:
        print(f"No such file or directory: {path}")

if __name__ == "__main__":
    file_or_folder = input("Enter the path of the file or folder to securely delete: ")
    secure_delete(file_or_folder)
