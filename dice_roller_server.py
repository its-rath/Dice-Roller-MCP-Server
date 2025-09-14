#!/usr/bin/env python3
"""
Simple Dice Roller MCP Server - Complete dice rolling toolkit for games and decisions
"""
import os
import sys
import logging
import random
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("dice-roller-server")

# Initialize MCP server - NO PROMPT PARAMETER!
mcp = FastMCP("dice-roller")

# === UTILITY FUNCTIONS ===
def parse_dice_notation(notation):
    """Parse dice notation like 2d6+3 into components"""
    try:
        # Handle modifiers
        modifier = 0
        if '+' in notation:
            parts = notation.split('+')
            notation = parts[0]
            modifier = int(parts[1])
        elif '-' in notation:
            parts = notation.split('-')
            notation = parts[0]
            modifier = -int(parts[1])
        
        # Parse XdY format
        if 'd' in notation.lower():
            parts = notation.lower().split('d')
            num_dice = int(parts[0]) if parts[0] else 1
            num_sides = int(parts[1])
            return num_dice, num_sides, modifier
        else:
            # Single number means 1dN
            return 1, int(notation), modifier
    except:
        return None, None, None

def roll_dice_set(num_dice, num_sides):
    """Roll multiple dice and return results"""
    return [random.randint(1, num_sides) for _ in range(num_dice)]

def format_roll_result(rolls, modifier, total):
    """Format roll results nicely"""
    result = f"🎲 Rolled: {rolls}"
    if modifier != 0:
        sign = "+" if modifier > 0 else ""
        result += f" {sign}{modifier}"
    result += f" = **{total}**"
    return result

# === MCP TOOLS ===

