import os
from helpers import markdown_to_html_node, extract_title
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


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    # Convert markdown to HTML using markdown_to_html_node() and .to_html()
    markdown_to_html = markdown_to_html_node(markdown).to_html()

    # Get title using extract_title()
    title = extract_title(markdown)

    # Replace {{ Title }} and {{ Content }} in template with generated title and HTML
    full_html = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", markdown_to_html)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    # Write full HTML page to dest_path (create dirs if needed)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Handling Subfolders
    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files_in_content = os.listdir(dir_path_content)
    for file in files_in_content:  # file is just a name
        file_path = os.path.join(dir_path_content, file)  # now i have a path
        print(file_path)
        if os.path.isfile(file_path):  # here i use full path
            # shutil.copy(file_path, destination)
            # instead of copy i need to generate if it is an md file
            # is an md file?
            if file_path.endswith(".md"):
                # it is an md file so i generate full_html
                # first i calculate destination path
                destination = os.path.join(dest_dir_path, file.replace(".md", ".html"))
                generate_page(file_path, template_path, destination, basepath)

        elif os.path.isdir(file_path):  # here i use full path too
            generate_pages_recursive(
                os.path.join(dir_path_content, file),
                template_path,
                os.path.join(dest_dir_path, file),
                basepath,
            )  # recursive call
