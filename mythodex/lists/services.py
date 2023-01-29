from lists.models import UserList, ItemUserList

def add_list(name, description):

    new_list = UserList(
        name=name,
        description=description,
    )
    return new_list