@mcp.tool()
async def flip_coin(count: str = "1") -> str:
    """Flip one or more coins and return heads or tails results."""
    logger.info(f"Flipping {count} coin(s)")
    
    try:
        num_flips = int(count) if count.strip() else 1
        if num_flips < 1 or num_flips > 100:
            return "❌ Error: Please flip between 1 and 100 coins"
        
        results = []
        heads_count = 0
        tails_count = 0
        
        for _ in range(num_flips):
            result = random.choice(["Heads", "Tails"])
            results.append(result)
            if result == "Heads":
                heads_count += 1
            else:
                tails_count += 1
        
        if num_flips == 1:
            emoji = "🪙" if results[0] == "Heads" else "🌑"
            return f"{emoji} **{results[0]}!**"
        else:
            return f"""🪙 Flipped {num_flips} coins:
Results: {', '.join(results)}

📊 Summary:
- Heads: {heads_count} ({heads_count/num_flips*100:.1f}%)
- Tails: {tails_count} ({tails_count/num_flips*100:.1f}%)"""
    
    except ValueError:
        return f"❌ Error: Invalid count '{count}'. Please provide a number."
    except Exception as e:
        logger.error(f"Error flipping coin: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_dice(notation: str = "1d6") -> str:
    """Roll dice using standard notation like 1d20, 2d6+3, 3d8-2, etc."""
    logger.info(f"Rolling dice: {notation}")
    
    try:
        if not notation.strip():
            notation = "1d6"
        
        num_dice, num_sides, modifier = parse_dice_notation(notation)
        
        if num_dice is None:
            return f"❌ Error: Invalid dice notation '{notation}'. Use format like 1d20, 2d6+3, etc."
        
        if num_dice < 1 or num_dice > 100:
            return "❌ Error: Please roll between 1 and 100 dice"
        
        if num_sides < 2 or num_sides > 1000:
            return "❌ Error: Dice must have between 2 and 1000 sides"
        
        rolls = roll_dice_set(num_dice, num_sides)
        total = sum(rolls) + modifier
        
        result = format_roll_result(rolls, modifier, total)
        
        if num_dice > 1:
            result += f"\nIndividual rolls: {', '.join(map(str, rolls))}"
        
        return result
    
    except Exception as e:
        logger.error(f"Error rolling dice: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_dnd_stats() -> str:
    """Roll D&D ability scores using 4d6 drop lowest method for all six stats."""
    logger.info("Rolling D&D ability scores")
    
    try:
        stats = []
        details = []
        
        for stat_name in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
            rolls = roll_dice_set(4, 6)
            rolls.sort(reverse=True)
            dropped = rolls[-1]
            kept = rolls[:3]
            total = sum(kept)
            stats.append(total)
            details.append(f"**{stat_name:12}**: {total:2} (rolled {rolls}, dropped {dropped})")
        
        total_points = sum(stats)
        modifier_total = sum((stat - 10) // 2 for stat in stats)
        
        return f"""⚔️ **D&D Ability Scores** (4d6 drop lowest):

{chr(10).join(details)}

📊 **Summary**:
- Total: {total_points} points
- Average: {total_points/6:.1f}
- Modifier total: {'+' if modifier_total >= 0 else ''}{modifier_total}
- Array: [{', '.join(map(str, sorted(stats, reverse=True)))}]"""
    
    except Exception as e:
        logger.error(f"Error rolling D&D stats: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_advantage(die_type: str = "20") -> str:
    """Roll with advantage (roll twice, take higher) for D&D 5e."""
    logger.info(f"Rolling d{die_type} with advantage")
    
    try:
        sides = int(die_type) if die_type.strip() else 20
        
        if sides < 2 or sides > 1000:
            return "❌ Error: Die must have between 2 and 1000 sides"
        
        roll1 = random.randint(1, sides)
        roll2 = random.randint(1, sides)
        result = max(roll1, roll2)
        
        emoji = "⚡" if result == sides else "🎯" if result >= sides * 0.75 else "🎲"
        
        return f"""{emoji} **Rolling d{sides} with Advantage**:
First roll: {roll1}
Second roll: {roll2}
**Result: {result}** (took the higher)"""
    
    except ValueError:
        return f"❌ Error: Invalid die type '{die_type}'. Please provide a number."
    except Exception as e:
        logger.error(f"Error rolling with advantage: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_disadvantage(die_type: str = "20") -> str:
    """Roll with disadvantage (roll twice, take lower) for D&D 5e."""
    logger.info(f"Rolling d{die_type} with disadvantage")
    
    try:
        sides = int(die_type) if die_type.strip() else 20
        
        if sides < 2 or sides > 1000:
            return "❌ Error: Die must have between 2 and 1000 sides"
        
        roll1 = random.randint(1, sides)
        roll2 = random.randint(1, sides)
        result = min(roll1, roll2)
        
        emoji = "💀" if result == 1 else "😰" if result <= sides * 0.25 else "🎲"
        
        return f"""{emoji} **Rolling d{sides} with Disadvantage**:
First roll: {roll1}
Second roll: {roll2}
**Result: {result}** (took the lower)"""
    
    except ValueError:
        return f"❌ Error: Invalid die type '{die_type}'. Please provide a number."
    except Exception as e:
        logger.error(f"Error rolling with disadvantage: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_percentile() -> str:
    """Roll percentile dice (d100) for percentage-based checks."""
    logger.info("Rolling percentile dice")
    
    try:
        tens = random.randint(0, 9) * 10
        ones = random.randint(0, 9)
        result = tens + ones if tens + ones > 0 else 100
        
        emoji = "💯" if result == 100 else "⭐" if result >= 95 else "✨" if result >= 90 else "🎲"
        
        return f"""{emoji} **Percentile Roll (d100)**:
Tens die: {tens if tens > 0 else "00"}
Ones die: {ones}
**Result: {result}%**"""
    
    except Exception as e:
        logger.error(f"Error rolling percentile: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_fudge(count: str = "4") -> str:
    """Roll Fudge/Fate dice returning + (plus), - (minus), or blank results."""
    logger.info(f"Rolling {count} Fudge dice")
    
    try:
        num_dice = int(count) if count.strip() else 4
        
        if num_dice < 1 or num_dice > 20:
            return "❌ Error: Please roll between 1 and 20 Fudge dice"
        
        results = []
        total = 0
        symbols = {1: "+", 0: "◯", -1: "-"}
        
        for _ in range(num_dice):
            roll = random.randint(-1, 1)
            results.append(symbols[roll])
            total += roll
        
        sign = "+" if total > 0 else ""
        
        return f"""🎲 **Fudge/Fate Dice Roll**:
Rolled {num_dice}dF: [{' '.join(results)}]
**Total: {sign}{total}**"""
    
    except ValueError:
        return f"❌ Error: Invalid count '{count}'. Please provide a number."
    except Exception as e:
        logger.error(f"Error rolling Fudge dice: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_exploding(notation: str = "1d6") -> str:
    """Roll exploding dice where max rolls trigger additional rolls."""
    logger.info(f"Rolling exploding dice: {notation}")
    
    try:
        if not notation.strip():
            notation = "1d6"
        
        num_dice, num_sides, modifier = parse_dice_notation(notation)
        
        if num_dice is None:
            return f"❌ Error: Invalid dice notation '{notation}'. Use format like 1d6, 2d8, etc."
        
        if num_dice < 1 or num_dice > 20:
            return "❌ Error: Please roll between 1 and 20 exploding dice"
        
        if num_sides < 2 or num_sides > 100:
            return "❌ Error: Exploding dice must have between 2 and 100 sides"
        
        all_rolls = []
        explosions = 0
        
        for i in range(num_dice):
            die_rolls = []
            roll = random.randint(1, num_sides)
            die_rolls.append(roll)
            
            while roll == num_sides and explosions < 10:  # Limit explosions
                roll = random.randint(1, num_sides)
                die_rolls.append(roll)
                explosions += 1
            
            all_rolls.append(die_rolls)
        
        total = sum(sum(die) for die in all_rolls) + modifier
        
        result = f"💥 **Exploding Dice Roll ({notation}!)**:\n"
        for i, die_rolls in enumerate(all_rolls, 1):
            if len(die_rolls) > 1:
                result += f"Die {i}: {die_rolls} (exploded!)\n"
            else:
                result += f"Die {i}: {die_rolls}\n"
        
        if modifier != 0:
            sign = "+" if modifier > 0 else ""
            result += f"\nModifier: {sign}{modifier}\n"
        
        result += f"\n**Total: {total}**"
        
        if explosions > 0:
            result += f"\n🎆 Total explosions: {explosions}"
        
        return result
    
    except Exception as e:
        logger.error(f"Error rolling exploding dice: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_pool(pool_size: str = "5", target: str = "6", die_type: str = "10") -> str:
    """Roll a dice pool counting successes against a target number."""
    logger.info(f"Rolling pool of {pool_size}d{die_type} against target {target}")
    
    try:
        size = int(pool_size) if pool_size.strip() else 5
        target_num = int(target) if target.strip() else 6
        sides = int(die_type) if die_type.strip() else 10
        
        if size < 1 or size > 50:
            return "❌ Error: Pool size must be between 1 and 50"
        
        if sides < 2 or sides > 100:
            return "❌ Error: Die must have between 2 and 100 sides"
        
        if target_num < 1 or target_num > sides:
            return f"❌ Error: Target must be between 1 and {sides}"
        
        rolls = roll_dice_set(size, sides)
        successes = sum(1 for roll in rolls if roll >= target_num)
        criticals = sum(1 for roll in rolls if roll == sides)
        
        emoji = "🌟" if successes >= size * 0.75 else "✅" if successes > 0 else "❌"
        
        result = f"""{emoji} **Dice Pool Result**:
Rolling {size}d{sides}, target {target_num}+
Rolls: {sorted(rolls, reverse=True)}

**Successes: {successes}/{size}**"""
        
        if criticals > 0:
            result += f"\n⭐ Critical rolls: {criticals}"
        
        return result
    
    except ValueError:
        return "❌ Error: Invalid input. Please provide numbers for pool size, target, and die type."
    except Exception as e:
        logger.error(f"Error rolling dice pool: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting Dice Roller MCP server...")
    logger.info("Ready to roll! 🎲")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)