#!/usr/bin/env bash

list=${HOME}/binlist

if [ -d ${HOME} ]; then
  echo "creating list of all installed packages"
  eix -I -# > ${list}
  echo "created list of all installed packages at ${list}"
  exit
else
  echo "error no user directory exists"
  exit
fi
