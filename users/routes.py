from flask import (
    Blueprint,
    Flask,
    render_template,
    session,
    g,
    flash,
    redirect,
    request,
)
from users.services import UserService, UserEditForm


user_routes = Blueprint("user_routes", __name__)

##############################################################################
# User Routes


@user_routes.route("/users/<int:user_id>")
def show_user(user_id):
    user = UserService.get_by_id(user_id)
    return render_template("users/user.html", user=user)


@user_routes.route("/users/edit", methods=["GET", "POST"])
def edit_user():
    user_id = int(request.args["user_id"])

    if not g.user:
        flash("Please login to edit a profile.", "danger")
        return redirect("/login")

    if g.user.id != user_id:
        flash(
            f"{g.user.id} is not {user_id} Unauthorized to edit that profile.", "danger"
        )
        return redirect(f"/users/{g.user.id}")

    user = UserService.get_by_id(user_id)
    form = UserEditForm(obj=user)

    if not form.validate_on_submit():
        return render_template(f"/users/edit.html", user=user, form=form)

    try:
        user = UserService.update(user.id, form)
        flash(f"Succesfully updated profile", "success")
        return redirect(f"/users/{g.user.id}")
    except:
        flash(f"Unable to update profile", "error")
        return render_template(f"/users/edit.html", user=user, form=form)


@user_routes.route("/users/delete", methods=["POST"])
def delete_user():

    if not g.user:
        flash("Please login to edit a profile.", "danger")
        return redirect("/login")

    user_id = int(request.args["user_id"])
    form = UserEditForm()

    if g.user.id != user_id:
        flash(
            f"{g.user.id} is not {user_id} Unauthorized to edit that profile.", "danger"
        )
        return redirect(f"/users/{g.user.id}")

    if not form.validate_on_submit():
        return redirect(f"/users/edit?user_id={g.user.id}")

    try:
        UserService.delete(user_id, form)
        flash(f"Your profile has been removed", "success")
        return redirect("/")
    except:
        flash(f"Unable to update profile", "error")
        return render_template(f"/users/edit.html", form=form)
