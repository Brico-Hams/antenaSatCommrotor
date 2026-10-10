package org.bricohams.portablesatstation

enum class CalibrationPhase(val step: Int) {
    CHECK_AND_HOME(1), LEVEL_AND_ZERO(2), TRUE_HEADING(3), CONFIRM(4);
    fun next(): CalibrationPhase = entries[minOf(ordinal + 1, entries.lastIndex)]
    companion object {
        fun restore(name: String?): CalibrationPhase =
            entries.firstOrNull { it.name == name } ?: CHECK_AND_HOME
    }
}

object NumericInput {
    fun finite(text: String, minimum: Double, maximum: Double, maximumInclusive: Boolean = true): Double {
        val value = text.trim().replace(',', '.').toDoubleOrNull()
            ?: throw IllegalArgumentException("invalid_number")
        require(value.isFinite() && value >= minimum &&
            (if (maximumInclusive) value <= maximum else value < maximum)) { "invalid_number" }
        return value
    }
}
