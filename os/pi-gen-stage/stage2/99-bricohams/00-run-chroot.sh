#!/bin/sh
set -eu

install -d -o root -g root -m 0755 /opt/bricohams
chown -R root:root /opt/bricohams/src

chmod 0755 /usr/local/libexec/bricohams-gpio-safe-state \
    /usr/local/sbin/bricohams-os-profile-setup
chown root:root /usr/local/libexec/bricohams-gpio-safe-state \
    /usr/local/sbin/bricohams-os-profile-setup
chmod 0644 /etc/systemd/system/bricohams-profile-setup.service
chmod 0644 /etc/systemd/system/bricohams-gpio-safe-state.service
install -d -o root -g root -m 0755 /etc/bricohams
install -d -o root -g root -m 0755 /etc/systemd/system/multi-user.target.wants
ln -s ../bricohams-profile-setup.service \
    /etc/systemd/system/multi-user.target.wants/bricohams-profile-setup.service
ln -s ../bricohams-gpio-safe-state.service \
    /etc/systemd/system/multi-user.target.wants/bricohams-gpio-safe-state.service

# Banners (/etc/motd, /etc/issue, /etc/issue.net) are static files copied by 00-run.sh from files/etc.
