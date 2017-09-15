#!/usr/bin/env bash

SETDIR=/etc/portage/sets
SETPY=${SETDIR}/pyup
SETPL=${SETDIR}/plup
SETRUB=${SETDIR}/rubup
SETSYS=${SETDIR}/sysup
SETBASE=${SETDIR}/baseup
SETAPP=${SETDIR}/appup
SETDEV=${SETDIR}/devup
SETGNO=${SETDIR}/gnoup
SETMED=${SETDIR}/medup
SETNET=${SETDIR}/netup
SETXII=${SETDIR}/xup

TMP=$(tempfile)

if [ -d "${SETDIR}" ]; then
    eix -# -u > "${TMP}"
    cat "${TMP}" | egrep -i "(portage|gcc|glibc|xfce|dev-lang|sys-kernel)" > ${SETBASE}
    cat "${TMP}" | egrep -i "(sec-|sys-apps|sys-auth|sys-block|sys-boot|sys-cluster|sys-devel|sys-fabric|sys-fs|sys-freebsd|sys-libs|sys-power|sys-process)" > ${SETSYS}
    cat "${TMP}" | egrep -i "dev-python" > ${SETPY}
    cat "${TMP}" | egrep -i "dev-perl" > ${SETPL}
    cat "${TMP}" | egrep -i "dev-ruby" > ${SETRUB}
    cat "${TMP}" | egrep -i "app-" > ${SETAPP}
    cat "${TMP}" | egrep -i "gnome-" > ${SETGNO}
    cat "${TMP}" | egrep -i "media-" > ${SETMED}
    cat "${TMP}" | egrep -i "(net-|www-|^virtual)" > ${SETNET}
    cat "${TMP}" | egrep -i "x11" > ${SETXII}
    cat "${TMP}" | egrep -i "^(dev-ada|dev-cpp|dev-db|dev-dotnet|dev-embedded|dev-erlang|dev-go|dev-haskell|dev-java|dev-libs|dev-lisp|dev-lua|dev-ml|dev-php|dev-qt|dev-scheme|dev-tcltk|dev-tex|dev-texlive|dev-util|dev-vcs)" > ${SETDEV}
    rm "${TMP}"
fi
