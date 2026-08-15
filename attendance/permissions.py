from rest_framework.permissions import BasePermission


class IsTeacherOrHead(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.role in
            ['HEAD', 'TEACHER']
        )