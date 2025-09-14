# Dice Roller MCP Server

A Model Context Protocol (MCP) server that provides a complete dice rolling toolkit for games, decision-making, and random number generation.

## Purpose

This MCP server provides a secure interface for AI assistants to perform various dice rolling operations including coin flips, D&D mechanics, and specialized dice systems.

## Features

### Current Implementation
- **`flip_coin`** - Flip one or more coins for heads/tails results
- **`roll_dice`** - Roll dice using standard notation (2d6+3, 1d20, etc.)
- **`roll_dnd_stats`** - Generate D&D ability scores using 4d6 drop lowest
- **`roll_advantage`** - Roll with advantage (D&D 5e mechanic)
- **`roll_disadvantage`** - Roll with disadvantage (D&D 5e mechanic)
- **`roll_percentile`** - Roll d100 for percentage-based checks
- **`roll_fudge`** - Roll Fudge/Fate dice (+, -, or blank)
- **`roll_exploding`** - Roll exploding dice that reroll on maximum
- **`roll_pool`** - Roll dice pools counting successes against target

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)

## Installation

See the step-by-step instructions provided with the files.

## Usage Examples

In Claude Desktop, you can ask:
- "Flip a coin to help me decide"
- "Roll 2d6+3 for damage"
- "Generate D&D stats for my new character"
- "Roll with advantage on my attack"
- "Roll percentile dice"
- "Roll 5d10 counting 7+ as successes"
- "Roll exploding d6s"
- "Roll 4 Fudge dice"

## Architecture