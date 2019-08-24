#!/bin/bash -x

RELEASE_URL=https://api.github.com/repos/goretk/libgore/releases/latest

mkdir -p dltmp

for i in linux darwin windows; do
   curl -s $RELEASE_URL | grep browser_download_url | cut -d '"' -f 4 | grep $i | \
      xargs -n 1 -I url curl -sL url | bsdtar -xvf - -C dltmp
done

cp -v dltmp/*/{*.dll,*.so,*.dylib} pygore/.
