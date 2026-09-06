import os
from creating import generate_pages_recursive, copy_to_public_from_static
import sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    path = __file__
    root_dir = os.path.dirname(os.path.dirname(path))
    static_path = os.path.join(root_dir, "static")
    public_path = os.path.join(root_dir, "docs")

    copy_to_public_from_static(static_path, public_path)
    # generating page
    content_path = os.path.join(root_dir, "content")
    template = os.path.join(root_dir, "template.html")
    generate_pages_recursive(content_path, template, public_path, basepath)


main()
