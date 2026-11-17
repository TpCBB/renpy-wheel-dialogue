<h1 align="center">Ren’Py Visual Novel Dialogue Wheel Patch</h1>

<p align="center"><strong>Scroll through the story. Make your own choices.</strong></p>

<p align="center">Scroll up to go back, down to continue. Stop at choices without replaying previous selections.</p>

<p align="center">
  <img src="https://img.shields.io/badge/release-v0.1.0-blue" alt="release v0.1.0">
  <img src="https://img.shields.io/badge/engine-Ren'Py-orange" alt="Ren'Py">
  <img src="https://img.shields.io/badge/install-single_file-green" alt="Single-file installation">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license"></a>
</p>

<p align="center">
  <strong><a href="https://github.com/TpCBB/renpy-wheel-dialogue/releases/latest">Download ↗</a></strong> ·
  <a href="#installation">Installation</a> ·
  <a href="#features">Features</a> ·
  <a href="https://github.com/TpCBB/renpy-wheel-dialogue/releases">Releases</a>
</p>

<p align="center"><a href="https://github.com/TpCBB/renpy-wheel-dialogue/blob/main/README.md?plain=0">简体中文</a> · English</p>

---

## Installation

1. Download and extract the patch.
2. Copy `zzzz_wheel_dialogue.rpy` into your game's `game` folder.
3. Launch the game and start scrolling.

```text
Your game/
├── Game executable
└── game/
    └── zzzz_wheel_dialogue.rpy   ← Put it here
```

## Features

| Input | Action |
| --- | --- |
| Scroll up | Roll back dialogue |
| Scroll down | Advance dialogue; reveal unfinished text first |
| At a choice | Wait for manual selection, without replaying the previous choice |

## Uninstall

Close the game, then delete `zzzz_wheel_dialogue.rpy` and its matching `.rpyc` file from the `game` folder.

> Some custom interfaces need adaptation. Rollback follows the game's existing restrictions. Back up your saves first and avoid installing multiple wheel patches together.

<details>
<summary>AI adaptation prompt</summary>

```text
Inspect the current game and adapt this wheel patch: scroll up uses native
rollback; scroll down advances ordinary dialogue. Reveal unfinished text first,
stop at choices, and never replay an old choice through wheel-down input.
Inspect the engine, existing mods and custom screens before changing anything.
Do not globally modify dismiss or button selection. Preserve saves and existing
key bindings; use an independent, removable extension.
Test in isolation: consecutive dialogue, slow text, choose A, roll back,
scroll down without selecting, then manually choose B.
Distinguish tested and untested scenarios. Do not promise universal compatibility.
See MAINTAINER-NOTES.md (Chinese) and TESTING.md for implementation notes.
```

</details>

[MIT License](LICENSE) · [Test report](TESTING.md) · [Maintainer notes (Chinese)](MAINTAINER-NOTES.md)
