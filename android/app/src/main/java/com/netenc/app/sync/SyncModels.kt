package com.netenc.app.sync

data class HelloResponse(
    val ok: Boolean = false,
    val schema_version: Int = 1,
    val device_id: String = "",
    val lan_ip: String = "",
    val stats: Map<String, Any?> = emptyMap()
)

data class ManifestItem(
    val uid: String,
    val entity: String = "lesson",
    val last_updated: String? = null,
    val content_hash: String? = null,
    val deleted: Boolean = false
)

data class ManifestResponse(
    val schema_version: Int = 1,
    val generated_at: String? = null,
    val items: List<ManifestItem> = emptyList()
)

data class PullRequest(val uids: List<String>)

data class PushResponse(
    val applied: List<String> = emptyList(),
    val rejected: List<Map<String, Any?>> = emptyList(),
    val conflicts: List<Map<String, Any?>> = emptyList(),
    val server_time: String? = null
)
