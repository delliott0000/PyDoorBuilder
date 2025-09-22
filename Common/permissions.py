from dataclasses import dataclass, fields

__all__ = ("Permissions", "ADMIN_PERMISSIONS")


@dataclass(kw_only=True, frozen=True, slots=True)
class Permissions:
    create: bool = False

    preview_safe: bool = False
    preview_company: bool = False
    preview_global: bool = False

    view_safe: bool = False
    view_company: bool = False
    view_global: bool = False

    acquire_safe: bool = False
    acquire_company: bool = False
    acquire_global: bool = False

    update_safe: bool = False
    update_company: bool = False
    update_global: bool = False

    generate_safe: bool = False
    generate_company: bool = False
    generate_global: bool = False

    delete_safe: bool = False
    delete_company: bool = False
    delete_global: bool = False

    reassign_safe: bool = False
    reassign_company: bool = False
    reassign_global: bool = False


ADMIN_PERMISSIONS = Permissions(**{key.name: True for key in fields(Permissions)})
