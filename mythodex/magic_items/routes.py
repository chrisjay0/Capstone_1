 
from flask import Blueprint, Flask, render_template, session, g, flash, redirect, request
from magic_items.services import MagicItemService, ItemForm, ItemFilterForm, CollectionAddForm, CollectionService, ItemCollectionService
from users.services import UserService



magic_routes = Blueprint('magic_routes', __name__)


#########################################################################################################
#########################################################################################################
##
## Magic Item Routes


@magic_routes.route("/magic-items/new", methods=["GET", "POST"])
def add_item():

    if not g.user:
        flash("Please login to create a new magic item", "danger")
        return redirect("/login")

    form = ItemForm()

    if form.validate_on_submit():
        try:
            item = MagicItemService.create(g.user.id, form)
            flash("new item " + item.name + " added", "success")
            return redirect(f"/magic-items/{item.id}")

        except:
            flash("error", "danger")
            return render_template("magic_items/new_magic_item.html", form=form)

    return render_template("magic_items/new_magic_item.html", form=form)

@magic_routes.route("/magic-items/<int:item_id>", methods=["GET"])
def show_item(item_id):
    item = MagicItemService.get(item_id)
    if item.created_by:
        user = UserService.get_by_id(item.created_by)
        return render_template("magic_items/magic_item.html", item=item, user=user,)
    return render_template("magic_items/magic_item.html", item=item,)


@magic_routes.route("/magic-items", methods=["GET"])
def show_items():
    form = ItemFilterForm(object=request.args)

    if 'created_by' in request.args and request.args['created_by'] == '':
        flash("Please login or signup to your magic items", "danger")
        return redirect("/login")
    
    
    items = MagicItemService.get_filtered(**request.args)
        

    return render_template(
        "magic_items/magic_items.html",
        items=items,
        form=form,
    )

