const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const root = path.resolve(__dirname, "..");
const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), "utf8");

test("pi-gen recipe is pinned to the official 64-bit Trixie Lite build", () => {
  const commit = read("os/pi-gen.commit").trim();
  const config = read("os/pi-gen.config");
  const build = read("os/build-image.sh");
  assert.equal(commit, "d346cd53562b3c6b4f94c9155175f814258c456d");
  assert.match(build, /https:\/\/github\.com\/RPi-Distro\/pi-gen\.git/);
  assert.match(build, /git -C "\$PI_GEN_DIR" checkout --detach "\$PI_GEN_COMMIT"/);
  assert.match(config, /^RELEASE='trixie'$/m);
  assert.match(config, /^STAGE_LIST='stage0 stage1 stage2'$/m);
  assert.match(config, /^ENABLE_SSH=0$/m);
  assert.doesNotMatch(config, /FIRST_USER_PASS|WPA_PASSWORD|PUBKEY_SSH_FIRST_USER/);
});

test("boot setup maps only the frozen auxiliary-board buses", () => {
  const stage = read("os/pi-gen-stage/stage2/99-bricohams/00-run.sh");
  const build = read("os/build-image.sh");
  const pcb = read("docs/CM5-PCB.md");
  const contract = JSON.parse(read("hardware/cm5/interface.json"));
  assert.match(stage, /dtparam=i2c_arm=on/);
  assert.match(stage, /enable_uart=1/);
  assert.match(stage, /dtoverlay=spi1-3cs,cs0_pin=18,cs1_pin=17,cs2_pin=16/);
  assert.match(stage, /Deliberately do not enable or remap SPI0/);
  assert.match(stage, /console=serial0,115200/);
  assert.match(stage, /repurpose GNSS UART0/);
  assert.match(stage, /overlay != "nospi10"/);
  assert.match(stage, /spi\[01\]\?/);
  assert.match(stage, /i2c_arm\(_baudrate\)\?/);
  assert.match(stage, /serial-getty@ttyAMA0\.service/);
  assert.match(pcb, /\| 14 \| 8 \| GNSS UART TX/);
  assert.match(pcb, /\| 15 \| 10 \| GNSS UART RX/);
  assert.match(pcb, /SPI1 CS2, POL driver/);
  assert.match(pcb, /ID_SD\/ID_SC/);
  assert.equal(contract.board.revision, "A");
  assert.equal(contract.board.gpioContractStatus, "frozen for software integration");
  assert.equal(contract.board.hardwareStatus, "routed digital review; not fabricated; power front-end DNP; not commissioned; DO NOT ORDER");
  assert.equal(contract.peripherals.spi.bus, "SPI1");
  assert.equal(contract.peripherals.i2c.bus, "I2C1");
  assert.equal(contract.softwareContract.bootSafety.gnssUart, "UART0");
  assert.equal(contract.softwareContract.bootSafety.spiBus, "SPI1");
  assert.equal(contract.softwareContract.bootSafety.i2cBus, "I2C1");
  assert.equal(contract.softwareContract.bootSafety.spi0SubstituteAllowed, false);
  assert.equal(contract.softwareContract.bootSafety.staleDeviceTreeOverlayMayReassignFrozenGpio, false);
  assert.equal(contract.softwareContract.bootSafety.verifyTargetImageOverlaysAndDeviceNodes, true);
  assert.equal(contract.peripherals.gnss.txBcm, 14);
  assert.equal(contract.peripherals.gnss.rxBcm, 15);
  assert.equal(contract.peripherals.gnss.ppsBcm, 27);
  const gpio = Object.fromEntries(contract.gpio.map(({ signal, bcm }) => [signal, bcm]));
  const expectedGpio = {
    I2C1_SDA: 2, I2C1_SCL: 3,
    AZ_LIMIT_MIN_N: 4, AZ_LIMIT_MAX_N: 5,
    EL_LIMIT_MIN_N: 6, EL_LIMIT_MAX_N: 7,
    POL_LIMIT_MIN_N: 8, POL_LIMIT_MAX_N: 9,
    ESTOP_AUX_N: 10, WATCHDOG_HEARTBEAT: 11, MOTOR_ARM_REQUEST: 12,
    TCA9548A_RESET_N: 13, GNSS_UART_TX: 14, GNSS_UART_RX: 15,
    SPI1_CS2_POL: 16, SPI1_CS1_EL: 17, SPI1_CS0_AZ: 18,
    SPI1_MISO: 19, SPI1_MOSI: 20, SPI1_SCLK: 21,
    PTT_VHF_REQUEST: 22, PTT_UHF_REQUEST: 23,
    FAULT_AZ_N: 24, FAULT_EL_N: 25, FAULT_POL_N: 26, GNSS_PPS: 27,
  };
  assert.deepEqual(
    Object.fromEntries(Object.keys(expectedGpio).map((signal) => [signal, gpio[signal]])),
    expectedGpio,
  );
  assert.equal(contract.peripherals.i2c.gpioExpander.pins.GPA0, "AZ_ENABLE_REQUEST");
  assert.equal(contract.peripherals.i2c.gpioExpander.pins.GPA1, "EL_ENABLE_REQUEST");
  assert.equal(contract.peripherals.i2c.gpioExpander.pins.GPA2, "POL_ENABLE_REQUEST");
  assert.equal(contract.peripherals.i2c.gpioExpander.pins.GPA3, "MOTOR_PERMIT_FEEDBACK_N");
  assert.equal(contract.peripherals.i2c.gpioExpander.pins.GPA4, "PTT_VHF_FEEDBACK_N");
  assert.equal(contract.peripherals.i2c.gpioExpander.pins.GPA5, "PTT_UHF_FEEDBACK_N");
  assert.equal(contract.peripherals.i2c.gpioExpander.pins.GPA6, "PA_VHF_FAULT_N");
  assert.equal(contract.peripherals.i2c.gpioExpander.pins.GPA7, "PA_UHF_FAULT_N");
  assert.equal(contract.peripherals.i2c.gpioExpander.pins["GPB0-GPB7"], "reserved; no connect");
  assert.equal(
    contract.peripherals.i2c.gpioExpander.resetBehavior,
    "all GPIO inputs; external pulls keep enables deasserted",
  );
  assert.equal(contract.peripherals.i2c.gpioExpander.address, "0x20");
  assert.equal(contract.peripherals.i2c.mux.address, "0x70");
  assert.deepEqual(contract.peripherals.i2c.channels, {
    "0": "ENCODER_AZ_AS5600",
    "1": "ENCODER_EL_AS5600",
    "2": "ENCODER_POL_AS5600",
    "3": "COMPASS_LIS3MDL",
    "4": "IMU_LSM6DSOX",
  });
  assert.equal(contract.board.externalBattery.nominalInterfaceV, 12);
  assert.equal(contract.board.externalBattery.massIncludedInFiveKgObjective, false);
  assert.equal(contract.board.conversion.raw12VBatteryMayConnectToCm5ioUsbCPower, false);
  assert.equal(contract.board.conversion.raw12VBatteryMayConnectToCm5io40Pin5V, false);
  assert.equal(
    contract.board.usbPowerDataTopology.cm5ioUsbCPowerInputSeparateFromUsbDataHost,
    true,
  );
  assert.equal(contract.board.usbPowerDataTopology.requiresNegotiatedUsbCPdContract, true);
  assert.equal(
    contract.board.usbPowerDataTopology.powerTargetStatus,
    "conditional design target; not a CM5IO rating or proof of available power",
  );
  assert.equal(contract.board.externalBattery.candidate.manufacturer, "ECO-WORTHY");
  assert.equal(contract.board.externalBattery.candidate.variant, "40308275183822");
  assert.equal(contract.board.externalBattery.candidate.nominalCapacityAh, 30);
  assert.equal(contract.board.externalBattery.candidate.nominalEnergyWhIfCapacityVerified, 360);
  assert.match(contract.board.externalBattery.candidate.status, /candidate only/);
  assert.equal(contract.board.externalBattery.provisionalFullChargeV, 14.6);
  assert.equal(contract.board.externalBattery.minimumCapacityEstablishesTwoHourAutonomy, false);
  assert.equal(contract.board.externalBattery.autonomyObjectiveHours, 2);
  assert.equal(contract.board.conversion.preliminaryBatteryInputComponentRatingV, 30);
  assert.match(contract.board.conversion.preliminaryInputRatingStatus, /screening only/);
  assert.equal(contract.board.conversion.auxiliaryLogicMustBeIsolatedFromBatteryInput, true);
  assert.equal(contract.board.externalBattery.motorAndLogicRailsFrozen, false);
  assert.equal(contract.board.conversion.allProtectionAndRegulatorRatingsFrozen, false);
  assert.match(build, /hardware\/cm5\/interface\.json/);
  const docs = read("docs/BRICOHAMS-OS.md");
  assert.match(docs, /ECO-WORTHY 12 V \/ 30 Ah LiFePO4/);
  assert.match(docs, /40308275183822/);
  assert.match(docs, /candidate only, not an approved or/);
  assert.match(docs, /two-hour objective requires measured/);
  assert.match(docs, /isolated 5 V auxiliary-logic regulator/);
});

