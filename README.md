# Sync users from Tableau Server to Salesforce
This project provides an example of how to automatically sync users from a Tableau Server to a Salesforce org.  This workflow is for people who manage their users in Tableau Server, and want those users to be automatically created in their Salesforce org. The entire workflow involves several pieces, but this project includes just the python script (orange) that adds users to Salesforce.
![Overview](https://github.com/takashibinns/tabpy-tableau-sf-user-sync/blob/main/screenshots/Workflow.png?raw=true)


## Python Script variables
In order for the python script to run, you will need to update the following variables
```python
# Generic password for users' first login (they will get prompted to enter a new password)
genericPassword = '<generic-user-password>'

# What profile should we use for the new users? (must be the salesforce ID of the profile)
userProfileId = '<salesforce-profile-id>'

# Salesforce conn info (details used to authenticate to your salesforce org)
security_token = '<admin-user-security-token>'
consumer_key = '<connected-app-consumer-key>'
consumer_secret = '<connected-app-consumer-key>'
sf_username = '<admin-sf-username>'
sf_password = '<admin-sf-password>'
```

## Prep 
## Requirements

### Tableau Server w/ Data Management Add-on
Since the users come from Tableau Server, this is a requirement.  The users get pushed to Salesforce from a Tableau Prep flow, and that requires Data Management Add-on to schedule

### Admin account in Salesforce
In order to authenticate to Salesforce (and add the new users), you will need two things from Salesforce:
* **Admin User** - You will need to provide the username, password, and security token of a user who has permissions to create users
* **Connected App** - Create a connected app, that can be run by the above admin user.  You will need the connected app's consumer secret + key

### TabPy Server
The Tableau Prep flow leverages a python script to make the Salesforce REST API calls for adding new users.  In order to do this, you need a TabPy server running that executes the python script.  Check out the [TabPy github page](https://github.com/tableau/TabPy), for more details on how to set this up.  For my example, I deployed via Heroku.
