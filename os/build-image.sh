#!/usr/bin/env bash
set -Eeuo pipefail

fail() {
    printf 'OS image build: %s\n' "$*" >&2
    exit 1
}

[[ "$(uname -s)" == Linux ]] || fail "run this recipe on Linux (or inside a Linux VM), not Windows."
command -v git >/dev/null || fail "git is required."
command -v docker >/dev/null || fail "Docker Engine is required."
command -v rsync >/dev/null || fail "rsync is required."
command -v findmnt >/dev/null || fail "findmnt is required."
command -v sha256sum >/dev/null || fail "sha256sum is required."

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
PI_GEN_COMMIT="$(tr -d '\r\n' < "$SCRIPT_DIR/pi-gen.commit")"
[[ "$PI_GEN_COMMIT" =~ ^[0-9a-f]{40}$ ]] || fail "os/pi-gen.commit must contain one full Git commit ID."

: "${BUILD_ROOT:?Set BUILD_ROOT to a new path on a native Linux filesystem with at least 60 GiB free.}"
case "$BUILD_ROOT" in
    *[[:space:]]*) fail "BUILD_ROOT must not contain whitespace; pi-gen rejects paths with spaces." ;;
esac
mkdir -p -- "$BUILD_ROOT"
BUILD_ROOT="$(realpath -- "$BUILD_ROOT")"
case "$BUILD_ROOT" in
    *[[:space:]]*) fail "the resolved BUILD_ROOT must not contain whitespace." ;;
esac
case "$(findmnt -n -o FSTYPE -T "$BUILD_ROOT")" in
    drvfs|9p|exfat|fuseblk|ntfs|vfat)
        fail "BUILD_ROOT must be on a native Linux filesystem, not a Windows/shared filesystem." ;;
esac
available_kib="$(df -Pk "$BUILD_ROOT" | awk 'NR == 2 { print $4 }')"
[[ "$available_kib" =~ ^[0-9]+$ ]] || fail "could not determine free space for BUILD_ROOT."
(( available_kib >= 60 * 1024 * 1024 )) || fail "need at least 60 GiB free on the BUILD_ROOT filesystem."

PI_GEN_DIR="$BUILD_ROOT/pi-gen"
OUTPUT_DIR="${OUTPUT_DIR:-$BUILD_ROOT/artifacts}"
[[ ! -e "$PI_GEN_DIR" ]] || fail "$PI_GEN_DIR already exists; choose a new empty BUILD_ROOT."
mkdir -p -- "$OUTPUT_DIR"
OUTPUT_DIR="$(realpath -- "$OUTPUT_DIR")"
case "$OUTPUT_DIR/" in
    "$PI_GEN_DIR/"|"$PI_GEN_DIR/"*) fail "OUTPUT_DIR must be outside the pi-gen checkout." ;;
esac

git clone --filter=blob:none --no-checkout --single-branch --branch arm64 \
    https://github.com/RPi-Distro/pi-gen.git "$PI_GEN_DIR"
git -C "$PI_GEN_DIR" fetch --depth=1 origin "$PI_GEN_COMMIT"
git -C "$PI_GEN_DIR" checkout --detach "$PI_GEN_COMMIT"
[[ "$(git -C "$PI_GEN_DIR" rev-parse HEAD)" == "$PI_GEN_COMMIT" ]] ||
    fail "the pi-gen checkout does not match the pinned commit."

stage_source="$SCRIPT_DIR/pi-gen-stage/stage2/99-bricohams"
stage_target="$PI_GEN_DIR/stage2/99-bricohams"
[[ -d "$stage_source" ]] || fail "missing BricoHams pi-gen stage."
cp -a -- "$stage_source" "$stage_target"
chmod +x "$stage_target/00-run.sh"

files="$stage_target/files"
install -d -- "$files/opt/bricohams/src/radio" \
    "$files/opt/bricohams/src/rotor" \
    "$files/usr/share/bricohams-os" \
    "$files/opt/bricohams" \
    "$files/usr/share/doc/bricohams-os"
