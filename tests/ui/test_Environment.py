#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from tests.ui.baseui import BaseUI
from lib.ui.locators import locators
from lib.common.helpers import generate_name


class Environment(BaseUI):

    def test_create_env(self):
        "create new Environment"
        name = generate_name(6)
        self.login.login(self.katello_user, self.katello_passwd)
        self.navigator.go_to_environments()
        self.environment.create(name)

    def test_remove_env(self):
        "Delete an Environment "
        name = generate_name(6)
        self.login.login(self.katello_user, self.katello_passwd)
        self.navigator.go_to_environments()
        self.environment.create(name)
        self.environment.delete(name, really=True)
        self.assertTrue(self.user.wait_until_element(locators["notif.success"]))
