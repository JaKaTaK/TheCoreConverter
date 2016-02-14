##################################################
#
# Filename: TheCoreRemapper.py
# Author: Jonny Weiss, Mark Rösler
# Description: Script to take the LM layouts of TheCore and generate the other 44 layouts.
# Change Log:
#   9/25/12 - Created
#   9/26/12 - Finished initial functionality
#
##################################################
from enum import Enum
import collections  # @UnusedImport
import configparser
import os  # @UnusedImport

from conflict_checks import *  # @UnresolvedImport @UnusedWildImport
from same_checks import *  # @UnresolvedImport @UnusedWildImport

class ConfigParser(configparser.ConfigParser):
    """Case-sensitive ConfigParser."""

    def optionxform(self, opt):
        return opt

    def write(self, file):
        return super().write(file, space_around_delimiters=False)

class Races(Enum):
    Protoss = "P"
    Terran = "T"
    Random = "R"
    Zerg = "Z"

class Sides(Enum):
    Right = "R"
    Left = "L"

class Sizes (Enum):
    Small = "S"
    Medium = "M"
    Large = "L"

class LogLevel(Enum):
    Info = "INFO"
    Warn = "WARN"
    Error = "ERROR"
    
class Logger:
    def __init__(self, title, filepath=None, log_file=[LogLevel.Warn, LogLevel.Error], log_consol=[LogLevel.Info, LogLevel.Error]):
        self.title = title
        self.filepath = filepath
        self.log_file = log_file
        self.log_consol = log_consol
        self.messages = {}
        self.messages[LogLevel.Info] = []
        self.messages[LogLevel.Warn] = []
        self.messages[LogLevel.Error] = []
        print(self.get_start_str())

    
    def get_start_str(self):
        output = "============================\n" 
        output = output + "Start " + self.title + "\n"
        output = output + "----------------------------"
        return output
    
    def log(self, log_level, msg):
        msg_str = self.get_message_str(log_level, msg)
        self.messages[log_level].append(msg_str)
        if log_level in self.log_consol:
            print(msg_str)
        
    def finish(self):
        output = "----------------------------\n"
        output = output + "Finished (" + self.title + ") - "
        for log_level_file in self.log_file:
            output = output + log_level_file.value + "s: " + str(len(self.messages[log_level_file])) + " "
        output = output + "\n"
        output = output + "============================"
        print(output)
        if not self.filepath is None:
            with open(self.filepath, 'w') as file:
                file.write(self.get_start_str() + "\n")
                for log_level_file in self.log_file:
                    for line in self.messages[log_level_file]:
                        file.write(line)
                file.write(output)
        
    def get_message_str(self, log_level, msg):
        msg_str = "[" + log_level.value + "]: " + msg
        if msg.count('\n') > 0:
            msg_str = msg_str + "\n" 
        return msg_str

# Read the settings
settings_parser = ConfigParser()
settings_parser.read('MapDefinitions.ini')

layout_parser = ConfigParser()
layout_parser.read('KeyboardLayouts.ini')

default_filepath = 'NewDefaults.ini'
default_parser = ConfigParser()
default_parser.read(default_filepath)

ddefault_filepath = 'different_default.ini'
ddefault_parser = ConfigParser()
ddefault_parser.read(ddefault_filepath)

inherit_filepath = 'TheCoreSeed.ini'
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
        if race == Races.Protoss:
            self.P = value
        elif race == Races.Random:
            self.R = value
        elif race == Races.Terran:
            self.T = value
        elif race == Races.Zerg:
            self.Z = value

    def get_raw_value(self, race):
        if race == Races.Protoss:
            return self.P
        elif race == Races.Random:
            return self.R
        elif race == Races.Terran:
            return self.T
        elif race == Races.Zerg:
            return self.Z

    def get_value(self, race):
        value = self.get_raw_value(race)
        if value is None:
            value = self.default
        return value

    def get_values_id(self):
        values = ""
        for race in Races:
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
            values = values + race.value + ":" + value + "\n"
        return values