test("revision-A safe-state service uses the contract and holds arm/PTT/watchdog inactive", () => {
  const contract = JSON.parse(read("hardware/cm5/interface.json"));
  const helper = read("os/pi-gen-stage/stage2/99-bricohams/files/usr/local/libexec/bricohams-gpio-safe-state");
  const unit = read("os/pi-gen-stage/stage2/99-bricohams/files/etc/systemd/system/bricohams-gpio-safe-state.service");
  const gpio = Object.fromEntries(contract.gpio.map(({ signal, bcm, safeLevel, direction }) =>
    [signal, { bcm, safeLevel, direction }]));
  const expected = {
    WATCHDOG_HEARTBEAT: [11, "LOW"],
    MOTOR_ARM_REQUEST: [12, "LOW"],
    TCA9548A_RESET_N: [13, "HIGH"],
    PTT_VHF_REQUEST: [22, "LOW"],
    PTT_UHF_REQUEST: [23, "LOW"],
  };
  for (const [signal, [bcm, safeLevel]] of Object.entries(expected)) {
    assert.deepEqual(gpio[signal], { bcm, safeLevel, direction: "output" });
    assert.match(helper, new RegExp(
      `"${signal}"\\s*:\\s*\\(${bcm},\\s*"${safeLevel}"\\)`,
    ));
  }
  assert.match(helper, /\/usr\/share\/bricohams-os\/cm5-interface\.json/);
  assert.match(helper, /contract\["softwareContract"\]/);
  assert.match(helper, /\/etc\/bricohams\/gpiochip/);
  assert.match(helper, /gpiod\.request_lines/);
  assert.match(helper, /while not stopping/);
  assert.match(helper, /time\.sleep\(0\.1\)/);
  assert.match(helper, /lines\.release\(\)/);
  assert.doesNotMatch(helper, /gpiochip0/);
  assert.match(unit, /Restart=on-failure/);
  assert.match(unit, /Type=simple/);
  assert.match(unit, /ConditionPathExists=\/etc\/bricohams\/gpiochip/);
  assert.equal(contract.softwareContract.unverifiedHardwareMustRemainDisabled, true);
  assert.equal(contract.softwareContract.bootSafety.automaticMotorArmOnStartupAllowed, false);
  assert.equal(contract.softwareContract.bootSafety.automaticPttOnStartupAllowed, false);
  assert.deepEqual(
    contract.softwareContract.bootSafety.repeatFailOffInitializationAfter,
    ["reboot", "service restart", "GPIO provider recovery", "MCP23017 reset or power loss"],
  );
  assert.equal(contract.softwareContract.bootSafety.motorArmOnColdBoot, "OFF");
  assert.equal(contract.softwareContract.bootSafety.perAxisEnablesOnColdBoot, "OFF");
  assert.equal(contract.softwareContract.bootSafety.pttRequestsOnColdBoot, "OFF");
  assert.equal(contract.softwareContract.bootSafety.spi0SubstituteAllowed, false);
  assert.equal(contract.softwareContract.bootSafety.staleDeviceTreeOverlayMayReassignFrozenGpio, false);
  assert.equal(contract.softwareContract.bootSafety.verifyTargetImageOverlaysAndDeviceNodes, true);
  assert.equal(contract.softwareContract.bootSafety.softwareDoesNotReplaceExternalHardwareFailOff, true);
  assert.equal(gpio.MOTOR_ARM_REQUEST.bcm, 12);
  assert.equal(gpio.MOTOR_ARM_REQUEST.safeLevel, "LOW");
  assert.equal(gpio.WATCHDOG_HEARTBEAT.bcm, 11);
  assert.equal(gpio.WATCHDOG_HEARTBEAT.safeLevel, "LOW");
});

