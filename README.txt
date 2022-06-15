# Description of files

f.txt: Original input list of files
f_new.txt: List excluding T0 REPLAYs and Run2022A (since it was reprocessed)
failedFilesMerged.txt: Files we failed getting information from.
producedFiles.txt: List Jsons produced
logs: Condor logfiles for each job (each job represents 1 file)
jsons: All jsons produced

# Work description
This was submitted via CMS Connect. jobXX empty directories need to be created beforehand.

```
for ((i=0;i<6000;++i)); do mkdir job$i; done
```
