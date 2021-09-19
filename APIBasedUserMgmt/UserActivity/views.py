from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from UserActivity.models import UsersActivity, UserProfile


class UserActivityViewset(viewsets.ViewSet):
    """
    (GET) Api for all User Activities.
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        response = dict()
        user_dict = dict()
        response["ok"] = True
        response["members"] = list()
        all_users = UserProfile.objects.all()
        for user in all_users:
            user_activity = UsersActivity.objects.filter(user=user)
            if user_activity:
                user_dict = {
                    "id": user_activity[0].user.id,
                    "real_name": user_activity[0].user.real_name,
                    "tz": user_activity[0].user.time_zone,
                }
                user_dict['activity_periods'] = list()
                for all_activity in user_activity:
                    user_dict['activity_periods'].append(
                        all_activity.extra_feild)
                response['members'].append(user_dict)
        return Response(response)
