#!/bin/bash

RELEASE_URL=https://api.github.com/repos/goretk/libgore/releases/latest
LINUX_URL=`curl -s $RELEASE_URL | grep browser_download_url | cut -d '"' -f 4 | grep linux`
DARWIN_URL=`curl -s $RELEASE_URL | grep browser_download_url | cut -d '"' -f 4 | grep darwin`
WINDOWS_URL=`curl -s $RELEASE_URL | grep browser_download_url | cut -d '"' -f 4 | grep windows`

mkdir -p dltmp

curl -sL $LINUX_URL | bsdtar -xvf - -C dltmp
curl -sL $DARWIN_URL | bsdtar -xvf - -C dltmp
curl -sL $WINDOWS_URL | bsdtar -xvf - -C dltmp

cp -v dltmp/*/{*.dll,*.so,*.dylib} pygore/.
