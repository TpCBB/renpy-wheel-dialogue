<h1 align="center">Ren’Py 视觉小说滚轮对话补丁</h1>

<p align="center"><strong>滚轮看剧情，选项自己选。</strong></p>

<p align="center">上滚回看，下滚继续。遇到选项停下，回退后也不自动重选。</p>

<p align="center">
  <img src="https://img.shields.io/badge/release-v0.1.0-blue" alt="release v0.1.0">
  <img src="https://img.shields.io/badge/engine-Ren'Py-orange" alt="Ren'Py">
  <img src="https://img.shields.io/badge/install-单文件-green" alt="单文件安装">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license"></a>
</p>

<p align="center">
  <strong><a href="https://github.com/TpCBB/renpy-wheel-dialogue/releases/latest">下载补丁 ↗</a></strong> ·
  <a href="#使用方法">使用方法</a> ·
  <a href="#功能">功能介绍</a> ·
  <a href="CHANGELOG.md">更新记录</a>
</p>

<p align="center">简体中文 · <a href="https://github.com/TpCBB/renpy-wheel-dialogue/blob/main/README.en.md?plain=0">English</a></p>

---

## 使用方法

1. 下载并解压补丁。
2. 将 `zzzz_wheel_dialogue.rpy` 放进游戏的 `game` 文件夹。
3. 启动游戏，即可使用。

```text
游戏目录/
├── 游戏启动程序
└── game/
    └── zzzz_wheel_dialogue.rpy   ← 放在这里
```

## 功能

| 操作 | 效果 |
| --- | --- |
| 滚轮向上 | 回退对话 |
| 滚轮向下 | 推进对话；文字未显示完时先补全 |
| 遇到选项 | 停下等待手动选择，不自动重选旧选项 |

## 卸载

退出游戏，删除 `game` 文件夹里的 `zzzz_wheel_dialogue.rpy` 和同名 `.rpyc` 文件即可。

> 部分自定义界面需单独适配；回退遵循游戏原有设置。建议先备份存档，避免同时安装多个滚轮补丁。

<details>
<summary>给 AI 的适配提示词</summary>

```text
请检查当前游戏并适配本滚轮补丁：上滚沿用原生回退，下滚推进普通对话；
逐字文本先补全，遇到选项停下，回退后不自动重选。
先检查引擎、已有插件和自定义界面，不要全局修改 dismiss 或按钮选择。
保留存档和原有键位，采用可卸载的独立扩展。
在隔离项目中实测：连续对话、慢文本、选 A 后回退、下滚停住、改选 B。
明确说明已测和未测场景，不要承诺所有游戏通用。
详细经验请参考 MAINTAINER-NOTES.md 与 TESTING.md。
```

</details>

[MIT 许可证](LICENSE) · [测试记录](TESTING.md) · [维护说明](MAINTAINER-NOTES.md)
