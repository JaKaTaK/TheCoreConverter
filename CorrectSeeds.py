#!/usr/bin/python
##################################################
#
# Filename: correct_seeds.py
# Author: Mark Rösler
# Description: Script to correct the seed layouts if all wrong inhertis are fixed
#
##################################################
import collections
import configparser

class ConfigParser(configparser.ConfigParser):
    """Case-sensitive ConfigParser."""
 
    def optionxform(self, opt):
        return opt
    
    def write(self, file):
        return super().write(file, space_around_delimiters=False)

PROTOSS = "P"
TERRAN = "T"
RANDOM = "R"
ZERG = "Z"
races = [PROTOSS, TERRAN, RANDOM, ZERG]

RIGHT = "R"
LEFT = "L"
sides = [LEFT, RIGHT]

SMALL = "S"
MEDIUM = "M"
LARGE = "L"
sizes = [SMALL, MEDIUM, LARGE]

# Read the settings
settings_parser = ConfigParser()
settings_parser.read('MapDefinitions.ini')

layout_parser = ConfigParser()
layout_parser.read('KeyboardLayouts.ini')

default_filepath = 'Defaults.ini'
default_parser = ConfigParser()
default_parser.read(default_filepath)

ddefault_filepath = 'DifferentDefault.ini'
ddefault_parser = ConfigParser()
ddefault_parser.read(ddefault_filepath)

inherit_filepath = 'Inheritance.ini'
inherit_parser = ConfigParser()
inherit_parser.read(inherit_filepath)
    
prefix = settings_parser.get("Filenames", "Prefix")
suffix = settings_parser.get("Filenames", "Suffix")
seed_layout = settings_parser.get("Filenames", "Seed_files_folder")

hotkeyfile_parsers = {}

class Hotkey:
    
    def __init__(self, name, section, P=None, T=None, Z=None, R=None, default=None, copyOf=None):
        self.name = name
        self.section = section
        self.P = P
        self.T = T
        self.Z = Z
        self.R = R
        self.default = default
        self.copyOf = copyOf

    def set_value(self, race, value):
        if race == PROTOSS:
            self.P = value
        elif race == RANDOM:
            self.R = value
        elif race == TERRAN:
            self.T = value
        elif race == ZERG:
            self.Z = value
    
    def default_instead_of_none_value(self, value):
        if value is None:
            value = self.default
        return value
    
    def get_raw_value(self, race):
        if race == PROTOSS:
            return self.P
        elif race == RANDOM:
            return self.R
        elif race == TERRAN:
            return self.T
        elif race == ZERG:
            return self.Z
    
    def get_value(self, race):
        return self.default_instead_of_none_value(self.get_raw_value(race))
    
    def get_values_id(self):
        values = ""
        for race in races:
            value = self.get_value(race)
            first = True
            alternates = value.split(",")
            alternates.sort()
            for alternate in alternates:
                if first:
                    value = alternate
                    first = False
                else:
                    value = value + "," + alternate 
            values = values + race + ":" + value + "\n"
        return values
        
def init_seed_hotkeyfile_parser():
    for race in races:
        hotkeyfile_parser = ConfigParser()
        hotkeyfilepath = create_filepath(race, LEFT, MEDIUM)
        hotkeyfile_parser.read(hotkeyfilepath)
        hotkeyfile_parsers[race] = hotkeyfile_parser

def create_filepath(race, side, size, path=""):
    filename = prefix + " " + race + side + size + " " + suffix
    filepath = filename
    if path:
        filepath = path + "/" + filename
    return filepath

def order(filepath):
    read_parser = ConfigParser()
    read_parser.read(filepath)

    dicti = {}
    for section in read_parser.sections():
        items = read_parser.items(section)
        items.sort()
        dicti[section] = items

    open(filepath, 'w').close()  # clear file

    write_parser = ConfigParser()  # on other parser just for the safty
    write_parser.read(filepath)

    write_parser.add_section("Settings")
    write_parser.add_section("Hotkeys")
    write_parser.add_section("Commands")

    for section in dicti.keys():
        if not write_parser.has_section(section):
            write_parser.add_section(section)
        items = dicti.get(section)
        for item in items:
            write_parser.set(section, item[0], item[1])

    file = open(filepath, 'w')
    write_parser.write(file)
    file.close()

def create_model():
    model = {}
    for section in default_parser.sections():
        section_dict = {}
        for item in default_parser.items(section):
            key = item[0]
            hotkey = Hotkey(key, section)

            default = item[1]
            hotkey.default = default

            for race in races:
                if hotkeyfile_parsers[race].has_option(section, key):
                    value = hotkeyfile_parsers[race].get(section, key)  #
                    hotkey.set_value(race, value)

            if inherit_parser.has_option(section, key):
                copyof = inherit_parser.get(section, key)
                hotkey.copyOf = copyof
            section_dict[key] = hotkey
        model[section] = section_dict
    return model

def correct_seeds(model):
    for section in model:
        for hotkey in collections.OrderedDict(sorted(model[section].items())).values():
            if not hotkey.copyOf:
                continue
            hotkeycopyof = resolve_copyof(model, section, hotkey)
            for race in races:
                value = hotkey.get_value(race)
                copyofvalue = hotkeycopyof.get_value(race)
                value_set = set(str(value).split(","))
                copyofvalue_set = set(str(copyofvalue).split(","))
                if value_set != copyofvalue_set:
                    if hotkey.default == copyofvalue:
                        hotkeyfile_parsers[race].remove_option(section, hotkey.name)
                        print(race + " " + hotkey.name + " copy of " + hotkeycopyof.name + 
                              " org value:" + value + " removed because org default is equal copyof value: " + copyofvalue)
                    else:
                        hotkeyfile_parsers[race].set(section, hotkey.name, copyofvalue)
                        print(race + " " + hotkey.name + " copy of " + hotkeycopyof.name + 
                              " org value:" + value + " copyof value: " + copyofvalue)
    for race in races:
        hotkeyfile_parser = hotkeyfile_parsers[race]
        hotkeyfilepath = create_filepath(race, LEFT, MEDIUM)
        file = open(hotkeyfilepath, 'w')
        hotkeyfile_parser.write(file)
        file.close()
        
    

def resolve_copyof(model, section, hotkey):
    while True:
        if hotkey.copyOf:
            hotkey = model[section][hotkey.copyOf]
        else:
            return hotkey


init_seed_hotkeyfile_parser()
model = create_model()
correct_seeds(model)
