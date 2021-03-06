# Generated by Django 2.2.11 on 2020-04-27 16:53

from django.db import IntegrityError, migrations, transaction


def forwards(apps, schema_editor):
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    SocialAccount = apps.get_model("socialaccount", "SocialAccount")

    # Find existing SocialApp for the salesforce-production provider.
    # Change it to use the salesforce provider and client id/secret from settings.
    try:
        app = SocialApp.objects.get(provider="salesforce-production")
    except SocialApp.DoesNotExist:
        pass
    else:
        app.provider = "salesforce"
        app.name = "Salesforce"
        app.client_id = "-"
        app.secret = ""
        app.save()

        # Update provider on existing salesforce-production accounts
        SocialAccount.objects.filter(provider="salesforce-production").update(
            provider="salesforce"
        )

        # Update provider on salesforce-test and salesforce-custom accounts unless they are duplicates
        for account in SocialAccount.objects.filter(
            provider__in=("salesforce-test", "salesforce-custom")
        ):
            try:
                with transaction.atomic():
                    account.provider = "salesforce"
                    account.save()
            except IntegrityError:
                account.delete()

        # Remove the old SocialApps (and any related tokens)
        for provider_name in ("salesforce-test", "salesforce-custom"):
            try:
                other_app = SocialApp.objects.get(provider=provider_name)
            except SocialApp.DoesNotExist:
                pass
            else:
                other_app.delete()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0084_on_delete"),
    ]

    operations = [migrations.RunPython(forwards, backwards)]
