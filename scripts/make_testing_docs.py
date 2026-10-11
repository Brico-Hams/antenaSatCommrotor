"""Generate the testing section (es/en/hu), bench figures and the results register CSV."""
import sys, json, csv, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from testdata import sec_b
from testdata.sec_a import SECTIONS
from testdata.bench import LEVELS, EQUIP, STOP, TESTER
from _figkit import frame, ROOT, NAVY, ORANGE, GREY
LANGS = ('es', 'en', 'hu')
DIR = {'es': ROOT/'docs/testing', 'en': ROOT/'docs/en/testing', 'hu': ROOT/'docs/hu/testing'}
FIGDIR = ROOT/'docs/testing/fig'
SUF = {'es': '', 'en': '.en', 'hu': '.hu'}
L = {  # labels
 'action': dict(es='Acción', en='Action', hu='Művelet'), 'exp': dict(es='Esperado', en='Expected behaviour', hu='Várt viselkedés'),
 'crit': dict(es='Criterio de aprobación', en='Pass criterion', hu='Elfogadási kritérium'),
 'rec': dict(es='Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE', en='Measured result ____ · Date ____ · Instrument ____ · Status: PENDING', hu='Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ'),
 'beh': dict(es='Comportamiento esperado del componente', en='Expected component behaviour', hu='A komponens várt viselkedése'),
 'back': dict(es='Volver al índice', en='Back to the index', hu='Vissza a tartalomjegyzékhez'),
}
FILES = {  # file -> (section codes, title)
 '02-electronica.md': (['PWR', 'DRV', 'SNS'], dict(es='Electrónica: alimentación, drivers y sensores', en='Electronics: power, drivers and sensors', hu='Elektronika: táplálás, meghajtók és érzékelők')),
 '03-puerta-pcb.md': (['PCB'], dict(es='Puerta previa a fabricar las PCB', en='Pre-fabrication gate for the PCBs', hu='Gyártás előtti kapu a PCB-khez')),
 '04-mecanica.md': (['MEC'], dict(es='Mecánica del rotor', en='Rotor mechanics', hu='A forgató mechanikája')),
 '05-rf-y-radio.md': (['ANT', 'RAD'], dict(es='Antena, RF y radio SDR', en='Antenna, RF and SDR radio', hu='Antenna, RF és SDR rádió')),
 '06-software-y-os.md': (['SW'], dict(es='Software, hosts CM5 e imagen del sistema operativo', en='Software, CM5 hosts and OS image', hu='Szoftver, CM5 hostok és OS-kép')),
 '07-app-android.md': (['APP'], dict(es='Aplicación Android', en='Android app', hu='Android-alkalmazás')),
 '08-sistema.md': (['SYS'], dict(es='Integración del sistema (G3 / G4)', en='System integration (G3 / G4)', hu='Rendszerintegráció (G3 / G4)')),
}
AUTH = 'Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina · bricohams.org'
FIGS = {'T1': 'T1-banco-pruebas', 'T2': 'T2-comprobador-gpio', 'T3': 'T3-fixture-mecanico'}
def fig(code, lang): return f'![{code}]({"fig" if lang == "es" else "../../testing/fig"}/{FIGS[code]}{SUF[lang]}.svg)\n\n*{code}* — BricoHams · {AUTH}\n'
SEC = {s['code']: s for s in SECTIONS}
def render_section(s, lang):
    o = [f"## {s['code']} — {s['title'][lang]}\n", f"**{L['beh'][lang]}.** {s['behaviour'][lang]}\n"]
    for tid, tx in s['tests']:
        a, e, c = tx[lang]
        o.append(f"### {tid}\n- [ ] **{L['action'][lang]}:** {a}\n- **{L['exp'][lang]}:** {e}\n- **{L['crit'][lang]}:** {c}\n- _{L['rec'][lang]}_\n")
    return '\n'.join(o)
