import copy
from static_to_public import copy_from_to
from markdown_to_html import generate_pages_recursive
import os
import sys
import shutil

def main(argv):
    if len(argv) == 2:
        basepath = argv[1]
    else: basepath = '/'
    src = './content'
    dst = './docs'
    static_content = './static'
    verbose = False

    abs_dest = os.path.abspath(dst)
    if os.path.exists(abs_dest):
        shutil.rmtree(abs_dest)
    if verbose:
        print("STEP 1 removing", dir_dest, 'to remake it at', abs_dest, '\n')
        
    copy_from_to(static_content, dst, verbose)
    copy_from_to(src, dst, verbose)
    
    generate_pages_recursive(os.path.abspath(src), "template.html", dst, basepath)

if __name__ == "__main__":
    main(sys.argv)  # the argv[0] is the current filename.

