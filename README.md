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
   ```
4. **(Optional) Set Secrets**
```bash
docker mcp secret set DICE_API_KEY="your-secret-key"
docker mcp secret list
```

5. **Create Custom Catalog**
6. ```bash
   mkdir -p ~/.docker/mcp/catalogs
   nano ~/.docker/mcp/catalogs/custom.yaml
   ```
Add this entry:
```bash
version: 2
name: custom
displayName: Custom MCP Servers
registry:
  dice_roller:
    description: "Simple dice roller MCP server"
    title: "Dice Roller"
    type: server
    dateAdded: "2025-09-14T00:00:00Z"
    image: dice-roller-mcp-server:latest
    ref: ""
    tools:
      - name: flip_coin
      - name: roll_dice
      - name: custom_roll
      - name: roll_table
    metadata:
      category: productivity
      tags:
        - dice
        - randomness
        - games
      license: MIT
      owner: local
```
6. **Update Registry**
 ```bash
   nano ~/.docker/mcp/registry.yaml
   ```
Add:
```yaml
   registry:
  dice_roller:
    ref: ""
```
7. **Configure Claude Desktop**
Edit your config file:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json

Windows: %APPDATA%\Claude\claude_desktop_config.json

Linux: ~/.config/Claude/claude_desktop_config.json


Add to the args array:
```json
"--catalog=/mcp/catalogs/custom.yaml"
```

8. Restart Claude Desktop

9. Test Your Server
    ```bash
    docker mcp server list
    docker logs [container_name]
    ```


💬 Usage Examples
In Claude Desktop, try:

“Flip a coin”

“Roll a d20”

“Roll 3d6”

“Pick a random item from this list: sword, shield, potion”
