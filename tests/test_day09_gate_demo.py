"""Deliberately failing check to demonstrate that the release gate blocks packaging.

Remove this file in the repair commit. It exists only for the Day 9 red-gate demonstration.
"""


def test_release_gate_demo_must_fail():
    assert False, "Deliberate failure: this must block package, publish and deploy"
