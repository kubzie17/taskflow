"""Deliberately failing test for the Day 9 release-gate demonstration.

This must make the `test` job fail so that `package`, `publish` and `deploy`
are skipped. Remove this file in a follow-up commit to repair the gate.
"""


def test_release_gate_demo_is_deliberately_false():
    assert 1 + 1 == 3, "Deliberate gate demo: a failing check must block packaging"