@magic_routes.route("/magic-items/edit", methods=["GET", "POST"])
def edit_item():

    if not g.user:
        flash("Please login to create a new magic item", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    item = MagicItemService.get(magic_item_id)
    item.description = item.description[1]
    form = ItemForm(obj=item)

    if form.validate_on_submit():
        try:
            edited_item = MagicItemService.update(g.user.id,magic_item_id,form)
            flash("new item " + edited_item.name + " edited", "success")
            return redirect(f"/magic-items/{edited_item.id}")

        except:
            flash("error", "danger")
            return render_template("magic_items/edit_magic_item.html", form=form, item=item)

    return render_template("magic_items/edit_magic_item.html", form=form, item=item)


@magic_routes.route("/magic-items/delete", methods=["POST"])
def delete_item():

    if not g.user:
        flash("Please login to manage magic items", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    item = MagicItemService.get(magic_item_id)

    if g.user.id is not item.created_by:
        flash("Not authorized to make changes to that magic item", "danger")
        return redirect(f"/magic-items?created_by={g.user.id}")

    MagicItemService.delete(g.user.id, magic_item_id)
    flash(f'{item.name} has been deleted','success')
    return redirect(f"/magic-items?created_by={g.user.id}")

@magic_routes.route("/magic-items/random", methods=["GET"])
def random_item():
    item = MagicItemService.random()
    return render_template("magic_items/magic_item.html", item=item)


#########################################################################################################
#########################################################################################################
##
## Collection Routes


@magic_routes.route("/collections/new", methods=["GET", "POST"])
def add_new_collection():

    if not g.user:
        flash("Please login to create a new collection", "danger")
        return redirect("/login")

    form = CollectionAddForm()

    if form.validate_on_submit():
        if not request.args:
            try:
                collection = CollectionService.create(g.user.id, form)
                flash("new collection " + collection.name + " added", "success")
                return redirect(f"/collections/{collection.id}")

            except:
                flash("error", "danger")
                return render_template("magic_items/new_collection.html", form=form)
        else:
            try:
                magic_item_id = int(request.args["magic_item_id"])
                collection = CollectionService.create(g.user.id, form)
                CollectionService.add_magic_item(magic_item_id, collection.id)
                flash(f"new collection {collection.name} created", "success")
                return redirect(f"/collections/{collection.id}")

            except:
                flash("error", "danger")
                return render_template("magic_items/new_collection.html", form=form)

    return render_template("magic_items/new_collection.html", form=form)


@magic_routes.route("/collections", methods=["GET"])
def show_collections():

    if request.args and request.args["user_id"] == "":
        flash("Please login or signup to manage your collections", "danger")
        return redirect("/login")

    collections = CollectionService.get_filtered(**request.args)
    return render_template(
        "magic_items/collections.html",
        collections=collections,
    )


@magic_routes.route("/collections/<int:collection_id>", methods=["GET"])
def show_single_collection(collection_id):
    collection = CollectionService.get(collection_id)
    inventory = ItemCollectionService.get_inventory_numbers(collection.id)
    return render_template(
        "magic_items/collection.html", collection=collection, inventory=inventory
    )


@magic_routes.route("/collections/edit", methods=["GET", "POST"])
def edit_collection():

    if not g.user:
        flash("Please login to manage collections.", "danger")
        return redirect("/login")

    collection_id = int(request.args["collection_id"])
    collection = CollectionService.get(collection_id)
    form = CollectionAddForm(obj=collection)

    if g.user.id != collection.user_id:
        flash("Unauthorized to edit that collection", "danger")
        return redirect(f"/collections?user_id={g.user.id}")

    if not form.validate_on_submit():
        return render_template(
            "/magic_items/edit_collection.html", collection=collection, form=form
        )

    try:
        collection = CollectionService.update(g.user.id,collection_id, form)
        flash(f"Succesfully updated {collection.name}!", "success")
        return redirect(f"/collections/{collection.id}")

    except:
        flash("Unable to update {collection.name}", "danger")
        return render_template(
            "/magic_items/edit_collection.html", collection=collection, form=form
        )


@magic_routes.route("/collections/add-item", methods=["POST"])
def add_item_to_collection():

    if not g.user:
        flash("Please login to manage your collections", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    collection_id = int(request.args["collection_id"])

    CollectionService.add_magic_item(magic_item_id, collection_id)

    return redirect(f"/collections/{collection_id}")


@magic_routes.route("/collections/reduce-item", methods=["POST"])
def reduce_item_in_collection():

    if not g.user:
        flash("Please login to manage your collections", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    collection_id = int(request.args["collection_id"])

    CollectionService.reduce_magic_item(magic_item_id, collection_id)

    return redirect(f"/collections/{collection_id}")


@magic_routes.route("/collections/remove-item", methods=["POST"])
def remove_item_in_collection():

    if not g.user:
        flash("Please login to manage your collections", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    collection_id = int(request.args["collection_id"])

    CollectionService.remove_magic_item(magic_item_id, collection_id)

    return redirect(f"/collections/{collection_id}")


@magic_routes.route("/collections/delete", methods=["POST"])
def delete_collection():

    if not g.user:
        flash("Please login to manage your collections", "danger")
        return redirect("/login")

    collection_id = int(request.args["collection_id"])
    collection = CollectionService.get(collection_id)

    if g.user.id is not collection.user_id:
        flash("Not authorized to make changes to that collection", "danger")
        return redirect(f"/collections?user_id={g.user.id}")

    CollectionService.delete(collection_id, g.user.id)
    return redirect(f"/collections?user_id={g.user.id}")


@magic_routes.route("/collections/random", methods=["GET"])
def random_collection():

    collection = CollectionService.random()
    inventory = ItemCollectionService.get_inventory_numbers(collection.id)
    return render_template(
        "magic_items/collection.html", collection=collection, inventory=inventory
    )


@magic_routes.route("/collections/random-item", methods=["GET"])
def random_item_in_collection():
    
    collection_id = int(request.args['collection_id'])
    
    item = CollectionService.random_item(collection_id)
    user = UserService.get_by_id(item.created_by)
    
    return render_template("magic_items/magic_item.html",item=item,user=user,)

