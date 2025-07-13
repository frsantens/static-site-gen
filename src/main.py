from static_to_public import copy_from_to
from markdown_to_html import generate_pages_recursive
import os
import sys

def main(argv):
    if len(argv) == 2:
        basepath = argv[1]
    else: basepath = '/'
    src = './content'
    dst = './docs'
    verbose = False
    copy_from_to(src, dst, verbose)
    generate_pages_recursive(os.path.abspath(src), "template.html", dst, basepath)

if __name__ == "__main__":
    main(sys.argv)  # the argv[0] is the current filename.

