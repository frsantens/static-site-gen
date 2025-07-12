from static_to_public import copy_from_to
import sys

def main(argv=None):
    # if len(argv) > 1:
    #     src = argv[1]
    #     dst = argv[2]
    # verbose = False
    # if len(sys.argv) > 3 and sys.argv[3] == "-v":
    #     verbose = True
    #     copy_from_to(src='./static', dst='./public', verbose=False)
    # else:
    src = './static'
    dst = './public'
    verbose = False
    copy_from_to(src, dst, verbose)


if __name__ == "__main__":
    main()  # the argv[0] is the current filename.
