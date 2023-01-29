

def shorten_description(magic_item):
    desc = magic_item.description
    if len(desc) <= 55:
        return desc
    return desc[0:55] + '...'
    