# ADR-011: TLE: 3 fuentes, filtrado por alias, validación de checksum, la época más reciente gana

**Estado:** Aceptada

## Contexto
El usuario indica CelesTrak (grupo amateur), AMSAT `dailytle.txt` y PE0SAT `mykepler.txt`.

## Decisión
El firmware descarga las tres, las concatena, valida el checksum módulo 10 de cada línea y conserva solo los satélites del catálogo (`firmware/data/satellites.json`); si hay duplicados conserva la época más reciente. Se admite también pegar un TLE manual.

## Justificación y evidencia
`tests/test_tle.cpp`: rechaza una línea con checksum erróneo, filtra por alias y la época calculada coincide con python-sgp4 (1575909509).

## Consecuencias y límites
Se usa `setInsecure()` en HTTPS (sin validar la cadena de certificados) porque los datos son públicos y llevan checksum; un atacante en la red podría dar TLE falsos. Las URLs `http://` del usuario se usan tal cual. Las frecuencias del catálogo proceden de los documentos del proyecto del usuario (oct. 2026): **verificar en el estado de satélites de AMSAT antes de transmitir**.
