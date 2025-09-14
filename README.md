# 🎲 Dice Roller MCP Server

A lightweight Model Context Protocol (MCP) server that provides dice-rolling functionality for AI assistants. It supports coin flips, Dungeons & Dragons-style rolls, and general-purpose randomization mechanics.

---

## 🧠 Purpose

This MCP server enables AI agents to simulate dice-based randomness for games, decision-making, and probability-based tasks. Whether you're flipping a coin or rolling a d20, this server delivers fast, reliable results.

---

## ⚙️ Features

### Current Tools

- **`flip_coin`** – Simulates a fair coin toss (Heads or Tails)
- **`roll_dice`** – Rolls a standard die (d4, d6, d8, d10, d12, d20, d100)
- **`custom_roll`** – Rolls multiple dice with custom sides (e.g., 3d6, 2d20)
- **`roll_table`** – Selects a random item from a user-defined list or table

All tools return formatted strings and include error handling for invalid input.

---

## 📦 Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp`)
- Claude Desktop (for integration and testing)

---

## 🚀 Installation

Follow these steps to set up and run the server:

1. **Create Project Directory**
   ```bash
   mkdir dice-roller-mcp-server
   cd dice-roller-mcp-server

2. **Save the Required Files**

Dockerfile

requirements.txt

dice_roller_server.py

README.md

CLAUDE.md

3. **Build Docker Image**
 ```bash
    docker build -t dice-roller-mcp-server .

4. **(Optional) Set Secrets**
