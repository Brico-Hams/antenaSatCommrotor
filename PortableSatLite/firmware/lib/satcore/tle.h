// tle.h - parse 3-line TLE text (CelesTrak / AMSAT / PE0SAT formats) and keep only the satellites whose name matches an alias list.
#pragma once
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
struct TleEntry { char name[26]; char l1[70]; char l2[70]; int cat; unsigned long epoch_unix; };
namespace tle {
static inline bool icontains(const char *hay, const char *needle) {
  size_t n = strlen(needle); if (!n) return false;
  for (const char *p = hay; *p; p++) { size_t i = 0; while (i < n && p[i] && tolower((unsigned char)p[i]) == tolower((unsigned char)needle[i])) i++; if (i == n) return true; }
  return false;
}
static inline int checksum_ok(const char *l) {           // standard mod-10 checksum of columns 1..68 vs column 69
  if (strlen(l) < 69) return 0; int s = 0;
  for (int i = 0; i < 68; i++) { if (isdigit((unsigned char)l[i])) s += l[i] - '0'; else if (l[i] == '-') s += 1; }
  return (s % 10) == (l[68] - '0');
}
// TLE epoch (cols 19-32: YYDDD.DDDDDDDD) -> unix seconds
static inline unsigned long epoch_unix(const char *l1) {
  char yy[3] = {l1[18], l1[19], 0}; int y = atoi(yy); y += (y < 57) ? 2000 : 1900; double day = atof(l1 + 20);
  // days from 1970-01-01 to Jan 1 of year y
  long d = 0; for (int k = 1970; k < y; k++) d += ((k % 4 == 0 && k % 100 != 0) || k % 400 == 0) ? 366 : 365;
  return (unsigned long)((d + day - 1.0) * 86400.0);
}
static inline void rtrim(char *s) { int n = strlen(s); while (n > 0 && (s[n-1] == '\r' || s[n-1] == '\n' || s[n-1] == ' ')) s[--n] = 0; }
// aliases[i] = semicolon-separated alternative name fragments for catalog entry i. Returns number of entries stored (replacing same cat if newer).
static inline int parse(const char *text, const char *const *aliases, int n_alias, TleEntry *out, int max_out, int &count) {
  const char *p = text; char line[3][100]; int li = 0; int added = 0;
  while (*p) {
    const char *e = strchr(p, '\n'); size_t len = e ? (size_t)(e - p) : strlen(p); if (len > 98) len = 98;
    char tmp[100]; memcpy(tmp, p, len); tmp[len] = 0; rtrim(tmp);
    p = e ? e + 1 : p + len; if (!tmp[0]) continue;
    if (tmp[0] == '1' && tmp[1] == ' ' && li >= 1) { strcpy(line[1], tmp); li = 2; }
    else if (tmp[0] == '2' && tmp[1] == ' ' && li == 2) {
      strcpy(line[2], tmp);
      if (checksum_ok(line[1]) && checksum_ok(line[2])) {
        for (int a = 0; a < n_alias; a++) {
          char buf[120]; strncpy(buf, aliases[a], 119); buf[119] = 0; bool hit = false;
          for (char *tok = strtok(buf, ";"); tok; tok = strtok(NULL, ";")) if (icontains(line[0], tok)) { hit = true; break; }
          if (!hit) continue;
          unsigned long ep = epoch_unix(line[1]); int slot = -1;
          for (int k = 0; k < count; k++) if (out[k].cat == a) slot = k;
          if (slot >= 0 && out[slot].epoch_unix >= ep) break;           // keep the freshest source
          if (slot < 0) { if (count >= max_out) break; slot = count++; }
          strncpy(out[slot].name, line[0], 25); out[slot].name[25] = 0; strncpy(out[slot].l1, line[1], 69); out[slot].l1[69] = 0;
          strncpy(out[slot].l2, line[2], 69); out[slot].l2[69] = 0; out[slot].cat = a; out[slot].epoch_unix = ep; added++; break;
        }
      }
      li = 0;
    } else { strncpy(line[0], tmp[0] == '0' && tmp[1] == ' ' ? tmp + 2 : tmp, 99); line[0][99] = 0; li = 1; }
  }
  return added;
}
}  // namespace tle
