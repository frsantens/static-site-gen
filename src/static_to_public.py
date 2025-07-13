import os
import shutil

def copy_from_to(dir_src, dir_dest, verbose):
    if not os.path.isdir(dir_src):
        raise Exception('not a directory, takes two dirs as arguments')
    if not os.path.exists(dir_src):
        raise Exception('source directory does not exist')
    abs_src = os.path.abspath(dir_src)
    abs_dest = os.path.abspath(dir_dest)
    if os.path.exists(abs_dest):
        shutil.rmtree(abs_dest)
        if verbose:
            print("STEP 1 removing", dir_dest, 'to remake it at', abs_dest, '\n')
    os.mkdir(abs_dest)
    
    copy_recursive(abs_src, abs_dest, verbose)

def copy_recursive(src, dest, verbose):
    entries_list = os.listdir(src)
    if verbose:
        print("source dir contains:", entries_list, '\n')
    dest_nested = dest
    for entr in entries_list:
        entr_path = os.path.join(src, entr)
        if os.path.isdir(entr_path):            
            dest_nested = os.path.join(dest, entr)
            if verbose:
                print(" filepath:", os.path.abspath(entr_path))
                print(f'  ->  making dir {entr} at dest={dest_nested}')
                print(f"\ndoing recursive: copy_recursive({entr}, {dest_nested})")
            os.mkdir(dest_nested)
            copy_recursive(entr_path, dest_nested, verbose)
        elif os.path.isfile(entr_path) and not entr.endswith('.md'):
            if verbose:
                print(" filepath:", os.path.abspath(entr_path))
                print(f"   -> coppying file {entr} to {dest}\n")
            shutil.copy(entr_path,dest)
            
            

    