#!/usr/bin/env bash

RELEASE_URL=https://api.github.com/repos/goretk/libgore/releases/latest

mkdir -p dltmp

for i in $(curl -s $RELEASE_URL | grep browser_download_url); do
   curl -sL $i | bsdtar -xvf - -C dltmp
done

cp -v dltmp/*/{*.dll,*.so,*.dylib} pygore/.
