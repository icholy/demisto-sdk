"""This file is a part of the generating yml design. Generating a yml file from a python file.

This is an example for an integration containing a general configuration, commands and helper functions.
"""

from details_collector import DetailsCollector

# The exact keyword details should be used to init the DetailsCollector of the integration
details = DetailsCollector(conf="some configuration")


# Adding a decorator from the DetailsCollector object in the following way
@details.add_command(command_name='first_command')
def this_is_a_command(command_name):
    """Some Documentation"""
    print(f"my command name is {command_name}")


# Example of helper function not being affected by the DetailsCollector
def this_is_a_helper_func():
    """Some helper docs"""
    print("helper")


# Multiple usage of the same decorator are welcome.
# To not use the kwargs sent, we need to use **kwargs in function declaration.
@details.add_command(command_name='other_command')
def this_is_another_command(arg1, **kwargs):
    """Some other command"""
    print(f"other command with arg {arg1}")


# This is called as a sanity check making sure the decorators do not interrupt the run
this_is_a_command()
this_is_another_command("hello")
