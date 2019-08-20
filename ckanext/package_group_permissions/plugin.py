from ckan.common import _, c

import ckan.authz as authz
import ckan.logic.auth as logic_auth
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import helpers


class PackageGroupPermissionsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'package_group_permissions')

    # IAuthFunctions
    def get_auth_functions(self):
        auth_functions = {
            'member_create': self.member_create
        }
        return auth_functions

    def member_create(self, context, data_dict):
        """
        This code is largely borrowed from /src/ckan/ckan/logic/auth/create.py
        With a modification to allow users to add datasets to any group
        :param context:
        :param data_dict:
        :return:
        """
        group = logic_auth.get_group_object(context, data_dict)
        user = context['user']

        # User must be able to update the group to add a member to it
        permission = 'update'
        # However if the user is member of group then they can add/remove datasets
        if not group.is_organization and data_dict.get('object_type') == 'package':
            permission = 'manage_group'

        if c.controller in ['package', 'dataset'] and c.action in ['groups']:
            authorized = helpers.user_has_admin_access(include_editor_access=True)
            # Fallback to the default CKAN behaviour
            if not authorized:
                authorized = authz.has_user_permission_for_group_or_org(group.id,
                                                                        user,
                                                                        permission)
        else:
            authorized = authz.has_user_permission_for_group_or_org(group.id,
                                                                    user,
                                                                    permission)
        if not authorized:
            return {'success': False,
                    'msg': _('User %s not authorized to edit group %s') %
                           (str(user), group.id)}
        else:
            return {'success': True}

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_all_groups': helpers.get_all_groups,
        }
