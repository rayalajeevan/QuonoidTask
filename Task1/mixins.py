from django.conf import settings
import requests
class ApiMixins():
    def __init__(self):
        pass

    def get_activities(self,user_type):
        try:
            reqObj=requests.get(settings.BORED_BASE_URL+settings.TYPE_ENDPOINT.format(user_type))
            if reqObj.status_code==200:
                return reqObj.json()
            print("hello")
            return None
        except Exception as exc:
            print(exc)
            return None
