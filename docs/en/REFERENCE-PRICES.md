# Reference prices and open budget

## Scope and method

The persistent table is [reference-prices.csv](../../bom/reference-prices.csv).
Collection date: **2026-10-10**. These are indicative public observations,
not binding offers or availability guarantees. No project files were sent to
a manufacturer to obtain a quote.

`unit_reference_eur` is the unit reference price. `mean_eur` is populated only
when there are two comparable observations for the same component. A single
observation is not a market average. Out-of-stock quotes are identified and
do not make a purchasable basket. Empty fields mean **pending**, not zero.
A known price without an approved quantity also does not yield a line-item
cost.

The recorded conversion from the research is EUR 1 = USD 1.1206 and GBP
0.84763, per the [ECB reference](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml)
dated 2026-10-09 and consulted on 2026-10-10. The daily link is mutable:
check the date and rate again before purchase. Currency-conversion fees,
import VAT, customs duties, and shipping are excluded. German references
with known VAT are divided by 1.19; Spanish references by 1.21. VAT is not
deducted when its inclusion has not been confirmed.

## Main references

| ID | Reference quantity | EUR/unit | Basis |
| --- | ---: | ---: | --- |
| CM5 | 1 | 115.67 | Mean of two pre-VAT quotes; one unavailable |
| CM5IO | 1 | 18.40 | One pre-VAT observation |
| SDR | 2 | 535.43 | USD 600 per LimeSDR Mini; before import taxes |
| DRV | 3 | 15.97 | TMC5160 v1.5; pre-VAT |
| ENC | 3 | 5.31 | AS5600; before import taxes |
| COMPASS | 1 | 8.88 | LIS3MDL; before import taxes |
| IMU | 1 | 10.33 | Normalized mean; one shop out of stock |
| GPS | 1 | 25.93 | Normalized mean |
| ASA | 1 reference spool | 23.46 | Pre-VAT mean; actual consumption pending |
| BAT | 1 external | 99.99 | Displayed price; VAT inclusion unconfirmed |
| PP-PACK | 1 reference pack | 15.16 | Ten complete red/black pairs; before import |
| PP-TOOL | 1 optional tool | 35.69 | Reusable crimper; budget separately |

The CM5, CM5IO, two SDRs, three drivers, three encoders, compass, IMU, and
GPS subset totals **EUR 1,313.90**, normalized pre-VAT. With one reference
spool of ASA it totals **EUR 1,337.35**. These are alternative subtotals,
not addends. **Neither is the price of the complete station.** The EUR 99.99
battery remains separate because its tax basis is unconfirmed. The CSV
retains decimal precision for calculations; round only at the end.

The following still lack complete quotes: linear PAs, filters/duplexer and
RF switching, coax/SMA, motors and mechanical transmission, tripod,
fasteners, auxiliary PCB/PCBA, converters, selected harnesses and fuses,
charger, USB3 interconnects, audio/K1, consumables, and measuring tools.
The table contains pending rows for these categories: do not hide them by
summing only the priced rows.

## External power, Powerpole, and fuses

The selected battery is ECO-WORTHY variant **40308275183822**, SKU
**DE-L13060202003-1**, a pack without a charger. The public listing states
12.8 V, 30 Ah, 360 Wh, 3.55 kg, dimensions 183 x 176 x 83 mm, and M5
terminals. 12.8 x 30 = **384 Wh**, which differs from the published 360 Wh.
For planning, retain the lower figure, 360 Wh; neither figure demonstrates
measured usable energy. The listing states a maximum charge/discharge
current of 30 A and maximum charge voltage of 14.6 V; peak durations or
thresholds from other BMS models are not attributed to this one. Charge
temperature is 0 to 55 C and discharge temperature -20 to 55 C; automatic
cold-temperature cutoff has not been demonstrated.

Only the external battery is excluded from the station's **5 kg** target.
Its mass still counts toward carried weight and its cost remains in the
budget. The tripod, cables, radio, connectors, and installed filters remain
included. Two-hour runtime must be measured with the real RX/TX and motor
duty cycle.

WP30-10 contains ten complete red/black pairs and twenty contacts: five
mated pairs. One pair requires two ends; do not count the pack and the
allocations of its same contacts twice. Use a tool and wire compatible with
the exact contacts. Install a main fuse close to battery positive and branch
fuses for computing, motors, and RF. The BMS does not replace these fuses.
Commercial examples rated 5 A or 15 A **do not set** approved current
ratings: select ratings based on wire, normal current, inrush, temperature,
and DC interrupt capacity.

## USB-C and EMI filtering

The Raspberry Pi 27 W mains supply is a bench reference only; it does not
solve battery-powered operation. The USB-C supply must provide the compatible
5 V/5 A profile, and its cable must be qualified. A sink PD trigger is not
a USB-C power supply and does not authorize applying 9-20 V to the CM5IO.

The type 31 2631801202 toroid has a reference price of **EUR 2.56 pre-VAT**
per core, not per completed choke. Four to eight cores would cost
EUR 10.24-20.48 before tax/shipping, but this is neither a complete EMI
budget nor a selected quantity. Common-mode chokes, clamp-on ferrites, and
damped differential LC filtering remain optional/pending-DNP. Qualify DCR,
current, imbalance/saturation, temperature, frequency, voltage drop, and
converter stability. Compare RX noise and TX spurs with and without the
filter; include installed filter mass in the 5 kg limit.

## Purchases by module

Use the [antenna](MODULE-ANTENNA.md), [rotor](MODULE-ROTOR.md),
[radio](MODULE-RADIO.md), and [integrated](MODULE-INTEGRATED.md) build paths.
Their local BOMs are parts lists, not independent baskets to be summed
without review: in the integrated build, count the CM5/CM5IO once and assign
shared parts to a single module. Alternatives, tools, and optional references
are not automatically added to the selected subtotal.

To close the budget, specify the MPN/revision, quantity for each assembly
step, units consumed versus packs purchased, availability, VAT, and shipping
for every order. Record supplier and date, and reconcile the local BOMs with
this table. Until then, the total cost remains **open**.
