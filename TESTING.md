# Validation report — historical test artifact

Release v0.1.0 uses the same executable patch code as the tested artifact below; only the version comment changed. The SHA256 below identifies the original tested file, not the renamed release. No additional engine runs are claimed for this documentation/version-label update.

Date: 2026-11-17. Platform: Windows. Status: preview, not universal compatibility certification.

## Exact tested artifact

`game/zzzz_wheel_dialogue.rpy`

SHA256: `3AB733298C8AE36AD6E1CBAA232ADCB56C645FCFD6A35158078E7135C94EDED0`

## Actual engine integration matrix

Both runs used an original isolated synthetic ADV project and independent save directories, not the original commercial games. The engines were launched and received raw pygame mouse down/up events (buttons 4 and 5), and keyboard events for manual choices. This is actual engine event processing, **not operating-system physical wheel automation**.

| Scenario | Ren'Py 7.4.11.2266 / Python 2 | Ren'Py 8.1.3.23091805 / Python 3 |
|---|---|---|
| Final artifact loads | Pass | Pass |
| Slow text: first wheel completes, next advances | Pass | Pass |
| Three consecutive dialogue lines | Pass | Pass |
| Extra wheel at standard menu does not select | Pass | Pass |
| Select A, wheel up returns to menu | Pass | Pass |
| Wheel down at returned menu does not replay A | Pass | Pass |
| Manually select B instead | Pass | Pass |

Final run observed sequence on both engines:

```text
LINE ONE -> wheel5 -> wheel5 -> LINE TWO
LINE TWO -> wheel5 -> wheel5 -> LINE THREE
LINE THREE -> wheel5 -> wheel5 -> MENU ENTER
wheel5 -> (still menu)
manual keyboard selection -> BRANCH A
wheel4 -> MENU ENTER
wheel5 -> (still menu)
manual keyboard selection -> BRANCH B
```

The project also has 8 passing Python mock unit tests. These cover gates, original input, list-shadowing regression, repeated initialization, binding identity restoration, legacy widget lookup and unknown-text handling. Mock tests do not substitute for engine tests. GitHub Actions configuration is included; a hosted Actions run has not yet occurred.

## Defects discovered and fixed during testing

1. Global `dismiss` interception affected callers other than dialogue, including DismissBehavior. Replaced with a temporary SayBehavior instance binding.
2. Ren'Py store `list` shadowing made a native list fail an isinstance check. Removed the assumption and added regression coverage.
3. Restricting the binding to SayBehavior initially skipped unfinished slow text. Added verified `say/what` Text completion via its native event handling before advancement. Re-tested the final artifact on both engine versions above.

## Not validated

- OS-level physical mouse wheel, touchpad momentum and device-specific input.
- macOS, Linux, Android, Web and all other Ren'Py versions.
- Complete original commercial game playthroughs.
- Save/load round trips, restart/reload longevity, wrapper chains with other mods.
- NVL, custom screens, custom menu layers, QTE, timed choices and minigames.
- Viewport scrolling, arbitrary modal overlays, history screen interactions.
- Auto-forward, skipping, accessibility, non-abortable text tags and unusual slow-text callbacks.

The desktop automation tool's private-file DACL integrity check blocked OS-level automation in this session. No ACL change was made for that tool. Raw engine input tests were used instead and are labelled as such.

## Release gate

This artifact can be shared as an **alpha preview** with this matrix and these limitations. Broader stable claims require more engines, real desktop input, fixture expansion and community game reports. Do not describe it as working with every Ren'Py game. Do not ship third-party engine files, game assets, saves or private logs.
