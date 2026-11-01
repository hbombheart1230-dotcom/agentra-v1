"""P15 RF-014 (20261101-13h): node-binding evidence for the Scanner repeat/risk/memory-bias wrappers in graphs.nodes.scanner_node.

Verifies ONLY that each public wrapper delegates to its `_r3_impl` with `facade=<the scanner_node module>` at call time (patched with pure
sentinel closures). It is NOT proof of the whole RF-009 runtime repeat/risk/NOOP behavior. scanner_node.py is read-only here.
"""
from __future__ import annotations

import copy
import unittest
from unittest import mock

from graphs.nodes import scanner_node as node


class ScannerNodeConsumerSeamTests(unittest.TestCase):
    def test_repeat_symbol_penalty_wrapper_delegates_with_node_facade(self):
        calls = []

        def sentinel(state, *, symbol, policy, facade):
            calls.append({"state": state, "symbol": symbol, "policy": policy, "facade_is_node": facade is node})
            return {"sentinel": "repeat_symbol_penalty", "symbol": symbol}

        state = {"persisted_state": {}}
        before = copy.deepcopy(state)
        with mock.patch.object(node, "_repeat_symbol_penalty_r3_impl", sentinel):
            result = node._repeat_symbol_penalty(state, symbol="005930", policy={})
        self.assertEqual(result, {"sentinel": "repeat_symbol_penalty", "symbol": "005930"})
        self.assertEqual(calls, [{"state": state, "symbol": "005930", "policy": {}, "facade_is_node": True}])
        self.assertIs(calls[0]["state"], state)
        self.assertEqual(state, before)  # no mutation of the fake state

        def boom(state, *, symbol, policy, facade):
            raise RuntimeError("impl-boom")

        with mock.patch.object(node, "_repeat_symbol_penalty_r3_impl", boom):
            with self.assertRaisesRegex(RuntimeError, "impl-boom"):
                node._repeat_symbol_penalty(state, symbol="005930", policy={})

    def test_repeat_blocker_cooldown_penalty_wrapper_delegates_with_node_facade(self):
        calls = []

        def sentinel(state, *, symbol, policy, facade):
            calls.append((state is not None, symbol, dict(policy), facade is node))
            return {"sentinel": "cooldown"}

        state = {"persisted_state": {}}
        before = copy.deepcopy(state)
        with mock.patch.object(node, "_repeat_blocker_cooldown_penalty_r3_impl", sentinel):
            self.assertEqual(node._repeat_blocker_cooldown_penalty(state, symbol="005930", policy={}), {"sentinel": "cooldown"})
        self.assertEqual(calls, [(True, "005930", {}, True)])
        self.assertEqual(state, before)

        def boom(state, *, symbol, policy, facade):
            raise ValueError("cooldown-boom")

        with mock.patch.object(node, "_repeat_blocker_cooldown_penalty_r3_impl", boom):
            with self.assertRaisesRegex(ValueError, "cooldown-boom"):
                node._repeat_blocker_cooldown_penalty(state, symbol="005930", policy={})

    def test_resolve_scanner_repeat_guard_policy_wrapper_delegates_with_node_facade(self):
        calls = []

        def sentinel(policy, *, facade):
            calls.append((dict(policy), facade is node))
            return {"sentinel": "policy"}

        policy = {}
        with mock.patch.object(node, "_resolve_scanner_repeat_guard_policy_r3_impl", sentinel):
            self.assertEqual(node._resolve_scanner_repeat_guard_policy(policy), {"sentinel": "policy"})
        self.assertEqual(calls, [({}, True)])
        self.assertEqual(policy, {})

        def boom(policy, *, facade):
            raise KeyError("policy-boom")

        with mock.patch.object(node, "_resolve_scanner_repeat_guard_policy_r3_impl", boom):
            with self.assertRaises(KeyError):
                node._resolve_scanner_repeat_guard_policy({})

    def test_memory_bias_observation_only_wrapper_delegates_with_node_facade(self):
        calls = []

        def sentinel(state, *, facade):
            calls.append((state, facade is node))
            return False

        with mock.patch.object(node, "_memory_bias_observation_only_r3_impl", sentinel):
            self.assertIs(node._memory_bias_observation_only({}), False)
            self.assertIs(node._memory_bias_observation_only(), False)
        self.assertEqual(calls, [({}, True), (None, True)])

        with mock.patch.object(node, "_memory_bias_observation_only_r3_impl", lambda state, *, facade: True):
            self.assertIs(node._memory_bias_observation_only({}), True)  # call-time monkeypatch is honored, not captured at import


if __name__ == "__main__":
    unittest.main()
