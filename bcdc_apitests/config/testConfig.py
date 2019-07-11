'''
Global test properties, 

Storing these external to the fixtures so they can be accessed more
easily by helper functions
'''

import getpass

# first three initials of the current test user, using this to keep
# test objects unique allowing multiple dev's to work on test developemnt
# without encountering object naming conflicts
TEST_USER = getpass.getuser()[0:3].lower()

# all test objects created in ckan should have this prefix appended to them
TEST_PREFIX = "zzztest"

# The directory where the various .json files that contain test data
# are located
TEST_DATA_DIRECTORY = "test_data"
TEST_PARAMETERS_FILE = 'testParams.json'
TEST_USER_CONFIG = "userConfig.json"

# test org name
TEST_ORGANIZATION = '{0}_{1}_testorg'.format(TEST_PREFIX, TEST_USER)

# test package name
TEST_PACKAGE = '{0}_{1}_testpkg'.format(TEST_PREFIX, TEST_USER)

# test resource name
TEST_RESOURCE = '{0}_{1}_testresource'.format(TEST_PREFIX, TEST_USER)

# path to the rest api
BCDC_REST_DIR = "/api/3/action"

# user configuration, contains all the informaiton necessary to create these
# new users.
TEST_ADMIN_USER = 'admin'
TEST_EDITOR_USER = 'editor'
TEST_VIEWER_USER = 'viewer'

# default test passwords will need to be retrieved as a secret
USER_CONFIG = {TEST_EDITOR_USER:
                {'email': 'test_editor@gov.bc.ca',
                 'role': 'editor'}, 
               TEST_VIEWER_USER: 
                {'email': 'test_viewer@gov.bc.ca',
                 'role': 'viewer'},
               TEST_ADMIN_USER: 
                {'email': 'test_admin@gov.bc.ca',
                 'role': 'admin'},
               }