T = {
 'intro': dict(
  es='''# Pruebas: componentes, comportamiento y banco

Esta sección describe CÓMO probar cada componente del PortableSatStation **antes de fabricar las PCB** y antes de integrar la estación: banco de pruebas, checklists, comportamiento esperado y criterios de aprobación. Complementa las puertas G0-G4 de [ACCEPTANCE.md](../ACCEPTANCE.md) y el registro de [VALIDATION.md](../VALIDATION.md).

> **Estado:** prototipo digital, **no validado físicamente**. Nada de lo que sigue se ha medido todavía: todos los ensayos están PENDIENTES hasta anotar medida, fecha e instrumento. Los criterios con referencia `Gn-m` provienen de ACCEPTANCE.md; los demás son valores de ingeniería **propuestos** por esta revisión que deben confirmarse o ajustarse con el primer prototipo. Compilar o pasar pruebas de software no valida cableado, mecánica ni RF.

## Cómo usar esta sección
1. Monte el banco de la guía [01-banco-de-pruebas.md](01-banco-de-pruebas.md) por niveles (B0 → B4).
2. Ejecute los checklists en orden: electrónica → puerta PCB → mecánica → RF/radio → software/OS → app Android → sistema.
3. Anote cada resultado en [registro-pruebas.csv](registro-pruebas.csv) (una fila por ensayo) con fecha, revisión Git, instrumentos y operador.
4. **Parada:** si falla un ensayo de seguridad (PWR, DRV-02/05, SNS-04, MEC-05) no avance a motores bajo carga ni a RF.
5. No pida la fabricación de ninguna PCB hasta cerrar la [puerta previa](03-puerta-pcb.md).

## Seguridad
Supervisión adulta, parada de emergencia accesible, fuente con límite de corriente, motores sin carga en las primeras pruebas, gafas al taladrar/lijar, sin transmitir sin licencia, carga de 50 Ω (no antena) para todo ensayo de TX, 12 V nunca en la cabecera del CM5.

## Mapa de ensayos
| Documento | Secciones | Puerta |
|---|---|---|
''',
  en='''# Testing: components, behaviour and bench

This section describes HOW to test every PortableSatStation component **before the PCBs are manufactured** and before the station is integrated: test bench, checklists, expected behaviour and pass criteria. It complements gates G0-G4 in [ACCEPTANCE.md](../ACCEPTANCE.md) and the record in [VALIDATION.md](../VALIDATION.md).

> **Status:** digital prototype, **not physically validated**. Nothing below has been measured yet: every test is PENDING until result, date and instrument are recorded. Criteria with a `Gn-m` reference come from ACCEPTANCE.md; the others are engineering values **proposed** by this review that must be confirmed or adjusted with the first prototype. Building or passing software tests does not validate wiring, mechanics or RF.

## How to use this section
1. Build the bench from [01-banco-de-pruebas.md](01-banco-de-pruebas.md) by levels (B0 → B4).
2. Run the checklists in order: electronics → PCB gate → mechanics → RF/radio → software/OS → Android app → system.
3. Record every result in [registro-pruebas.csv](registro-pruebas.csv) (one row per test) with date, Git revision, instruments and operator.
4. **Stop:** if a safety test fails (PWR, DRV-02/05, SNS-04, MEC-05) do not proceed to loaded motors or RF.
5. Do not order any PCB until the [pre-fabrication gate](03-puerta-pcb.md) is closed.

## Safety
Adult supervision, accessible emergency stop, current-limited supply, unloaded motors in early tests, eye protection when drilling/sanding, no transmitting without a licence, 50 Ω load (not an antenna) for every TX test, 12 V never on the CM5 header.

## Test map
| Document | Sections | Gate |
|---|---|---|
''',
  hu='''# Tesztelés: komponensek, viselkedés és tesztpad

Ez a szakasz azt írja le, HOGYAN kell tesztelni a PortableSatStation minden komponensét **a PCB-k gyártása előtt** és az állomás integrálása előtt: tesztpad, ellenőrzőlisták, várt viselkedés és elfogadási kritériumok. Kiegészíti az [ACCEPTANCE.md](../ACCEPTANCE.md) G0-G4 kapuit és a [VALIDATION.md](../VALIDATION.md) nyilvántartását.

> **Állapot:** digitális prototípus, **fizikailag nem validált**. Az alábbiak közül még semmit sem mértek meg: minden teszt FÜGGŐ, amíg az eredmény, a dátum és a műszer nincs feljegyezve. A `Gn-m` hivatkozású kritériumok az ACCEPTANCE.md-ből származnak; a többi ennek a felülvizsgálatnak a **javasolt** mérnöki értéke, amelyet az első prototípussal meg kell erősíteni vagy módosítani. A szoftverfordítás vagy az átmenő szoftvertesztek nem validálják a kábelezést, a mechanikát vagy az RF-et.

## Hogyan használd ezt a szakaszt
1. Építsd fel a padot a [01-banco-de-pruebas.md](01-banco-de-pruebas.md) szerint szintenként (B0 → B4).
2. Futtasd az ellenőrzőlistákat sorrendben: elektronika → PCB-kapu → mechanika → RF/rádió → szoftver/OS → Android-alkalmazás → rendszer.
3. Minden eredményt jegyezz a [registro-pruebas.csv](registro-pruebas.csv) fájlba (tesztenként egy sor) dátummal, Git-revízióval, műszerekkel és kezelővel.
4. **Állj meg:** ha egy biztonsági teszt elbukik (PWR, DRV-02/05, SNS-04, MEC-05), ne lépj tovább terhelt motorokra vagy RF-re.
5. Egyetlen PCB-t se rendelj meg, amíg a [gyártás előtti kapu](03-puerta-pcb.md) nincs lezárva.

## Biztonság
Felnőtt felügyelet, elérhető vészleállító, áramkorlátos táp, a korai tesztekben terheletlen motorok, védőszemüveg fúráskor/csiszoláskor, engedély nélkül nem adunk, minden TX-tesztnél 50 Ω-os lezárás (nem antenna), a 12 V soha nem kerül a CM5 tüskesorára.

## Tesztek térképe
| Dokumentum | Szakaszok | Kapu |
|---|---|---|
'''),
}
GATE = {'02-electronica.md': 'G1E', '03-puerta-pcb.md': 'G1E', '04-mecanica.md': 'G1', '05-rf-y-radio.md': 'G2 / G4', '06-software-y-os.md': 'G0', '07-app-android.md': 'G3', '08-sistema.md': 'G3 / G4', '01-banco-de-pruebas.md': '—'}
BENCH_T = dict(es='Diseño del banco de pruebas', en='Test bench design', hu='A tesztpad kialakítása')
def bench_doc(lang):
    o = [f"# {BENCH_T[lang]}\n"]
    o.append({'es': 'El banco permite probar cada bloque con módulos reales y cableado de prototipo **antes** de fabricar las PCB: si el circuito equivalente no pasa en el banco, la placa no se pide.',
              'en': 'The bench lets every block be tested with real modules and prototype wiring **before** the PCBs are made: if the equivalent circuit does not pass on the bench, the board is not ordered.',
              'hu': 'A pad lehetővé teszi, hogy minden blokkot valódi modulokkal és prototípus-kábelezéssel teszteljünk **a PCB-k gyártása előtt**: ha az egyenértékű áramkör nem teljesít a padon, a panelt nem rendeljük meg.'}[lang] + '\n')
    o.append(fig('T1', lang))
    hdr = {'es': ('Nivel', 'Contenido', 'Pruebas'), 'en': ('Level', 'Contents', 'Tests'), 'hu': ('Szint', 'Tartalom', 'Tesztek')}[lang]
    o.append({'es': '## Niveles del banco', 'en': '## Bench levels', 'hu': '## A pad szintjei'}[lang] + f"\n\n| {hdr[0]} | {hdr[1]} | {hdr[2]} |\n|---|---|---|")
    for code, name, desc, tests in LEVELS: o.append(f"| **{code}** {name[lang]} | {desc[lang]} | {tests} |")
    o.append('\n' + {'es': '## Cadena de parada', 'en': '## Stop chain', 'hu': '## Leállítási lánc'}[lang] + '\n\n' + STOP[lang] + '\n')
    o.append({'es': '## Comprobador del contrato GPIO', 'en': '## GPIO-contract tester', 'hu': '## GPIO-szerződés tesztelő'}[lang] + '\n\n' + TESTER[lang] + '\n\n' + fig('T2', lang))
    o.append({'es': '## Fixture mecánico', 'en': '## Mechanical fixture', 'hu': '## Mechanikai rögzítő'}[lang] + '\n\n' + {
        'es': 'Rotor atornillado a un tablero rígido de 18 mm con tres puntos de apoyo; brazo con la carga objetivo de 0,5 kg a distancia conocida; goniómetro fijo al eje y indicador de dial sobre el brazo para holgura; báscula para la masa; cámara térmica sobre drivers y motor.',
        'en': 'Rotor bolted to a rigid 18 mm board on three support points; arm with the 0.5 kg target load at a known distance; protractor fixed to the shaft and dial indicator on the arm for backlash; scale for mass; thermal camera on drivers and motor.',
        'hu': 'A forgató merev, 18 mm-es lapra csavarozva három támasztási ponton; a 0,5 kg-os célterhelést viselő kar ismert távolságban; a tengelyre rögzített szögmérő és a karon mérőóra a holtjátékhoz; mérleg a tömeghez; hőkamera a meghajtókon és a motoron.'}[lang] + '\n\n' + fig('T3', lang))
    h = {'es': ('Ref.', 'Cant.', 'Equipo / componente', 'Usado en'), 'en': ('Ref.', 'Qty', 'Equipment / component', 'Used in'), 'hu': ('Hiv.', 'Db', 'Eszköz / komponens', 'Felhasználás')}[lang]
    o.append({'es': '## Lista de equipos y componentes del banco', 'en': '## Bench equipment and component list', 'hu': '## A pad eszköz- és komponenslistája'}[lang] + f"\n\n| {h[0]} | {h[1]} | {h[2]} | {h[3]} |\n|---|---|---|---|")
    idx = {'es': 2, 'en': 3, 'hu': 4}[lang]
    for e in EQUIP: o.append(f"| {e[0]} | {e[1]} | {e[idx]} | {e[5]} |")
    o.append('\n' + {'es': '## Criterios para liberar la fabricación de PCB', 'en': '## Criteria to release PCB manufacturing', 'hu': '## A PCB-gyártás felszabadításának feltételei'}[lang] + '\n\n' + {
        'es': '1. PWR, DRV y SNS APROBADOS en B1 con el circuito equivalente.\n2. Comprobador GPIO: las 26 señales coinciden (PCB-05).\n3. ERC/DRC sin errores, hashes verificados y revisión por una segunda persona (PCB-01…03, 08).\n4. Ningún pedido sin aprobación explícita del responsable. [Puerta previa](03-puerta-pcb.md).',
        'en': '1. PWR, DRV and SNS APPROVED on B1 with the equivalent circuit.\n2. GPIO tester: all 26 signals match (PCB-05).\n3. ERC/DRC with no errors, hashes verified and review by a second person (PCB-01…03, 08).\n4. No order without explicit approval by the owner. [Pre-fabrication gate](03-puerta-pcb.md).',
        'hu': '1. PWR, DRV és SNS JÓVÁHAGYVA a B1 szinten az egyenértékű áramkörrel.\n2. GPIO-tesztelő: mind a 26 jel egyezik (PCB-05).\n3. ERC/DRC hiba nélkül, ellenőrzött hashek és egy második személy általi átnézés (PCB-01…03, 08).\n4. Kifejezett tulajdonosi jóváhagyás nélkül nincs rendelés. [Gyártás előtti kapu](03-puerta-pcb.md).'}[lang] + '\n')
    o.append(f"[{L['back'][lang]}](README.md)\n")
    return '\n'.join(o)
