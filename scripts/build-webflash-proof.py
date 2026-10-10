"""PlatformIO post extra-script: record the configured uploader without uploading."""
import json
import hashlib
from pathlib import Path

Import("env")


def source_tree():
    root = Path(env.subst("$PROJECT_DIR")).parent
    files = []
    for directory in ("firmware/src", "firmware/include", "web"):
        for file in (root / directory).rglob("*"):
            if file.is_file():
                files.append(file)
    files.append(root / "firmware/platformio.ini")
    entries = [
        {"path": file.relative_to(root).as_posix(),
         "sha256": hashlib.sha256(file.read_bytes()).hexdigest()}
        for file in sorted(files, key=lambda item: item.relative_to(root).as_posix())
    ]
    digest = hashlib.sha256(
        "".join(f"{entry['sha256']}  {entry['path']}\n" for entry in entries).encode()
    ).hexdigest()
    return {"sha256": digest, "files": entries}


def record_upload(source, target, env):
    build = Path(env.subst("$BUILD_DIR"))
    if (build / "firmware.bin").stat().st_mtime < (build / "firmware.elf").stat().st_mtime:
        raise RuntimeError("Stale firmware.bin: run the normal PlatformIO build before webflash-proof")
    firmware = env.File(str(build / "firmware.bin"))
    command = env.subst("$UPLOADCMD", source=[firmware])
    images = [
        {"offset": int(str(offset), 0), "source": env.subst(path)}
        for offset, path in env.get("FLASH_EXTRA_IMAGES", [])
    ]
    images.append({
        "offset": int(env.subst("$ESP32_APP_OFFSET"), 0),
        "source": str(build / "firmware.bin"),
    })
    proof = {
        "board": env.GetProjectOption("board"),
        "platform": env.GetProjectOption("platform"),
        "mcu": env.BoardConfig().get("build.mcu"),
        "command": command,
        "images": images,
        "packages": [
            {"name": package.metadata.name, "version": str(package.metadata.version)}
            for package in env.PioPlatform().get_installed_packages()
        ],
        "libdeps": env.subst("$PROJECT_LIBDEPS_DIR/$PIOENV"),
        "framework": env.PioPlatform().get_package_dir("framework-arduinoespressif32"),
        "toolchain": env.PioPlatform().get_package_dir("toolchain-xtensa-esp32"),
        "sourceTree": source_tree(),
    }
    (build / "webflash-upload.json").write_text(
        json.dumps(proof, indent=2, default=str), encoding="utf-8"
    )


env.AddCustomTarget(
    "webflash-proof",
    "$BUILD_DIR/${PROGNAME}.bin",
    record_upload,
    title="Record upload recipe",
    description="Record actual PlatformIO upload command; never connect to a device",
)
