#!/usr/bin/env bash

# relies on binlist existing prior to running
list=${HOME}/binlist
fails=${HOME}/failist

for PACKAGE in $(cat ${list});
do
  printf "Building binary package for ${PACKAGE}... "
  emerge --quiet-build -uN --ignore-default-opts -1 --quiet=y --buildpkgonly ${PACKAGE};
  if [[ $? -eq 0 ]];
  then
    echo "built";
  else
    echo "failed";
    echo ${?} >> ${fails};
  fi
done
