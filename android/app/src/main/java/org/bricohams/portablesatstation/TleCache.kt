package org.bricohams.portablesatstation

import android.content.Context
import java.io.File
import java.io.FileOutputStream
import java.nio.file.Files
import java.nio.file.StandardCopyOption

/** Download failures never replace the last validated, app-private catalogue. */
class TleCache(private val directory: File) {
    constructor(context: Context) : this(context.filesDir)
    private val file = File(directory, "validated-tle.txt")
    @Synchronized fun load(): TleCatalogue? {
        if (!file.exists()) return null
        return file.inputStream().use { TleCatalogue.parse(TleDownload.readBounded(it, -1)) }
    }
    @Synchronized fun save(value: TleCatalogue) {
        val validated = TleCatalogue.parse(value.bytes)
        val staging = File(directory, "validated-tle.new")
        try {
            FileOutputStream(staging).use { output -> output.write(validated.bytes); output.fd.sync() }
            // Never fall back to a delete-first or non-atomic replacement if the filesystem refuses.
            Files.move(staging.toPath(), file.toPath(), StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING)
        } finally { Files.deleteIfExists(staging.toPath()) }
    }
}
