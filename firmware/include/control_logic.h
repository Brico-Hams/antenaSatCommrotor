#pragma once
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <initializer_list>

// Build-time mechanical profile. Defaults are the reference NEMA14 build;
// other profiles (e.g. env:esp32_nema17) override them with -D flags.
#ifndef ROTOR_MICROSTEPS
#define ROTOR_MICROSTEPS 16
#endif
#ifndef ROTOR_TRANSMISSION_RATIO
#define ROTOR_TRANSMISSION_RATIO 25
#endif
#ifndef ROTOR_MAX_RATE_STEPS
#define ROTOR_MAX_RATE_STEPS 500.0
#endif
#ifndef ROTOR_ACCELERATION_STEPS
#define ROTOR_ACCELERATION_STEPS 300.0
#endif

namespace Control {
constexpr int fullStepsPerRevolution = 200;
constexpr int microsteps = ROTOR_MICROSTEPS;
constexpr int transmissionRatio = ROTOR_TRANSMISSION_RATIO; // reference: two 20:100 belt stages, 5 x 5
constexpr int stepsPerRevolution =
  fullStepsPerRevolution * microsteps * transmissionRatio;
static_assert(microsteps >= 1 && microsteps <= 256 &&
              (microsteps & (microsteps - 1)) == 0, "Microsteps must be a power of two");
static_assert(transmissionRatio >= 1 && transmissionRatio <= 100, "Unsupported transmission ratio");
static_assert(stepsPerRevolution >= 3600, "Need at least 0.1 deg per microstep");
// Homing offsets are exact fractions of a revolution; keep them integral.
static_assert(stepsPerRevolution % 800 == 0, "Revolution must be divisible by 800 microsteps");
constexpr double stepsPerDegree = stepsPerRevolution / 360.0;
constexpr double maxRate = ROTOR_MAX_RATE_STEPS;  // microsteps/s; reference 500 = 2.25 deg/s
constexpr double acceleration = ROTOR_ACCELERATION_STEPS; // microsteps/s^2
// Motor task runs near 1 kHz and emits at most one step per tick.
static_assert(maxRate > 0 && maxRate <= 700.0, "maxRate must stay below the 1 kHz step tick");
static_assert(acceleration > 0 && acceleration <= 2000.0, "Unsupported acceleration");
constexpr double maxDegreesPerSecond = maxRate / stepsPerDegree;
constexpr uint32_t maxTleAge = 14 * 86400;
inline bool validCredentials(const char *ssid, const char *password, const char *token) {
  size_t s = std::strlen(ssid), p = std::strlen(password), t = std::strlen(token);
  if (s < 1 || s > 32 || p < 12 || p > 63 || t < 24 || t > 128) return false;
  for (const char *v : {ssid, password, token})
    for (const char *c = v; *c; ++c) if (*c < 32 || *c > 126) return false;
  return true;
}
inline double wrap(double d) {
  d = std::fmod(d, 360.0);
  return d < 0 ? d + 360.0 : d;
}
inline double difference(double a, double b) {
  double d = wrap(a - b + 180.0) - 180.0;
  return d;
}
inline bool inRange(double az, double el) {
  return std::isfinite(az) && std::isfinite(el) &&
         az >= -180 && az <= 180 && el >= 0 && el <= 90;
}
inline bool mechanicalAz(double trueAz, double northOffset, double &result) {
  if (!std::isfinite(trueAz) || !std::isfinite(northOffset)) return false;
  result = difference(trueAz, northOffset);
  return true;
}
inline bool leap(int y) {
  return y % 4 == 0 && (y % 100 != 0 || y % 400 == 0);
}
inline int64_t daysBeforeYear(int y) {
  int64_t days = 0;
  for (int n = 1970; n < y; ++n) days += leap(n) ? 366 : 365;
  return days;
}
inline int64_t utc(int y, int m, int d, int h, int minute, int second) {
  const int lengths[] = {31,28,31,30,31,30,31,31,30,31,30,31};
  if (y < 2024 || y > 2099 || m < 1 || m > 12 || d < 1 ||
      d > lengths[m-1] + (m == 2 && leap(y) ? 1 : 0) ||
      h < 0 || h > 23 || minute < 0 || minute > 59 || second < 0 || second > 59)
    return 0;
  int64_t days = daysBeforeYear(y) + d - 1;
  for (int n = 1; n < m; ++n) days += lengths[n-1] + (n == 2 && leap(y) ? 1 : 0);
  return days * 86400 + h * 3600 + minute * 60 + second;
}
inline bool numeric(const char *line, int start, int length, double &out) {
  char buffer[24];
  if (length >= int(sizeof(buffer))) return false;
  std::memcpy(buffer, line + start, length);
  buffer[length] = 0;
  char *end;
  out = std::strtod(buffer, &end);
  if (end == buffer || !std::isfinite(out)) return false;
  while (*end == ' ') ++end;
  return *end == 0;
}
inline bool checksum(const char *line, char type) {
  if (std::strlen(line) != 69 || line[0] != type || line[1] != ' ' ||
      line[68] < '0' || line[68] > '9') return false;
  int sum = 0;
  for (int i = 0; i < 68; ++i) {
    if (line[i] < 32 || line[i] > 126) return false;
    if (line[i] >= '0' && line[i] <= '9') sum += line[i] - '0';
    if (line[i] == '-') ++sum;
  }
  return sum % 10 == line[68] - '0';
}
inline int64_t tleEpoch(const char *line) {
  double year, day;
  if (!numeric(line, 18, 2, year) || !numeric(line, 20, 12, day)) return 0;
  int y = int(year) + (year < 57 ? 2000 : 1900);
  if (y < 1970 || day < 1 || day >= (leap(y) ? 367 : 366)) return 0;
  return daysBeforeYear(y) * 86400 + int64_t((day - 1) * 86400);
}
inline bool validTle(const char *one, const char *two) {
  if (!checksum(one, '1') || !checksum(two, '2') ||
      std::memcmp(one + 2, two + 2, 5) != 0) return false;
  for (int i = 2; i < 7; ++i)
    if (one[i] < '0' || one[i] > '9') return false; // numeric NORAD, not Alpha-5
  double derivative;
  if (!numeric(one, 33, 10, derivative)) return false;
  for (int start : {44, 53}) {
    if (one[start] != ' ' && one[start] != '+' && one[start] != '-') return false;
    for (int i = start + 1; i < start + 6; ++i)
      if (one[i] < '0' || one[i] > '9') return false;
    if (one[start + 6] != '+' && one[start + 6] != '-' && one[start + 6] != ' ') return false;
    if (one[start + 7] < '0' || one[start + 7] > '9') return false;
  }
  double inclination, node, arg, anomaly, motion, eccentricity;
  if (!numeric(two, 8, 8, inclination) || !numeric(two, 17, 8, node) ||
      !numeric(two, 34, 8, arg) || !numeric(two, 43, 8, anomaly) ||
      !numeric(two, 52, 11, motion) || !numeric(two, 26, 7, eccentricity))
    return false;
  for (int i = 26; i < 33; ++i) if (two[i] < '0' || two[i] > '9') return false;
  return tleEpoch(one) > 0 && inclination >= 0 && inclination <= 180 &&
    node >= 0 && node < 360 && arg >= 0 && arg < 360 && anomaly >= 0 &&
    anomaly < 360 && motion > 0 && motion <= 18 && eccentricity < 10000000;
}
inline bool fresh(int64_t now, int64_t epoch) {
  return now > 0 && epoch > 0 && now >= epoch - 86400 &&
         now - epoch <= maxTleAge;
}
struct Axis {
  int32_t position = 0;
  double target = 0, speed = 0, phase = 0;
  void stop() { target = position; speed = phase = 0; }
  // One step maximum per tick: delayed scheduling never emits a burst.
  int tick(double dt) {
    if (dt <= 0 || dt > .02) { speed = phase = 0; return 0; }
    double remaining = target - position;
    double wanted = std::fabs(remaining) < .5 ? 0 :
      (remaining > 0 ? 1 : -1) * std::fmin(maxRate,
        std::sqrt(2 * acceleration * std::fabs(remaining)));
    double delta = acceleration * dt;
    if (speed < wanted) speed = std::fmin(wanted, speed + delta);
    else speed = std::fmax(wanted, speed - delta);
    phase += std::fabs(speed) * dt;
    if (phase < 1 || speed == 0) return 0;
    phase -= 1;
    int step = speed > 0 ? 1 : -1;
    position += step;
    return step;
  }
};
}
