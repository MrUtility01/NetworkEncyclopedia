package com.netenc.app.sync

import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

/**
 * LAN sync — aligned with server/app.py:
 * GET  /api/sync/hello
 * GET  /api/sync/manifest?since=
 * POST /api/sync/pull  { "uids": [] }
 * POST /api/sync/push  { "records": [] }
 * Auth: Authorization Bearer + X-NetEnc-Token
 */
class SyncClient(
    baseUrl: String,
    private val token: String = "",
    private val deviceId: String = "android"
) {
    private val base = baseUrl.trimEnd('/')
    private val client = OkHttpClient.Builder()
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    private fun req(path: String): Request.Builder {
        val b = Request.Builder().url("$base$path")
        if (token.isNotBlank()) {
            b.header("Authorization", "Bearer $token")
            b.header("X-NetEnc-Token", token)
        }
        b.header("X-NetEnc-Device", deviceId)
        b.header("Accept", "application/json")
        return b
    }

    private fun ensureOk(r: okhttp3.Response, body: String): String {
        if (r.code == 401) {
            throw IllegalStateException("unauthorized (401) — توکن Sync را بررسی کنید")
        }
        if (!r.isSuccessful) {
            throw IllegalStateException("HTTP ${r.code}: ${body.take(200)}")
        }
        return body
    }

    fun hello(): String {
        client.newCall(req("/api/sync/hello").get().build()).execute().use { r ->
            val body = r.body?.string() ?: ""
            return ensureOk(r, body)
        }
    }

    fun manifest(since: String? = null): ManifestResponse {
        val q = if (since.isNullOrBlank()) "" else "?since=${java.net.URLEncoder.encode(since, "UTF-8")}"
        client.newCall(req("/api/sync/manifest$q").get().build()).execute().use { r ->
            val body = ensureOk(r, r.body?.string() ?: "{}")
            val o = JSONObject(body)
            val items = mutableListOf<ManifestItem>()
            val arr = o.optJSONArray("items") ?: JSONArray()
            for (i in 0 until arr.length()) {
                val it = arr.getJSONObject(i)
                items.add(
                    ManifestItem(
                        uid = it.getString("uid"),
                        entity = it.optString("entity", "lesson"),
                        last_updated = it.optString("last_updated", null),
                        content_hash = it.optString("content_hash", null),
                        deleted = it.optBoolean("deleted", false)
                    )
                )
            }
            return ManifestResponse(
                schema_version = o.optInt("schema_version", 1),
                generated_at = o.optString("generated_at", null),
                items = items
            )
        }
    }

    fun pull(uids: List<String>): String {
        val json = JSONObject().put("uids", JSONArray(uids))
        val body = json.toString().toRequestBody("application/json".toMediaType())
        client.newCall(req("/api/sync/pull").post(body).build()).execute().use { r ->
            return ensureOk(r, r.body?.string() ?: "{}")
        }
    }

    fun push(recordsJsonArray: JSONArray): String {
        val json = JSONObject().put("records", recordsJsonArray)
        val body = json.toString().toRequestBody("application/json".toMediaType())
        client.newCall(req("/api/sync/push").post(body).build()).execute().use { r ->
            return ensureOk(r, r.body?.string() ?: "{}")
        }
    }
}
