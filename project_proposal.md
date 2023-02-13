This website will be designed to allow the management of multiple lists of magic items, and their pertinent properties, to allow for fast access for a user running a tabletop roleplaying game.

To acheive this the site will access publicly available API's with names of various magic items, their stats, special rules/abilities, monetary cost, and other pertinent notes.

The database schema will track the following tables:
- Users
- UserList (lists that the users make to track magic items)
- UserItems (a list of user made items)
- Item-UserList (a keyed list relating the userlists to magic items on the next table)
- MagicItem (a list of all items on the database)
- Rarity (a table of the varying magic item rarities the main MagicItem table will reference)
- ItemType (a table of the varying magic item classifications the main MagicItem table will reference)
- ItemVariant (a table of the varying magic item variations the main MagicItem table will reference)

User info, passwords need to be secure. There should also be an option for user lists to be public of private.

Users will be able to login and have saved custom lists of magic items. The site will allow them to modify the list, select a random item from the list, or generate a cost value of a specific item if a player may be purchasing it in the game.

Additionally, the user may create completely custom items and add them to the list, as well as share them with their players.
