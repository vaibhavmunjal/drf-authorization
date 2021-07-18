# drf-authorization
Different ways to handle authorizations in Django restframework
----
----


DRF Provides classes `BasePermission` for custom permissions logic, Classes `DjangoModelPermissions`, `DjangoObjectPermissions` to deal with authorization, but these classes only checks for queryset model(queryset.model) permissions.

[permissions.py](./app/api/permissions/permissions.py) provides the functionality for:
* List of permissions to deal on request, action basis
* List of custom Permission Class for any particular request or action


DRF default class
```py
class DjangoModelPermissions:
    perms_map = {
        "GET": [],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
    ...
    ...
```

The Above deals only with the model permission i.e
```py
model = Blog
queryset = Blog.Objects.all()
# the perms_map will become
perms_map = {
    "GET": [],
    "OPTIONS": [],
    "HEAD": [],
    "POST": ["app.add_blog"],
    "PUT": ["app.change_blog"],
    "PATCH": ["app.change_blog"],
    "DELETE": ["app.delete_blog"],
}
```


* To Check for list of permission on request, action basis

  * On Request Basis
  ```py
  permission_classes = (RequestPermissions,)
  request_perms_map = {
      "GET": ["app.view_blog"] # To Check for list of Permissions on get request
  }
  ```

  * On Action Basis
  ```py
    permission_classes = (ActionPermissions,)
    action_perms_map = {
        "list": ["app.can_view_blog"],
    }
  ```

  * On Request and Action Basis
  ```py
    permission_classes = (RequestActionPermissions,)
    perms_map = {
        "GET": ["app.view_blog"],
        "list": ["app.can_view_blog"]
    }
  ```



* List of classes to check for permission on any specific request or action

```py
permission_classes = (ChainPermissions,) # get/operate on permissions_map
request_perms_map = { # List of permission to deal on RequestPermissions
    "GET": ["app.view_blog"]
}
action_perms_map = { # List of permission to deal on ActionPermissions
    "list": ["app.view_blog"]
}
permissions_map = {
    "GET": (RequestPermissions,),
    "list": (ActionPermissions, CustomPermissions,)  # To deal with list of custom permission for specific request/action
}
```
