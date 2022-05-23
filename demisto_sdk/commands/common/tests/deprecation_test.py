import pytest

from demisto_sdk.commands.common.hook_validations.deprecation import \
    DeprecationValidator
from demisto_sdk.commands.common.hook_validations.integration import \
    IntegrationValidator
from demisto_sdk.commands.common.hook_validations.playbook import \
    PlaybookValidator
from demisto_sdk.commands.common.hook_validations.script import ScriptValidator
from demisto_sdk.commands.common.tests.integration_test import mock_structure

mocked_id_set = {"scripts": [
    {"sdca13-dasde12-ffe13-fdgs352": {
        "name": "script_1",
        "file_path": "script_1.yml",
        "deprecated": True,
        "depends_on": [
            "ic3_command1",
            "ic5_command1",
            "ic6_command3",
            "script_case_4",
            "script_case_7",
            "script_format_case_1"
            "ifc1_command3",
            "ifc1_command2"
        ]
    }
    },
    {
        "sdca13-dasde12-ffe13-fdgs353": {
            "name": "script_2",
            "file_path": "script_2.yml",
            "deprecated": False,
            "depends_on": [
                "ic1_command1",
                "ic5_command2",
                "ic6_command1",
                "ic6_command3",
                "script_case_3",
                "script_format_case_1",
                "ifc1_command3",
                "ifc1_command2"
            ]
        }
    }], "playbooks": [
    {"sdca13-dasde12-ffe13-fdgs3541": {
        "name": "playbook_1",
        "file_path": "playbook_1.yml",
        "deprecated": True,
        "implementing_scripts": [
            "IsIntegrationAvailable"
        ],
        "implementing_playbooks": [
            "playbook_case_4",
            "playbook_case_3"
        ],
        "command_to_integration": {
            "ic3_command1": "integration_case_3",
            "ic6_command2": "integration_case_6",
            "ifc1_command1": "integration_format_case_1",
            "ifc1_command3": "integration_format_case_1"
        }}},
        {"sdca13-dasde12-ffe13-fdgs35as": {
            "name": "playbook_2",
            "file_path": "playbook_2.yml",
            "implementing_scripts": [
                "script_case_2",
                "script_case_7",
                "script_format_case_1"
            ],
            "implementing_playbooks": [
                "playbook_case_2",
                "playbook_case_3",
                "playbook_format_case_1"
            ],
            "command_to_integration": {
                "ic2_command1": "integration_case_2",
                "ic5_command2": "integration_case_5",
                "ic6_command1": "integration_case_6",
                "ifc1_command1": "integration_format_case_1",
                "ifc1_command3": "integration_format_case_1"
            }}}
],
    "TestPlaybooks": [
    {"sdca13-dasde12-ffe13-fdgs3541": {
        "name": "testplaybook_1",
        "file_path": "testplaybook_1.yml",
        "deprecated": True,
        "implementing_scripts": [
            "script_case_5"
        ],
        "implementing_playbooks": [
            "playbook_case_5"
        ],
        "command_to_integration": {
            "ic7_command1": "integration_case_7",
            "ic7_command2": "integration_case_7",
            "ifc1_command1": "integration_format_case_1",
            "ifc1_command2": "integration_format_case_1",
            "ifc1_command3": "integration_format_case_1"
        }}},
        {"sdca13-dasde12-ffe13-fdgs35as": {
            "name": "testplaybook_2",
            "file_path": "testplaybook_2.yml",
            "implementing_scripts": [
                "script_case_6",
                "script_format_case_1"
            ],
            "implementing_playbooks": [
                "playbook_case_6",
                "playbook_format_case_1"
            ],
            "command_to_integration": {
                "ic7_command1": "integration_case_7",
                "ifc1_command1": "integration_format_case_1",
                "ifc1_command2": "integration_format_case_1",
                "ifc1_command3": "integration_format_case_1"
            }}}
]
}


def mock_deprecation_manager():
    # type: () -> DeprecationValidator
    deprecation_validator = DeprecationValidator(mocked_id_set)
    return deprecation_validator


