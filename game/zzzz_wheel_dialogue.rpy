# Wheel Dialogue 0.1.0 -- SPDX-License-Identifier: MIT
# Independent extension; see README.md for compatibility and removal.
init 999 python:
    import renpy.display.behavior as _ygwd_behavior

    config.keymap['rollforward'] = [
        k for k in config.keymap.get('rollforward', []) if k != 'mousedown_5'
    ]
    if hasattr(_ygwd_behavior, 'clear_keymap_cache'):
        _ygwd_behavior.clear_keymap_cache()

    # Block wheel replay even if the ordinary rollforward binding is later
    # changed. Do NOT globally turn the wheel into dismiss: other displayables
    # (including DismissBehavior) can attach arbitrary actions to that name.
    if not getattr(_ygwd_behavior.map_event, '_ygwd_wrapper', False):
        _ygwd_previous_map_event = _ygwd_behavior.map_event

        def _ygwd_map_event(ev, keysym):
            if keysym == 'rollforward' and _ygwd_previous_map_event(ev, 'mousedown_5'):
                return False
            return _ygwd_previous_map_event(ev, keysym)

        _ygwd_map_event._ygwd_wrapper = True
        _ygwd_behavior.map_event = _ygwd_map_event

    if not getattr(_ygwd_behavior.SayBehavior.event, '_ygwd_wrapper', False):
        _ygwd_previous_say_event = _ygwd_behavior.SayBehavior.event

        def _ygwd_say_event(self, ev, x, y, st):
            original = self.dismiss
            try:
                allowed = (renpy.current_interact_type() == 'say'
                           and not renpy.context()._menu
                           and renpy.get_screen('choice') is None
                           and not isinstance(original, (str, bytes))
                           and 'dismiss' in original)
            except Exception:
                allowed = False
            if not allowed or not _ygwd_previous_map_event(ev, 'mousedown_5'):
                return _ygwd_previous_say_event(self, ev, x, y, st)
            # Only complete the verified current ADV dialogue text. Unknown
            # screens fail closed instead of accidentally skipping unseen text.
            if not self.is_focused():
                return _ygwd_previous_say_event(self, ev, x, y, st)
            try:
                getter = (getattr(renpy, 'get_displayable', None)
                          or getattr(renpy, 'get_widget', None))
                text = getter('say', 'what') if getter else None
                import renpy.text.text as _ygwd_text
                known_text = isinstance(text, _ygwd_text.Text)
            except Exception:
                known_text = False
            if not known_text:
                raise renpy.display.core.IgnoreEvent()
            if text.slow:
                if text.style.slow_abortable:
                    import pygame
                    completion = pygame.event.Event(
                        renpy.display.core.EVENTNAME,
                        eventnames=['dismiss'], up=False)
                    text.event(completion, x, y, st)
                raise renpy.display.core.IgnoreEvent()
            try:
                self.dismiss = list(original) + ['mousedown_5']
                return _ygwd_previous_say_event(self, ev, x, y, st)
            finally:
                self.dismiss = original

        _ygwd_say_event._ygwd_wrapper = True
        _ygwd_behavior.SayBehavior.event = _ygwd_say_event
