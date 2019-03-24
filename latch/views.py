from functools import wraps

from http.client import HTTPException

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from latch.models import LatchSetup, UserProfile
from latch.forms import LatchPairForm, LatchUnpairForm
from latch.helpers import (
    instance,
    accountid,
    save_user_accountid,
    delete_user_account_id,
)


def latch_is_configured(view):
    """
    Decorator for views that check that Latch is configured in the site,
    showing an error message if not.
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not LatchSetup.objects.exists():
            return render(
                request,
                "latch_message.html",
                {"message": "Latch is not configured", "alert_type": "danger"},
            )
        else:
            return view(request, *args, **kwargs)

    return wrapper


@latch_is_configured
@login_required
def pair(request, template_name="latch_pair.html"):
    """
    Pairs the current user with a given latch token ID.
    """
    if accountid(request.user) is not None:
        return render(
            request,
            "latch_message.html",
            {"message": _("Account is already paired"), "alert_type": "danger"},
        )

    if request.method == "POST":
        return process_pair_post(request)
    else:
        form = LatchPairForm()
        return render(request, template_name, {"form": form})


def process_pair_post(request, template_name="latch_message.html"):
    form = LatchPairForm(request.POST)
    if form.is_valid():
        form.clean()
        latch = instance()
        try:
            account_id = latch.pair(form.cleaned_data["latch_pin"])
            if "accountId" in account_id.get_data():
                save_user_accountid(request.user, account_id.get_data()["accountId"])
                context = {
                    "message": _("Account paired with Latch"),
                    "alert_type": "success",
                }
            else:
                context = {
                    "message": _("Account not paired with Latch"),
                    "alert_type": "danger",
                }
        except HTTPException as err:
            context = {
                "message": _("Error pairing the account: %(error)s") % {"error": err},
                "alert_type": "danger",
            }

        return render(request, template_name, context=context)


@login_required
def unpair(request, template_name="latch_unpair.html"):
    """
    Unpairs a given user.
    """
    if request.method == "POST":
        form = LatchUnpairForm(request.POST)
        if form.is_valid():
            return do_unpair(request)
    else:
        form = LatchUnpairForm()
    return render(request, template_name, {"form": form})


def do_unpair(request, template_name="latch_message.html"):
    try:
        acc_id = accountid(request.user)
        if acc_id:
            latch = instance()
            latch.unpair(accountid(request.user))
            delete_user_account_id(acc_id)
            context = {
                "message": _("Latch removed from your account"),
                "alert_type": "success",
            }
        else:
            context = {
                "message": _("Your account is not latched"),
                "alert_type": "success",
            }
    except UserProfile.DoesNotExist:
        context = {"message": _("Your account has no profile"), "alert_type": "danger"}
    except HTTPException as err:
        context = {
            "message": _("Error unpairing the account: %(error)s") % {"error": err},
            "alert_type": "danger",
        }

    return render(request, template_name, context=context)


@login_required
def status(request, template_name="latch_status.html"):
    """
    Gives information about Latch status, if it's configured,
    and data relative to the user making the request.
    """
    configured = LatchSetup.objects.exists()
    acc_id = None
    account_status = None
    try:
        if configured:
            acc_id = accountid(request.user)
            if acc_id:
                latch_instance = instance()
                status_response = latch_instance.status(acc_id)
                data = status_response.get_data()["operations"]
                account_status = data["applicationId"]["status"]

    except HTTPException:
        return render(request, template_name, {"error": True})

    return render(
        request,
        template_name,
        {
            "configured": configured,
            "accountid": acc_id,
            "account_status": account_status,
        },
    )
