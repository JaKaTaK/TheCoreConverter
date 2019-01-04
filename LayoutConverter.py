import configparser, os, shutil, uuid
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

keymapper = ConfigParser()
keymapper.read('KeyMappings.ini')

layoutmapper = ConfigParser()
layoutmapper.read('KeyboardLayouts.ini')

class Conversion(Enum):
    LMtoRM = 'LeftToRightMaps'
    RMtoLM = 'LeftToRightMapsInverted'
    Layout = 'LayoutConversionType'

def remap_single_key_value(key, conversion_type, keymap_section=None, specific_values=None, command_name=None):
    #if a list of specific_values is provided, only translate if the key is in it
    remapped = key
    try:
        should_convert = True
        if specific_values: should_convert = keymapper.has_option(specific_values, command_name)

        if should_convert:
            if conversion_type == Conversion.RMtoLM:
                remapped = keymapper.key_for_value(Conversion.LMtoRM.value, key)
            elif conversion_type == Conversion.Layout and keymap_section:
                remapped = layoutmapper.get(keymap_section, key)
            else:
                remapped = keymapper.get(conversion_type.value, key)
    except configparser.NoOptionError:
        pass
    return remapped

def convert_hotkey_values(keystring, conversion_type, keymap_section=None, specific_values=None, command_name=None):
    remapped = ""

    commasplitkeys = keystring.split(",")
    commasplitcount = 1

    for cs in commasplitkeys:
        plussplitkeys = cs.split('+')
        plussplitcount = 1
        for ps in plussplitkeys:
            remapped += remap_single_key_value(ps, conversion_type, keymap_section, specific_values, command_name)
            if plussplitcount != len(plussplitkeys):
                remapped += "+"
            plussplitcount+=1

        if commasplitcount != len(commasplitkeys):
            remapped += ","
        commasplitcount+=1

    return remapped

# probably should use the configparse file write operation, not a custom file output
def convert_hotkey_file(inputfilename, outputfilename, conversion_type, keymap_section=None):
    t = conversion_type.value
    if keymap_section: t = keymap_section
    print(inputfilename + " converted to " + outputfilename + " conversion type: " + t)

    hotkeyfile = ConfigParser()
    hotkeyfile.allow_no_value=True
    hotkeyfile.read(inputfilename)

    with open (outputfilename, "w") as outputfile:
        for section in hotkeyfile.sections():
            outputfile.write("\n[" + section + "]\n")

            for item in hotkeyfile.items(section):
                if section == "Commands":
                    remapped = convert_hotkey_values(item[1], conversion_type, keymap_section)
                    if remapped:
                        outputfile.write(item[0] + "=" + remapped + "\n")
                elif section == "Hotkeys":
                    remapped = convert_hotkey_values(item[1], conversion_type, keymap_section, "MenuValues", item[0])
                    if remapped:
                        outputfile.write(item[0] + "=" + remapped + "\n")
                else:
                    outputfile.write(item[0] + "=" + item[1] + "\n")

def right_filename_from_left(left_name):
    if 'Left' in left_name:
        return left_name.replace('Left', 'Right')
    elif 'left' in left_name:
        return left_name.replace('left', 'right')

def left_filename_from_right(right_name):
    if 'Right' in right_name:
        return right_name.replace('Right', 'Left')
    elif 'right' in right_name:
        return right_name.replace('right', 'left')

def merge_file_into_file(file1, file2, new_name=None):
    hotkeyfile = ConfigParser()
    hotkeyfile.allow_no_value=True
    hotkeyfile.read(file2)
    hotkeyfile.read(file1) 
    f = file2
    if new_name: f = new_name
    hotkeyfile.write(open(f, 'w'))

def generate_right_profiles():

    for f in ["build", "temp"]:
        if os.path.isdir(f): shutil.rmtree(f)
        os.makedirs(f)

    for file_name in os.listdir(source_dir):
        right_version = right_filename_from_left(file_name)
        if right_version:
            tempfile = 'temp/' + str(uuid.uuid4())
            convert_hotkey_file(source_dir + file_name, tempfile, Conversion.LMtoRM)
            merge_file_into_file(tempfile, source_dir + right_version)

def unify_left_and_right_layouts():
    for file_name in os.listdir(source_dir):
        left_version = left_filename_from_right(file_name)
        if left_version:
            # this converts the right layout back to the left layout 
            # and merges it with the original left layout
            convert_hotkey_file(source_dir + file_name, 'temp/' + left_version, Conversion.RMtoLM)
            merge_file_into_file(source_dir + left_version, 'temp/' + left_version, 'temp/merged' + left_version)


# the right layouts should be tested in StarCraft and editied if need be
# once the right layouts look good, run the conversion again to generate all the other layouts

def generate_localized_layouts():
    layout_file = ConfigParser()
    layout_file.allow_no_value = True
    layout_file.read('KeyboardLayouts.ini')

    for file_name in os.listdir('temp'):
        if 'merged' in file_name:
            new_name = file_name.replace('merged', '')

            for s in layout_file.sections():
                if not os.path.isdir('build/' + s): os.makedirs('build/' + s)
                convert_hotkey_file('temp/' + file_name, 'build/' + s + '/' + new_name, Conversion.Layout, s)

                temp_name = str(uuid.uuid4())
                convert_hotkey_file('temp/' + file_name, 'temp/' + temp_name, Conversion.LMtoRM)
                right_name = right_filename_from_left(new_name)
                convert_hotkey_file('temp/' + temp_name, 'build/' + s + '/' + right_name, Conversion.Layout, s)

generate_right_profiles()
unify_left_and_right_layouts()
generate_localized_layouts()

shutil.rmtree('temp')

