#pylint: disable = F0401
from helpers import *
from java.util.UUID import fromString as id_to_player
from org.bukkit.util import Vector
from math import sin

ff_perm        = "utils.forcefield"
pass_perm      = "utils.forcefield.ignore"
ff_prefix      = "&8[&bFF&8] "
ff_users       = []
whitelists     = {}        # {ff_owner_id: [white, listed, ids]}
fd             = 6         # forcefield distance
Xv             = 2.95 / fd # used in move_away(), this is more efficient.

# /ff admin  is a future option I might implement


@hook.command("forcefield")
def on_forcefield_command(sender, args):
  if not is_player(sender) or not sender.hasPermission(ff_perm):
    noperm(sender)
    return True

  if not args or args[0].upper() in ["ON", "OFF"]: # Toggle
    forcefield_toggle(sender, args[:1])
    return True

  args[0] = args[0].upper() # If it gets to this point, there are argument(s).
  if args[0] in ["WHITELIST", "WL", "WLIST"]: # Whitelist commands
    if not args[1:] or args[1].upper() == "LIST":
      whitelist_list(sender)
      return True

    args[1] = args[1].upper() # If it gets too this point, there is a second argument.
    if args[1] == "CLEAR":
      whitelist_clear(sender)
    elif args[1] in ["ADD", "+"]:
      change_whitelist(sender, True, args[2:])
    elif args[1] in ["REMOVE", "DELETE", "REM", "DEL", "-"]:
      change_whitelist(sender, False, args[2:])
    else:
      forcefield_header(sender, "&cInvalid syntax. Use &e/ff ? &cfor info.")

  elif args[0] in ["HELP", "?"]: # /forcefield help
    forcefield_help(sender)
  else:
    forcefield_header(sender, "&cInvalid syntax. Use &e/ff ? &cfor info.")
  return True


def change_whitelist(sender, add, names): #Add names if add == True else Remove names.
  if names:
    sender_id = uid(sender)
    if sender_id not in whitelists:
      whitelists[sender_id] = []

    for name in names:
      player = server.getOfflinePlayer(name)
      if player.hasPlayedBefore():
        player_id = str(player.getUniqueId())
        pname     = player.getName()
        sname     = stripcolors(sender.getDisplayName())

        # add player to whitelist if not already added
        if add and player_id not in whitelists[sender_id]:
          if sender != player:
            whitelists[sender_id].append(player_id)
            forcefield_header(sender, "&bAdded &f%s &bto your forcefield whitelist." % pname)
            forcefield_header(player, "&f%s &badded you to his forcefield whitelist." % sname)
          else:
            forcefield_header(sender, "&cYou can't whitelist yourself.")

        # remove player from whitelist if whitelisted
        elif not add and player_id in whitelists[sender_id]:
          whitelists[sender_id].remove(player_id)
          forcefield_header(sender, "&cRemoved &f%s &cfrom your forcefield whitelist." % pname)
          forcefield_header(player, "&f%s &cremoved you from his forcefield whitelist." % sname)

        # player was already / not added to whitelist
        else:
          var = "already" if add == True else "not"
          forcefield_header(sender, "&f%s &cwas %s in your forcefield whitelist!" % (pname, var))

      else:
        forcefield_header(sender, "&cplayer &f%s &cwas not found." % name)
  else:
    forcefield_header(sender, "&cGive space-separated playernames.")


def whitelist_list(player):
  player_id = str(player.getUniqueId())
  count     = 0
  forcefield_header(player, "&bForcefield whitelist:")
  for user_id in whitelists.get(player_id, []):
    count += 1
    pname = server.getOfflinePlayer(id_to_player(user_id)).getName()
    msg(player, "&b %s. &f%s" % (count, pname))
  if count == 0:
    msg(player, "&c Your whitelist has no entries.")


def whitelist_clear(player):
  player_id = str(player.getUniqueId())
  if whitelists.get(player_id):
    whitelists.pop(player_id)
    forcefield_header(player, "&bForcefield whitelist cleared.")
  else:
    forcefield_header(player, "&cYou had no players whitelisted.")


