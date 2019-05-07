#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `pautomate` package."""
import pytest
from click.testing import CliRunner

from pautomate import cli


@pytest.fixture
def runner():
    """CliRunner fixture

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return CliRunner()


def test_command_line_cli_interface(runner):
    """Test the CLI."""
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert 'Console interface for pautomate' in result.output


def test_command_line_interface_help(runner):
    help_result = runner.invoke(cli.cli, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output
    assert all(
        [
            entry_point in help_result.output for entry_point in [
                '-t, --target', 'Target workspace', 'branches', 'dotnet', 'fetch',
            ]
        ],
    )


def test_fetch_entry_point(runner):
    help_result = runner.invoke(cli.fetch, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output


def test_branches_entry_point(runner):
    help_result = runner.invoke(cli.branches, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output


def test_dotnet_entry_point(runner):
    help_result = runner.invoke(cli.dotnet, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'Show this message and exit.' in help_result.output
    assert all(
        [
            entry_point in help_result.output for entry_point in [
                '-w, --watch', 'Run in watch mode',
            ]
        ],
    )
