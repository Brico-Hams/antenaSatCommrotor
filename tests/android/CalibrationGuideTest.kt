package org.bricohams.portablesatstation

import org.junit.Assert.*
import org.junit.Test

class CalibrationGuideTest {
    @Test fun guideIsDurableAndNeverInfersCalibration() {
        assertEquals(CalibrationPhase.CHECK_AND_HOME, CalibrationPhase.restore("bad"))
        assertEquals(CalibrationPhase.TRUE_HEADING, CalibrationPhase.restore(CalibrationPhase.TRUE_HEADING.name))
        assertEquals(CalibrationPhase.CONFIRM, CalibrationPhase.CONFIRM.next())
    }
    @Test fun numericInputRejectsEmptyNonNumericNonFiniteAndRange() {
        for (value in listOf("", "word", "NaN", "Infinity", "-Infinity", "181", "-181", "1e309")) {
            try { NumericInput.finite(value, -180.0, 180.0); fail(value) }
            catch (_: IllegalArgumentException) { }
        }
        assertEquals(12.5, NumericInput.finite("12,5", -180.0, 180.0), 0.0)
        assertEquals(-180.0, NumericInput.finite("-180", -180.0, 180.0), 0.0)
        try { NumericInput.finite("360", 0.0, 360.0, false); fail() }
        catch (_: IllegalArgumentException) { }
    }
}
