from typing import Union

from demisto_sdk.commands.common.content.objects.pack_objects.integration.integration import Integration
from demisto_sdk.commands.common.content.objects.pack_objects.script.script import Script
from demisto_sdk.commands.lint.lint_constants import LintFlags
from demisto_sdk.commands.lint.lint_global_facts import LintGlobalFacts
from demisto_sdk.commands.lint.lint_package_facts import LintPackageFacts
from demisto_sdk.commands.lint.linters.abstract_linters.python_base_linter import PythonBaseLinter
from demisto_sdk.commands.lint.json_output_formatters import BanditFormatter


class BanditLinter(PythonBaseLinter):
    LINTER_NAME = 'Bandit'

    def __init__(self, lint_flags: LintFlags, lint_global_facts: LintGlobalFacts):
        super().__init__(lint_flags.disable_bandit, lint_global_facts, self.LINTER_NAME,
                         json_output_formatter=BanditFormatter())

    def should_run(self, package: Union[Script, Integration]) -> bool:
        return all([
            self.has_lint_files(),
            super().should_run(package)
        ])

    def build_linter_command(self, package: Union[Script, Integration], lint_package_facts: LintPackageFacts) -> str:
        """
        Build command for executing bandit lint check https://github.com/PyCQA/bandit.
        Returns:
            (str): bandit command.
        """
        command = 'python3 -m bandit'
        # Reporting only issues with high and medium severity level
        command += ' -ll'
        # Reporting only issues of a high confidence level
        command += ' -iii'
        # Skip the following tests: Pickle usage, Use of insecure hash func, Audit url open,
        # Using xml.etree.ElementTree.fromstring,  Using xml.dom.minidom.parseString
        command += ' -s B301,B303,B310,B314,B318'
        # Aggregate output by filename
        command += ' -a file'
        # File to be excluded when performing lints check
        command += f" --exclude={','.join(self.EXCLUDED_FILES)}"
        # Only show output in the case of an error
        command += " -q"
        # Setting error format
        command += " --format custom --msg-template '{abspath}:{line}: {test_id} " \
                   "[Severity: {severity} Confidence: {confidence}] {msg}'"
        # Generating path patterns - path1,path2,path3,..
        files_list = [str(item) for item in lint_package_facts.lint_files]
        command += f" -r {','.join(files_list)}"
        return command
