#!/bin/bash

echo cpplint
cpplint --filter=-legal,-build/namespaces,-whitespace/tab $*

echo
echo cppcheck
cppcheck $*  --enable=all --inconclusive --platform=native --quiet --suppress=missingIncludeSystem 

STD='-std=c++11'
CLANG_ENABLED='-Wall -Wextra -pedantic -Weverything'
CLANG_DISABLED='-Wno-old-style-cast -Wno-reorder'

echo
echo clang
clang++ $CLANG_ENABLED $CLANG_DISABLED $STD -fsyntax-only -fcaret-diagnostics $*

echo
echo gcc
g++ -Wall -Wextra -Wpedantic -Wno-old-style-cast -Wno-reorder -fsyntax-only -fdiagnostics-show-caret $*

