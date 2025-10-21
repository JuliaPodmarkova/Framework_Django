from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Полн. доступ админу, только чтение всем остальным."""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_staff
        )


class IsWatcherOrAdminToChangeWorkplace(BasePermission):
    """
    Позволяет поменять рабочее место только смотрителю или админу.
    (реализуй логику по ролям, ниже пример, если у юзера специальное поле profile.is_watcher)
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        # Например: watcher должен иметь свойство is_watcher в профиле
        if hasattr(request.user, "profile") and getattr(
            request.user.profile, "is_watcher", False
        ):
            return True
        return False
