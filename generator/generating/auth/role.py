from typing import List
from generating.auth.permission import Permission


class Role(object):
  def __init__(self, permissions:List[Permission]=None):
    self.permissions = []
    if isinstance(permissions, List[Permission]):
      self.permissions = permissions

  def add_permission(self, permission:Permission=None):
    self.permissions.append(permission)