test("image installs the actual host packages without auto-starting motion or TX", () => {
  const packages = read("os/pi-gen-stage/stage2/99-bricohams/00-packages-nr");
  const stage = read("os/pi-gen-stage/stage2/99-bricohams/00-run.sh");
  const install = read("os/pi-gen-stage/stage2/99-bricohams/00-run-chroot.sh");
  const profiles = read("os/pi-gen-stage/stage2/99-bricohams/files/usr/local/sbin/bricohams-os-profile-setup");
  const unit = read("os/pi-gen-stage/stage2/99-bricohams/files/etc/systemd/system/bricohams-radio.service");
  const wrapper = read("os/pi-gen-stage/stage2/99-bricohams/files/usr/local/libexec/bricohams-radio-start");
  const radio = read("radio/pyproject.toml");
  const rotor = read("rotor/pyproject.toml");
  const rotorPackages = profiles.match(/ROTOR_PACKAGES = \(([\s\S]*?)\n\)/)?.[1];
  const radioPackages = profiles.match(/RADIO_PACKAGES = \(([\s\S]*?)\n\)/)?.[1];

  assert.ok(rotorPackages, "rotor profile dependency set exists");
  assert.ok(radioPackages, "radio profile dependency set exists");
  assert.match(packages, /^python3$/m);
  assert.doesNotMatch(packages, /^python3-venv$/m);
  assert.doesNotMatch(packages, /SoapySDR|soapysdr|LimeSuite|limesuite|bluez/i);
  assert.doesNotMatch(rotorPackages, /SoapySDR|soapysdr|LimeSuite|limesuite|bluez/i);
  assert.match(radioPackages, /python3-soapysdr/);
  assert.match(profiles, /"rotor-only": \(ROTOR_PACKAGES, \("rotor",\)\)/);
  assert.match(profiles, /"radio-only": \(RADIO_PACKAGES, \("radio",\)\)/);
  assert.match(profiles, /"integrated":/);
  assert.match(profiles, /"soapysdr-module-lms7"/);
  assert.match(profiles, /"python3-soapysdr"/);
  assert.match(profiles, /"bluez"/);
  assert.match(profiles, /"python3-smbus2"/);
  assert.match(profiles, /--no-install-recommends/);
  assert.match(profiles, /portable-sat-radio.*--help/);
  assert.match(profiles, /portable-sat-rotor.*--help/);
  assert.match(profiles, /profile is already recorded; refusing to replace/);
  assert.match(radio, /portable-sat-radio = "radio\.main:main"/);
  assert.match(rotor, /name = "portable-sat-rotor"/);
  assert.match(install, /bricohams-profile-setup\.service/);
  assert.doesNotMatch(install, /bricohams-radio\.service/);
  assert.match(stage, /radio_files="\$rootfs\/usr\/share\/bricohams-os\/radio-files"/);
  assert.match(stage, /mv -- "\$source_path" "\$target_path"/);
  assert.match(profiles, /if "radio" in modules:[\s\S]*?radio_files = \(/);
  assert.match(profiles, /unselected = \{"radio", "rotor"\} - set\(modules\)/);
  assert.match(profiles, /shutil\.rmtree\(source_path\)/);
  assert.match(profiles, /if "radio" not in modules:[\s\S]*?shutil\.rmtree\(radio_staging\)/);
  assert.match(install, /multi-user\.target\.wants\/bricohams-profile-setup\.service/);
  assert.match(unit, /ConditionPathExists=\/etc\/bricohams\/radio-host\.json/);
  assert.match(unit, /Documentation=file:\/usr\/share\/doc\/bricohams-os\/docs\/BRICOHAMS-OS\.md/);
  assert.match(unit, /User=bricohams-radio/);
  assert.doesNotMatch(install, /bricohams-radio\.service[\s\S]*enable/);
  assert.doesNotMatch(wrapper, /--rotor|--gpio-chip|--arm-line|--ptt-line|--gate-line/);
  assert.match(wrapper, /--operation-profile", "STANDALONE_MANUAL"/);
  assert.match(wrapper, /profile != "radio-only\\n"/);
  assert.match(wrapper, /if profile != "radio-only\\n":\s+raise RuntimeError\(/);
  assert.match(wrapper, /"radio service supports radio-only manual mode only; integrated tracking "\s+"adapter is pending and cannot fall back to manual"/);
});

test("first-boot profile selection is local, one-time, and never starts a module service", () => {
  const selectorUnit = read("os/pi-gen-stage/stage2/99-bricohams/files/etc/systemd/system/bricohams-profile-setup.service");
  const selector = read("os/pi-gen-stage/stage2/99-bricohams/files/usr/local/sbin/bricohams-os-profile-setup");
  assert.match(selectorUnit, /After=cloud-init\.target/);
  assert.match(selectorUnit, /Before=getty@tty1\.service/);
  assert.match(selectorUnit, /StandardInput=tty/);
  assert.match(selectorUnit, /ConditionPathExists=!\/etc\/bricohams\/profile/);
  assert.match(selector, /"rotor-only"/);
  assert.match(selector, /"radio-only"/);
  assert.match(selector, /"integrated"/);
  assert.match(selector, /sys\.stdin\.isatty\(\)/);
  assert.match(selector, /gpiodetect/);
  assert.match(selector, /gpioinfo/);
  assert.match(selector, /systemctl", "start", "bricohams-gpio-safe-state\.service"/);
  assert.match(selector, /PENDING_PROFILE_PATH/);
  assert.match(selector, /no profile was recorded/);
  assert.doesNotMatch(selector, /systemctl", "(?:enable|start)", "bricohams-radio\.service"/);
  assert.doesNotMatch(selector, /systemctl", "(?:enable|start)", "bricohams-rotor\.service"/);
  assert.match(selector, /Rotor BSP\/production adapter remains pending/);
  assert.match(selector, /Integrated operation remains pending/);
});

test("installation guides keep antenna-only software-free and full station pending", () => {
  const rotor = read("os/install/rotor-only.md");
  const radio = read("os/install/radio-only.md");
  const antenna = read("os/install/antenna-only.md");
  const station = read("os/install/full-station.md");
  assert.match(rotor, /does \*\*not\*\* install BlueZ, SoapySDR, LimeSuite/);
  assert.match(rotor, /production CM5 BSP\/`open_adapter` provider/);
  assert.match(radio, /STANDALONE_MANUAL/);
  assert.match(radio, /TX remains inhibited/);
  assert.match(antenna, /does not need this Raspberry Pi OS image/);
  assert.match(station, /dependency-install profile only/);
  assert.match(
    station.replace(/\s+/g, " "),
    /integrated radio wrapper rejects the profile rather than silently switching to manual operation/,
  );
});

test("host config is a strict non-secret identity record with a private runtime token", () => {
  const config = read("os/pi-gen-stage/stage2/99-bricohams/files/usr/local/lib/bricohams_os/config.py");
  const writer = read("os/pi-gen-stage/stage2/99-bricohams/files/usr/local/sbin/bricohams-radio-config");
  const requirements = read("os/runtime-requirements.txt");
  assert.match(config, /O_NOFOLLOW/);
  assert.match(config, /info\.st_uid != 0/);
  assert.match(config, /bricohams-radio mode 0640/);
  assert.match(config, /duplicate JSON key/);
  assert.match(config, /radio\/token/);
  assert.match(writer, /service remains disabled/);
  assert.match(requirements, /^sgp4==2\.25$/m);
  assert.match(requirements, /^smbus2==0\.5\.0$/m);
  assert.match(requirements, /^pyserial==3\.5$/m);
  assert.match(requirements, /^spidev==3\.8$/m);
  assert.match(read("os/build-requirements.txt"), /^setuptools==75\.8\.2$/m);
  assert.doesNotMatch(config, /password|wpa|private.?key/i);
});

test("Python config schema rejects ambiguous, unsafe, or non-production identities on Linux", {
  skip: process.platform !== "linux",
}, () => {
  const pythonPath = path.join(
    root,
    "os/pi-gen-stage/stage2/99-bricohams/files/usr/local/lib",
  );
  const program = [
    "import json",
    "from bricohams_os.config import _unique_object, validate_config",
    "good = {'version': 1, 'peer': '/org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF',",
    "        'vhfSerial': 'VHF-01', 'uhfSerial': 'UHF-02', 'hardwareRate': 1000000}",
    "assert validate_config(good) == good",
    "invalid = [",
    "    {**good, 'peer': '/tmp/untrusted'},",
    "    {**good, 'uhfSerial': good['vhfSerial']},",
    "    {**good, 'hardwareRate': True},",
    "    {**good, 'hardwareRate': 48000},",
    "    {**good, 'extra': 'not allowed'},",
    "]",
    "for candidate in invalid:",
    "    try:",
    "        validate_config(candidate)",
    "    except ValueError:",
    "        pass",
    "    else:",
    "        raise AssertionError('invalid radio config was accepted')",
    "try:",
    "    json.loads('{\"version\":1,\"version\":1}', object_pairs_hook=_unique_object)",
    "except ValueError:",
    "    pass",
    "else:",
    "    raise AssertionError('duplicate config key was accepted')",
  ].join("\n");
  const result = spawnSync("python3", ["-c", program], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONPATH: pythonPath },
  });
  assert.equal(result.status, 0, result.error ? result.error.message : result.stderr);
});

test("image stage preserves upstream OS identity and checks private build artifacts", () => {
  const stage = read("os/pi-gen-stage/stage2/99-bricohams/00-run.sh");
  const docs = read("docs/BRICOHAMS-OS.md");
  const config = read("os/pi-gen.config");
  assert.match(stage, /BEGIN BRICOHAMS CM5IO REV-A BUS CONFIGURATION/);
  assert.match(stage, /ssh_host_/);
  assert.match(stage, /wpa_supplicant\.conf/);
  assert.match(stage, /radio-host\.json/);
  assert.match(stage, /multi-user\.target\.wants\/bricohams-radio\.service/);
  assert.doesNotMatch(stage, /os-release/);
  assert.doesNotMatch(config, /FIRST_USER_PASS|WPA_PASSWORD|PUBKEY_SSH_FIRST_USER/);
  assert.match(docs, /not an official Raspberry Pi product/);
  assert.match(docs, /does \*\*not\*\* flash an SD[\s\S]*?card or eMMC/);
  assert.match(docs, /does not configure a station Wi-Fi access point/);
  assert.match(docs, /requires an explicit choice: `rotor-only`, `radio-only`,[\s\S]*?or `integrated`/);
  assert.match(read("os/licenses/pi-gen-BSD-3-Clause.txt"), /Copyright \(c\) 2015 Raspberry Pi \(Trading\) Ltd\./);
  assert.match(read("os/build-image.sh"), /LICENSES\//);
  assert.match(read("os/build-image.sh"), /docs\/SOURCES\.md/);
  assert.match(read("os/build-image.sh"), /docs\/".*bricohams-os\/docs\//);
  assert.match(read("os/build-image.sh"), /install\/".*bricohams-os\/os\/install\//);
});

test("GitHub image publication is opt-in and validation is separate", () => {
  const workflow = read(".github/workflows/os.yml");
  assert.match(workflow, /hardware\/cm5\/interface\.json/);
  assert.match(workflow, /files\/usr\/local\/libexec\/bricohams-gpio-safe-state/);
  assert.match(workflow, /workflow_dispatch:/);
  assert.match(workflow, /build_image:/);
  assert.match(workflow, /if:.*inputs\.build_image/);
  assert.match(workflow, /actions\/upload-artifact@v4/);
  assert.match(workflow, /tests\/os-image\.test\.cjs/);
});
