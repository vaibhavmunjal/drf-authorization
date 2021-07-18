from rest_framework.permissions import (
    BasePermission,
    DjangoObjectPermissions,
)


##############################################################
##################    CUSTOM PERMISSIONS    ##################
##############################################################
class CustomPermissions(BasePermission):
    """
    Add logic to `has_permission`, `has_object_permission` for authorization
    """

    def has_permission(self, request, view):
        """Apply Custom logic to authorize

        if request.user.namename == "mvm":
            return True # Authorization Successful
        return False # Authorization Failed
        """
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """Apply Custom logic to authorize

        if obj.author.username == "mvm":
            return True # Authorization Successful
        return False # Authorization Failed
        """
        return super().has_object_permission(request, view, obj)


##############################################################
#########    CUSTOM PERMISSIONS ON REQUEST BASIS    ##########
##############################################################
class RequestPermissions(DjangoObjectPermissions):
    """
    perms_map in DjangoObjectPermissions define permissions related to 
    queired model only
    e.g.: 'POST': ['%(app_label)s.add_%(model_name)s'],

    This class provide the functionality to add custome permissions on
    perms list for request.method
    e.g.: 'POST': ['permissions_1', 'permission_2, ...],
    """

    def request_perms_map(self, request_perms_map):
        """
        Override `self.perms_map` with the `request_perms_map`
        """
        for request, permissions in request_perms_map.items():
            self.perms_map[request] = permissions

    def has_permission(self, request, view):
        # get request_perms_map from view (APIClass)
        self.request_perms_map(getattr(view, "request_perms_map", {}))
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        # get request_perms_map from view (APIClass)
        self.request_perms_map(getattr(view, "request_perms_map", {}))
        return super().has_object_permission(request, view, obj)


##############################################################
#########    CUSTOM PERMISSIONS ON ACTION BASIS    ###########
##############################################################
class ActionPermissions(BasePermission):
    """
    DRF handles permission on request.method basis,
    but there can be cases when request.method is not such useful
    e.g GET is used for list and retrieve, but list and retrieve can
    have different permissions requirements

    This class will handle the permission on action basis
    """

    # default action grant authorization to any one
    action_perms_map = {
        "create": [],
        "retrieve": [],
        "update": [],
        "partial_update": [],
        "destroy": [],
        "list": [],
    }
    authenticated_users_only = True

    def set_action_perms_map(self, action_perms_map={}):
        # Override self.action_perms_map with APIClass action_perms_map dict
        for action, permissions in action_perms_map.items():
            self.action_perms_map[action] = permissions

    def is_anonymous(self, request):
        return not request.user or (
            not request.user.is_authenticated and self.authenticated_users_only
        )

    def is_superuser(self, request):
        return request.user.is_superuser

    def has_permission(self, request, view):
        if self.is_anonymous(request):
            return False
        if self.is_superuser(request):
            return True
        self.set_action_perms_map(getattr(view, "action_perms_map"))

        # get permission mapping from APIClass
        perms = self.action_perms_map.get(getattr(view, "action", []), [])
        if not perms:
            return True
        # Check Does user have following permissions
        return request.user.has_perms(perms)

    def has_object_permission(self, request, view, obj):
        # For different requirements this function can be defined differently
        return self.has_permission(request, view)


