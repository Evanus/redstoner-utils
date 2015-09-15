from helpers import *
import org.bukkit.Material as Material

"""
remake of dicodes blockplacemods
"""

togPerm = "utils.toggle"

@hook.event("block.BlockPlaceEvent", "low")
def block_place(event):
    block     = event.getBlockPlaced()
    material  = block.getType()
    sender    = event.getPlayer()
    py_player = get_py_player(sender)
    if (material in (Material.WOOD_STEP, Material.STEP)) and py_player.slab_toggle and block.getData() < 8:
        block.setData(block.getData() + 8)
    elif (material == Material.CAULDRON) and py_player.cauldron_toggle:
        block.setData(block.getData() + 3)

@hook.event("player.PlayerInteractEvent", "high")
def on_interact(event):
    block  = event.getClickedBlock()
    sender = event.getPlayer()
    py_player = get_py_player(sender)
    if str(event.getAction()) != "RIGHT_CLICK_BLOCK":
        return
    if block.getType() == Material.CAULDRON and py_player.cauldron_toggle:
        block.setData(block.getData() - 1 if block.getData() > 0 else 3)
    else:
        return

def help(sender):
    msg(sender, "&a-=[&6BPM&a]=-")
    msg(sender, "&6Aliases for /toggle: \n &e/set, /setting and /config\n")
    msg(sender, "&6Available settings: \n &eSlab and Cauldron\n")
    msg(sender, "&6Slab: \n&eThe slab setting flips slabs to the top half \nof the block on placing them.\n")
    msg(sender, "&6Cauldron: \n&eThe cauldron setting fills cauldrons on placing them.\n")

@hook.command("toggle")
def toggle_command(sender, cmd, label, args):
    py_player = get_py_player(sender)
    if sender.hasPermission(togPerm) and sender.getWorld().getName() == "creative":
        if len(args) > 0:              
            if str(args[0]) == "slab":
                if py_player.slab_toggle == True:
                    msg(sender, "&a Disabled automatically flipping slabs.")
                    py_player.slab_toggle = False
                else:
                    msg(sender, "&a Enabled automatically flipping slabs.")
                    py_player.slab_toggle = True      
            elif str(args[0]) == "cauldron":
                if py_player.cauldron_toggle == True:
                    msg(sender, "&a Disabled automatically filling cauldrons.")
                    py_player.cauldron_toggle = False 
                else:
                    msg(sender, "&a Enabled automatically filling cauldrons.")
                    py_player.cauldron_toggle = True
            else:
                    help(sender)
        else:
                help(sender)  
    elif sender.getWorld() != "creative":
        msg(sender, "&aBPM doesn't work in this world.")
    else:
        msg(sender, "&aNo permission.")


