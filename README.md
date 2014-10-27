DataMap
=======

DataMap Senior Design Project

Installation Prerequisites
--------------------------
DataMap is written to run on Debian derivatives and has been successfully
tested on Debian 7.6 (wheezy). The following packages are required for a
DataMap collection node:
+ cmake
+ g++
+ gcc
+ iw
+ libboost-dev
+ libboost-filesystem-dev
+ libboost-regex-dev
+ libboost-test-dev
+ libboost-thread-dev
+ libmysqlclient-dev
+ libpcap-dev
+ libsctp-dev
+ libssl-dev
+ libxml2-dev
+ make
+ python-mysqldb
+ screen
+ subversion
+ wireless-tools

In addition to the above packages, DataMap depends on [aircrack-ng] and
[vermont]; the steps for installing these dependencies are given below.
1. `aircrack-ng`

        wget http://download.aircrack-ng.org/aircrack-ng-1.2-beta3.tar.gz
        tar xvzf aircrack-ng-1.2-beta3.tar.gz
        cd aircrack-ng-1.2-beta3
        make
        sudo make install

2. `vermont`
    1. Follow the below steps to build `vermont`:

            git clone https://github.com/tumi8/vermont.git
            cd vermont
            git checkout -b datamap-dev c2f170a89ae9dd909b6d38cef52a5c565f1c7ffa
            git am DataMap13-vermont.patch
            mkdir build
            cd build
            cmake -D SUPPORT_MYSQL=ON ..
            make

    2. `vermont` uses `cmake` which by default **does not** provide an
       [uninstall target][cmake-uninstall]. You can install `vermont` with the
       standard:

            sudo make install

       DataMap does not require a full install of `vermont`; the required the
       components can be installed with:

            sudo install -m 0755 build/vermont /bin/vermont
            sudo install -m 0755 db_config.xml /bin/vermont_config.xml

        To uninstall:

            sudo rm -f /bin/vermont /bin/vermont_config.xml /bin/vermont_config.xml.tmp

The following packages are required for a DataMap server:
+ make
+ mysql-server
+ apache2
+ libapache2-mod-php5
+ php5-mysql

Installing DataMap
------------------
To configure and install DataMap, run the following commands from the DataMap
root directory:

    ./configure.py
    sudo make install

The `configure.py` will prompt you for a series of configuration parameters.
Many of the parameters have defaults that should work fine, but you may change
them if you like. It is important the the IP addresses provided to this script
match the ones that will be used when the system is actually deployed and
running. Any of the values in the configuration script can be changed by
running th script again or editing the `.config` file.

[aircrack-ng]: http://www.aircrack-ng.org/
[vermont]: https://github.com/tumi8/vermont
[cmake-uninstall]: http://www.cmake.org/Wiki/CMake_FAQ#Can_I_do_.22make_uninstall.22_with_CMake.3F