def init_seed_hotkeyfile_parser():
    for race in Races:
        hotkeyfile_parser = ConfigParser()
        hotkeyfilepath = create_filepath(race, Sides.Left, Sizes.Medium)
        hotkeyfile_parser.read(hotkeyfilepath)
        hotkeyfile_parsers[race] = hotkeyfile_parser

def create_filepath(race, side, size, path=""):
    filename = prefix + " " + race.value + side.value + size.value + " " + suffix
    filepath = filename
    if path:
        filepath = path + "/" + filename
    return filepath

def new_keys_from_seed_hotkeys():
    logger = Logger("Search for new Keys in seed layouts", log_consol=[LogLevel.Info], log_file=[])
    for race in Races:
        for section in hotkeyfile_parsers[race].sections():
            for item in hotkeyfile_parsers[race].items(section):
                key = item[0]
                if not default_parser.has_option(section, key):
                    default_parser.set(section, key, "")
                    logger.log(LogLevel.Info, "New key found " + key + " added to " + default_filepath + " please add a default value")

    file = open(default_filepath, 'w')
    default_parser.write(file)
    file.close()
    order(default_filepath)
    default_parser.read(default_filepath)
    logger.finish()

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

def check_defaults():
    logger = Logger("Check defaults", "defaults.log", log_consol=[LogLevel.Error], log_file=[LogLevel.Warn, LogLevel.Error])
    for section in default_parser.sections():
        for item in default_parser.items(section):
            key = item[0]
            default = item[1]
            multidefault = ddefault_parser.has_option(section, key)
            if not default or multidefault:
                seedhas = True
                for race in Races:
                    if not hotkeyfile_parsers[race].has_option(section, key):
                        seedhas = False
                inherit = inherit_parser.has_option(section, key)

                if multidefault:
                    if not seedhas and not inherit:
                        logger.log(LogLevel.Error, "key has multiple different defaults - please set in all seed layouts a value for this key (or at leased unbound it) " + key)
                if not default:
                    if seedhas or inherit:
                        logger.log(LogLevel.Warn, "[WARN] no default " + key)
                    else:
                        logger.log(LogLevel.Warn, "[ERROR] no default " + key)
    logger.finish()

def create_model():
    model = {}
    for section in default_parser.sections():
        section_dict = {}
        for item in default_parser.items(section):
            key = item[0]
            hotkey = Hotkey(key, section)

            default = item[1]
            hotkey.default = default

            for race in Races:
                if hotkeyfile_parsers[race].has_option(section, key):
                    value = hotkeyfile_parsers[race].get(section, key)  #
                    hotkey.set_value(race, value)

            if inherit_parser.has_option(section, key):
                copyof = inherit_parser.get(section, key)
                hotkey.copyOf = copyof
            section_dict[key] = hotkey
        model[section] = section_dict
    return model

def generate(seed_model):
    logger = Logger("Generation", log_consol=[LogLevel.Info], log_file=[])
    seed_models = init_models()
    for race in Races:
        logger.log(LogLevel.Info, "generate model for race: " + race.value + " side: L size: M keyboardlayout: " + seed_layout)
        seed_models[race][Sides.Left][Sizes.Medium] = extract_race(seed_model, race)
        logger.log(LogLevel.Info, "generate model for race: " + race.value + " side: R size: M keyboardlayout: " + seed_layout)
        seed_models[race][Sides.Right][Sizes.Medium] = convert_side(seed_models[race][Sides.Left][Sizes.Medium], Sides.Right)
        logger.log(LogLevel.Info, "generate model for race: " + race.value + " side: L size: S keyboardlayout: " + seed_layout)
        seed_models[race][Sides.Left][Sizes.Small] = shift_left(seed_models[race][Sides.Left][Sizes.Medium], Sides.Left)
        logger.log(LogLevel.Info, "generate model for race: " + race.value + " side: R size: S keyboardlayout: " + seed_layout)
        seed_models[race][Sides.Right][Sizes.Small] = shift_right(seed_models[race][Sides.Right][Sizes.Medium], Sides.Right)
        logger.log(LogLevel.Info, "generate model for race: " + race.value + " side: L size: L keyboardlayout: " + seed_layout)
        seed_models[race][Sides.Left][Sizes.Large] = shift_right(seed_models[race][Sides.Left][Sizes.Medium], Sides.Left)
        logger.log(LogLevel.Info, "generate model for race: " + race.value + " side: R size: L keyboardlayout: " + seed_layout)
        seed_models[race][Sides.Right][Sizes.Large] = shift_left(seed_models[race][Sides.Right][Sizes.Medium], Sides.Right)
    translate_and_create_files(seed_models, logger)
    logger.finish()

