import os

from markdown_blocks import markdown_to_html_node
from pathlib import Path

"""
extract_title: 
Pulls the '# ' header from the given md file string and returns it. If no '# ' header exists - raise an exception.
"""
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Provided markdown does not contain a '# ' heading")

"""Generate an HTML page from a markdown file and template.

Reads markdown from from_path, converts it to HTML, extracts the
title, injects both into the template, and writes the result to
dest_path.

Args:
    from_path: path to source markdown file
    template_path: path to an html template file
    dest_path: location where the final html file will be written to disk (parent directories are created as needed)

Returns:
    None
"""
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    #read both files and store content in str variables
    md = ""
    with open(from_path) as f:
        md = f.read()

    html_template = ""
    with open(template_path) as f:
        html_template = f.read()

    #get title and content, inject into html template
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    new_html = html_template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    #write new html to dest_path, creating directories as necessary
    dest_path_dirs = os.path.dirname(dest_path)
    os.makedirs(dest_path_dirs, exist_ok=True) #will not execute if dirs already exist 
    with open(dest_path, mode="w") as f:
        f.write(new_html)

"""Recursively crawls a directory tree generating HTML files for all md files found

Iterates through current dir_path_content directory entries.
if a file is found, calls generate_page function to generate an HTML page.
Page is written to a destination path.
otherwise (if entry is a sub-directory) recursively calls itself with the sub-directory.

Args:
    dir_path_content: path to source directory
    template_path: path to an html template file
    dest_dir_path: location where the final html file will be written to disk (parent directories are created as needed by generate_page function)

Returns:
    None
"""
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    src_entries = os.listdir(dir_path_content)

    for entry in src_entries:
        entry_path = os.path.join(dir_path_content, entry)

        # Markdown source files need to become HTML output files, so keep the same
        # name/location in the destination tree but change the file extension to .html
        # Example: content/index.md -> public/index.html
        if os.path.isfile(entry_path):
            dest_path = Path(os.path.join(dest_dir_path, entry)).with_suffix('.html')
            generate_page(entry_path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(entry_path, template_path, dest_path)