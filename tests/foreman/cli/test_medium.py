# -*- encoding: utf-8 -*-
"""Test for Medium  CLI"""

from fauxfactory import gen_alphanumeric
from robottelo.cli.base import CLIReturnCodeError
from robottelo.cli.factory import make_location, make_medium, make_org, make_os
from robottelo.cli.medium import Medium
from robottelo.datafactory import valid_data_list
from robottelo.decorators import run_only_on, tier1, tier2
from robottelo.test import CLITestCase

URL = "http://mirror.fakeos.org/%s/$major.$minor/os/$arch"
OSES = [
    'Archlinux',
    'Debian',
    'Gentoo',
    'Redhat',
    'Solaris',
    'Suse',
    'Windows',
]


class MediumTestCase(CLITestCase):
    """Test class for Medium CLI"""
    @run_only_on('sat')
    @tier1
    def test_positive_create_with_name(self):
        """Check if Medium can be created

        @Feature: Medium - Positive Create

        @Assert: Medium is created

        """
        for name in valid_data_list():
            with self.subTest(name):
                medium = make_medium({'name': name})
                self.assertEqual(medium['name'], name)

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_location(self):
        """Check if medium with location can be created

        @Feature: Medium - Positive create

        @Assert: Medium is created and has new location assigned

        """
        location = make_location()
        medium = make_medium({'location-ids': location['id']})
        self.assertIn(location['name'], medium['locations'])

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_organization_by_id(self):
        """Check if medium with organization can be created

        @Feature: Medium - Positive create

        @Assert: Medium is created and has new organization assigned

        """
        org = make_org()
        medium = make_medium({'organization-ids': org['id']})
        self.assertIn(org['name'], medium['organizations'])

    @run_only_on('sat')
    @tier1
    def test_positive_delete_by_id(self):
        """Check if Medium can be deleted

        @Feature: Medium - Positive Delete

        @Assert: Medium is deleted

        """
        for name in valid_data_list():
            with self.subTest(name):
                medium = make_medium({'name': name})
                Medium.delete({'id': medium['id']})
                with self.assertRaises(CLIReturnCodeError):
                    Medium.info({'id': medium['id']})

    # pylint: disable=no-self-use
    @run_only_on('sat')
    @tier2
    def test_positive_add_os(self):
        """Check if Medium can be associated with operating system

        @Feature: Medium - Add operating system

        @Assert: Operating system added

        """
        medium = make_medium()
        os = make_os()
        Medium.add_operating_system({
            'id': medium['id'],
            'operatingsystem-id': os['id'],
        })

    @run_only_on('sat')
    @tier2
    def test_positive_remove_os(self):
        """Check if operating system can be removed from media

        @Feature: Medium - Remove operating system

        @Assert: Operating system removed

        """
        medium = make_medium()
        os = make_os()
        Medium.add_operating_system({
            'id': medium['id'],
            'operatingsystem-id': os['id'],
        })
        medium = Medium.info({'id': medium['id']})
        self.assertIn(os['title'], medium['operating-systems'])
        Medium.remove_operating_system({
            'id': medium['id'],
            'operatingsystem-id': os['id'],
        })
        medium = Medium.info({'id': medium['id']})
        self.assertNotIn(os['name'], medium['operating-systems'])

    @run_only_on('sat')
    @tier1
    def test_positive_update_name(self):
        """Check if medium can be updated

        @Feature: Medium - Update medium

        @Assert: Medium updated

        """
        new_name = gen_alphanumeric(6)
        medium = make_medium()
        Medium.update({
            'name': medium['name'],
            'new-name': new_name,
        })
        medium = Medium.info({'id': medium['id']})
        self.assertEqual(medium['name'], new_name)
