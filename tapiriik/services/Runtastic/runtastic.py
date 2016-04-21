from tapiriik.settings import WEB_ROOT
from tapiriik.services.service_base import ServiceAuthenticationType, ServiceBase
from tapiriik.services.interchange import UploadedActivity, ActivityType, ActivityStatistic, ActivityStatisticUnit
from tapiriik.services.api import APIException, UserException, UserExceptionType, APIExcludeActivity
from tapiriik.services.pwx import PWXIO
from lxml import etree
import json
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
import dateutil.parser
import requests
import logging
import re

logger = logging.getLogger(__name__)

class RuntasticService(ServiceBase):
    ID = "runtastic"
    DisplayName = "Runtastic"
    DisplayAbbreviation = "RC"
    AuthenticationType = ServiceAuthenticationType.UsernamePassword
    RequiresExtendedAuthorizationDetails = True
    ReceivesStationaryActivities = False

    def WebInit(self):
        self.UserAuthorizationURL = WEB_ROOT + reverse("auth_simple", kwargs={"service": self.ID})

    def Authorize(self, email, password):
        from tapiriik.auth.credential_storage import CredentialStore
        data = {"user[email]": email, "user[password]": password, "authenticity_token": ""}

        resp = requests.post("https://www.runtastic.com/en/d/users/sign_in.json", data=data)
        # TODO Check success atribute of api return, motivato service looks like our service
        # TODO Save session and cookie
        if resp.status_code != 200:
            raise APIException("Invalid login")

        user_id = resp.json()["current_user"]["id"]

        return (user_id, {}, {"Email": CredentialStore.Encrypt(email), "Password": CredentialStore.Encrypt(password)})

    def DownloadActivityList(self, serviceRecord, exhaustive=False):
        # TODO not implemented
        pass

    def DownloadActivity(self, serviceRecord, activity):
        # TODO not implemented
        pass

    def UploadActivity(self, serviceRecord, activity):
        # TODO not implemented
        pass

    def RevokeAuthorization(self, serviceRecord):
        # nothing to do here...
        pass

    def DeleteCachedData(self, serviceRecord):
        # nothing cached...
        pass