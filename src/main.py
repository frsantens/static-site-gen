from static_to_public import copy_from_to
from markdown_to_html import generate_page, generate_pages_recursive
import os

def main():
    src = './static'
    dst = './public'
    verbose = False
    copy_from_to(src, dst, verbose)
    generate_pages_recursive(os.path.abspath("./content/"), "template.html", dst)
    # generate_page("content/index.md","template.html","public/index.html")
    # generate_page("content/contact/index.md","template.html","public/contact/index.html")
    # generate_page("content/blog/glorfindel/index.md","template.html","public/blog/glorfindel/index.html")
    # generate_page("content/blog/majesty/index.md","template.html","public/blog/majesty/index.html")
    # generate_page("content/blog/tom/index.md","template.html","public/blog/tom/index.html")

if __name__ == "__main__":
    main()  # the argv[0] is the current filename.

