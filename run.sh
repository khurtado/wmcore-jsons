#!/bin/bash

cat /etc/redhat-release

# CMSSW software
export initial=$PWD
# Get help scripts
wget --no-check-certificate http://stash.osgconnect.net/+khurtado/wmcore/aod_report.py > /dev/null 2>&1
wget --no-check-certificate http://stash.osgconnect.net/+khurtado/wmcore/dqmio_report.py > /dev/null  2>&1
wget --no-check-certificate http://stash.osgconnect.net/+khurtado/wmcore/nano_lumis.py > /dev/null 2>&1

source /cvmfs/cms.cern.ch/cmsset_default.sh
scramv1 project CMSSW CMSSW_12_3_5
cd CMSSW_12_3_5
eval `scramv1 runtime -sh`
cd  $initial

filename="$1"
if grep -q "NANOAOD" <<< "$filename";  then
    cmd="nano_lumis.py"
elif grep -q "DQMIO" <<< "$filename";  then 
    cmd="dqmio_report.py"
else
    cmd="aod_report.py"
fi


basefile="$(basename $filename)"
echo python3 $initial/$cmd "root://cmsxrootd.fnal.gov/$filename" --output=${basefile%.*}.json
python3 $initial/$cmd "root://cmsxrootd.fnal.gov/$filename" --output=${basefile%.*}.json
res=$?
echo $res
if [ $res != 0 ]; then
    echo  $filename  >> failedFiles.txt
fi
ls -l
