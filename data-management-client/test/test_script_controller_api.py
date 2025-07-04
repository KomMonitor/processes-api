# coding: utf-8

"""
    KomMonitor Data Access API

    erster Entwurf einer Datenzugriffs-API, die den Zugriff auf die KomMonitor-Datenhaltungsschicht kapselt.

    The version of the OpenAPI document: 0.0.1
    Contact: christian.danowski-buhren@hs-bochum.de
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.api.script_controller_api import ScriptControllerApi


class TestScriptControllerApi(unittest.TestCase):
    """ScriptControllerApi unit test stubs"""

    def setUp(self) -> None:
        self.api = ScriptControllerApi()

    def tearDown(self) -> None:
        pass

    def test_add_process_script_as_body(self) -> None:
        """Test case for add_process_script_as_body

        Register a new process script
        """
        pass

    def test_delete_process_script(self) -> None:
        """Test case for delete_process_script

        Delete the process script
        """
        pass

    def test_delete_process_script_by_script_id(self) -> None:
        """Test case for delete_process_script_by_script_id

        Delete the process script
        """
        pass

    def test_get_process_script_code(self) -> None:
        """Test case for get_process_script_code

        retrieve the process script code associated to a certain indicator as JavaScript file
        """
        pass

    def test_get_process_script_code_for_indicator(self) -> None:
        """Test case for get_process_script_code_for_indicator

        retrieve the process script code associated to a certain indicator as JavaScript file
        """
        pass

    def test_get_process_script_for_indicator(self) -> None:
        """Test case for get_process_script_for_indicator

        retrieve information about the associated process script for a certain indicator
        """
        pass

    def test_get_process_script_for_script_id(self) -> None:
        """Test case for get_process_script_for_script_id

        retrieve information about the associated process script for a certain scriptId
        """
        pass

    def test_get_process_script_template(self) -> None:
        """Test case for get_process_script_template

        retrieve an empty script template, that defines how to implement process scripts for KomMonitor as JavaScript file.
        """
        pass

    def test_get_process_scripts(self) -> None:
        """Test case for get_process_scripts

        retrieve information about available process scripts
        """
        pass

    def test_update_process_script_as_body(self) -> None:
        """Test case for update_process_script_as_body

        Modify/Update an existing process script
        """
        pass

    def test_update_process_script_as_body_by_script_id(self) -> None:
        """Test case for update_process_script_as_body_by_script_id

        Modify/Update an existing process script
        """
        pass


if __name__ == '__main__':
    unittest.main()