def init_models():
    models = {}
    for race in Races:
        models[race] = {}
        for side in Sides:
            models[race][side] = {}
    return models

def extract_race(seed_model, race):
    model_dict = {}
    for section in seed_model:
        model_dict[section] = {}
        for key, hotkey in seed_model[section].items():
            value = resolve_inherit(seed_model, section, hotkey, race)
            model_dict[section][key] = value
    return model_dict

def resolve_inherit(model, section, hotkey, race):
    hotkey = resolve_copyof(model, section, hotkey)
    value = hotkey.get_value(race)
    return value

def resolve_copyof(model, section, hotkey):
    while True:
        if hotkey.copyOf:
            hotkey = model[section][hotkey.copyOf]
        else:
            return hotkey

def convert_side(seed_model, side):
    return modify_model(seed_model, settings_parser, 'GlobalMaps', side)

def modify_model(seed_model, parser, parser_section, side):
    model_dict = {}
    for section in seed_model:
        model_dict[section] = {}
        for key, value in seed_model[section].items():
            if section == "Settings":
                newvalue = value
            else:
                newvalue = modify_value(value, parser, parser_section, side)
            model_dict[section][key] = newvalue
    return model_dict

def modify_value(org_value, parser, section, side):
    altgr = "0"
    if parser == layout_parser and side == Sides.Right:
        altgr = layout_parser.get(section, "AltGr")

    newalternates = []
    for alternate in org_value.split(","):
        keys = alternate.split("+")
        newkeys = []
        # filter "Shift" only to make sure it is the same output as the old script
        if altgr == "1" and keys.count("Alt") == 1 and keys.count("Control") == 0 and keys.count("Shift") == 0:
            newkeys.append("Control")
        for key in keys:
            if parser.has_option(section, key):
                newkey = parser.get(section, key)
            else:
                newkey = key
            newkeys.append(newkey)
        newalternate = ""
        first = True
        for newkey in newkeys:
            if not first:
                newalternate = newalternate + "+"
            else:
                first = False
            if not newkey:
                newalternate = ""
            else:
                newalternate = newalternate + newkey
        newalternates.append(newalternate)
    first = True
    newvalues = ""
    for newalternate in newalternates:
        if not newalternate:
            continue
        if not first:
            newvalues = newvalues + ","
        else:
            first = False
        newvalues = newvalues + newalternate
    return newvalues

def shift_left(seed_model, side):
    shift_section = side.value + 'ShiftLeftMaps'
    return shift(seed_model, shift_section, side)

def shift_right(seed_model, side):
    shift_section = side.value + 'ShiftRightMaps'
    return shift(seed_model, shift_section, side)

def shift(seed_model, shift_section, side):
    return modify_model(seed_model, settings_parser, shift_section, side)

def translate_and_create_files(models, logger):
    layouts = layout_parser.sections()
    for race in Races:
        for side in Sides:
            for size in Sizes:
                for layout in layouts:
                    if layout != seed_layout:
                        logger.log(LogLevel.Info, "translate race: " + race.value + " side: " + side.value + " size: " + size.value + " keyboardlayout: " + layout)
                        model = translate(models[race][side][size], layout, side)
                    else:
                        model = models[race][side][size]
                    create_file(model, race, side, size, layout, logger)

