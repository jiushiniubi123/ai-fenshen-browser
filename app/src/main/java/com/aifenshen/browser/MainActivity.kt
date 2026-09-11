package com.aifenshen.browser

import android.app.Activity
import android.os.Bundle
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoView

/**
 * AI 分身浏览器 —— 空壳 App（issue #3：跑通 GeckoView 内核）。
 *
 * 100% 原生 Kotlin + 裸 GeckoView（ADR 0003）：不引入跨端框架、不封装多余抽象层。
 * 打开 App 直接加载主力网站（Z.ai 网页版）。
 * 分身管理、侧边栏、电脑版模式属于后续 issue，本工程只打地基。
 */
class MainActivity : Activity() {

    private lateinit var geckoView: GeckoView
    private lateinit var session: GeckoSession

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        geckoView = findViewById<GeckoView>(R.id.gecko_view)

        // GeckoRuntime：应用级单例，进程内只创建一次，所有 GeckoSession 共享；
        // 后续 issue 的分身隔离（ADR 0004 会话 contextId）也建立在它之上。
        val geckoRuntime = runtime ?: GeckoRuntime.create(applicationContext).also { runtime = it }

        session = GeckoSession()
        session.open(geckoRuntime)
        geckoView.setSession(session)

        // 主力网站（Z.ai 网页版）
        session.loadUri(PRIMARY_SITE_URL)
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        if (session.canGoBack) {
            session.goBack()
        } else {
            finish()
        }
    }

    override fun onDestroy() {
        if (this::session.isInitialized) {
            if (this::geckoView.isInitialized) {
                geckoView.releaseSession(session)
            }
            session.close()
        }
        super.onDestroy()
    }

    companion object {
        /** 主力网站（Z.ai 网页版），本空壳版本打开 App 即加载它 */
        private const val PRIMARY_SITE_URL = "https://chat.z.ai"

        /** 应用级共享的 Gecko 运行时，进程内只创建一次 */
        private var runtime: GeckoRuntime? = null
    }
}