##############################################################
############    ACTION+REQUEST PERMISSIONS     ###############
##############################################################
class RequestActionPermissions(BasePermission):
    """
    Handle Permissions on Request + action basis
    """

    perms_map = {
        "GET": [],
        "OPTIONS": [],
        "HEAD": [],
        "POST": [],
        "PUT": [],
        "PATCH": [],
        "DELETE": [],
        "create": [],
        "retrieve": [],
        "update": [],
        "partial_update": [],
        "destroy": [],
        "list": [],
    }
    permission_factor = "all"  # action, request, all
    authenticated_users_only = True

    def set_perms_map(self, perms_map={}):
        for action, permissions in perms_map.items():
            self.perms_map[action] = permissions

    def is_anonymous(self, request):
        return not request.user or (
            not request.user.is_authenticated and self.authenticated_users_only
        )

    def is_superuser(self, request):
        return request.user.is_superuser

    def has_permission(self, request, view):
        if self.is_anonymous(request):
            return False
        if self.is_superuser(request):
            return True
        self.set_perms_map(getattr(view, "perms_map"))

        perms = []
        if self.permission_factor == "all":
            perms = self.perms_map.get(getattr(request, "method"))
            perms += self.perms_map.get(getattr(view, "action", []), [])
        elif self.permission_factor == "request":
            perms = self.perms_map.get(getattr(request, "method"))
        elif self.permission_factor == "action":
            perms = self.perms_map.get(getattr(view, "action", []), [])
        if not perms:
            return True
        return request.user.has_perms(perms)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


##############################################################
###############    CHAINING PERMISSIONS     ##################
##############################################################
class ChainPermissions(BasePermission):
    """
    In many Cases it is possible that different request or action may contains
    different permissions or custom permission classes

    e.g. {
        'GET': (IsAuthenticated, IsStaff, AnyOtherCustomPermission, ...)
        'list': (IsAuthenticated, AnyOtherCustomPermission, ...)
        'retrieve': (IsAuthenticated, AnyOtherCustomPermission, ...)
    }

    In above mapping, in place of permissions list, permission classes are defined,
    The mapping shows above have same permission classes for list, retrieve
    these can be combined as well
    e.g. {
        'GET': (IsAuthenticated, IsStaff, AnyOtherCustomPermission, ...)
        ('list', 'retrieve'): (IsAuthenticated, AnyOtherCustomPermission, ...)
    }

    To handle these type of requirements(permission handling) a workaround is defined here
    """

    def _have_permissions(self, permissions_classes, request, view, obj):
        """
        Iterate over each class in permissions_classes,
        check for permissions applied in class if any permission is denied return False
        """
        for permission_class in permissions_classes:
            if obj:
                if (
                    permission_class().has_object_permission(request, view, obj)
                    is False
                ):
                    return False
            elif permission_class().has_permission(request, view) is False:
                return False
        return True

    def _verify(self, request, view, obj=None):
        """
        Get permissions_map from API Class,
        get request.method, action
        Check is any exists in permissions_map.keys() or
        exists in key of permissions_map.keys()
        # ([action in key for key in permissions_map.keys()])
        Get respective value (permissions_map[key])
        Apply the value in _have_permissions
        return the respective result
        """
        # get permissions_map (request.method/action: permissions) from APIViewClass
        permissions_map = getattr(view, "permissions_map", {})
        keys = permissions_map.keys()
        # get action from APIViewClass
        action = getattr(view, "action")
        if action is None:
            action = ""
        verified = False

        # Check Is request.method exists in keys
        if request.method in keys:
            # Check permissions for request.method
            if not self._have_permissions(
                permissions_map[request.method], request, view, obj
            ):
                # If not authorized return False
                return False
            verified = True
        # Check Is action exists in keys
        if action in keys:
            # Check permissions for action
            if not self._have_permissions(permissions_map[action], request, view, obj):
                # If not authorized return False
                return False
            verified = True
        elif not verified:
            # Iterate Over keys of permission_map
            for key in keys:
                # Workaround for tuple keys e.g. ('list', 'retrieve'): permissions
                # Check Is action or request.method exists in key
                if request.method in key or action in key:
                    # Check permissions for key
                    if not self._have_permissions(
                        permissions_map[key], request, view, obj
                    ):
                        # If not authorized return False
                        return False
        return True

    def has_permission(self, request, view):
        return self._verify(request, view)

    def has_object_permission(self, request, view, obj):
        return self._verify(request, view, obj)
