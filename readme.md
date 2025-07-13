# usage:

generates html pages from md files to be hosted on github.

sh build.sh <"{repo-name}/">

1. wipes './docs'
2. Copies (non markdown) files from './static/' to './docs' (creates dir and subdirs)
3. converts markdown to html and places them correctly in './docs'

This is a project made from a boot.dev python course
