'''
Created on May 14, 2019

@author: KJNETHER

Most of this will get replaced when deployed to pipeline as secrets
could get retrieved from env vars.
'''

import logging
import os.path
import pkgutil

import pytest

import parameterized.fixtures.setup_fixtures
from bcdc_apitests.fixtures.load_config import ckan_apitoken

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# declare the namespace to be used by the import if it is optionally imported
DBCSecrets = None  # pylint: disable=invalid-name


# pylint: disable=redefined-outer-name


@pytest.fixture()
def import_dbcsecrets():  # @DontTrace
    '''
    Optional import of DBCSecrets, imports if it can be found
    '''
    global DBCSecrets  # pylint: disable=global-statement

    # using the DBC Secrets module if it exists, otherwise will rely on
    # environment variables
    dbc_secrets_exists = pkgutil.find_loader('DBCSecrets')
    logger.debug('dbc_secrets_exists: %s', dbc_secrets_exists)
    if dbc_secrets_exists:
        # can find the package therefor import it
        import DBCSecrets.GetSecrets  # @UnresolvedImport pylint: disable=import-error
        logger.debug('IMPORTED DBCSecrets')
        if 'GetSecrets' in dir(DBCSecrets):
            logger.debug('SUCCESS FOUND DBCSECRETS.GetSecrets')
    yield DBCSecrets


@pytest.fixture()
def secret_file():
    '''
    :return: full path to the secret file that arms the tests
    '''
    scrt_file = None
    if 'BCDC_URL' not in os.environ:

        scrt_file = os.path.join(os.path.dirname(__file__), '..', '..', 'secrets',
                                 'secrets.json')
        scrt_file = os.path.realpath(scrt_file)
        logger.debug("secret file path: %s", scrt_file)
    logger.debug("yielding: %s", scrt_file)
    yield scrt_file


@pytest.fixture()
def env():
    '''
    :return: the env that the test is set up to run in,
             this value is used by secrets to determine what
             keys to pull from pmp, resources, host names etc
    '''
    return 'DLV'


@pytest.fixture()
def ckan_host(secret_file, env, import_dbcsecrets):
    '''
    gets the host for the given env
    '''
    # for developing going to use key value pairs, once integrated
    # with jenkins job can configure so that secrets are retrieved from
    # pmp.
    # code below demos how that might work
    #
    # integration with openshift, retrieve these from env vars
    logger.debug('DBCSecrets: %s', DBCSecrets)
    logger.debug('dir: %s', dir())
    logger.debug('dir(DBCSecrets): %s', dir(DBCSecrets))
    logger.debug("Module DBCSecrets can be found: %s",
                 (('DBCSecrets' in dir()) and
                  'GetSecrets' in dir(DBCSecrets)))
    logger.debug('import_dbcsecrets: %s', import_dbcsecrets)
    if 'BCDC_URL' in os.environ:
        host = None
        logger.info("Env Var BCDC_URL is set: %s", os.environ['BCDC_URL'])
    elif 'GetSecrets' in dir(DBCSecrets):
        # if the DBCSecrets module was imported
        logger.debug("using secrets file: %s", secret_file)
        creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
        misc_params = creds.getMiscParams()

        host_key = '{0}_HOST'.format(env)
        logging.debug("host_key: %s", host_key)
        host = misc_params.getParam(host_key)
    else:
        msg = 'unable to retrieve secrets either using the environment %s or ' + \
              'from the secrets file %s'
        msg = msg.format('BCDC_URL', secret_file)
        raise SecretsNotFound(msg)
    return host


@pytest.fixture()
def ckan_url(ckan_host):
    '''
    returns ckan url for the env
    '''
    # for now hard coding the env to DLV, could be TST, PRD
    # env = 'DLV'
    if 'BCDC_URL' in os.environ:
        url = os.environ['BCDC_URL']
    else:
        url = 'https://{0}'.format(ckan_host)
    return url


@pytest.fixture()
def ckan_superadmin_apitoken(secret_file, env, import_dbcsecrets):
    '''
    Gets the ckan superadmin api token.  Will use this token to generate other 
    users.
    '''
    if 'BCDC_API_KEY' in os.environ:
        token = os.environ['BCDC_API_KEY']
    elif 'GetSecrets' in dir(DBCSecrets):
        logger.debug("GetSecrets module exists, secrets file: %s", secret_file)
        creds = DBCSecrets.GetSecrets.CredentialRetriever(secretFileName=secret_file)
        misc_params = creds.getMiscParams()
        token_key = '{0}_TOKEN'.format(env)
        logger.debug("token_key: %s", token_key)
        token = misc_params.getParam(token_key)
    else:
        logger.debug("secret file: %s", secret_file)
        msg = 'unable to retrieve secrets either using the environment %s or ' + \
              'from the secrets file %s'
        msg = msg.format('BCDC_URL', secret_file)
        raise SecretsNotFound(msg)
    return token

@pytest.fixture()
def ckan_superadmin_auth_header(ckan_superadmin_apitoken):
    '''
    authorization header using the super admin api token.  
    
    super admin is used by fixtures to do setup and tear down.  for the 
    most part testing will use a different token.
    '''
    api_headers = {'X-CKAN-API-KEY': ckan_superadmin_apitoken,
                   'content-type': 'application/json;charset=utf-8'}
    return api_headers

@pytest.fixture()
def ckan_apitoken(user_label_fixture, ckan_superadmin_apitoken):
    '''
    :param user_label_fixture:  identifies the user that should be 
                                used for this test
    
    '''
    # user_label_fixture will be populated with the values in 
    # the property test_users from the testParams.json file.
    # they are keywords: admin, editor, viewer
    logger.debug("user_label_fixture: %s", user_label_fixture)
    # depending on the usertype, use craigs boostrapping code to 
    # add new users
    
    # for now to make work just continue to use super admin 
    # api tokens
    return ckan_superadmin_apitoken

@pytest.fixture()
def ckan_auth_header(ckan_apitoken):
    api_headers = {'X-CKAN-API-KEY': ckan_apitoken,
                   'content-type': 'application/json;charset=utf-8'}
    return api_headers

class SecretsNotFound(Exception):
    """
    Base class for other exceptions
    """

    def __init__(self, message):  # pylint: disable=super-init-not-called
        self.message = message