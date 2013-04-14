DataMap
=======

DataMap Senior Design Project


Compiling/Installing
====================

DataMap can be compiled and installed using the following commands (you probably alread did the first two if you are reading this):

git clone https://github.com/DataMap13/DataMap.git
cd DataMap
./configure
make
sudo make install

The configure script will prompt you for a series of configuration parameters. Many of the parameters have defaults that should work fine, but you may change them if you like. It is important the the IP addresses provided to this script match the ones that will be used when the system is actually deployed and running. Any of the values in the configuration script can be changed by running th script again (or editing the .config file) and most will not require recompilation or reinstallation.


Updating Vermont (for developers)
================

When making updates to vermont, you can make changes directly in the vermont/ directory and compile (using make) and run your changes there. Note that you should run the full DataMap compile first. When you are done making changes. execute the following command (from the root DataMap/ directory):

tar uvf vermont_patch.tar [files]

where [files] is a space separated list of the source files that you have updated or added. This will add any new files to the patch archive and update existing ones. This patch is applied to vermont during DataMap compilation. Finally, you can commit and push the changes to the patch file (vermont_patch.tar) using git.
