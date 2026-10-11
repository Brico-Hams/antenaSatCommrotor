#!/usr/bin/env bash
# Runs every host-side check. Needs: g++, python3 with numpy sgp4 PyNEC trimesh manifold3d playwright, and a clone of Hopperpop/Sgp4-Library (SGP4_LIB=.../src).
set -e; cd "$(dirname "$0")/.."
export SGP4_LIB=${SGP4_LIB:-$PWD/../ext/Sgp4-Library/src}
python3 tests/test_satcore.py
python3 tests/test_sgp4_lib.py
python3 tests/test_tracker.py
g++ -std=c++17 -I firmware/lib/satcore -o tests/out/test_tle tests/test_tle.cpp && ./tests/out/test_tle
python3 tests/test_webui.py
python3 cad/test_gears.py
python3 calc/antenna_nec.py >/dev/null && python3 calc/beamwidth.py && python3 calc/feed_network.py >/dev/null && python3 calc/rotor_calc.py >/dev/null && python3 calc/mass_budget.py >/dev/null
echo "ALL CHECKS PASSED"
