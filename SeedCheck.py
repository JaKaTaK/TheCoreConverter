#!/usr/bin/env python3
#
# This script aims at running checks across .SC2Hotkeys seeds in source_dir
#
# Features:
# * check all .SC2Hotkeys seeds in source_dir
# * produce a single file check log per seed in a target directory
# * provide help to fix issues => identify command to be remapped and display unavailable keys
#
# File structure:
# * pick seed from source_dir
# * get config file in checkconfig directory
#	~ Defaults.ini
#	~ DifferentDefaults.ini
#	~ SameChecks.py
#	~ ConflictChecks.py
# * output report in check
#	~ one file per seed, warnings to be ignored won't flag at "git diff"
#
# Ideas and challenges:
# * leverage on Debug.ini ? => is it really necessary… keep in mind "KISS"
# * maybe need some config file ? => try to find a way without that
# * TheCore Left-Right mirror and related headhaches with default keys
#
# Checks to be implemented:
# * under construction
#
# Quality checks: => low priority, maybe consider drop this feature
# * EmptyDefault: check for empty Defaults.ini entries
#	~ need to update Defaults.ini when a new command is not references
# * MissingCommandCard:
#	~ report when a command has no conflict in Conflicts.py

import configparser
from enum import Enum

source_dir = 'hotkey_sources/'

class ConfigParser(configparser.ConfigParser):
    def optionxform(self, opt):
        return opt

    def key_for_value(self, section, value):
        match = value
        for item in self.items(section):
            if item[1] == value:
                match = item[0]
        return match

    def write(self, file):
        return super().write(file, space_around_delimiters=False)

