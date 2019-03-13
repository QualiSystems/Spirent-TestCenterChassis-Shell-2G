#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `TestCenterChassisDriver
"""

from cloudshell.api.cloudshell_api import AttributeNameValue, CloudShellAPISession
from shellfoundry.releasetools.test_helper import create_autoload_resource

stc_chassis = {'stc-stcweb': {'address': '192.168.42.218',
                              'controller': '192.168.85.12',
                              'port': '8888',
                              'modules': 1},
               'stc-labserver': {'address': '192.168.42.218',
                                 'controller': '192.168.42.182',
                                 'port': '',
                                 'modules': 1}}


class TestStcChassisShell(object):

    session = None

    def setup(self):
        self.session = CloudShellAPISession('localhost', 'admin', 'admin', 'Global')

    def teardown(self):
        for resource in self.session.GetResourceList('Testing').Resources:
            self.session.DeleteResource(resource.Name)

    def test_hello_world(self):
        pass

    def test_stc_chassis(self):
        self._get_inventory('stc-stcweb', stc_chassis['stc-stcweb'])
        self._get_inventory('stc-labserver', stc_chassis['stc-labserver'])

    def _get_inventory(self, name, properties):
        attributes = [AttributeNameValue('STC Chassis Shell 2G.Controller Address', properties['controller']),
                      AttributeNameValue('STC Chassis Shell 2G.Controller TCP Port', properties['port']),
                      AttributeNameValue('STC Chassis Shell 2G.Split Dual Media', properties['dual_media'])]
        resource = create_autoload_resource(self.session, 'STC Chassis Shell 2G', properties['address'], name,
                                            attributes)
        self.session.AutoLoad(resource.Name)
        resource_details = self.session.GetResourceDetails(resource.Name)
        assert(len(resource_details.ChildResources) == properties['modules'])
        self.session.DeleteResource(resource.Name)
