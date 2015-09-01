from helpers import *
import org.bukkit.block.BlockFace as BlockSide
import org.bukkit.Material as Material

"""
remake of dicodes blockplacemods
"""

slab_toggle_list = []
cauldron_toggle_list = []
inventory_toggle_list = []

sides = {
    BlockSide.DOWN  : 0,
    BlockSide.UP    : 1,
    BlockSide.NORTH : 2,
    BlockSide.SOUTH : 3,
    BlockSide.WEST  : 4,
    BlockSide.EAST  : 5
}

blocks = {Material.DROPPER, Material.HOPPER, Material.FURNACE, Material.DISPENSER}

tog_perm = "utils.toggle"

@hook.event("block.BlockPlaceEvent", "monitor")
def on_block_place(event):
    material = block.getType()
    user = server.getPlayer().getName()
    if (material in (Material.WOOD_STEP, Material.STEP)) and user in slab_toggle_list:
        block.setData(block.getData() + 8)
    elif (material == Material.CAULDRON) and user in cauldron_toggle_list:
        block.setData(block.getData() + 3)
    elif (material in blocks) and user in inventory_toggle_list:
        inv = user.getInventory().getItemInHand()
        state = block.getState()
        block_inv = state.getInventory()
        block_inv.setItem(int(slot), toStack(inv))

"""
Idk if this is needed, but meh. makes it look cleaner
"""

#	block handelling

def slab():
    user = server.getPlayer().getName()
    if user in slab_toggle_list:
        msg(sender, "&a Disabled automatically flipping slabs.")
        slab_toggle_list.remove(name)
    else:
        msg(sender, "&a Enabled automatically flipping slabs.")
        slab_toggle_list.remove(name)        

def cauldron():
    user = server.getPlayer().getName()
    if user in cauldron_toggle_list:
        msg(sender, "&a Disabled automatically filling cauldrons.")
        cauldron_toggle_list.remove(name)
    else:
        msg(sender, "&a Enabled automatically filling cauldrons.")
        cauldron_toggle_list.remove(name)

def inventory():
    user = server.getPlayer().getName()
    if user in inventory_toggle_list:
        msg(sender, "&a disabled automatically putting items in inventories.")
        inventory_toggle_list.remove(name)
    else:
        msg(sender, "&a Enabled automatically putting items in inventories.")
        inventory_toggle_list.remove(name)

#	Command handelling

@hook.command("toggle")
def toggle_command(sender, args):
    name = sender.getName()
    if sender.hasPermission(togPerm) and sender.getWorld(Creative):
        if args[0] == "slab":
            slab()
        elif args[0] == "cauldron":
            cauldron()
        elif args[0] == "inv" or "inventory":
            inventory()
        else:
            msg(sender, "&9Unknown argument \n &3please use: &9slab&3, &9inventory &3or &9cauldron&3.")

@hook.command("set")
def set_command(sender, args):
    return toggle_command(sender, args)

@hook.command("setting")
def set_command(sender, args):
    return toggle_command(sender, args)
