from .models import pcloudAccount
from datetime import datetime
from utility.pcloud import login, endSession


def getAuth():
    account = pcloudAccount.objects.first()
    if account:
        today = datetime.now().date()
        diff = (today - account.lastUpdate).days
        if diff > 20:
            response = login(account.email, account.password)
            if response != 400:
                endSession(account.auth)
                account.auth = response
                account.save()
                return response
            else:
                return None
        else:
            return account.auth
    return None
