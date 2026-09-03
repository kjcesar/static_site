from textnode import TextNode, TextType
import os
import shutil


def copy_files_recursively(source, destination):
    """
    It copy files from a source to a destination
    """
    files_in_source = os.listdir(source)
    for file in files_in_source:  # file is just a name
        file_path = os.path.join(source, file)  # now i have a path
        print(file_path)
        if os.path.isfile(file_path):  # here i use full path
            shutil.copy(file_path, destination)
        elif os.path.isdir(file_path):  # here i use full path too
            os.mkdir(
                os.path.join(destination, file)
            )  # creating the subfolder in the destination using file name
            copy_files_recursively(
                os.path.join(source, file), os.path.join(destination, file)
            )  # recursive call


def copy_to_public_from_static(source, destination):
    """
    Function that copies all the contents from a source directory to a destination directory (in our case, static to public)

    It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    It should copy all files and subdirectories, nested files, etc.
    I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.

    """
    # deleting destination for a clean copy
    print("deleting destination")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    # creating destination
    print("creating public")
    os.mkdir(destination)

    copy_files_recursively(source, destination)


def main():
    path = __file__
    root_dir = os.path.dirname(os.path.dirname(path))
    static_path = os.path.join(root_dir, "static")
    public_path = os.path.join(root_dir, "public")

    copy_to_public_from_static(static_path, public_path)


main()
