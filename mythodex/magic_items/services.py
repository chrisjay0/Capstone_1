

ITEM_RARITY  = ['Common','Uncommon','Rare','Very Rare']

ITEM_TYPES = ['Scroll','Rod','Armor','Ammunition','Ring','Potion','Staff','Wondrous Items','Wand','Weapon',]

def shorten_description(magic_item):
    desc = magic_item.description
    if len(desc) <= 55:
        return desc
    return desc[0:55] + '...'
    