from typing import List
from generating.auth.permission import Permission, PermissionType
from generating.auth.role import Role


class AdminRole(Role):
  def __init__(self, permissions: List[Permission] = [Permission(PermissionType.SUPER)]):
    super().__init__(permissions)