def write_docs():
    for lang in LANGS:
        d = DIR[lang]; d.mkdir(parents=True, exist_ok=True)
        rows = [f"| [01-banco-de-pruebas.md](01-banco-de-pruebas.md) | {BENCH_T[lang]} | — |"]
        for fn, (codes, title) in FILES.items():
            rows.append(f"| [{fn}]({fn}) | {title[lang]} ({', '.join(codes)}) | {GATE[fn]} |")
        extra = {'es': '\n\nFiguras con el logo de BricoHams y los autores: T1 (banco), T2 (comprobador GPIO), T3 (fixture mecánico) en `fig/`.\n\nRegistro: [registro-pruebas.csv](registro-pruebas.csv). Montaje: [guía de ensamblaje](../assembly/README.md). Ayuda de la app: `android/app/src/main/res/raw*/`.\n',
                 'en': '\n\nFigures with the BricoHams logo and authors: T1 (bench), T2 (GPIO tester), T3 (mechanical fixture) in `fig/`.\n\nRecord: [registro-pruebas.csv](registro-pruebas.csv). Assembly: [assembly guide](../assembly/README.md). App help: `android/app/src/main/res/raw*/`.\n',
                 'hu': '\n\nA BricoHams-logóval és a szerzőkkel ellátott ábrák: T1 (pad), T2 (GPIO-tesztelő), T3 (mechanikai rögzítő) a `fig/` mappában.\n\nNyilvántartás: [registro-pruebas.csv](registro-pruebas.csv). Összeszerelés: [összeszerelési útmutató](../assembly/README.md). Az alkalmazás súgója: `android/app/src/main/res/raw*/`.\n'}[lang]
        (d/'README.md').write_text(T['intro'][lang] + '\n'.join(rows) + extra, encoding='utf-8')
        (d/'01-banco-de-pruebas.md').write_text(bench_doc(lang), encoding='utf-8')
        for fn, (codes, title) in FILES.items():
            body = f"# {title[lang]}\n\n" + {'es': 'Cada ensayo es una casilla: márquela solo con medida, fecha e instrumento anotados en el registro.', 'en': 'Each test is a checkbox: tick it only with the measurement, date and instrument recorded in the register.', 'hu': 'Minden teszt egy jelölőnégyzet: csak akkor jelöld be, ha a mérés, a dátum és a műszer rögzítve van a nyilvántartásban.'}[lang] + '\n\n'
            body += '\n'.join(render_section(SEC[c], lang) for c in codes) + f"\n[{L['back'][lang]}](README.md)\n"
            (d/fn).write_text(body, encoding='utf-8')
    # register CSV (language-neutral ids, ES descriptions + EN)
    with open(DIR['es']/'registro-pruebas.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n'); w.writerow(['id', 'section', 'action_es', 'action_en', 'date', 'git_revision', 'instrument', 'operator', 'measured_result', 'status', 'notes'])
        for s in SECTIONS:
            for tid, tx in s['tests']: w.writerow([tid, s['code'], tx['es'][0], tx['en'][0], '', '', '', '', '', 'PENDIENTE', ''])
    for lang in ('en', 'hu'):
        import shutil; shutil.copyfile(DIR['es']/'registro-pruebas.csv', DIR[lang]/'registro-pruebas.csv')
if __name__ == '__main__':
    write_docs(); print(sum(len(s['tests']) for s in SECTIONS), 'tests')