def translate(seed_model, layout, side):
    return modify_model(seed_model, layout_parser, layout, side)

def create_file(model, race, side, size, layout, logger):
    hotkeyfile_parser = ConfigParser()
    for section in model:
        if not hotkeyfile_parser.has_section(section):
                hotkeyfile_parser.add_section(section)
        for key, value in model[section].items():
            hotkeyfile_parser.set(section, key, value)
    if not os.path.isdir(layout):
        os.makedirs(layout)
    filepath = create_filepath(race, side, size, layout)
    hotkeyfile = open(filepath, 'w')
    hotkeyfile_parser.write(hotkeyfile)
    hotkeyfile.close()
    order(filepath)
    logger.log(LogLevel.Info, filepath + " created")
    return filepath

def analyse(model):
    same_check(model)
    conflict_check(model)
    wrong_inherit(model)
    suggest_inherit(model)


def same_check(model):
    logger = Logger("same check", "same_check.log", log_consol=[], log_file=[LogLevel.Error])
    for race in Races:
        for same_set in SAME_CHECKS:  # @UndefinedVariable
            same_set.sort()
            first_key = same_set[0]
            for section in collections.OrderedDict(sorted(model.items())):
                if not first_key in model[section]:
                    continue
                mismatched = False
                value = model[section][first_key].get_value(race)
                for key in same_set:
                    if not model[section][key].get_value(race) == value:
                        mismatched = True
                if mismatched:
                    log_msg = "Mismatched values in race: " + race.value
                    for key in same_set:
                        log_msg = log_msg + "\n\t" + key + " = " + model[section][key].get_value(race)
                    logger.log(LogLevel.Error, log_msg)
    logger.finish()

def conflict_check(model):
    logger = Logger("conflict check", "conflict_check.log", log_consol=[], log_file=[LogLevel.Error])
    for race in Races:
        for commandcard_key, conflict_set in collections.OrderedDict(sorted(CONFLICT_CHECKS.items())).items():  # @UndefinedVariable
            conflict_set.sort()
            count_hotkeys = {}
            for section in model:
                for key, hotkey in model[section].items():
                    if key in conflict_set:
                        values = hotkey.get_value(race).split(",")
                        for value in values:
                            if not value:
                                continue
                            if not value in count_hotkeys:
                                count_hotkeys[value] = 1
                            else:
                                count_hotkeys[value] = count_hotkeys[value] + 1
            
            
            for value, count in collections.OrderedDict(sorted(count_hotkeys.items())).items():
                if count > 1:
                    log_msg = "Conflict of hotkeys in race: " + race.value + " commandcard: " + commandcard_key
                    for key in conflict_set:
                        for section in collections.OrderedDict(sorted(model.items())):
                            if not key in model[section]:
                                continue
                            raw_values = model[section][key].get_value(race)
                            values = raw_values.split(",")
                            values.sort()
                            issue = False
                            for issue_value in values:
                                if issue_value == value:
                                    issue = True
                            if issue:        
                                log_msg + log_msg + "\n\t" + key + " = " + raw_values
                    logger.log(LogLevel.Error, log_msg)
    logger.finish()
                
