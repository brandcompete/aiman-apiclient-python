#!/bin/bash

if [ -d "dist" ];
then
  echo "[BCCICD] Cleaning previous builds"
  rm dist/*
else
	echo "First build, nothing to clean"
fi

echo "[BCCICD] Building"
python3 -m build

echo "[CICD] Publishing"
python3 -m twine upload dist/*

#echo "[CICD] Publishing to TEST PyPI"
#python3 -m twine upload --repository testpypi dist/* --verbose

echo "[BCCICD] Done ... Exiting"
