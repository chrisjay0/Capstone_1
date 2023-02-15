# from app import db
# import time

# from lists.models import ItemUserList, UserList
# from users.models import User
# from magic_items.models import MagicItem, ItemVariant

# import requests

# # new_list = UserList(
# #     name='test',
# #     desc='nin',
# #     user_id=1,
# # )

# # db.session.add(new_list)
# # db.session.commit()

# print(MagicItem.query.filter_by(name='Ammunition, +2').first().id)


def display(**names):
    for name in names.keys():
        print(name)
  
def main():
      
    # passing dictionary key-value 
    # pair as arguments
    display(fname ="John",
            mname ="F.", 
            lname ="Kennedy")
# Driver's code
main()