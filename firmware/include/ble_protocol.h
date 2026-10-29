#pragma once
#include <cstddef>
#include <cstdint>
#include <cstring>
namespace ControlBLE {
constexpr uint32_t protocolVersion = 1;
constexpr uint32_t apiVersion = 2; // 2: POST /api/time and mechanical profile in status
constexpr const char *firmwareVersion = "0.3.0-prototype";
constexpr size_t maxRequest = 2048;
constexpr size_t frameBytes = 20, headerBytes = 4, payloadBytes = 16;
constexpr uint8_t magic = 0x53, startFlag = 1, endFlag = 2;
// One bounded JSON message: no execution until valid END and full JSON/auth.
struct Assembler {
  char data[maxRequest + 1]{};
  size_t length = 0;
  uint16_t expected = 0;
  bool active = false;
  void reset() { length = expected = 0; active = false; data[0] = 0; }
  // -1 malformed, 0 incomplete, 1 complete; caller resets after consuming.
  int feed(const uint8_t *frame, size_t size) {
    if (size < 5 || size > frameBytes || frame[0] != magic || (frame[1] & ~3)) {
      reset(); return -1;
    }
    uint16_t sequence = frame[2] | (uint16_t(frame[3]) << 8);
    if (frame[1] & startFlag) {
      if (active || sequence != 0) { reset(); return -1; }
      reset(); active = true;
    }
    size_t count = size - headerBytes;
    if (!active || sequence != expected || length + count > maxRequest ||
        std::memchr(frame + headerBytes, 0, count)) { reset(); return -1; }
    std::memcpy(data + length, frame + headerBytes, count);
    length += count; data[length] = 0; ++expected;
    if (frame[1] & endFlag) { active = false; return 1; }
    return 0;
  }
};
inline bool validPasskey(uint32_t passkey) { return passkey >= 100000 && passkey <= 999999; }
inline bool authorized(bool provisioning, bool secure, const char *expected, const char *provided) {
  if (provisioning || !secure || std::strlen(expected) < 24) return false;
  size_t a = std::strlen(expected), b = std::strlen(provided);
  if (a != b) return false;
  unsigned mismatch = 0;
  for (size_t i = 0; i < a; ++i) mismatch |= uint8_t(expected[i]) ^ uint8_t(provided[i]);
  return mismatch == 0;
}
}
