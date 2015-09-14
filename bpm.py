from helpers import *
import org.bukkit.block.BlockFace as BlockSide
import org.bukkit.Material as Material

"""
remake of dicodes blockplacemods
"""

slabToggle      = []
cauldronToggle  = []
inventoryToggle = []

blocks = {Material.DROPPER, Material.HOPPER, Material.FURNACE, Material.DISPENSER}
info   = "please use: &9Slab&3, &9Inventory&3, &9Cauldron &3or &9Help&3."

togPerm = "utils.toggle"

@hook.event("block.BlockPlaceEvent", "monitor")
def blockPlace(event):
    block    = event.getBlockPlaced()
    material = block.getType()
    n        = event.getPlayer().getName()

    if (material in (Material.WOOD_STEP, Material.STEP)) and n in slabToggle:
        block.setData(block.getData() + 8)

    elif (material == Material.CAULDRON) and n in cauldronToggle:
        block.setData(block.getData() + 3)

    elif (material in blocks) and n in inventoryToggle:
        inv = user.getInventory().getItemInHand()
        state = block.getState()
        blockInv = state.getInventory()
        blockInv.setItem(int(slot), toStack(inv))        
def help():
    msg(sender, "&a-=[&6BPM&a]=-")
    msg(sender, "&6Aliases for /toggle: \n &e/set, /setting and /config\n")
    msg(sender, "&6Available settings: \n &eSlab, Cauldron and Inventory\n")
    msg(sender, "&6Slab: \n&eThe slab setting flips slabs to the top half \nof the block on placing them.\n")
    msg(sender, "&6Cauldron: \n&eThe cauldron setting fills cauldrons on placing them.\n")
    msg(sender, "&6Inventory: \n&eThe inventory setting puts a block in an item with an inventory.\n")
@hook.command("toggle")
def toggleCommand(sender, cmd, label, args):
    name = sender.getName()
    try:
        if sender.hasPermission(togPerm) and sender.getWorld().getName() == "creative":
            if len(args) > 0:              
                if str(args[0]) == "slab":
                    if name in slabToggle:
                        msg(sender, "&a Disabled automatically flipping slabs.")
                        slabToggle.remove(name)
                    else:
                        msg(sender, "&a Enabled automatically flipping slabs.")
                        slabToggle.append(name)      

                elif str(args[0]) == "cauldron":
                    if name in cauldronToggle:
                        msg(sender, "&a Disabled automatically filling cauldrons.")
                        cauldronToggle.remove(name)
                    else:
                        msg(sender, "&a Enabled automatically filling cauldrons.")
                        cauldronToggle.append(name)

                elif str(args[0]) == "inv" or "inventory":
                    if name in cauldronToggle:
                        msg(sender, "&a Disabled automatically putting items in inventories.")
                        cauldronToggle.remove(name)
                    else:
                        msg(sender, "&a Enabled automatically putting items in inventories.")
                        cauldronToggle.append(name)

                elif str(args[0]) == "help" or "?" or "wut":
                    help()

                elif len(args) > 1:
                    msg(sender,"&aToo many arguments, \n&3&s") % info

                else:
                    msg(sender, "&9Unknown argument \n &3%s") % info
            else:
                help()  


        elif sender.getWorld() != "creative":
            msg(sender, "&aBPM doesn't work in this world.")
            print sender.getWorld().getName() 
        else:
            msg(sender, "&aNo permission.")
    except:
        print trace()