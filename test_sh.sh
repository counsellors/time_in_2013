#! /usr/bin/bash
hello () 
{ 
    var="hello"; 
    echo "Hello" 
    echo "Hello: param num is $#" 
    echo "Hello: $@" 
    echo "Hello: $*" 
    echo "Hello: $0 $1 $2" 
    echo "Hello: var=$var"; 
} 
var="hello"; 
echo "main: param num is $#" 
echo "main: $@" 
echo "main: $*" 
echo "main: $0 $1 $2" 
echo "main: var=$var"; 
hello h1 h2