rsync -a \
    --exclude='.venv/' --exclude='build/' --exclude='dist/' \
    --exclude='*.egg-info/' --exclude='__pycache__/' --exclude='*.pyc' \
    --exclude='.pytest_cache/' --exclude='.mypy_cache/' --exclude='.ruff_cache/' \
    "$REPO_ROOT/radio/" "$files/opt/bricohams/src/radio/"
rsync -a \
    --exclude='.venv/' --exclude='build/' --exclude='dist/' \
    --exclude='*.egg-info/' --exclude='__pycache__/' --exclude='*.pyc' \
    --exclude='.pytest_cache/' --exclude='.mypy_cache/' --exclude='.ruff_cache/' \
    "$REPO_ROOT/rotor/" "$files/opt/bricohams/src/rotor/"
install -m 0644 "$SCRIPT_DIR/runtime-requirements.txt" \
    "$files/opt/bricohams/runtime-requirements.txt"
install -m 0644 "$SCRIPT_DIR/build-requirements.txt" \
    "$files/opt/bricohams/build-requirements.txt"
install -m 0644 "$SCRIPT_DIR/licenses/pi-gen-BSD-3-Clause.txt" \
    "$files/usr/share/doc/bricohams-os/pi-gen-BSD-3-Clause.txt"
for document in AUTHORS.md ACKNOWLEDGEMENTS.md DISCLAIMER.md NOTICE.md; do
    install -m 0644 "$REPO_ROOT/$document" \
        "$files/usr/share/doc/bricohams-os/$document"
done
rsync -a "$REPO_ROOT/docs/" "$files/usr/share/doc/bricohams-os/docs/"
rsync -a "$SCRIPT_DIR/install/" "$files/usr/share/doc/bricohams-os/os/install/"
install -m 0644 "$SCRIPT_DIR/pi-gen.commit" \
    "$files/usr/share/doc/bricohams-os/pi-gen.commit"
install -m 0644 "$SCRIPT_DIR/runtime-requirements.txt" \
    "$files/usr/share/doc/bricohams-os/runtime-requirements.txt"
install -m 0644 "$SCRIPT_DIR/build-requirements.txt" \
    "$files/usr/share/doc/bricohams-os/build-requirements.txt"
rsync -a "$REPO_ROOT/LICENSES/" "$files/usr/share/doc/bricohams-os/LICENSES/"
install -m 0644 "$REPO_ROOT/docs/SOURCES.md" \
    "$files/usr/share/doc/bricohams-os/SOURCES.md"
install -m 0644 "$REPO_ROOT/hardware/cm5/interface.json" \
    "$files/usr/share/bricohams-os/cm5-interface.json"
install -m 0644 "$SCRIPT_DIR/pi-gen.config" "$PI_GEN_DIR/config"

(
    cd -- "$PI_GEN_DIR"
    ./build-docker.sh
)

shopt -s nullglob
images=("$PI_GEN_DIR"/deploy/*-lite.zip)
(( ${#images[@]} == 1 )) ||
    fail "expected exactly one Raspberry Pi OS Lite archive; inspect $PI_GEN_DIR/deploy and its build logs."
image="${images[0]}"
[[ -s "$image" && ! -L "$image" ]] || fail "the generated image archive is empty or is not a regular file."
if find "$files" -type f \( -name 'authorized_keys' -o -name 'ssh_host_*' \
        -o -name 'wpa_supplicant.conf' -o -name 'radio-host.json' \) -print -quit | grep -q .; then
    fail "the staged files contain a credential/key-bearing path; refusing to export the image."
fi

destination="$OUTPUT_DIR/$(basename -- "$image")"
checksum="$destination.sha256"
[[ ! -e "$destination" && ! -e "$checksum" ]] ||
    fail "refusing to overwrite an existing image or checksum in $OUTPUT_DIR."
install -m 0644 "$image" "$destination"
(cd -- "$OUTPUT_DIR" && sha256sum "$(basename -- "$destination")" > "$(basename -- "$checksum")")
printf 'Image: %s\nSHA-256: ' "$destination"
sha256sum "$destination"
printf 'No SD card was written. Review the commissioning gates before first use.\n'
