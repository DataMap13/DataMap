DataMap
=======

DataMap Senior Design Project


Updating Vermont
================

When making updates to vermont, you can make changes directly in the vermont/ directory and compile (using make) and run your changes there. Note that you should run the full DataMap compile first. When you are done making changes. execute the following command (from the root DataMap/ directory):

tar uvf vermont_patch.tar [files]

where [files] is a space separated list of the source files that you have updated or added. This will add any new files to the patch archive and update existing ones. This patch is applied to vermont during DataMap compilation. Finally, you can commit and push the changes to the patch file (vermont_patch.tar) using git.
