# ckanext-package-group-permissions
A CKAN extension to allow any user with admin or editor role in an organisation to assign datasets in their organisation to any group in CKAN.

## Our use case

We wanted the ability for any user with admin or editor role in an organisation to be able to assign datasets in their organisation to any group in CKAN.

Previously, this was handled manually, i.e. each admin/editor user was assigned as an admin of each group in CKAN by adding them via the API. This process was very time consuming as the number of admins/editors and groups increased.

We tried implementing the suggestions outlined in this Stack Overflow question: https://stackoverflow.com/questions/37279610/ckan-package-group-permissions - however we were unable to get it working as desired.

## Our solution

Our solution ended up being a little simpler for our requirements:

### Override CKAN `member_create` function

The overridden function is largely based on the core CKAN `member_create` function, with an additional check to see if the user is an admin or editor of the organisation that owns the dataset.

### Template overrides

This solution also requires some CKAN templates to be overridden:

`templates/package/group_list.html`

Overridden to display **all** groups to the user **if** the user has `package_update` permission for the dataset.

If the user does not have `package_update` permission - it falls back to the CKAN default of displaying only the groups that user is assigned to.

`templates/group/snippets/group_item.html`

Overridden to display the **delete** button on a group assigned to the dataset if the user has `member_delete` permission for the group.

This also supports the default CKAN behaviour to display the delete button on any groups that user is assigned to.
