import os
import getpass
import subprocess
from colorama import Fore, Style

def secure_delete(path):
    """
    Securely delete a file or directory at a specified path
    """
    # Check if the path exists
    if not os.path.exists(path):
        print(f"{Fore.RED}Error: No such file or directory: {path}{Style.RESET_ALL}")
        return

    # The 'shred' command overwrites a file with random data multiple times, making it hard to recover
    # '-u' option deletes the file after overwriting
    # '-v' option shows progress
    if os.path.isfile(path):
        delete = input(f"{Fore.YELLOW}Are you sure you want to delete the file at {path}? [yes/no]: {Style.RESET_ALL}")
        if delete.lower() == "yes":
            result = subprocess.run(['shred', '-u', '-v', path], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"{Fore.RED}Error: {result.stderr}{Style.RESET_ALL}")
            else:
                print(result.stdout)
        else:
            print("The file was not deleted.")
    elif os.path.isdir(path):
        delete = input(f"{Fore.YELLOW}Are you sure you want to delete the entire directory at {path}? [yes/no]: {Style.RESET_ALL}")
        if delete.lower() == "yes":
            # Recursively delete all files in a directory
            for dirpath, dirnames, filenames in os.walk(path, topdown=False):
                for name in filenames:
                    file_path = os.path.join(dirpath, name)
                    result = subprocess.run(['shred', '-u', '-v', file_path], capture_output=True, text=True)
                    if result.returncode != 0:
                        print(f"{Fore.RED}Error: {result.stderr}{Style.RESET_ALL}")
                    else:
                        print(result.stdout)
            # Finally, delete the directory itself
            try:
                os.rmdir(path)
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        else:
            print("The directory was not deleted.")
    else:
        print(f"{Fore.RED}Error: Not a file or directory: {path}{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"{Fore.BLUE}This program will securely delete a file or directory. Please use with caution as deleted data may not be recoverable.{Style.RESET_ALL}")
    file_or_folder = input("Enter the path of the file or folder to securely delete: ")
    secure_delete(file_or_folder)
