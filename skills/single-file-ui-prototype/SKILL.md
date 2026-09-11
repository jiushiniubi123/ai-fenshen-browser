---
name: single-file-ui-prototype
description: 当被原型化的界面不属于任何 web 项目（游戏 mod 的 XML/Lua UI、桌面应用、无框架仓库）时，用一个自包含 HTML 文件做出几个结构不同的 UI 方案供用户对比。适用于用户说"优化这个界面""再来几款方案""这几个都不行"，或需要在预览面板里比较布局差异时。
agent_created: true
---

# 单文件 UI 原型

`prototype` skill 的 UI 分支假设存在一个 web 项目（有 route、有 task runner）。
当被评估的界面根本不在浏览器里跑——例如文明6 mod 的 `SBR_ChoosePopup.xml`——那套流程不适用。
本 skill 覆盖这种情况：**用一个自包含 HTML 文件把界面画出来**，让用户在预览面板里切换对比。

HTML 只是**载体**，不是交付物。交付物是"选定的方案"，之后再按目标平台（XML/Lua、Qt、原生控件）
重新实现。原型里的代码不能直接上线。

## 先确认是这一支

- 被原型化的界面有真实的宿主平台，且不是 web → 用本 skill。
- 有 web 项目、有现成 route → 用 `prototype` 的 UI 分支（sub-shape A）。
- 问题是"这段逻辑/状态机对不对"而不是"长什么样" → 用 `prototype` 的 LOGIC 分支。

## 最容易踩的坑：让容器宽度决定折叠

第一版原型把响应式规则写成 media query。结果用户在窄预览面板里看，
三个方案**全部折叠成单列列表**，结构差异完全消失，反馈是"都不行"。

正确做法：

- 弹窗/面板**始终按原始尺寸布局**（例如 880×720），再用 `transform:scale()` 整体缩放适配预览区。
  缩放不改变布局，各方案的结构差异在任何面板宽度下都可见。
- 响应式折叠规则写成 **class 驱动**（`.popup.narrow .a-grid{...}`）而不是 media query，
  再用一个开关按钮手动触发，用来演示窄屏行为。media query 会跟着预览面板宽度跑，不可控。

缩放适配的实现要点：

```js
const s = Math.min(1, (vp.clientWidth - 6) / W, (vp.clientHeight - 6) / H);
wrapper.style.width  = (W * s) + 'px';   // 外层占位盒收缩到视觉尺寸
wrapper.style.height = (H * s) + 'px';
panel.style.transform = 'scale(' + s + ')';
panel.style.transformOrigin = 'top left';
```

外层 `position:relative`，面板 `position:absolute;top:0;left:0`。
缩放后要重算的场景：`resize`、`load`、以及 `requestAnimationFrame` 补一次首帧。

注意：如果给面板加了入场动画，**不要让 keyframes 动 `transform`**，否则会覆盖掉缩放。

## 变体怎么才算"结构不同"

颜色、文案、间距的差别是 tweak，不是变体。真正的变体在**布局 / 信息层级 / 主操作位置**上互相不同意。
下面这组差异是够用的（同一份数据、同一套功能）：

| 轴 | 例子 |
|---|---|
| 列表形态 | 双列卡片网格 / 单列密集行 / 数据表 / 手风琴 |
| 空间隐喻 | 纵向滚动列表 / 横向时间轴 / 分页卡组 |
| 主操作位置 | 通栏横幅 / 侧栏卡片 / 页脚内联 / 独立卡片 |
| 详情呈现 | 悬停 tooltip / 行内展开 / 固定详情条 |
| 交互模型 | 点选 / 键盘优先命令面板 / 翻页浏览 |

两三个变体挤在同一个轴上就是 wallpaper。起草时明确要求自己"这一版不许用网格"之类。

## 正交开关比堆更多变体省事

当用户说"都不行"而没说原因时，与其再加四个布局，不如先加两个**与布局正交**的开关：

- **配色**：靠 CSS 变量整套切换（`.theme-light` 覆盖 `:root` 的变量），一份标记两套皮肤。
  所有颜色都必须走 `var(--x)`，包括被强调文字（用 `--strong` 而不是直接写 `#fff`），
  否则浅色皮肤下会出现白字压浅底。