def suggest_inherit(model):
    logger = Logger("suggest inherit", "suggest_inherit.log", log_consol=[], log_file=[LogLevel.Info])
    outputdict = {}
    for section in model:
        outputdict[section] = {}
        for hotkey1 in model[section].values():
            values_id = hotkey1.get_values_id()
            for hotkey2 in model[section].values():
                if hotkey1.name == hotkey2.name:
                    continue
                equal = True
                for race in Races:
                    value = hotkey1.get_value(race)
                    value2 = hotkey2.get_value(race)
                    value_set = set(str(value).split(","))
                    value2_set = set(str(value2).split(","))
                    if value_set != value2_set:
                        equal = False
                        break
                if equal:
                    if not values_id in outputdict[section]:
                        outputdict[section][values_id] = {}
                    if not hotkey1.name in outputdict[section][values_id]:
                        outputdict[section][values_id][hotkey1.name] = hotkey1
                    if not hotkey2.name in outputdict[section][values_id]:
                        outputdict[section][values_id][hotkey2.name] = hotkey2

    for section in collections.OrderedDict(sorted(outputdict.items())):
        for values_id in collections.OrderedDict(sorted(outputdict[section].items())):
            hotkeys = outputdict[section][values_id]
            first = True
            log_msg = ""
            for hotkey in collections.OrderedDict(sorted(hotkeys.items())).values():
                if first:
                    for race in Races:
                        value = hotkey.get_value(race)
                        log_msg = log_msg + race.value + ": " + str(value) + "   "
                    first = False
                    log_msg = log_msg + "\n"
                log_msg = log_msg + "\t" + hotkey.name + " default: " + hotkey.default
                if hotkey.copyOf:
                    hotkeycopyof = model[section][hotkey.copyOf]
                    log_msg = log_msg + " copyof: " + hotkeycopyof.name + " default: " + hotkeycopyof.default
                log_msg = log_msg + "\n"
            logger.log(LogLevel.Info, log_msg)
    logger.finish()

def wrong_inherit(model):
    logger = Logger("wrong inherit", "wrong_inherit.log", log_consol=[], log_file=[LogLevel.Error])
    for section in collections.OrderedDict(sorted(model.items())):
        for hotkey in collections.OrderedDict(sorted(model[section].items())).values():
            if not hotkey.copyOf:
                continue
            hotkeycopyof = resolve_copyof(model, section, hotkey)
            equal = True
            for race in Races:
                value = hotkey.get_value(race)
                copyofvalue = hotkeycopyof.get_value(race)
                value_set = set(str(value).split(","))
                copyofvalue_set = set(str(copyofvalue).split(","))
                if value_set != copyofvalue_set:
                    equal = False
            if not equal:
                log_msg = hotkey.name + " != " + hotkeycopyof.name + "\n"
                for race in Races:
                    value = hotkey.get_raw_value(race)
                    copyofvalue = hotkeycopyof.get_value(race)
                    if not value:
                        value = " "
                    if not copyofvalue:
                        copyofvalue = " "
                    log_msg = log_msg + "\t" + race.value + ": " + str(value) + "\t" + str(copyofvalue) + "\n"
                default = hotkey.default
                if not default:
                    default = " "
                copyofdefault = hotkeycopyof.default
                if not copyofdefault:
                    copyofdefault = " "
                log_msg = log_msg + "\tD: " + str(default) + "\t" + str(copyofdefault) + " (default)"
                logger.log(LogLevel.Error, log_msg)
    logger.finish()


print("___________.__           _________                      _________                                   __                " + "\n" + 
    "\\__    ___/|  |__   ____ \\_   ___ \\  ___________   ____ \\_   ___ \\  ____   _______  __ ____________/  |_  ___________ " + "\n" + 
    "  |    |   |  |  \\_/ __ \\/    \\  \\/ /  _ \\_  __ \\_/ __ \\/    \\  \\/ /  _ \\ /    \\  \\/ // __ \\_  __ \\   __\\/ __ \\_  __ \\" + "\n" + 
    "  |    |   |   Y  \\  ___/\\     \\___(  <_> )  | \\/\\  ___/\\     \\___(  <_> )   |  \   /\\  ___/|  | \\/|  | \\  ___/|  | \\/" + "\n" + 
    "  |____|   |___|  /\\___  >\\______  /\\____/|__|    \\___  >\\______  /\\____/|___|  /\\_/  \\___  >__|   |__|  \\___  >__|   " + "\n" + 
    "                \\/     \\/        \\/                   \\/        \\/            \\/          \\/                 \\/       " + "\n\n\n")

init_seed_hotkeyfile_parser()
# check sections
new_keys_from_seed_hotkeys()
check_defaults()
model = create_model()
generate(model)
analyse(model)
