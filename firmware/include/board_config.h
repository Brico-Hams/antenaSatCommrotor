#pragma once

// Frozen with modular carrier: ESP32-DevKitC V4, 38-pin WROOM-32E ONLY.
// Not WROVER/PSRAM, S3/C3, or generic differently-pinned DevKit modules.
namespace Board {
constexpr bool carrierVerified = false; // Set true only after physical carrier checkout.
constexpr int azStep = 26, azDir = 27, elStep = 14, elDir = 13;
constexpr int enable = 25;                 // active LOW, external 10k pull-up
constexpr int estop = 34;                  // NC to GND; open/HIGH = fault
constexpr int azMin = 35, azMax = 36, elMin = 39, elMax = 32;
// All four limits NC to GND: HIGH/open = reached limit or broken wire.
constexpr int gpsRx = 16, gpsTx = 17; // Available on WROOM-32E, NOT WROVER.
constexpr int azSda = 21, azScl = 22, elSda = 18, elScl = 19;
constexpr bool encoders = false;
constexpr int azDirection = 1, elDirection = 1;
constexpr int azEncoderDirection = 1, elEncoderDirection = 1;
constexpr unsigned gpsBaud = 9600;
// Provision locally before flashing. Empty credentials disable the control API.
constexpr const char *apSsid = "PortableSatStation";
constexpr const char *apPassword = "";
constexpr const char *apiToken = "";
constexpr const char *staSsid = "";
constexpr const char *staPassword = "";
// PEM trust anchor(s) for selected HTTPS providers; empty means updates refused.
// Never substitute setInsecure(). Certificate expiry is checked against GNSS UTC.
constexpr const char *tlsRoots = "";
}
