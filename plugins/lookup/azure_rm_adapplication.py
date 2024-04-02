# (c) 2018 Yunge Zhu, <yungez@microsoft.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
name: azure_service_principal_attribute

requirements:
    - msgraph-sdk

author:
    - Yunge Zhu (@yungezz)

version_added: "1.12.0"

short_description: Look up Azure service principal attributes.

description:
  - Describes object id of your Azure service principal account.
options:
  azure_client_id:
    description: azure service principal client id.
  azure_secret:
    description: azure service principal secret
  azure_tenant:
    description: azure tenant
  azure_cloud_environment:
    description: azure cloud environment
  object_id:
    description: XXX
  display_name:
    description: XXX
  app_id:
    description: XXX
  attribute: 
    description: XXX
    default: app_id
  
"""

EXAMPLES = """
set_fact:
  app_id: "{{ lookup('azure_service_principal_attribute',
                         azure_client_id=azure_client_id,
                         azure_secret=azure_secret,
                         azure_tenant=azure_tenant,
                         display_name=display_name,
                         attribute=app_id) }}"
"""

RETURN = """
_raw:
  description:
    Returns object id of service principal.
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_native

try:
    from azure.cli.core import cloud as azure_cloud
    from azure.identity._credentials.client_secret import ClientSecretCredential
    import asyncio
    from msgraph import GraphServiceClient
    from msgraph.generated.applications.applications_request_builder import ApplicationsRequestBuilder
    from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
except ImportError:
    pass


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        self.set_options(direct=kwargs)

        credentials = {}
        credentials['azure_client_id'] = self.get_option('azure_client_id', None)
        credentials['azure_secret'] = self.get_option('azure_secret', None)
        credentials['azure_tenant'] = self.get_option('azure_tenant', 'common')

        options = {}
        options['object_id'] = self.get_option('object_id', None)
        options['app_id'] = self.get_option('app_id', None)
        options['display_name'] = self.get_option('display_name', None)
        options['attribute'] = self.get_option('attribute', None)

        if credentials['azure_client_id'] is None or credentials['azure_secret'] is None:
            raise AnsibleError("Must specify azure_client_id and azure_secret")

        try:
            azure_credential_track2 = ClientSecretCredential(client_id=credentials['azure_client_id'],
                                                             client_secret=credentials['azure_secret'],
                                                             tenant_id=credentials['azure_tenant'])

            client = GraphServiceClient(azure_credential_track2)

            if options['object_id']:
                applications = [asyncio.get_event_loop().run_until_complete(self.get_application(options['object_id']))]

            else:
                sub_filters = []
                if options['app_id'] :
                    sub_filters.append("appId eq '{0}'".format(options['app_id'] ))
                elif options['display_name']:
                    sub_filters.append("displayName eq '{0}'".format(options['display_name']))
                apps = asyncio.get_event_loop().run_until_complete(self.get_applications(client, sub_filters))
                applications = list(apps)
            response = [getattr(app, options['attribute']) for app in applications]

            if not response:
                return []
            return response
        except Exception as ex:
            raise AnsibleError(ex)
        return False

    async def get_application(self, _client, obj_id):
        return await self._client.applications.by_application_id(obj_id).get()

    async def get_applications(self, _client, sub_filters):	
        if sub_filters:
            request_configuration = ApplicationsRequestBuilder.ApplicationsRequestBuilderGetRequestConfiguration(
                query_parameters=ApplicationsRequestBuilder.ApplicationsRequestBuilderGetQueryParameters(
                    filter=(' and '.join(sub_filters)),
                ),
            )
            applications = await _client.applications.get(request_configuration=request_configuration)
            return applications.value
        else:
            applications_list = []
            applications = await _client.applications.get()
            for app in applications.value:
                applications_list.append(app)

            if applications.odata_next_link:
                next_link = applications.odata_next_link
            else:
                next_link = None

            while next_link:
                applications = await self._client.applications.with_url(next_link).get()
                next_link = applications.odata_next_link
                for app in applications.value:
                    applications_list.append(app)
            return applications_list

            

