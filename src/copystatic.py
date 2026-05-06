import shutil
import os

"""
copy_dir_content: 
Deletes a given destination folder and recreates it fresh before recursively copying all contents from a given source folder into the new destination folder. 
Deletion of the destination folder only happens once before the recursive copying sequence begins.

Input: source directory, destination directory
Returns: None
"""
def copy_dir_content(src, dst):
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