#!/usr/bin/env bash

list=${HOME}/binlist
fails=${HOME}/failinst

for PACKAGE in $(cat ${LIST});
do
  printf "Installing binary package for ${PACKAGE}... "
  emerge --quiet-build -uN --ignore-default-opts -1 --quiet=y --usepkgonly ${PACKAGE};
  if [[ $? -eq 0 ]];
  then
    echo "installed";
  else
    echo "failed";
    echo ${?} >> ${fails};
  fi
done
