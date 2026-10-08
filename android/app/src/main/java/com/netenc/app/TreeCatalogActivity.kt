package com.netenc.app

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.BaseExpandableListAdapter
import android.widget.EditText
import android.widget.ExpandableListView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.netenc.app.data.AppDatabase
import com.netenc.app.data.LessonEntity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * فهرست درختی: فصل → زیرفصل → درس (مثل ویندوز)
 */
class TreeCatalogActivity : AppCompatActivity() {
    data class SubNode(val title: String, val lessons: List<LessonEntity>)
    data class ChapterNode(val order: Int, val title: String, val subs: List<SubNode>)

    private lateinit var list: ExpandableListView
    private lateinit var header: TextView
    private var tree: List<ChapterNode> = emptyList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val search = EditText(this).apply {
            hint = "جستجو در عناوین و محتوا…"
            setPadding(24, 16, 24, 16)
            textSize = 14f
        }
        header = TextView(this).apply {
            text = "در حال بارگذاری درخت…"
            setPadding(24, 12, 24, 8)
            textSize = 13f
        }
        list = ExpandableListView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutDirection = View.LAYOUT_DIRECTION_RTL
            addView(search)
            addView(header)
            addView(list, LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f
            ))
        }
        setContentView(root)

        search.setOnEditorActionListener { _, _, _ ->
            val q = search.text.toString().trim()
            if (q.isNotBlank()) {
                startActivity(
                    Intent(this, SearchActivity::class.java).putExtra("q", q)
                )
            }
            true
        }

        lifecycleScope.launch { loadTree() }
    }

    private suspend fun loadTree() {
        val lessons = withContext(Dispatchers.IO) {
            AppDatabase.get(this@TreeCatalogActivity).lessonDao().allActive()
        }
        val byChapter = lessons.groupBy { it.chapterOrder to it.chapterTitle }
            .toSortedMap(compareBy { it.first })
        tree = byChapter.map { (key, list) ->
            val (order, title) = key
            val subs = list.groupBy { it.subTitle.ifBlank { "عمومی" } }
                .map { (st, ls) -> SubNode(st, ls.sortedBy { it.lessonOrder }) }
            ChapterNode(order, title.ifBlank { "فصل $order" }, subs)
        }
        header.text = "${tree.size} فصل · ${lessons.size} درس — برای باز کردن لمس کنید"
        list.setAdapter(TreeAdapter(tree))
        list.setOnChildClickListener { _, _, groupPos, childPos, _ ->
            // child is subchapter header index mixed — we use nested structure differently
            false
        }
    }

    private inner class TreeAdapter(
        private val data: List<ChapterNode>
    ) : BaseExpandableListAdapter() {

        // سطح ۱: فصل‌ها — سطح ۲: ترکیب زیرفصل+درس به‌صورت خطوط
        private fun flatChildren(ch: ChapterNode): List<Pair<String, LessonEntity?>> {
            val out = mutableListOf<Pair<String, LessonEntity?>>()
            for (sub in ch.subs) {
                out.add("▸ ${sub.title}" to null)
                for (les in sub.lessons) {
                    val mark = if (les.fullContent.length > 80) "✓" else "○"
                    out.add("    $mark ${les.titleFa}" to les)
                }
            }
            return out
        }

        override fun getGroupCount() = data.size
        override fun getChildrenCount(g: Int) = flatChildren(data[g]).size
        override fun getGroup(g: Int) = data[g]
        override fun getChild(g: Int, c: Int) = flatChildren(data[g])[c]
        override fun getGroupId(g: Int) = g.toLong()
        override fun getChildId(g: Int, c: Int) = (g * 10000 + c).toLong()
        override fun hasStableIds() = true

        override fun getGroupView(g: Int, expanded: Boolean, convert: View?, parent: ViewGroup?): View {
            val tv = (convert as? TextView) ?: TextView(this@TreeCatalogActivity).apply {
                setPadding(28, 22, 28, 22)
                textSize = 15f
                setBackgroundColor(0xFF1A2332.toInt())
                setTextColor(0xFFE7ECF3.toInt())
            }
            val ch = data[g]
            val arrow = if (expanded) "▼" else "▶"
            val n = ch.subs.sumOf { it.lessons.size }
            tv.text = "$arrow ${ch.order}. ${ch.title}  ($n)"
            return tv
        }

        override fun getChildView(g: Int, c: Int, last: Boolean, convert: View?, parent: ViewGroup?): View {
            val tv = (convert as? TextView) ?: TextView(this@TreeCatalogActivity).apply {
                setPadding(36, 14, 36, 14)
                textSize = 13f
                setTextColor(0xFFC9D4E5.toInt())
            }
            val (label, les) = flatChildren(data[g])[c]
            tv.text = label
            tv.setBackgroundColor(if (les == null) 0xFF121820.toInt() else 0xFF0F1419.toInt())
            tv.setOnClickListener {
                if (les != null) {
                    startActivity(
                        Intent(this@TreeCatalogActivity, LessonDetailActivity::class.java)
                            .putExtra("uid", les.uid)
                    )
                }
            }
            return tv
        }

        override fun isChildSelectable(g: Int, c: Int) = true
    }
}
