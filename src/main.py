from copystatic import copy_dir_content
from gencontent import generate_pages_recursive

def main():
    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_content = "./content"

    copy_dir_content(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, "template.html", dir_path_public)

main()