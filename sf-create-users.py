from simple_salesforce import Salesforce
import requests
import pandas as pd
import numpy as np
import copy
import json

def add_users(df):

    # Init a data structure to return
    results = pd.DataFrame(columns=["Username","Status"])
    message = ''
    error = False

    # Generic password for users' first login
    genericPassword = '<generic-user-password>'

    # What profile should we use for the new users?
    userProfileId = '<salesforce-profile-id>'
    
    # Salesforce conn info
    security_token = '<admin-user-security-token>'
    consumer_key = '<connected-app-consumer-key>'
    consumer_secret = '<connected-app-consumer-key>'
    sf_username = '<admin-sf-username>'
    sf_password = '<admin-sf-password>'
    sf_url = 'https://login.salesforce.com'

    # set parameters for SFDC login
    params = {
        "grant_type": "password",
        "client_id": consumer_key,              # Connected App: Consumer Key
        "client_secret": consumer_secret,       # Connected App: Consumer Secret
        "username": sf_username,                # Admin Username for Salesforce
        "password": sf_password+security_token  # Concat your password and your security token
    }

    #   Authenticate to Salesforce
    try:
        # make the request and get the access_token and instance_url for future posts
        r = requests.post(
            sf_url + "/services/oauth2/token", params=params)
        # store the tocken and instance url
        access_token = r.json().get("access_token")
        instanceUrl = r.json().get("instance_url")
    except Exception as e:
        message = f"Error: Could not authenticate to Salesforce as {sf_username}"
        error = True

    #   Could we authenticate to Salesforce?
    if error:

        #   Loop through the frame, and return the same message for each row
        for index, row in df.iterrows():
            results[index] = { 'status': message }
        
        #   Return the dataframe
        return results

    else :
        
        #   instantiate the sf object for easy crud operations
        sf = Salesforce(instance_url=instanceUrl, session_id=access_token)

        #   Define the default values for a new user
        defaultUserValues = {
            'Alias':'dummy',
            'DefaultGroupNotificationFrequency':'N',
            'DigestFrequency':'N',
            'Email': 'tbinns@tableau.com',
            'EmailEncodingKey': 'ISO-8859-1',
            'LanguageLocaleKey': 'en_US',
            'LastName': 'dumb',
            'LocaleSidKey': 'en_US',
            'ProfileId': userProfileId,
            'TimeZoneSidKey': 'America/New_York',
            'Username': 'dummyusertestfornow1@somethingsomething.test',
            'UserPermissionsCallCenterAutoLogin':False,
            'UserPermissionsMarketingUser':False,
            'UserPermissionsOfflineUser': False
        }

        #   Loop through the frame, and add each user
        for index, row in df.iterrows():

            #   Only make the API call if the username was supplied (it would fail anyways)
            if len(row.get('Username', '')) == 0:
                results.loc[index] = ['', 'No username provided, so skipping this row']
            else: 

                #   Define a user based on the dataframe
                user = {
                    'Alias': row.get('Alias',defaultUserValues['Alias']),
                    'DefaultGroupNotificationFrequency': row.get('DefaultGroupNotificationFrequency', defaultUserValues['DefaultGroupNotificationFrequency']),
                    'DigestFrequency': row.get('DigestFrequency', defaultUserValues['DigestFrequency']),
                    'Email': row.get('Email', defaultUserValues['Email']),
                    'EmailEncodingKey': row.get('EmailEncodingKey', defaultUserValues['EmailEncodingKey']),
                    'LanguageLocaleKey': row.get('LanguageLocaleKey', defaultUserValues['LanguageLocaleKey']),
                    'FirstName': row.get('FirstName', ''),
                    'LastName': row.get('LastName', defaultUserValues['LastName']),
                    'LocaleSidKey': row.get('LocaleSidKey', defaultUserValues['LocaleSidKey']),
                    'ProfileId': row.get('ProfileId', defaultUserValues['ProfileId']),
                    'TimeZoneSidKey': row.get('TimeZoneSidKey', defaultUserValues['TimeZoneSidKey']),
                    'Username': row.get('Username', ''),
                    'UserPermissionsCallCenterAutoLogin': row.get('UserPermissionsCallCenterAutoLogin', defaultUserValues['UserPermissionsCallCenterAutoLogin']),
                    'UserPermissionsMarketingUser': row.get('UserPermissionsMarketingUser', defaultUserValues['UserPermissionsMarketingUser']),
                    'Tableau_Username__c': row.get('Tableau_Username__c', '')
                }

                #   Define the default password
                defaultPassword = row.get('Password', genericPassword)
            
                #   Try to add the user
                try:
                    # Create the new user
                    newUser = sf.User.create(user)
                    print(f"User {user.get('Username')} (id: {newUser['id']})was added to Salesforce")

                    # Set a default password for the user
                    try:
                        # simple_salesforce doesn't handle this API call's response well
                        # so it throws a python exception, even though the API call is successful
                        sf.set_password(newUser['id'], defaultPassword)
                    except Exception as e:
                        print(f"Password set for {user.get('Username')}")
                    
                    status = 'Success'
                except Exception as e:
                    status = f"Error: {e.content[0]['message']}"

                #   Create a new row for this user
                results.loc[index] = [user.get('Username'), status]
        
        #   All done, so return the entire dataframe
        return results

def get_output_schema():
    return pd.DataFrame({
        "Username": prep_string(),
        "Status": prep_string(),
    })
