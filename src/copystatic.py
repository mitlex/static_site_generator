import shutil
import os

def copy_dir_content(src, dst):
    """Recursively copies contents from source to destination.

    Deletes the destination directory if it exists and recreates it before 
    starting the copy process. All files and subdirectories are copied 
    recursively.

    Args:
        src (str): The path to the source directory.
        dst (str): The path to the destination directory.

    Returns:
        None
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    def _recurse(current_src, current_dst):
        src_content = os.listdir(current_src)
        
        for entry in src_content:
            entry_path = os.path.join(current_src, entry)
            
            if os.path.isfile(entry_path):
                shutil.copy(entry_path, current_dst)
            else:
                new_dst_path = os.path.join(current_dst, entry)
                os.mkdir(new_dst_path)
                _recurse(entry_path, new_dst_path)

    _recurse(src, dst)