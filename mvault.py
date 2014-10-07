#!/usr/bin/env python
"""
    Module for uploading and managing membership information on PBS's Membership Vault.

.. moduleauthor:: Rob Vincent <rvincent@opb.org>

    --------------------------

    The MIT License (MIT)

    Copyright (c) 2014 Oregon Public Broadcasting

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

"""
import requests
import json
import argparse

from config import BASE_ENDPOINT, CALLSIGN, KEY, SECRET


class Member():
    """
    Model for a member record for PBS's Membership Vault.

    """

    def __init__(self):
        self.create_date = None         # read-only, datetime
        self.update_date = None         # read-only
        self.activation_date = None     # read-only
        self.start_date = None          # required, when the membership starts
        self.expire_date = None         # required, when the membership expires

        self.membership_id = ''         # required, the member ID we define for the member
        self.offer = ''                 # required, identifier of an offer we define
        self.first_name = ''            # required
        self.last_name = ''             # required
        self.email = ''                 # optional, email address of member
        self.notes = ''                 # information about membership
        self.additional_metadata = ''   # metadata we supply and use
        self.status = 'On'              # status of membership, On or Off
        self.provisional = False        # boolean, temporary access waiting for verification

    @staticmethod
    def _fetch_value(dict, key, default):
        if key in dict:
            return dict[key]
        else:
            return default

    @staticmethod
    def _iso8661(date):
        return date.isoformat("T")[:-7] + "Z"

    def __str__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.membership_id)

    def parse(self, dict):
        try:
            self.create_date = self._fetch_value(dict, 'create_date', None)
            self.update_date = self._fetch_value(dict, 'update_date', None)
            self.activation_date = self._fetch_value(dict, 'activation_date', None)
            self.start_date = self._fetch_value(dict, 'start_date', None)
            self.expire_date = self._fetch_value(dict, 'expire_date', None)

            self.membership_id = self._fetch_value(dict, 'membership_id', '')
            self.offer = self._fetch_value(dict, 'offer', '')
            self.first_name = self._fetch_value(dict, 'first_name', '')
            self.last_name = self._fetch_value(dict, 'last_name', '')
            self.email = self._fetch_value(dict, 'email', '')
            self.notes = self._fetch_value(dict, 'notes', '')
            self.additional_metadata = self._fetch_value(dict, 'additional_metadata', '')
            self.status = self._fetch_value(dict, 'status', 'On')
            self.provisional = self._fetch_value(dict, 'provisional', False)
            return True

        except Exception:
            return False

    def payload(self):
        return json.dumps({
            'offer': self.offer,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'notes': self.notes,
            'additional_metadata': self.additional_metadata,
            'status': self.status,
            'provisional': self.provisional,
            'start_date': self._iso8661(self.start_date),
            'expire_date': self._iso8661(self.expire_date)
        })


class Vault():
    """
    Interface for PBS's Membership Vault.

    """

    def __init__(self, **kwargs):
        self.callsign = kwargs.get('callsign', CALLSIGN)
        self.key = kwargs.get('key', KEY)
        self.secret = kwargs.get('secret', SECRET)

    def _get(self, endpoint, membership_id=None):
        if membership_id:
            return requests.get(BASE_ENDPOINT + '/%s/%s/%s' % (self.callsign, endpoint, membership_id), auth=(self.key, self.secret))
        else:
            return requests.get(BASE_ENDPOINT + '/%s/%s/' % (self.callsign, endpoint), auth=(self.key, self.secret))

    def _put(self, endpoint, arg, payload):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.put(BASE_ENDPOINT + '/%s/%s/%s' % (self.callsign, endpoint, arg), 
            data=payload, auth=(self.key, self.secret), headers=headers)

    def membership_list(self):
        """
        Pull a list of the station member records in the Membership Vault.

        :returns: list of Member records.

        """
        return self._get('memberships')

    def membership_update(self, member):
        """
        Creates or updates a member record in the Membership Vault.

        :param member: Member record
        :returns: Result of update.

        """
        return self._put('memberships', member.membership_id, member.payload())

    def membership_get(self, membership_id):
        """
        Gets a member record by ID.

        :param membership_id: Station specified membership ID
        :returns: Member object

        """
        return self._get('memberships', membership_id)


def list_members():
    response = vault.membership_list()
    response_json = json.loads(response.text)

    if 'errors' in response_json:
        print response_json['errors']
    elif 'objects' in response_json:
        for member_dict in response_json['objects']:
            member = Member()
            member.parse(member_dict)
            print member


def get_member(membership_id):
    import pprint

    response = vault.membership_get(membership_id)
    response_json = json.loads(response.text)
    member = Member()
    member.parse(response_json)
    pprint.pprint(member.__dict__)


vault = Vault()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help="list members in Membership Vault", action="store_true")
    parser.add_argument("-m", "--member", help="fetch a specified member by ID", type=str)
    args = parser.parse_args()

    if args.list:
        list_members()

    if args.member:
        get_member(args.member)


