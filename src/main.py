import sys

from copystatic import copy_dir_content
from gencontent import generate_pages_recursive

def main():
    """Executes the static site generation process.

    This function coordinates the build process by copying static assets
    to the output directory and recursively generating HTML pages from 
    Markdown content. It determines the base URL path from command-line 
    arguments to support different hosting environments (like GitHub Pages).

    Args:
        None directly, but reads from sys.argv:
            sys.argv[1] (str, optional): The base path for the generated site.
                Defaults to "/".

    Returns:
        None

    Side Effects:
        - Clears and populates the './docs' directory with static files.
        - Generates HTML files in './docs' based on './content' and 'template.html'.
    """
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