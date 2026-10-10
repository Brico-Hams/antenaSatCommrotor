#!/usr/bin/env bash
set -Eeuo pipefail

: "${ROOTFS_DIR:?pi-gen did not set ROOTFS_DIR}"
: "${SUB_STAGE_DIR:?pi-gen did not set SUB_STAGE_DIR}"

rootfs="$(realpath -- "$ROOTFS_DIR")"
[[ "$rootfs" != / ]] || { echo "refusing to write into host root" >&2; exit 1; }
cp -a -- "$SUB_STAGE_DIR/files/." "$rootfs/"

radio_files="$rootfs/usr/share/bricohams-os/radio-files"
install -d -m 0755 \
    "$radio_files/etc/systemd/system" \
    "$radio_files/usr/local/lib/bricohams_os" \
    "$radio_files/usr/local/libexec" \
    "$radio_files/usr/local/sbin"
for relative in \
    etc/systemd/system/bricohams-radio.service \
    usr/local/lib/bricohams_os/__init__.py \
    usr/local/lib/bricohams_os/config.py \
    usr/local/libexec/bricohams-radio-start \
    usr/local/sbin/bricohams-radio-config; do
    source_path="$rootfs/$relative"
    target_path="$radio_files/$relative"
    [[ -f "$source_path" && ! -L "$source_path" ]] || {
        echo "missing regular radio-profile file: $relative" >&2
        exit 1
    }
    mv -- "$source_path" "$target_path"
done

install -d -m 0755 "$rootfs/etc/bricohams"
boot_config="$rootfs/boot/firmware/config.txt"
[[ -f "$boot_config" && ! -L "$boot_config" ]] || {
    echo "expected Raspberry Pi OS boot config at /boot/firmware/config.txt" >&2
    exit 1
}
cmdline="$rootfs/boot/firmware/cmdline.txt"
[[ -f "$cmdline" && ! -L "$cmdline" ]] || {
    echo "expected Raspberry Pi OS kernel command line at /boot/firmware/cmdline.txt" >&2
    exit 1
}
[[ "$(awk 'END { print NR }' "$cmdline")" == 1 ]] || {
    echo "Raspberry Pi kernel command line must remain a single line" >&2
    exit 1
}
cmdline_tokens="$(tr -s '[:space:]' '\n' < "$cmdline")"
default_serial_console_count="$(printf '%s\n' "$cmdline_tokens" |
    grep -Ec '^console=serial0,115200$' || true)"
serial_console_count="$(printf '%s\n' "$cmdline_tokens" |
    grep -Ec '^console=(serial[0-9]+|ttyAMA[0-9]+|ttyS[0-9]+)(,.*)?$' || true)"
[[ "$default_serial_console_count" == 1 && "$serial_console_count" == 1 ]] || {
    echo "unexpected serial kernel-console configuration; refusing to repurpose GNSS UART0" >&2
    exit 1
}
cmdline_tmp="$(mktemp "$cmdline.XXXXXX")"
if ! awk '{
    separator = ""
    for (i = 1; i <= NF; i++) {
        if ($i != "console=serial0,115200") {
            printf "%s%s", separator, $i
            separator = " "
        }
    }
    print ""
}' "$cmdline" > "$cmdline_tmp"; then
    rm -f -- "$cmdline_tmp"
    echo "could not remove the serial console from the GNSS UART" >&2
    exit 1
fi
chmod --reference="$cmdline" "$cmdline_tmp"
mv -- "$cmdline_tmp" "$cmdline"
if grep -Fq '# BEGIN BRICOHAMS CM5IO REV-A BUS CONFIGURATION' "$boot_config"; then
    echo "boot config already contains the BricoHams bus block" >&2
    exit 1
fi
if awk -F= '
    tolower($1) == "dtoverlay" {
        overlay = tolower($2)
        sub(/,.*/, "", overlay)
        if (overlay != "nospi10" && overlay ~ /(spi[01]|i2c|uart)/) conflict = 1
    }
    END { exit(conflict ? 0 : 1) }
' "$boot_config" || grep -Eiq '^[[:space:]]*(dtparam=(spi[01]?|i2c_arm(_baudrate)?)(=|,)|enable_uart=)' \
        "$boot_config"; then
    echo "unexpected existing SPI/I2C/UART assignment in boot config; refusing stale/conflicting overlay" >&2
    exit 1
fi
cat >> "$boot_config" <<'EOF'

# BEGIN BRICOHAMS CM5IO REV-A BUS CONFIGURATION
# CM5IO GPIO contract: I2C1 on BCM 2/3; SPI1, three CS on BCM 18/17/16;
# GNSS UART0 on BCM 14/15. Deliberately do not enable or remap SPI0.
[all]
dtparam=i2c_arm=on
enable_uart=1
dtoverlay=spi1-3cs,cs0_pin=18,cs1_pin=17,cs2_pin=16
# END BRICOHAMS CM5IO REV-A BUS CONFIGURATION
EOF

for private_path in \
    "$rootfs/etc/bricohams/radio-host.json" \
    "$rootfs/var/lib/bricohams/radio/token" \
    "$rootfs/etc/wpa_supplicant/wpa_supplicant.conf"; do
    [[ ! -e "$private_path" ]] || {
        echo "refusing to export an image containing runtime configuration or a token" >&2
        exit 1
    }
done
if find "$rootfs/home" "$rootfs/root" -type f -name authorized_keys \
        -print -quit 2>/dev/null | grep -q .; then
    echo "refusing to export an image containing an authorized SSH key" >&2
    exit 1
fi
if find "$rootfs/etc/ssh" -maxdepth 1 -type f -name 'ssh_host_*_key*' \
        -print -quit 2>/dev/null | grep -q .; then
    echo "refusing to export an image containing SSH host keys" >&2
    exit 1
fi
if find "$rootfs/etc/NetworkManager/system-connections" -type f -name '*.nmconnection' \
        -exec grep -qE '(^|[.])(psk|password|secret|wep-key[0-9]|private-key-password)=' {} \; \
        -print -quit 2>/dev/null | grep -q .; then
    echo "refusing to export an image containing saved network credentials" >&2
    exit 1
fi
if find "$rootfs/etc/systemd/system" -type l -path '*/multi-user.target.wants/bricohams-radio.service' \
        -print -quit 2>/dev/null | grep -q .; then
    echo "radio service must not be enabled in the base image" >&2
    exit 1
fi
for unit in serial-getty@serial0.service serial-getty@ttyAMA0.service; do
    if [[ -e "$rootfs/etc/systemd/system/getty.target.wants/$unit" \
            || -L "$rootfs/etc/systemd/system/getty.target.wants/$unit" ]]; then
        echo "serial getty $unit conflicts with the GNSS UART" >&2
        exit 1
    fi
done
