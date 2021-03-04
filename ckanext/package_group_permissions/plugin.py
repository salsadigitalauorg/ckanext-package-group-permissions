import ckan.authz as authz
import ckan.logic.auth as logic_auth
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.package_group_permissions import helpers

_ = toolkit._
g = toolkit.g


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

    @toolkit.chained_auth_function
    def member_create(self, next_auth, context, data_dict):
        """
        This code is largely borrowed from /src/ckan/ckan/logic/auth/create.py
        With a modification to allow users to add datasets to any group
        :param context:
        :param data_dict:
        :return:
        """
        authorized = False
        if g.controller in ['package', 'dataset'] and g.action in ['groups']:
            authorized = helpers.user_has_admin_access(include_editor_access=True)

        if not authorized:
            # Fallback to the default CKAN behaviour
            return next_auth(context, data_dict)
        else:
            return {'success': True}

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_all_groups': helpers.get_all_groups,
        }
