#!/bin/sh

if test -z $1; then
    echo "provide directory"
    exit 1
fi

DIR="$1"

cd $DIR
for b1 in LT*B1*; do
    basename=`echo $b1 | cut -d'_' -f1`
    echo ${basename}...
    mkdir -p $basename
    cp ${basename}_* $basename/
    cd $basename
    LD_LIBRARY_PATH=/usr/local/MATLAB/MATLAB_Compiler_Runtime/v80/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Compiler_Runtime/v80/bin/glnxa64:/usr/local/MATLAB/MATLAB_Compiler_Runtime/v80/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Compiler_Runtime/v80/sys/java/jre/glnxa64/jre/lib/amd64/native_threads:/usr/local/MATLAB/MATLAB_Compiler_Runtime/v80/sys/java/jre/glnxa64/jre/lib/amd64/server:/usr/local/MATLAB/MATLAB_Compiler_Runtime/v80/sys/java/jre/glnxa64/jre/lib/amd64 XAPPLRESDIR=/usr/local/MATLAB/MATLAB_Compiler_Runtime/v80/X11/app-defaults /opt/src/Fmask_Linux
    cd ..
    cp -r ${basename}/*Fmask* .
    rm -rf $basename
done

exit  0


exit 0