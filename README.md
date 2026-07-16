# Trace for Blog (SystraceForBlog)

[简体中文](README.zh-CN.md)

Perfetto, legacy Systrace HTML, and ART method-trace case files used by
[Android Performance](https://www.androidperformance.com/) articles. The legacy
repository name is preserved because published articles link to its directories.

<!-- android-performance-ecosystem:start -->
## Android performance ecosystem

The [Android Performance Ecosystem](https://github.com/Gracker/android-performance-ecosystem) brings its navigation Hub and seven core projects into an optional path from instrumentation and capture to analysis, system knowledge, and reproducible cases.

| Stage | Project | Purpose | Address |
| --- | --- | --- | --- |
| Navigate | [Android Performance Ecosystem](https://github.com/Gracker/android-performance-ecosystem) | Maintain the shared project map, handoff metadata, generated README navigation, and drift checks. | [GitHub](https://github.com/Gracker/android-performance-ecosystem) |
| Instrument | [TraceFix](https://github.com/Gracker/TraceFix) | Inject app-side android.os.Trace sections at build time so method work is visible at runtime. | [GitHub](https://github.com/Gracker/TraceFix) |
| Capture and measure | [Perfetto Tools](https://github.com/Gracker/perfetto-tools) | Capture repeatable Perfetto traces and collect FPS or Simpleperf measurements. | [GitHub](https://github.com/Gracker/perfetto-tools) |
| Analyze | [SmartPerfetto](https://github.com/Gracker/SmartPerfetto) | Investigate traces with an AI-assisted Web UI, CLI, reports, sessions, comparisons, and evidence workflow. | [GitHub](https://github.com/Gracker/SmartPerfetto) |
| Agent analysis | [Perfetto Skills](https://github.com/Gracker/Perfetto-Skills) | Give agents a portable Perfetto analysis Skill for Android, Linux, and Chromium, with selected assets synchronized through pinned workflows. | [GitHub](https://github.com/Gracker/Perfetto-Skills) |
| Learn | [Android Performance Blog](https://github.com/Gracker/Gracker.github.io) | Teach Perfetto and Systrace analysis through articles, system explanations, and case studies. | [AndroidPerformance.com](https://www.androidperformance.com/) · [GitHub](https://github.com/Gracker/Gracker.github.io) |
| System knowledge | Android Internal Wiki | An alpha knowledge base for Android mechanisms from App to Framework, Native, and Kernel. | **Coming soon** |
| Reproduce | [Trace for Blog (SystraceForBlog)](https://github.com/Gracker/SystraceForBlog) | Provide the Perfetto, Systrace, and related case files used by articles for hands-on reproduction. | [GitHub](https://github.com/Gracker/SystraceForBlog) |
<!-- android-performance-ecosystem:end -->

## Case catalog

[`catalog.json`](catalog.json) is the machine-readable inventory. It covers all
15 existing artifacts with byte size, SHA-256, content format, packaging,
article mapping, provenance, license/consent state, and privacy/sanitization
review state.

| Case ID | Area | Artifacts | Related article |
| --- | --- | --- | --- |
| `perfetto-aosp-demo-scroll` | Scrolling / rendering | 1 Perfetto protobuf | [MainThread and RenderThread](https://www.androidperformance.com/2025/08/02/Android-Perfetto-07-MainThread-And-RenderThread/) |
| `perfetto-wechat-moments-jank` | Scrolling jank | Perfetto protobuf + ZIP copy | Not recorded |
| `systrace-main-render-wangzhe` | MainThread / RenderThread | Systrace HTML ZIP + ART method trace | [Article](https://www.androidperformance.com/2019/11/06/Android-Systrace-MainThread-And-RenderThread/) |
| `systrace-main-render-flutter-wanandroid` | Flutter rendering | Systrace HTML ZIP + ART method trace | [Article](https://www.androidperformance.com/2019/11/06/Android-Systrace-MainThread-And-RenderThread/) |
| `systrace-binder-app-launch` | Binder | 1 Systrace HTML ZIP | [Article](https://www.androidperformance.com/2019/12/06/Android-Systrace-Binder/) |
| `systrace-input-launcher-scroll` | Input | 1 Systrace HTML ZIP | [Article](https://www.androidperformance.com/2019/11/04/Android-Systrace-Input/) |
| `systrace-input-list-jank` | Input / jank | 1 Systrace HTML ZIP | [Article](https://www.androidperformance.com/2019/11/04/Android-Systrace-Input/) |
| `systrace-smooth-launchers` | Scrolling smoothness | 3 Systrace HTML ZIPs | [Series](https://www.androidperformance.com/2021/04/24/android-systrace-smooth-in-action-1/) |
| `systrace-twitter-jank` | Scrolling jank | 1 Systrace HTML ZIP | Not recorded |
| `systrace-triple-buffer` | Buffering / rendering | 1 ZIP containing 5 Systrace HTML files | [Article](https://www.androidperformance.com/2019/12/15/Android-Systrace-Triple-Buffer/) |

## Use a case

Analyze a Perfetto protobuf with SmartPerfetto:

```bash
smp run "Android_Perfetto/demo_app_aosp_scroll.perfetto-trace" "Analyze scrolling jank"
```

Or ask an agent with Perfetto Skills to use
`$perfetto-performance-analysis` on the same file. Legacy `*.html.zip` files are
self-contained Systrace pages: inspect the archive first, extract locally, then
open the HTML in a browser. ART `*.trace` files are method traces, not Perfetto
protobufs.

## Data boundary

All current artifacts are historical. Their original license, consent, privacy
review, or sanitization record was not preserved, so the catalog deliberately
uses `null` and `pending`. Public visibility does not create a blanket data
license. Read [DATA_POLICY.md](DATA_POLICY.md) before using or contributing data.
`LICENSE-CODE` covers only original documentation and validation code, not the
trace/archive artifacts or linked articles.

## Verify

```bash
python3 scripts/validate_catalog.py
python3 -m unittest discover -s tests -v
git diff --check
```

The validator checks inventory completeness, hashes, sizes, required provenance
fields, safe relative paths, ZIP member paths, encryption, decompressed size,
member count, and compression ratio without extracting archives to disk.
