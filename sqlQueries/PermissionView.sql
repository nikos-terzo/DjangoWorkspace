-- SQLite
SELECT object_pk, username, codename, name
FROM guardian_userobjectpermission
LEFT JOIN auth_permission ON guardian_userobjectpermission.permission_id = auth_permission.id
LEFT JOIN auth_user ON guardian_userobjectpermission.user_id = auth_user.id;