def forcefield_help(player):
  msg(player, " ")
  forcefield_header(player, "&b&l/Forcefield help:         %s" % forcefield_check(player))
  msg(player, "&b You can use the forcefield to keep players on distance.")
  msg(player, "&b Commands:")
  msg(player, "&b 1. &6/ff &ohelp &b:                         aliases: &6?")
  msg(player, "&b 2. &6/ff &o(on off)")
  msg(player, "&b 3. &6/ff &owhitelist (list) &b:              aliases: &6wlist, wl")
  msg(player, "&b 4. &6/ff wl &oclear")
  msg(player, "&b 5. &6/ff wl &oadd <players> &b:          aliases: &6+")
  msg(player, "&b 6. &6/ff wl &oremove <players> &b:     aliases: &6delete, rem, del, - \n")


def forcefield_check(player): # Returns a string to tell the player its forcefield status
  return "&eYour forcefield is %s" % "&2ON" if str(player.getUniqueId()) in ff_users else "&cOFF"


def forcefield_toggle(player, arg): # arg is a list with max 1 string
  player_id = str(player.getUniqueId())
  enabled   = player_id in ff_users
  argoff    = arg[0].upper() == "OFF" if arg else False
  if enabled and (not arg or argoff): # 3 possibilities for arg: [], ["OFF"], ["ON"]. This is the most efficient way. (Case insensitive)
    ff_users.remove(player_id)
    forcefield_header(player, "&bForcefield toggle: &cOFF")
  elif not enabled and not argoff:
    ff_users.append(player_id)
    forcefield_header(player, "&bForcefield toggle: &2ON")


def forcefield_help(sender):
  msg(sender, "%s &a&l/ForceField Help:" % ff_prefix)
  msg(sender, "&aYou can use the forcefield to keep players on distance.")
  msg(sender, "&2Commands:")
  msg(sender, "&a1. &6/ff &ohelp &a: aliases: ?")
  msg(sender, "&a2. &6/ff &o(toggle)")
  msg(sender, "&a3. &6/ff &owhitelist (list) &a: aliases: wlist, wl")
  msg(sender, "&a4. &6/ff wl &oclear")
  msg(sender, "&a5. &6/ff wl &oadd <players> &a: aliases: &o+")
  msg(sender, "&a6. &6/ff wl &oremove <players> &a: aliases: &odelete, rem, del, -")


def forcefield_header(player, message):
  msg(player, "%s %s" % (ff_prefix, message))


#--------------------------------------------------------------------------------------------------------#


@hook.event("player.PlayerMoveEvent")
def on_move(event):
  player = event.getPlayer()
  if is_creative(player):
    player_id = uid(player)

    # moving player has forcefield, nearby player should be moved away
    if player_id in ff_users:
      for entity in player.getNearbyEntities(fd, fd, fd):
        whitelisted = (uid(entity) in whitelists.get(player_id, []))
        if is_player(entity) and not entity.hasPermission(pass_perm) and not whitelisted:
          move_away(player, entity)

    # nearby player has forcefield, moving player should be moved away
    if not player.hasPermission(pass_perm):
      for entity in player.getNearbyEntities(fd, fd, fd):
        entity_id   = uid(entity)
        ff_enabled  = (entity_id in ff_users)
        whitelisted = (player_id in whitelists.get(entity_id, []))
        if is_player(entity) and is_creative(entity) and ff_enabled and not whitelisted:
          move_away(entity, player)


def move_away(player, entity):
  # Pushes entity away from player

  player_loc = player.getLocation()
  entity_loc = entity.getLocation()

  dx = entity_loc.getX() - player_loc.getX()
  vx = sin(Xv * dx)
  dy = entity_loc.getY() - player_loc.getY()
  vy = sin(Xv * dy)
  dz = entity_loc.getZ() - player_loc.getZ()
  vz = sin(Xv * dz)
  entity.setVelocity(Vector(vx , vy, vz))


#--------------------------------------------------------------------------------------------------------#


@hook.event("player.PlayerQuitEvent")
def on_quit(event):
  player    = event.getPlayer()
  player_id = str(player.getUniqueId())
  if player_id in ff_users:
    ff_users.remove(player_id)