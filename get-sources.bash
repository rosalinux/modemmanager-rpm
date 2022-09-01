#!/bin/bash

SRC_REPO_NAME="ModemManager"
SRC_BRANCH="ayya-mtk-modem"

if [ -n "${1}" ]; then
    SRC_BRANCH="${1}"
fi

rm -rf ${SRC_REPO_NAME}.zip

wget --header "Authorization: token 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" \
     "https://codeload.github.com/rosalinux/${SRC_REPO_NAME}/zip/refs/heads/${SRC_BRANCH}" \
     -O ${SRC_REPO_NAME}.zip

export SRC_BRANCH
