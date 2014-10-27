#!/usr/bin/python
# -*- coding: utf-8 -*-

import apt.cache

_required_pkgs = {
    "node": [
        "make",
        "cmake",
        "gcc",
        "g++",
        "libboost-dev",
        "libboost-regex-dev",
        "libboost-thread-dev",
        "libboost-filesystem-dev",
        "libboost-test-dev",
        "libxml2-dev",
        "libmysqlclient-dev",
        "libpcap-dev",
        "libsctp-dev",
        "python-mysqldb",
        "screen",
        "subversion",
        "libssl-dev",
        "wireless-tools",
        "iw"
    ],
    "server": [
        "make",
        "mysql-server",
        "apache2",
        "libapache2-mod-php5",
        "php5-mysql"
    ]
}


def usage(program_name):
    print("Usage: {} [node|server]".format(program_name))


def _check_pkgs(required_packages):
    c = apt.cache.Cache()
    f = lambda pkg: not c[pkg].is_installed
    missing_pkgs = filter(f, required_packages)
    return missing_pkgs


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2 or not sys.argv[1] in ['node', 'server']:
        usage(sys.argv[0])
        exit(-1)
    
    missing_pkgs = _check_pkgs(_required_pkgs[sys.argv[1]])        
    if len(missing_pkgs) > 0:
        print('Unable to locate the following packages on your system:')
        print('\n'.join('\t*' + pkg for pkg in missing_pkgs))
        print('\nYou can install them with:')
        print('\tsudo apt-get install' + ' '.join(missing_pkgs))
        exit(-1)
