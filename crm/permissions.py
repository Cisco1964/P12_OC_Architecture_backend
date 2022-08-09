from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class ClientsPermissions(permissions.BasePermission):
    """
    Equipe gestion : tous les droits (CRUD)
    Equipe vente   : accès en lecture seule à tous les clients
                     droit de modification pour passer un prospect en client
                     droit de modification/d'accès pour tous les clients /
                     dont ils sont responsables
    Equipe support : accès en lecture seule à tous les clients
    """

    def has_permission(self, request, view):
        if request.user.role == "support":
            if request.method in permissions.SAFE_METHODS:
                return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE'] and obj.clientstatus is True:
            raise PermissionDenied("On ne peut pas modifier ou supprimer un client")
        elif request.user.role == 'gestion':
            return True
        elif request.user.role == 'vente':
            if obj.salescontact == request.user or obj.clientstatus is False:
                return True


class ContratsPermissions(permissions.BasePermission):
    """
    Equipe gestion : tous les droits (CRUD)
    Equipe vente   : accès en lecture seule à tous les contrats
                     droit de modification/d'accès pour tous les contrats dont ils sont responsables
    Equipe support : accès en lecture seule à tous les contrats
    """
    def has_permission(self, request, view):
        if request.user.role == "support":
            if request.method in permissions.SAFE_METHODS:
                return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE'] and obj.contratstatus is True:
            raise PermissionDenied("On ne peut pas modifier ou supprimer un contrat signé")
        elif request.user.role == 'vente' and obj.salescontact == request.user:
            return True
        elif request.user.role == 'gestion':
            return True


class EventsPermissions(permissions.BasePermission):
    """
    Equipe gestion : tous les droits (CRUD)
    Equipe vente   : accès en lecture seule à tous les évenements
                     droit de modification/d'accès pour tous les évènements
                     dont ils sont responsables
    Equipe support : accès en lecture seule à tous les évènements
                     droit de modification/d'accès pour tous les évènements
                     dont ils sont responsables
    """

    def has_permission(self, request, view):
        if request.user.role == "support":
            if request.method in permissions.SAFE_METHODS:
                return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE'] and obj.eventstatus is True:
            raise PermissionDenied("On ne peut pas modifier ou supprimer un évènement terminé")
        elif request.user.role == 'gestion' or request.user == obj.supportcontact or request.user == obj.contrat.salescontact:
            return True
