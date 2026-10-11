#pragma once
// ---- Pins (ESP32-DevKitC). Change here only. See docs/ELECTRONICS.md for the wiring table. ----
#define PIN_AZ_STEP 26
#define PIN_AZ_DIR  27
#define PIN_EL_STEP 25
#define PIN_EL_DIR  33
#define PIN_EN      14      // TMC2209 EN (active low), shared
#define PIN_AZ_LIM  32      // NC micro-switch to GND, INPUT_PULLUP (open/broken wire = 'pressed' = fail-safe)
#define PIN_EL_LIM  13
#define PIN_GPS_RX  16      // GNSS TX -> ESP32 RX2
#define PIN_GPS_TX  17
#define PIN_SDA0    21      // bus 0: MPU6050 (0x68), QMC5883L (0x0D), AS5600-AZ (0x36)
#define PIN_SCL0    22
#define PIN_SDA1    18      // bus 1: AS5600-EL (0x36)   (two AS5600 share an address -> separate buses)
#define PIN_SCL1    19
// ---- Mechanics ----
#define STEPS_PER_REV   200
#define MICROSTEPS      16
#define GEAR_RATIO      25.0     // 5:1 x 5:1 (cad/gears.py)
#define STEPS_PER_DEG   (STEPS_PER_REV * MICROSTEPS * GEAR_RATIO / 360.0)
#define AZ_MIN_DEG      0.0
#define AZ_MAX_DEG      450.0    // 90 deg of overlap = cable wrap, plus flip
#define EL_MIN_DEG      0.0
#define EL_MAX_DEG      180.0    // 0..180 so the antenna can flip over the zenith
#define MAX_SPEED_DEG_S 20.0
#define ACCEL_DEG_S2    40.0
// ---- Network ----
#define AP_PASS "satlite1234"    // CHANGE before use; minimum 8 characters
