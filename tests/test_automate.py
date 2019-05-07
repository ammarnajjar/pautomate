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
    assert '--target' in help_result.output
    assert 'Target workspace' in help_result.output
    assert 'branches' in help_result.output
    assert 'dotnet' in help_result.output
    assert 'fetch' in help_result.output


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
    assert '-w' in help_result.output
    assert '--watch' in help_result.output
    assert 'Run in watch mode' in help_result.output
