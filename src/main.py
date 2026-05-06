import sys

from copystatic import copy_dir_content
from gencontent import generate_pages_recursive

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    dir_path_static = "./static"
    dir_path_public = "./docs" #GitHub Pages serves sites from docs directory of main branch by default
    dir_path_content = "./content"

    copy_dir_content(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, "template.html", dir_path_public, basepath)

main()