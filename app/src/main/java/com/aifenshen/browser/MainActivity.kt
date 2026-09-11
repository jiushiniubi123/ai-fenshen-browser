// MainActivity.kt — AI 分身浏览器
// 普通 Activity（不引入 AppCompatActivity），100% 原生 Kotlin + 裸 GeckoView（ADR 0003）。
// 流程：GeckoRuntime（应用级一次） → GeckoSession.open → GeckoView.setSession → loadUri(主力网站)。
// 返回键：网页能后退则后退，否则 finish()。

package com.aifenshen.browser

import android.app.Activity
import android.content.Context
import android.os.Bundle
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.GeckoView

class MainActivity : Activity() {

    private lateinit var geckoView: GeckoView
    private lateinit var session: GeckoSession

    // 网页是否可后退：由 NavigationDelegate.onCanGoBack 回调维护。
    private var canGoBack = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        geckoView = findViewById(R.id.geckoView)

        // 应用级一次：进程内只创建一次 GeckoRuntime。
        val runtime = AppRuntime.getOrCreate(applicationContext)

        // 建会话并挂到 GeckoView。
        session = GeckoSession()
        session.open(runtime)
        session.navigationDelegate = object : GeckoSession.NavigationDelegate {
            override fun onCanGoBack(geckoSession: GeckoSession, canGoBack: Boolean) {
                this@MainActivity.canGoBack = canGoBack
            }
        }
        geckoView.setSession(session)

        // 加载主力网站（Z.ai 网页版）。
        session.loadUri("https://chat.z.ai")
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        // 能后退则网页内后退，否则退出当前界面。
        if (canGoBack) {
            session.goBack()
        } else {
            finish()
        }
    }

    /** GeckoRuntime 应用级单例：进程内只创建一次。 */
    private object AppRuntime {
        @Volatile
        private var instance: GeckoRuntime? = null

        fun getOrCreate(context: Context): GeckoRuntime =
            instance ?: synchronized(this) {
                instance ?: GeckoRuntime.create(context.applicationContext)
                    .also { instance = it }
            }
    }
}
