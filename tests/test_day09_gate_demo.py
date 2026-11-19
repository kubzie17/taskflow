"""Temporary Day 9 gate demonstration. Remove this file in the next commit.

This test fails on purpose to prove that a failing check blocks packaging,
publishing and deployment. It does not touch or weaken the application.
"""


def test_deliberate_failure_blocks_the_release_gate():
    release_gate_should_block = True
    assert release_gate_should_block is False, "Deliberate Day 9 failure: the release gate must stop here"
