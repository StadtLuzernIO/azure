#!/usr/bin/python
#
# Copyright (c) 2024 Raphael Mehr, Raphael Bächi
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: 
short_description: Manage Azure AD Conditional Access Policies
description:
    - This module allows you to manage Azure Active Directory Conditional Access Policies.
    - Conditional Access policies can be used to apply access controls for cloud apps based on various conditions.
author: Your Name
options:
    display_name:
        description:
            - The display name of the Conditional Access Policy.
        required: true
    
    policy_id:
        description:
            - The policy id of the Conditional Access Policy.
    policy_state:
        description:
            - The state of the Conditional Access Policy.
        choices:
            - enabled
            - disabled
            - enabledForReportingButNotEnforced
        required: false
        default: "enabledForReportingButNotEnforced"
    conditions:
        description:
            - The conditions under which the policy will be applied.
        type: dict
        suboptions:
           users:
                description:
                    - Users to whom the policy will be applied.
                type: dict
                suboptions:
                    include_users:
                        description:
                            - List of included users.
                        type: list
                        elements: str
                    exclude_users:
                        description:
                            - List of excluded users.
                        type: list
                        elements: str
                    include_groups:
                        description:
                            - List of included groups.
                        type: list
                        elements: str
                    exclude_groups:
                        description:
                            - List of excluded groups.
                        type: list
                        elements: str
                    include_roles:
                        description:
                            - List of included roles.
                        type: list
                        elements: str
                    exclude_roles:
                        description:
                            - List of excluded roles.
                        type: list
                        elements: str
                    include_guestorexternaluser:
                        description:
                            - List of included guests or external users.
                        type: list
                        elements: str
                    exclude_guestorexternaluser:
                        description:
                            - List of excluded guests or external users.
                            - Choice of "internalGuest", "b2bCollaborationGuest", "b2bCollaborationMember", "b2bDirectConnectUser", "otherExternalUser", "serviceProvider"
                        type: list
                        elements: str
            applications:
                description:
                    - Applications to which the policy will be applied if client_app_types is cloudapps.
                type: dict
                suboptions:
                    include_applications:
                        description:
                            - List of included applications.
                        type: list
                        elements: str
                    exclude_applications:
                        description:
                            - List of excluded applications.
                        type: list
                        elements: str
                    application_filter:
                        description:
                            - Filter rule for applications.
                        type: list
                        elements: str
                    include_user_actions:
                        description:
                            - List of user actions to include.
                        type: list
                        elements: str
                    include_authentication_context_class_references:
                        description:
                            - User actions to include. Supported values are urn:user:registersecurityinfo and urn:user:registerdevice
                        type: list
                        elements: str
            user_risk_levels:
                description:
                    - List of user risk levels.
                    - Choises are "high", "medium", "low" and "none"
                type: list
                elements: str
            sign_in_risk_levels:
                description:
                    - List of risk levels for sign-in events.
                    - Choises are "high", "medium", "low" and "none"
                type: list
                elements: str
            platforms:
                description:
                    - Platforms to which the policy will be applied.
                type: dict
                suboptions:
                    include_platforms:
                        description:
                            - List of included device platforms.
                            - Possible values are "android", "iOS", "windows", "windowsPhone", "macOS", "linux", "all"
                        type: list
                        elements: str
                    exclude_platforms:
                        description:
                            - List of excluded device platforms.
                            - Possible values are "android", "iOS", "windows", "windowsPhone", "macOS", "linux", "all"
                        type: list
                        elements: str
            locations:
                description:
                    - Locations to which the policy will be applied.
                type: dict
                suboptions:
                    include_locations:
                        description:
                            - List of included locations.
                            - Location IDs in scope of policy unless explicitly excluded, All, or AllTrusted
                        type: list
                        elements: str
                    exclude_locations:
                        description:
                            - List of excluded locations.
                            - Location IDs or AllTrusted.
                        type: list
                        elements: str
            client_app_types:
                description:
                    - Client application types included in the policy.
                    - Possible values are "all", "browser", "mobileAppsAndDesktopClients", "exchangeActiveSync", "easSupported" and "other".
                type: list
                elements: str
            device_filter:
                description:
                    - Rule for device filter.
                type: list
                elements: str
    grant_controls:
        description:
            - Controls specifying the access granted if the conditions are met.
        type: dict
        suboptions:
            operator:
                description:
                    - Defines the relationship of the grant controls.
                    - Possible values "AND", "OR"
                type: str
            built_in_controls:
                description:
                    - List of values of built-in controls required by the policy
                    - Possible values "block", "mfa", "compliantDevice", "domainJoinedDevice", "approvedApplication", "compliantApplication", "passwordChange"
                type: list
                elements: str
            terms_of_use:
                description:
                    - Which Terms of Use are activated.
                type: list
                elements: str
            authentication_strength:
                description:
                    - The authenticationStrength property
                type: list
                elements: str
            custom_authentication_factors:
                description:
                    - List of custom controls IDs required by the policy
                type: list
                elements: str
    session_controls:
        description:
            - Controls specifying the access session.
        type: dict
        suboptions:
            standard_controls:
                description:
                    - Standard session controls.
                type: list
                elements: str
            sign_in_frequency:
                description:
                    - Signin frequency session control.
                type: dict
                suboptions:
                    frequency_interval:
                        description:
                            - The possible values are "timeBased", "everyTime"
                        type: str
                    type:
                        description:
                            - Possible values are "days", "hours"
                        type: str
                    value:
                        description:
                            - The number of days or hours
                        type: int
'''
EXAMPLES = '''
- name: Set new conditional access policy
  azure.azcollection.azure_rm_conditional_access:
    display_name: "100 - <RING> - Admin protection - All apps: Require MFA For admins"
    policy_id: "9b895d92-2cd3-55c7-9d02-a6ac2d5ea44"
    policy_state: "enabled"
    conditions:
      users:
        exclude_groups: "ExclusionTempGroup, ExclusionPermGroup, EmergencyAccessAccountsGroup, SynchronizationServiceAccountsGroup"
        include_roles: "9b895d92-2cd3-44c7-9d02-a6ac2d5ea5c3, cf1c38e5-3621-4004-a7cb-879624dced7c"
    grant_controls:
      operator: "OR"
      built_in_controls: "mfa"
    
'''