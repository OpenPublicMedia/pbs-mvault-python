import unittest
import json
from datetime import datetime, timedelta

from mvault import Vault, Member
from config import CALLSIGN, KEY, SECRET

MEMBER = {
    'membership_id': '000001',
    'first_name': 'Mary',
    'last_name': 'Member',
    'email': 'mmember@pbs.org',
    'offer': '123',
    'status': 'Off'
}

class MvaultApiTests(unittest.TestCase):
    """
    Tests authentication and basic API functions.

    """
    
    def test_authentication(self):
        """
        Tests if we can connect using provide credentials.

        """
        vault = Vault()
        response = vault.membership_list()
        response_json = json.loads(response.text)
        if 'errors' in response_json:
            self.assertEquals(response.status_code, 404)
            self.assertEqual(response_json['errors'], "No memberships exist for this station")
        else:
            self.assertTrue(response.status_code, 200)
            self.assertTrue('objects' in response_json)

    def test_put_member(self):
        """
        Tests if we can put a member record into the Membership Vault.

        """
        vault = Vault()
        member = Member()
        member.parse(MEMBER)
        member.start_date = datetime.now()
        member.expire_date = datetime.now() + timedelta(weeks=52)

        response = vault.membership_update(member)
        self.assertEqual(response.status_code, 200)

    def test_get_member(self):
        """
        Tests if we can get a member record we put into the Membership Vault.

        """
        vault = Vault()
        member = Member()
        member.parse(MEMBER)
        member.start_date = datetime.now()
        member.expire_date = datetime.now() + timedelta(weeks=52)

        response = vault.membership_update(member)
        self.assertEqual(response.status_code, 200)

        response = vault.membership_get(member.membership_id)
        self.assertEquals(response.status_code, 200)

