from flask import request
import urlparse
import requests
import json

##https://iiko.biz:9900/api/0/auth/access_token?user_id=hakatonVk&user_secret=hakatonTest

class Iiko_settings:
    access_token = ''
    commonRequestTimeout = 5

def iiko_Get(params):
    #global access_token

    url = "http://localhost:3000/"
    url = "https://iiko.biz:9900/api/0/"

    if Iiko_settings.access_token == '':
        token_params = getToken()
        r = requests.get(url + token_params['appendix_url'] + '?', token_params['params'])
        Iiko_settings.access_token = json.loads(r.content)
        print 'new access_token: ' + Iiko_settings.access_token

    if Iiko_settings.access_token != '':
        r = requests.get(url + params['appendix_url'] + '?', params['params'])
        print 'Request:\n\turl: ' + r.url + '\n\tresponse code: ' + str(r.status_code)
        if r.headers['Content-Type'] == 'application/json':
            try:
                print json.loads(r.content)
            except Exception as e:
                print e.message


def getToken():
    url = "auth/access_token"
    data = {
        "user_secret" : "hakatonTest",
        "user_id" : "hakatonVk"
    }
    return {"appendix_url" : url, "params" : data}

#list of organizations
def getOrganizations(requestTimeout = Iiko_settings.commonRequestTimeout):
    # requestTimeout [seconds]
    url = "organization/list"
    data = {
        "access_token" : Iiko_settings.access_token,
        "request_timeout" : "00:00:0" + str(requestTimeout)
    }
    return {"appendix_url" : url, "params" : data}

#info about 1 organization
def getOrganization(organizationID, requestTimeout = Iiko_settings.commonRequestTimeout):
    # requestTimeout [seconds]
    url = "organization/" + organizationID
    data = {
        "access_token" : Iiko_settings.access_token,
        "request_timeout" : "00:00:0" + requestTimeout
    }
    return {"appendix_url" : url, "params" : data}

#get list of menu items for specific organization
def getMenu(revision):
    url = "nomenclature/" + organizationID
    data = {
        "access_token" : Iiko_settings.access_token,
        "revision" : revision
    }
    return {"appendix_url" : url, "params" : data}

#get list of cities for specific organization
def getGeoAddresses():
    url = "cities/cities" + organizationID
    data = {
        "access_token" : Iiko_settings.access_token,
        "organization" : organizationID
    }
    return {"appendix_url" : url, "params" : data}

#example
#iiko_Get(params = getOrganizations())
