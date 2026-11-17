import pathlib
import textwrap
import types
import unittest

PATCH = pathlib.Path(__file__).resolve().parents[1] / 'game' / 'zzzz_wheel_dialogue.rpy'

class PatchTests(unittest.TestCase):
    def setUp(self):
        import sys
        self.saved = {name: sys.modules.get(name) for name in ('renpy', 'renpy.display', 'renpy.display.behavior', 'renpy.text', 'renpy.text.text')}
        self.renpy = types.ModuleType('renpy')
        display = types.ModuleType('renpy.display')
        self.behavior = types.ModuleType('renpy.display.behavior')
        def original_map_event(event, key):
            bindings = {'dismiss': ['mouseup_1', 'K_RETURN'],
                        'rollforward': ['K_PAGEDOWN']}
            return event in bindings.get(key, [key])
        self.behavior.map_event = original_map_event
        behavior = self.behavior
        class SayBehavior:
            def __init__(self):
                self.dismiss = ['dismiss']
            def is_focused(self):
                return True
            def event(self, ev, x, y, st):
                return any(behavior.map_event(ev, key) for key in self.dismiss)
        self.behavior.SayBehavior = SayBehavior
        self.clears = 0
        def clear():
            self.clears += 1
        self.behavior.clear_keymap_cache = clear
        self.renpy.display = display
        display.behavior = self.behavior
        sys.modules.update({'renpy': self.renpy, 'renpy.display': display, 'renpy.display.behavior': self.behavior})
        text_package = types.ModuleType('renpy.text')
        text_module = types.ModuleType('renpy.text.text')
        class Text:
            slow = False
        text_module.Text = Text
        text_package.text = text_module
        self.renpy.text = text_package
        sys.modules.update({'renpy.text': text_package, 'renpy.text.text': text_module})
        self.renpy.get_displayable = lambda screen, ident: Text()
        self.interact = 'say'
        self.menu = False
        self.choice = None
        self.renpy.current_interact_type = lambda: self.interact
        self.renpy.context = lambda: types.SimpleNamespace(_menu=self.menu)
        self.renpy.get_screen = lambda name: self.choice
        self.config = types.SimpleNamespace(keymap={'rollforward': ['mousedown_5', 'K_PAGEDOWN'], 'dismiss': ['mouseup_1']})
        text = PATCH.read_text(encoding='utf-8').split('init 999 python:', 1)[1]
        self.code = compile(textwrap.dedent(text), str(PATCH), 'exec')
        self.env = {'renpy': self.renpy, 'config': self.config}
        exec(self.code, self.env)

    def tearDown(self):
        import sys
        for name, module in self.saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module

    def test_say_and_native_events(self):
        m = self.behavior.map_event
        self.assertFalse(m('mousedown_5', 'dismiss'))
        self.assertTrue(self.behavior.SayBehavior().event('mousedown_5', 0, 0, 0))
        self.assertTrue(m('mouseup_1', 'dismiss'))
        self.assertTrue(m('K_RETURN', 'dismiss'))
        self.assertFalse(m('mousedown_4', 'dismiss'))
        self.assertEqual(self.config.keymap['rollforward'], ['K_PAGEDOWN'])
        self.assertEqual(self.config.keymap['dismiss'], ['mouseup_1'])
        self.assertEqual(self.clears, 1)

    def test_menu_and_other_interactions_stop_wheel_dismiss(self):
        m = self.behavior.map_event
        self.choice = object()
        self.assertFalse(m('mousedown_5', 'dismiss'))
        self.choice = None
        self.menu = True
        self.assertFalse(m('mousedown_5', 'dismiss'))
        self.menu = False
        self.interact = 'menu'
        self.assertFalse(m('mousedown_5', 'dismiss'))
        self.interact = 'input'
        self.assertFalse(m('mousedown_5', 'dismiss'))

    def test_double_init_does_not_stack(self):
        wrapper = self.behavior.map_event
        exec(self.code, self.env)
        self.assertIs(wrapper, self.behavior.map_event)
        self.assertFalse(wrapper('mousedown_5', 'dismiss'))
        self.assertTrue(self.behavior.SayBehavior().event('mousedown_5', 0, 0, 0))

    def test_unknown_text_is_consumed(self):
        class IgnoreEvent(Exception):
            pass
        self.renpy.display.core = types.SimpleNamespace(IgnoreEvent=IgnoreEvent)
        self.renpy.get_displayable = lambda screen, ident: None
        with self.assertRaises(IgnoreEvent):
            self.behavior.SayBehavior().event('mousedown_5', 0, 0, 0)

    def test_legacy_widget_getter(self):
        self.renpy.get_widget = self.renpy.get_displayable
        del self.renpy.get_displayable
        self.assertTrue(self.behavior.SayBehavior().event('mousedown_5', 0, 0, 0))

    def test_store_list_shadow_regression(self):
        # Ren'Py store.list may be a revertable subclass, while SayBehavior
        # owns a native list. isinstance(native, store.list) is false.
        class RevertableList(list):
            pass
        self.env['list'] = RevertableList
        say = self.behavior.SayBehavior()
        self.assertNotIsInstance(say.dismiss, RevertableList)
        self.assertTrue(say.event('mousedown_5', 0, 0, 0))

    def test_say_restores_binding_identity(self):
        say = self.behavior.SayBehavior()
        original = say.dismiss
        say.event('mousedown_5', 0, 0, 0)
        self.assertIs(say.dismiss, original)
        say.dismiss = ['custom']
        self.assertFalse(say.event('mousedown_5', 0, 0, 0))

    def test_say_gate_and_rollforward_guard(self):
        say = self.behavior.SayBehavior()
        for kind in ('menu', 'input', 'pause'):
            self.interact = kind
            self.assertFalse(say.event('mousedown_5', 0, 0, 0))
        self.interact = 'say'
        self.choice = object()
        self.assertFalse(say.event('mousedown_5', 0, 0, 0))
        self.choice = None
        self.menu = True
        self.assertFalse(say.event('mousedown_5', 0, 0, 0))
        self.assertFalse(self.behavior.map_event('mousedown_5', 'rollforward'))
        self.assertTrue(self.behavior.map_event('K_PAGEDOWN', 'rollforward'))

if __name__ == '__main__':
    unittest.main()
