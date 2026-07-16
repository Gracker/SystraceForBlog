# Trace for Blog (SystraceForBlog)

[English](README.md)

本仓库保存 [Android Performance](https://www.androidperformance.com/) 文章使用的
Perfetto、旧版 Systrace HTML 和 ART method trace 案例。历史文章已经大量引用原仓库名和
目录，因此继续保留 `SystraceForBlog` 名称，对外展示为 Trace for Blog。

<!-- android-performance-ecosystem:start -->
## Android 性能分析生态

[Android Performance Ecosystem](https://github.com/Gracker/android-performance-ecosystem) 通过导航 Hub 与七个核心项目，把可选插桩、采集、分析、系统知识与可复现案例连接成一套完整路径。

| 阶段 | 项目 | 作用 | 地址 |
| --- | --- | --- | --- |
| 导航 | [Android Performance Ecosystem](https://github.com/Gracker/android-performance-ecosystem) | 维护统一项目地图、交接元数据、README 导航区块与漂移检查。 | [GitHub](https://github.com/Gracker/android-performance-ecosystem) |
| 插桩 | [TraceFix](https://github.com/Gracker/TraceFix) | 在编译期注入 App 侧 android.os.Trace section，让方法执行在运行时 Trace 中可见。 | [GitHub](https://github.com/Gracker/TraceFix) |
| 采集与测量 | [Perfetto Tools](https://github.com/Gracker/perfetto-tools) | 抓取可复现的 Perfetto Trace，并采集 FPS 或 Simpleperf 测量结果。 | [GitHub](https://github.com/Gracker/perfetto-tools) |
| 分析 | [SmartPerfetto](https://github.com/Gracker/SmartPerfetto) | 通过 AI 辅助 Web UI、CLI、报告、会话、对比和证据工作流分析 Trace。 | [GitHub](https://github.com/Gracker/SmartPerfetto) |
| Agent 分析 | [Perfetto Skills](https://github.com/Gracker/Perfetto-Skills) | 为 Agent 提供可移植的 Android、Linux、Chromium Perfetto 分析 Skill，并通过固定版本流程同步选定资产。 | [GitHub](https://github.com/Gracker/Perfetto-Skills) |
| 学习 | [Android Performance Blog](https://github.com/Gracker/Gracker.github.io) | 通过文章、系统原理和案例复盘讲解 Perfetto 与 Systrace 分析。 | [AndroidPerformance.com](https://www.androidperformance.com/) · [GitHub](https://github.com/Gracker/Gracker.github.io) |
| 系统知识 | Android Internal Wiki | 处于 alpha 阶段的 Android 系统知识库，覆盖 App、Framework、Native 与 Kernel 机制。 | **Coming soon** |
| 复现 | [Trace for Blog (SystraceForBlog)](https://github.com/Gracker/SystraceForBlog) | 提供文章使用的 Perfetto、Systrace 及相关案例文件，支持动手复现。 | [GitHub](https://github.com/Gracker/SystraceForBlog) |
<!-- android-performance-ecosystem:end -->

## 案例目录

[`catalog.json`](catalog.json) 是机器可读的事实源。它覆盖现有 15 个 artifact，记录
字节大小、SHA-256、内容格式、打包方式、文章映射、来源、授权/同意状态，以及隐私和
脱敏审核状态。

| Case ID | 领域 | 文件 | 对应文章 |
| --- | --- | --- | --- |
| `perfetto-aosp-demo-scroll` | 滑动 / 渲染 | 1 个 Perfetto protobuf | [MainThread 和 RenderThread](https://www.androidperformance.com/2025/08/02/Android-Perfetto-07-MainThread-And-RenderThread/) |
| `perfetto-wechat-moments-jank` | 滑动卡顿 | Perfetto protobuf + ZIP 副本 | 未记录 |
| `systrace-main-render-wangzhe` | 主线程 / 渲染线程 | Systrace HTML ZIP + ART method trace | [文章](https://www.androidperformance.com/2019/11/06/Android-Systrace-MainThread-And-RenderThread/) |
| `systrace-main-render-flutter-wanandroid` | Flutter 渲染 | Systrace HTML ZIP + ART method trace | [文章](https://www.androidperformance.com/2019/11/06/Android-Systrace-MainThread-And-RenderThread/) |
| `systrace-binder-app-launch` | Binder | 1 个 Systrace HTML ZIP | [文章](https://www.androidperformance.com/2019/12/06/Android-Systrace-Binder/) |
| `systrace-input-launcher-scroll` | Input | 1 个 Systrace HTML ZIP | [文章](https://www.androidperformance.com/2019/11/04/Android-Systrace-Input/) |
| `systrace-input-list-jank` | Input / 卡顿 | 1 个 Systrace HTML ZIP | [文章](https://www.androidperformance.com/2019/11/04/Android-Systrace-Input/) |
| `systrace-smooth-launchers` | 滑动流畅度 | 3 个 Systrace HTML ZIP | [系列文章](https://www.androidperformance.com/2021/04/24/android-systrace-smooth-in-action-1/) |
| `systrace-twitter-jank` | 滑动卡顿 | 1 个 Systrace HTML ZIP | 未记录 |
| `systrace-triple-buffer` | Buffer / 渲染 | 1 个 ZIP，内含 5 个 Systrace HTML | [文章](https://www.androidperformance.com/2019/12/15/Android-Systrace-Triple-Buffer/) |

## 使用案例

用 SmartPerfetto 分析 Perfetto protobuf：

```bash
smp run "Android_Perfetto/demo_app_aosp_scroll.perfetto-trace" "分析滑动卡顿"
```

也可以让安装了 Perfetto Skills 的 Agent 对同一文件使用
`$perfetto-performance-analysis`。旧版 `*.html.zip` 是自包含 Systrace 页面：先检查
压缩包，再在本机解压并用浏览器打开 HTML。ART `*.trace` 是 method trace，不是
Perfetto protobuf。

## 数据边界

当前文件都是历史资产，原始许可证、发布同意、隐私审核和脱敏记录没有完整保留下来，
所以清单明确使用 `null` 与 `pending`，不会为了“看起来完整”伪造元数据。仓库公开不等于
获得统一的数据许可证。使用或贡献前请读 [DATA_POLICY.md](DATA_POLICY.md)。
`LICENSE-CODE` 只覆盖本仓新增文档和校验代码，不覆盖 Trace、压缩包或链接文章。

## 验证

```bash
python3 scripts/validate_catalog.py
python3 -m unittest discover -s tests -v
git diff --check
```

校验器会检查目录覆盖、哈希、大小、来源必填字段、安全相对路径、ZIP member 路径、加密、
解压总量、member 数量和压缩比，并且不会把压缩包解压到磁盘。