class TestDeprecationValidator:

    INTEGRATIONS_VALIDATIONS_LS = [({'name': "integration_case_1", 'deprecated': True, 'script': {'commands': [{'name': 'ic1_command1'}]}},
                                    False, ["ic1_command1"], []),
                                   ({'name': "integration_case_2", 'script': {'commands': [
                                    {'name': 'ic2_command1', 'deprecated': True}]}}, False, ["ic2_command1"], []),
                                   ({'name': "integration_case_3", 'script': {'commands': [
                                    {'name': 'ic3_command1', 'deprecated': True}]}}, True, [], ["ic3_command1"]),
                                   ({'name': "integration_case_4", 'deprecated': False, 'script': {
                                    'commands': [{'name': 'ic4_command1'}]}}, True, [], ["ic4_command1"]),
                                   ({'name': "integration_case_5", 'deprecated': False, 'script': {'commands': [
                                    {'name': 'ic5_command1', 'deprecated': True}, {'name': 'ic5_command2'}]}}, True, [], ["ic5_command1", "ic5_command2"]),
                                   ({'name': "integration_case_6", 'script': {'commands': [{'name': 'ic6_command1', 'deprecated': True}, {
                                    'name': 'ic6_command2', 'deprecated': True}, {'name': 'ic6_command3'}]}},
                                    False, ["ic6_command1"], ["ic6_command3", "ic6_command2"]),
                                   ({'name': "integration_case_7", 'deprecated': True,
                                     'script': {'commands': [{'name': 'ic7_command1'}, {'name': 'ic7_command2'}]},
                                     'tests': ["testplaybook_1", "testplaybook_2"]}, False, ["ic7_command1"], ["ic7_command2"])
                                   ]

    @pytest.mark.parametrize("integration_yml, expected_bool_results, expected_commands_in_errors_ls, expected_commands_not_in_errors_ls",
                             INTEGRATIONS_VALIDATIONS_LS)
    def test_validate_integration(self, capsys, integration_yml, expected_bool_results, expected_commands_in_errors_ls, expected_commands_not_in_errors_ls):
        """
        Given
        - Case 1: integration with one deprecated command that is being used in a none-deprecated script.
        - Case 2: integration with one deprecated command that is being used in a none-deprecated playbook.
        - Case 3: integration with one deprecated command that is being used only in deprecated entities.
        - Case 4: integration with one none-deprecated command that is being used in both deprecated and none-deprecated entities.
        - Case 5: A deprecated integration with two commands, one deprecated and one none-dreprecated:
                  the none-deprecated command is being used in none-deprecated entities only,
                  and the deprecated command is being used in deprecated entities only.
        - Case 6: Integration with two deprecated commands and one none-deprecated command,
                  one deprecated command is being used in deprecated entities only,
                  one deprecated command is being used in none-deprecated entities only,
                  and the none-deprecated is being used in both deprecated and none-deprecated entities.
        - Case 7: Integration with two deprecated commands and two testplaybooks in the tests section,
                  one deprecated command is being used in both deprecated and none-deprecated testplaybooks.
                  and one deprecated command is being used only in a deprecated testplaybook.
        When
        - Running is_integration_deprecated_and_used on the given integration.
        Then
        - Ensure validation correctly identifies used deprecated commands in none deprecated entities.
        - Case 1: Should return False and that the command name appears in the error massage.
        - Case 2: Should return False and that the command name appears in the error massage.
        - Case 3: Should return True and that no command name appears in the error massage.
        - Case 4: Should return True and that no command name appears in the error massage.
        - Case 5: Should return True and that no command name appears in the error massage.
        - Case 6: Should return False and that only one command name (out of the two deprecated commands) appears in the error massage.
        - Case 7: Should return False and that only one command name (out of the two deprecated commands) appears in the error massage.
        """
        structure = mock_structure(current_file=integration_yml)
        validator = IntegrationValidator(structure)
        validator.deprecation_validator = mock_deprecation_manager()
        bool_result = validator.is_integration_deprecated_and_used()
        assert bool_result == expected_bool_results
        stdout = capsys.readouterr().out
        for command in expected_commands_in_errors_ls:
            assert command in stdout
        for command in expected_commands_not_in_errors_ls:
            assert command not in stdout

    INTEGRATIONS_FORMAT_VALIDATIONS = [({'name': "integration_format_case_1", 'script': {'commands': [{'name': 'ifc1_command1', 'deprecated': True}, {
        'name': 'ifc1_command2', 'deprecated': True}, {'name': 'ifc1_command3'}]}, 'tests': ["testplaybook_1", "testplaybook_2"]},
        "[IN153] - integration_format_case_1 integration contain deprecated commands that are being used:"
        "\nifc1_command1 is being used in the following locations:\ntestplaybook_2.yml\nplaybook_2.yml\nifc1_command2 is being used in the following"
        " locations:\ntestplaybook_2.yml\nscript_2.yml")]

    @pytest.mark.parametrize("integration_yml, expected_results", INTEGRATIONS_FORMAT_VALIDATIONS)
    def test_validate_integration_error_format(self, capsys, integration_yml, expected_results):
        """
        Given
        - Case 1: Integration with two deprecated commands, one none-deprecated command and two testplaybooks in the tests section,
                  one deprecated command is being used in both deprecated and none-deprecated testplaybooks and playbooks,
                  one deprecated command is being used in both deprecated and none-deprecated testplaybooks and scripts
                  and the none-deprecated command is being used in both deprecated and none-deprecated playbooks, testplaybooks and scripts
        When
        - Running is_integration_deprecated_and_used on the given integration.
        Then
        - Ensure the format of the validation is printed out correctly.
        - Case 1: Should print out the given integration and a list of each deprecated command that is being used,
          with a list of files paths of the none-deprecated entities that are using that command under that command.
        """
        structure = mock_structure(current_file=integration_yml)
        validator = IntegrationValidator(structure)
        validator.deprecation_validator = mock_deprecation_manager()
        validator.is_integration_deprecated_and_used()
        stdout = capsys.readouterr().out
        assert expected_results in stdout

    SCRIPTS_VALIDATIONS_LS = [({'name': "script_case_1", 'deprecated': True}, True),
                              ({'name': "script_case_2", 'deprecated': True}, False),
                              ({'name': "script_case_3", 'deprecated': True, 'tests': []}, False),
                              ({'name': "script_case_4", 'deprecated': True, 'tests': ["No Tests"]}, True),
                              ({'name': "script_case_5", 'deprecated': True, 'tests': ["testplaybook_1"]}, True),
                              ({'name': "script_case_6", 'deprecated': True, 'tests': ["testplaybook_2"]}, False),
                              ({'name': "script_case_7", 'deprecated': False}, True)
                              ]

    @pytest.mark.parametrize("script_yml, expected_results", SCRIPTS_VALIDATIONS_LS)
    def test_validate_script(self, script_yml, expected_results):
        """
        Given
        - Case 1: deprecated script that isn't being used in any external entities.
        - Case 2: deprecated script that is being used in none-deprecated entities.
        - Case 3: deprecated script with empty tests section that is being used in a none-deprecated script.
        - Case 4: deprecated script with "No Tests" in the tests section that is being used in a deprecated playbook.
        - Case 5: deprecated script with one deprecated test in the tests section.
        - Case 6: deprecated script with one none-deprecated test in the tests section.
        - Case 7: none-deprecated script that is is being used in both deprecated and none-deprecated sections.

        When
        - Running is_script_deprecated_and_used on the given script.
        Then
        - Ensure validation correctly identifies used deprecated commands in none deprecated entities.
        - Case 1: Should return True.
        - Case 2: Should return False.
        - Case 3: should return False.
        - Case 4: Should return True.
        - Case 5: Should return True.
        - Case 6: Should return False.
        - Case 7: Should return True.
        """
        structure = mock_structure(current_file=script_yml)
        validator = ScriptValidator(structure)
        validator.deprecation_validator = mock_deprecation_manager()
        assert validator.is_script_deprecated_and_used() == expected_results

    SCRIPTS_FORMAT_VALIDATIONS = [({'name': "script_format_case_1", 'deprecated': True, 'tests': ["testplaybook_2"]},
                                  "[SC107] - script_format_case_1 script is deprecated and being used in the following files:"
                                   "\nscript_2.yml\ntestplaybook_2.yml\nplaybook_2.yml")]

    @pytest.mark.parametrize("script_yml, expected_results", SCRIPTS_FORMAT_VALIDATIONS)
    def test_validate_script_error_format(self, capsys, script_yml, expected_results):
        """
        Given
        - Case 1: deprecated script with one none-deprecated testplaybook in the tests section,
                  the given script is used in both the testplaybook and another none-deprecated playbook, and both deprecated and none-deprecated integrations.
        When
        - Running is_script_deprecated_and_used on the given script.
        Then
        - Ensure the format of the validation is printed out correctly.
        - Case 1: Should print out a list with the name of the given script,
                  and a list of the files paths of the none-deprecated script and playbooks that are using the given script.
        """
        structure = mock_structure(current_file=script_yml)
        validator = ScriptValidator(structure)
        validator.deprecation_validator = mock_deprecation_manager()
        validator.is_script_deprecated_and_used()
        stdout = capsys.readouterr().out
        assert expected_results in stdout

    PLAYBOOKS_VALIDATIONS_LS = [({'name': "playbook_case_1", 'deprecated': True}, True),
                                ({'name': "playbook_case_2", 'deprecated': True}, False),
                                ({'name': "playbook_case_3", 'deprecated': False}, True),
                                ({'name': "playbook_case_4", 'deprecated': True, 'tests': ["No Tests"]}, True),
                                ({'name': "playbook_case_5", 'deprecated': True, 'tests': ["testplaybook_1"]}, True),
                                ({'name': "playbook_case_6", 'deprecated': True, 'tests': ["testplaybook_2"]}, False),
                                ]

    @pytest.mark.parametrize("playbook_yml, expected_results", PLAYBOOKS_VALIDATIONS_LS)
    def test_validate_playbook(self, playbook_yml, expected_results):
        """
        Given
        - Case 1: deprecated playbook that isn't being used in any external entities.
        - Case 2: deprecated playbook that is being used in none-deprecated entities.
        - Case 3: none-deprecated playbook that is is being used in both deprecated and none-deprecated sections.
        - Case 4: deprecated playbook with "No Tests" in the tests section that is being used in a deprecated playbook.
        - Case 5: deprecated playbook with one deprecated test in the tests section.
        - Case 6: deprecated playbook with one none-deprecated test in the tests section.
        When
        - Running is_playbook_deprecated_and_used on the given playbook.
        Then
        - Ensure validation correctly identifies used deprecated commands in none deprecated entities.
        - Case 1: Should return True.
        - Case 2: Should return False.
        - Case 3: Should return True.
        - Case 4: Should return True.
        - Case 5: Should return True.
        - Case 6: Should return False.
        """
        structure = mock_structure(current_file=playbook_yml)
        validator = PlaybookValidator(structure)
        validator.deprecation_validator = mock_deprecation_manager()
        assert validator.is_playbook_deprecated_and_used() == expected_results

    PLAYBOOKS_FORMAT_VALIDATIONS = [({'name': "playbook_format_case_1", 'deprecated': True, 'tests': ["testplaybook_2"]},
                                    "[PB118] - playbook_format_case_1 playbook is deprecated and being used in the following files:"
                                     "\ntestplaybook_2.yml\nplaybook_2.yml")]

    @pytest.mark.parametrize("playbook_yml, expected_results", PLAYBOOKS_FORMAT_VALIDATIONS)
    def test_validate_playbook_error_format(self, capsys, playbook_yml, expected_results):
        """
        Given
        - Case 1: deprecated playbook with one none-deprecated testplaybook in the tests section,
                  the given playbook is used in both the testplaybook and another none-deprecated playbook.
        When
        - Running is_playbook_deprecated_and_used on the given playbook.
        Then
        - Ensure the format of the validation is printed out correctly.
        - Case 1: Should print out a list with the name of the given playbook and a list of the files paths of the playbooks that are using the given playbook.
        """
        structure = mock_structure(current_file=playbook_yml)
        validator = PlaybookValidator(structure)
        validator.deprecation_validator = mock_deprecation_manager()
        validator.is_playbook_deprecated_and_used()
        stdout = capsys.readouterr().out
        assert expected_results in stdout