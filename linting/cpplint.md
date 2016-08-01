`cpplint` is a Google project. As such, it is quite opinionated.

    pip3 install cpplint

cpplint uses the `--filter` argument to control what checks are run.

    cpplint --filter=-legal,-build/namespaces,-whitespace/tab x.cpp