- **视口宽度**：宽屏 / 窄屏，用来演示响应式折叠。

这两个开关能让可见差异翻倍，成本远低于再写一个布局。

## 无头校验（写完先跑，别让用户替你发现崩了）

单文件 HTML 没法直接单测，但可以：

```js
const src = html.match(/<script>([\s\S]*?)<\/script>/)[1];
// stub 掉 document / location / history / window / setTimeout / requestAnimationFrame
const fns = new Function(src + '; return {VariantA,VariantB,VariantC};')();
for (const k of ['A','B','C']) {
  const h = fns['Variant' + k]();
  assert(!/undefined|NaN/.test(h), k + ' 渲染有 undefined/NaN');
}
```

要点：把 render 函数写成**纯字符串构造函数**，所有碰 DOM 的代码放进 `init()`，
并用 `if (typeof document !== 'undefined')` 包住。这样 Node 里 `new Function` 能直接跑，
不用手写一堆 stub。

再顺手用正则比对 CSS 里 `var(--x)` 的引用和 `--x:` 的定义是否配对——浅色皮肤最容易在这里漏。
顺手加一条：正则扫 `:[^;{}]*#[0-9a-fA-F]{3,8}`，把 var() 之外的写死颜色列出来。
列出的应该只有变量定义本身 + 原型外壳；如果出现在被评估的样式里，主题切换时它不会变，要改掉。

## 无头校验抓不到布局 bug —— 必须截图看

上面那套只能证明"没崩"，证明不了"能看"。真实翻车案例：`.btn.wide{flex:1}`
在横向 footer 里是均分宽度，在纵向详情面板里就变成**竖向拉伸**，按钮撑成一百多像素高。
JS 校验一路 ok，只有截图能看出来。

用系统自带的浏览器截，不要装 puppeteer：

```bash
# Windows：Edge 必定存在，不必找 Chrome
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
"$EDGE" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1220,1010 \
  --virtual-time-budget=3000 --screenshot="/abs/out.png" \
  "file:///abs/proto.html?variant=B&theme=night&scene=tech"
```

- `--virtual-time-budget=3000` 给 JS 和 `requestAnimationFrame` 留出跑完的时间，否则截到空页。
- 每个变体 × 每个关键场景都截，然后**真的去看图**。典型翻车：纵向 flex 里的 `flex:1`、
  变宽名称把后一列推歪、隐藏一列后剩下的内容悬在中间、计数标签和实际条数对不上。
- 截完删掉临时图，别留在交付目录里。

## 正交开关也要走 URL

只让 `?variant=` 进 URL 是不够的。皮肤/视口/场景这些正交开关如果不进 URL，
你就**没法截某个特定组合来自查**，用户也没法把"B 方案 + 羊皮纸 + 窄屏"这个组合发给别人。
把全部 state 都写进 `replaceState`，启动时从 search 里全部读回：

```js
history.replaceState(null,'','?variant='+s.v+'&theme='+s.theme+'&scene='+s.scene
  +(s.narrow?'&narrow=1':''));
```

## 一次只改一处

这份文件很长，改的时候**不要在一个批次里发多个 Edit**——后面的写入会覆盖前面的，
表现为"工具说成功了但文件里没变"。改完 `grep` 一下确认落盘，再发下一个 Edit。
排查时先 `grep` 而不是重读整份文件。

## 收尾

- 文件命名和文件顶部注释都标明是 prototype，写清楚它回答什么问题、有哪些变体、为什么这样切。
- 文件放在被原型化的模块旁边，但**不要**加进构建清单 / modinfo 的 `Files` 段。
  例外：如果那个模块目录本身就是**会被打包分发**的东西（mod 文件夹、要 zip 的插件目录），
  别把原型写进去——用户下次压缩就会把它一起发出去。放到工作目录，在回复里给出路径。
- 胜出方案按目标平台语法重新实现后，原型文件进 throwaway 分支，main 只留验证过的结论。
