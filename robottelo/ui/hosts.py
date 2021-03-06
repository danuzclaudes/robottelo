"""Utilities to manipulate hosts via UI."""
from robottelo.constants import RESOURCE_DEFAULT
from robottelo.ui.base import Base
from robottelo.ui.locators import common_locators, locators, tab_locators
from robottelo.ui.navigator import Navigator


class Hosts(Base):
    """Provides the CRUD functionality for Host."""

    def _configure_hosts(self, arch=None, custom_ptable=None, cv=None,
                         domain=None, env=None, host_group=None, ip_addr=None,
                         lifecycle_env=None, mac=None, media=None, os=None,
                         ptable=None, puppet_ca=None, puppet_master=None,
                         puppet_module=None, reset_puppetenv=True,
                         resource=None, root_pwd=None, subnet=None):
        strategy1, value1 = locators['host.select_puppetmodule']
        strategy2, value2 = locators['host.select_puppetclass']
        # Host tab
        if lifecycle_env:
            self.select(locators['host.lifecycle_env'], lifecycle_env)
        if cv:
            self.select(locators['host.cv'], cv)
        if reset_puppetenv:
            self.click(locators['host.reset_puppetenv'])
        if host_group:
            self.select(locators['host.group'], host_group)
        elif env and not host_group:
            # As selecting hostgroup changes env
            self.select(locators['host.environment'], env)
        if puppet_ca:
            self.select(locators['host.puppet_ca'], puppet_ca)
        if puppet_master:
            self.select(locators['host.puppet_master'], puppet_master)
        # Network tab
        if domain or mac or subnet or ip_addr:
            self.click(tab_locators['host.tab_network'])
        if domain:
            self.select(locators['host.domain'], domain)
        if mac:
            self.wait_until_element(locators['host.mac']).send_keys(mac)
        if subnet:
            self.select(locators['host.subnet'], subnet)
        if ip_addr:
            self.wait_until_element(locators['host.ip']).send_keys(ip_addr)
        # Operating system tab
        self.wait_for_ajax()
        if arch or os or media or ptable or custom_ptable or root_pwd:
            self.click(tab_locators['host.tab_os'])
        if arch:
            self.select(locators['host.arch'], arch)
        if os:
            self.select(locators['host.os'], os)
        if media:
            self.select(locators['host.media'], media)
        if ptable:
            self.select(locators['host.ptable'], ptable)
        if custom_ptable:
            self.wait_until_element(
                locators['host.custom_ptables']).send_keys(custom_ptable)
        if root_pwd:
            self.wait_until_element(
                locators['host.root_pass']).send_keys(root_pwd)
        # Puppet tab
        if puppet_module:
            self.click(tab_locators['host.tab_puppet'])
            self.click((strategy1, value1 % puppet_module))
            self.click((strategy2, value2 % puppet_module))

    def create(self, arch=None, cpus='1', cv=None, custom_ptable=None,
               domain=None, env=None, host_group=None, ip_addr=None,
               lifecycle_env=None, loc=None, mac=None, media=None,
               memory='768 MB', name=None, org=None, os=None, ptable=None,
               puppet_ca=None, puppet_master=None, reset_puppetenv=True,
               resource=None, root_pwd=None, subnet=None, network_type=None,
               network=None):
        """Creates a host."""
        self.click(locators['host.new'])
        self.wait_until_element(locators['host.name']).send_keys(name)
        if org is not None:
            self.select(locators['host.org'], org)
        if loc is not None:
            self.select(locators['host.loc'], loc)
        if resource is None:
            resource = RESOURCE_DEFAULT
        self.select(locators['host.deploy'], resource)
        self._configure_hosts(
            arch=arch,
            cv=cv,
            custom_ptable=custom_ptable,
            domain=domain,
            env=env,
            host_group=host_group,
            ip_addr=ip_addr,
            lifecycle_env=lifecycle_env,
            mac=mac,
            media=media,
            os=os,
            ptable=ptable,
            puppet_ca=puppet_ca,
            puppet_master=puppet_master,
            resource=resource,
            root_pwd=root_pwd,
            subnet=subnet,
        )
        if resource != RESOURCE_DEFAULT:
            self.click(tab_locators['host.tab_vm'])
            self.select(locators['host.vm_cpus'], cpus)
            self.select(locators['host.vm_memory'], memory)
        if network_type is not None:
            self.select(locators['host.network_type'], network_type)
        if network is not None:
            self.select(locators['host.network'], network)
        self.click(common_locators['submit'])

    def update(self, arch=None, cv=None, custom_ptable=None, domain=None,
               env=None, host_group=None, ip_addr=None, mac=None,
               lifecycle_env=None, media=None, name=None, new_name=None,
               os=None, ptable=None, puppet_ca=None, puppet_master=None,
               puppet_module=None, reset_puppetenv=False, resource=None,
               root_pwd=None, subnet=None):
        """Updates a Host."""
        element = self.search(name)
        self.click(element)
        self.click(locators['host.edit'])
        if new_name:
            self.wait_until_element(locators['host.name'])
            self.field_update('host.name', new_name)
        self._configure_hosts(
            arch=arch,
            cv=cv,
            custom_ptable=custom_ptable,
            domain=domain,
            env=env,
            host_group=host_group,
            ip_addr=ip_addr,
            lifecycle_env=lifecycle_env,
            mac=mac,
            media=media,
            os=os,
            ptable=ptable,
            puppet_ca=puppet_ca,
            puppet_master=puppet_master,
            puppet_module=puppet_module,
            reset_puppetenv=reset_puppetenv,
            resource=resource,
            root_pwd=root_pwd,
            subnet=subnet,
        )
        self.click(common_locators['submit'])

    def navigate_to_entity(self):
        """Navigate to Hosts entity page"""
        Navigator(self.browser).go_to_hosts()

    def _search_locator(self):
        """Specify locator for Hosts entity search procedure"""
        return locators['host.select_name']

    def delete(self, name, really=True):
        """Deletes a host."""
        self.delete_entity(
            name,
            really,
            locators['host.delete'],
            drop_locator=locators['host.dropdown'],
        )

    def update_host_bulkactions(self, host=None, org=None):
        """Updates host via bulkactions"""
        strategy1, value1 = locators['host.checkbox']
        self.click((strategy1, value1 % host))
        self.click(locators['host.select_action'])
        if org:
            self.click(locators['host.assign_org'])
            self.click(locators['host.fix_mismatch'])
            self.select(locators['host.select_org'], org)
        self.click(locators['host.bulk_submit'])
