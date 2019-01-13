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
# * argparse usage for debug => work first on core functions
#	~ batch usage to select only given seeds by path, activate fancy verbose helper, skip quality checks
#
###########################################$
# Checks to be implemented
###########################################$
#
# .SC2Hotkey checks:
# * CommandConflictWithHotkeys
#		direct access, or Shift+key commands
#		=> need Defaults.ini, then rely on .SC2Hotkey
# * SameCheck
#		check that commands are consistent
#		=> SameChecks.py?
# * UnboundCommand
# 		unbound command out of identified conflicts
# 		unbound command in identified conflicts
# * ConflictCheck
#		for all commands check conflicts
#		check that all commands are bound
#		=> need Defaults.ini and ConflictChecks.py
# * CommandRootConsistency
#		commands are either <command> or <command>/<unit>
#		we want to check that <command> are consistent with all <command>/<unit> as a general rule
#		there are exception => to be stored in a config file
#		=> need only .SC2Hotkey
#
# Quality checks: => low priority, maybe consider drop this feature
# * EmptyDefault: check for empty Defaults.ini entries
#	~ need to update Defaults.ini when a new command is not references
# * MissingConflict:
#	~ report when a command has no conflict in Conflicts.py
#
# Questionable checks:
# * Regression check
#		Difficult to evaluate which commands are important out of game data conflict extraction
# * TheCoreLeftRightMirror
#		Maybe overlap with some workflow

import configparser
from enum import Enum

## Global settings
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


def load_ini_file(inputfilename):
	inifile = ConfigParser()
	inifile.allow_no_value=True
	inifile.read(inputfilename)
	return inifile

################################################################################
## one function per check
## standard inputs: hotkey_file + output_file (<= file to drop all check report)

################################################################################
## general seed check function

###############
###  MAIN   ###
###############

## Load config files

## Loop over all target seeds and produce report

