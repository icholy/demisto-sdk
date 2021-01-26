import os

from demisto_sdk.commands.common.git_tools import filter_changed_files
from demisto_sdk.tests.constants_test import *


def test_filter_changed_files(mocker):
    """
        Given:
            - A string of git diff results
        When:
            - running filter_changed_files on the string
        Then:
            - Ensure the modified files are recognized correctly.
            - Ensure the added files are recognized correctly.
            - Ensure the renamed file is in a tup;e in the modified files.
            - Ensure modified metadata files are in the changed_meta_files and that the added one is not.
            - Ensure the added code and meta files are not in added files.
            - Ensure old format file is recognized correctly.
            - Ensure deleted file is recognized correctly.
            - Ensure ignored files are set correctly.
    """

    mocker.patch.object(os.path, 'isfile', return_value=True)
    diff_string = f"M	{VALID_INCIDENT_FIELD_PATH}\n" \
                  f"M	{VALID_PYTHON_INTEGRATION_PATH}\n" \
                  f"M	{VALID_INTEGRATION_TEST_PATH}\n" \
                  f"M	{VALID_METADATA1_PATH}\n" \
                  f"M	{VALID_CLASSIFIER_PATH}\n" \
                  f"M	{VALID_DESCRIPTION_PATH}\n" \
                  f"M	{VALID_LAYOUT_PATH}\n" \
                  f"R100	{VALID_INTEGRATION_TEST_PATH}	{VALID_INTEGRATION_TEST_PATH}\n" \
                  f"A	{VALID_PACK_IGNORE_PATH}\n" \
                  f"A	{VALID_INDICATOR_FIELD_PATH}\n" \
                  f"A	{VALID_SECRETS_IGNORE_PATH}\n" \
                  f"A	{VALID_PYTHON_INTEGRATION_PATH}\n" \
                  f"A	{VALID_INTEGRATION_TEST_PATH}\n" \
                  f"A	{VALID_DESCRIPTION_PATH}\n" \
                  f"A	{VALID_IMAGE_PATH}\n" \
                  f"A	{VALID_WIDGET_PATH}\n" \
                  f"A	{VALID_PYTHON_INTEGRATION_TEST_PATH}\n" \
                  f"A	{VALID_PIPEFILE_PATH}\n" \
                  f"A	{VALID_PIPEFILE_LOCK_PATH}\n" \
                  f"A	{VALID_README_PATH}\n" \
                  f"A	{VALID_METADATA2_PATH}\n" \
                  f"D	{VALID_SCRIPT_PATH}\n" \
                  f"D	{VALID_DASHBOARD_PATH}\n" \
                  f"A	{VALID_JSON_FILE_FOR_UNIT_TESTING}"

    modified_files_list, added_files_list, deleted_files, old_format_files, changed_meta_files, \
        ignored_files, new_packs = filter_changed_files(files_string=diff_string, print_ignored_files=True)

    # checking that modified files are recognized correctly
    assert VALID_INCIDENT_FIELD_PATH in modified_files_list
    assert VALID_CLASSIFIER_PATH in modified_files_list
    assert VALID_DESCRIPTION_PATH in modified_files_list
    assert VALID_INTEGRATION_TEST_PATH in old_format_files
    assert VALID_LAYOUT_PATH in modified_files_list

    # checking that there are no unwanted files in modified files
    assert VALID_PIPEFILE_LOCK_PATH not in modified_files_list
    assert VALID_SCRIPT_PATH not in modified_files_list

    # checking that files in tests dir are not in modified_files
    assert VALID_JSON_FILE_FOR_UNIT_TESTING not in modified_files_list

    # check that the modified code file is not there but the yml file is
    assert VALID_INTEGRATION_TEST_PATH in old_format_files
    assert VALID_PYTHON_INTEGRATION_PATH not in modified_files_list

    # check that the modified metadata file is in the changed_meta_files but the added one is not
    assert VALID_METADATA1_PATH in changed_meta_files
    assert VALID_METADATA2_PATH not in changed_meta_files

    # check that the added files are recognized correctly
    assert VALID_README_PATH in added_files_list
    assert VALID_INTEGRATION_TEST_PATH in old_format_files
    assert VALID_WIDGET_PATH in added_files_list
    assert VALID_INDICATOR_FIELD_PATH in added_files_list

    # check that the added code files and meta file are not in the added_files
    assert VALID_PYTHON_INTEGRATION_PATH not in added_files_list
    assert VALID_PYTHON_INTEGRATION_TEST_PATH not in added_files_list
    assert VALID_METADATA1_PATH not in added_files_list

    # check that non-image, pipfile, description or schema are in the ignored files and the rest are
    assert VALID_PIPEFILE_PATH not in ignored_files
    assert VALID_PIPEFILE_LOCK_PATH not in ignored_files
    assert VALID_DESCRIPTION_PATH not in ignored_files
    assert VALID_IMAGE_PATH not in ignored_files
    assert VALID_SECRETS_IGNORE_PATH in ignored_files
    assert VALID_PYTHON_INTEGRATION_TEST_PATH in ignored_files
    assert VALID_PACK_IGNORE_PATH in ignored_files

    # check recognized deleted file
    assert VALID_SCRIPT_PATH in deleted_files
    assert VALID_DASHBOARD_PATH in deleted_files
