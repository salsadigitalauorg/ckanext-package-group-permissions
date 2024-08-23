import ckan.plugins.toolkit as toolkit


def is_user_sysadmin(user=None):
    """Returns True if authenticated user is sysadmim
    :rtype: boolean
    """
    if user is None:
        user = toolkit.g.userobj
    return user is not None and user.sysadmin


def user_has_admin_access(include_editor_access=False):
    user = toolkit.g.userobj
    # If user is "None" - they are not logged in.
    if user is None:
        return False
    if is_user_sysadmin(user):
        return True

    groups_admin = user.get_groups('organization', 'admin')
    groups_editor = user.get_groups('organization', 'editor') if include_editor_access else []
    groups_list = groups_admin + groups_editor
    organisation_list = [g for g in groups_list if g.type == 'organization']
    return len(organisation_list) > 0


def get_all_groups():
    groups = toolkit.get_action('group_list')(
        data_dict={'include_dataset_count': False, 'all_fields': True})
    pkg_group_ids = set(group['id'] for group
                        in toolkit.g.pkg_dict.get('groups', []))
    return [[group['id'], group['display_name']]
            for group in groups if
            group['id'] not in pkg_group_ids]

