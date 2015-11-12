#! /usr/bin/bash

OS=$(uname -s)
DIST_NAME='UNKOWN'
DIST_VERSION='UNKOWN'
DIST_BITS='UNKOWN'
DIST_ARCH='UNKOWN'

function get_cur_os ( )
{
    case "${OS}" in
        'Linux')
            lsb_release_path=$(which lsb_release 2> /dev/null)
            if [ "${lsb_release_path}x" != "x" ]; then
                DIST_NAME=$(${lsb_release_path} -i | cut -d ':' -f2 )
                DIST_VERSION=$(${lsb_release_path} -r | cut -d ':' -f2 | sed 's/\t *//g')
            else
                if [ -r '/etc/debian_version' ]; then
                    if [ -r '/etc/dpkg/origins/ubuntu' ]; then
                        DIST_NAME='ubuntu'
                    else
                        DIST_NAME='debian'
                    fi
                    DIST_VERSION=$(cat /etc/debian_version | sed s/.*\///)
                elif [ -r '/etc/mandrake-release' ]; then
                    DIST_NAME=$(cat /etc/mandrake-release | sed s/.*\(// | sed s/\)//)
                    DIST_VERSION=$(cat /etc/mandrake-release | sed 's/.*release\ //' | sed 's/\ .*//')
                elif [ -r '/etc/redhat-release' ]; then
                    if [ -r '/etc/asplinux-release' ]; then
                        DIST_NAME='asplinux'
                        DIST_VERSION=$(cat /etc/asplinux-release | sed 's/.*release\ //' | sed 's/\ .*//' )
                    elif [ -r '/etc/altlinux-release' ]; then
                        DIST_NAME='altlinux'
                        DIST_VERSION=$(cat /etc/altlinux-release | sed 's/.*Linux\ //' | sed 's/\ .*//')
                    else
                        if [ "$(cat /etc/redhat-release | grep -i 'Red Hat Enterprise')x" != "x" ]; then
                            DIST_NAME='rhel'
                        else
                            DIST_NAME=$(cat /etc/redhat-release | cut -d ' ' -f1)
                        fi
                        DIST_VERSION=$(cat /etc/redhat-release | sed 's/.*release\ //' | sed 's/\ .*//' )
                    fi
                elif [ -r '/etc/arch-release' ]; then
                    DIST_NAME='archlinux'
                    DIST_VERSION=$(cat /etc/arch-release)
                elif [ -r '/etc/SuSe-release' ]; then
                    DIST_NAME='opensuse'
                    DIST_VERSION=$(cat /etc/SuSe-release | grep 'VERSION' | sed 's/.*=\ //')
                elif [ -r '/etc/sles-release' ]; then
                    DIST_NAME='sles'
                    DIST_VERSION=$(cat /etc/SuSe-release | grep 'VERSION' | sed 's/.*=\ //')
                elif [ -r '/etc/slackware-version' ]; then
                    if [ -r '/etc/zenwalk-version' ]; then
                        DIST_NAME='zenwalk'
                        DIST_VERSION=$(cat /etc/zenwalk-version)
                    elif [ -r '/etc/slax-version' ]; then
                        DIST_NAME='slax'
                        DIST_VERSION=$(cat /etc/slax-version | cut -d ' ' -f2)
                    else
                        DIST_NAME=$(cat /etc/slackware-version | cut -d ' ' -f1)
                        DIST_VERSION=$(cat /etc/slackware-version | cut -d ' ' -f2)
                    fi
                elif [ -r /etc/puppyversion ]; then 
                    DIST_NAME='puppy'
                    DIST_VERSION=$(cat /etc/puppyversion)
                fi
            fi
        ;;
        'OpenBSD'|'NetBSD'|'FreeBSD'|'SunOS')
            DIST_NAME=$OS
            if [ "$DIST_NAME" = "SunOS" ]; then
                DIST_NAME='solaris'
            fi
            DIST_VERSION=$(uname -r | sed 's/-.*//')
        ;;
        'Darwin')
            DIST_NAME='Macos'
            DIST_VERSION=$(sw_vers -productVersion)
        ;;
    esac


    case $(uname -m) in
        x86_64)
            DIST_BITS=64
        ;;
        i*86)
            DIST_BITS=32
        ;;
        *)
            DIST_BITS=?
        ;;
    esac

    DIST_NAME=$(echo $DIST_NAME | tr '[:upper:]' '[:lower:]')
    echo "$DIST_NAME-$DIST_VERSION-$DIST_BITS"
}

function add_hosts ()
{
    echo "192.168.1.100  git.mycompany.com" >> /etc/hosts;
}

function install_yum()
{
 yum -y install vim &&
  yum -y install cmake &&
  yum -y install gcc &&
  yum -y install gcc-c++ &&
 yum -y install autoconf &&
 yum -y install gettext-devel &&
 yum -y install snappy.x86_64 &&
 yum -y install libtool &&
 yum -y install automake &&
 yum -y install libpcap.x86_64 &&
 yum -y install perl-devel &&
 yum -y install gcc-c++ &&
 yum -y install java-1.8.0-openjdk.x86_64 &&
 yum -y install mlocate.x86_64 &&
 yum -y install zlib-devel &&
 yum -y install zlib-static &&
 yum -y install curl-devel &&
 yum -y install nc &&
 yum -y install wget &&
 yum -y install ntpdate &&
 # openssl installed before python compiler
 yum -y install openssl &&
 yum -y install openssl-devel &&
 yum -y install git &&
 ntpdate time.nist.gov
}

function install_ubuntu ()
{
    echo "need to do"
}

function install_python27 ()
{
    local PYTHON_TAR="Python-2.7.10.tgz"

    if [ ! -f  "$PYTHON_TAR" ]; then
        wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz ;
    else
        echo "python file exists."
    fi
    PYTHON_VER=`python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'`
    if [[ "$PYTHON_VER" != "2.7.10" ]]; then
        tar xzvf ${PYTHON_TAR} && cd Python-2.7.10 &&
        ./configure --prefix=/usr &&
        make && make install &&
        cd - &&
        # restore yum's python version
        sed -i "1s/python/python2.6/" /usr/bin/yum ;
    fi


}

function install_pip ()
{
    local PIP_FILE="get-pip.py "

    if [ ! -f  "$PIP_FILE" ]; then
        wget https://bootstrap.pypa.io/get-pip.py;
    else
        echo "python file exists."
    fi

    python ${PIP_FILE} &&
    pip install supervisor;

}

function install_git ()
{
    cd git ;
    if [[  ! -d git ]]; then
        git clone https://github.com/git/git.git ;
    fi
    cd git &&
    autoconf &&
    ./configure --with-curl --with-expat --prefix=/usr &&
    make &&
    make install && 
    cd - &&
    cd ..;

}


function main()
{
    mkdir git ;
    get_cur_os
    add_hosts
    if [[ "$DIST_NAME" == 'centos' ]]; then
        echo "is centos"
        install_yum
        install_python27
        install_pip
        install_git
        #statements
    elif [[ "$DIST_NAME" == 'macos'  ]]; then
        echo "is macos"
        #statements'
    else
        echo "is unkown"
    fi
}

main