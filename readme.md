## TL;DR
1. Make updates to a left hotkey profile found in the `hotkey_sources` folder. `The Core 4.0 Left.SC2Hotkeys`, for example.
2. Run `LayoutConverter.py`
3. If you think you might have bound a hotkey to it's default value that wasn't previously set to default, open up `The Core 4.0 Right.SC2Hotkeys` and update the binding if it isn't right.
4. Run the script again.
5. Grab the `build` folder and give it to people.

## Setup
Clone or download the project.  

You need [Python 3](https://www.python.org/downloads/) to run this script.  

From the command line in the project directory:  
`python LayoutConverter.py`

You can also try double-clicking the `LayoutConverter.py` file. 
Your PC might be smart enough to run it as a Python 3 script and it might not.

If you run the script and see errors like "No module named configparser" or "No module named enum",
your computer is probably trying to run it with Python 2. Try  
`python3 LayoutConverter.py` or `python3.6 LayoutConverter.py`

## Basic Overview 
This program serves three basic functions.

1. If you put a brand new file called `Sick New Hotkey Profile Left.SC2Hotkeys` into the `hotkey_sources` folder, 
running the script will generate a new hotkey profile called `Sick New Hotkey Profile Right.SC2Hotkeys`. 
The keyword `Left` or `left` has to be in the filename otherwise it will be ignored. 
You should almost never do this though, as it's going to be easier to modify an existing profile (more on this below).

2. If you make a change to the left profile, the script will translate those changes to the right profile and update it.

3. If there is a left and right pair of hotkey profiles in the `hotkey_sources` folder, 
the script will use them to generate a full set of hotkey profiles for different localizations (USQwerty, FrenchAzerty, and so on). 
You can find them in the build folder.

## How it Works
1. The script will start by reading hotkey values (like `Zealot=W`, for example) from a left profile (such as `TheCore 4.0 Left.SC2Hotkeys`) found in the `hotkey_sources` folder.

2. It will then use the mappings from the `KeyMappings.ini` file to translate the hotkey to the right version, i.e. `Zealot=W` becomes `Zealot=P`.
`Zealot=P` will then be written into `hotkey_sources/TheCore 4.0 Right.SC2Hotkeys`. If the file doesn't exist it will be created.
If the hotkey is already in the right hotkey profile as `Zealot=O`, for example, the value will be overwritten. 
If there is a value in the right profile that is not present in the left profile, like `SpawningPool/Drone=SemiColon` it will not be overwritten.

3. The script will then look for values in both the left and right versions of the hotkey files and use the translations found in `KeyboardLayouts.ini`
to generate all the localized versions of the profiles. Every section in the `KeyboardLayouts.ini` file represents a different localization,
so a new localization can be added just by adding a new section to the file. All the localizations will show up as subfolders inside a `build` folder.

For the most part (see below), just make changes to the left profile and let the script update the right profile.
Running the script will update the right profile and generate the distrubutable profiles all at once, 
so if you make a change to the left hotkey profile you don't need to run the script twice to get all the localized versions.

If you want to create a new version of The Core (5.0, let's say), copy `The Core 4.0 Left.SC2Hotkeys` and `The Core 4.0 Right.SC2Hotkeys` 
and rename them to `The Core 5.0 Left.SC2Hotkeys` and `The Core 5.0 Right.SC2Hotkeys`. Don't start from scratch (unless you really want to),
because the way these two files are paired together helps deal with the default key binding problem.

## Dealing With Default Bindings
There is one, big, extremely annoying thing about the way `*.SC2Hotkeys` files work, and it's the way default bindings behave.
If a hotkey is bound to it's default value, like `SpawningPool/Drone=S` (the morph drone into spawning pool command),
it will not show up in the key profile. This means that the script won't find a keybinding for `SpawningPool/Drone` in the left profile
and it won't be able to translate it to the right profile, even though it should be converted to `SpawningPool/Drone=SemiColon`.
For the most part this isn't an issue since the nature of The Core is that almost everything is rebound, but there are a few keys that may not be.

The way to deal with it is to just open up the right profile and look things over. If a key isn't bound correctly, just fix it in the right profile.
Once a keybinding has been set in the right profile it will stay there until it gets overwritten by a new binding from the left profile.
From that point on, unless you're creating a brand new left profile and generating a brand new right profile, the key will keep it's mapping
that you set in the right profile.

The only thing to watch out for after the initial issues with the default bindings have been fixed (which they have been),
is if you happen to bind a key back to it's default binding after it's been bound to a non-default key. 
If that's the case the binding will dissapear from the left profile, and it will not be updated in the right profile (the right profile will keep it's previous value).

This should be very rare, but it could happen. If you know how to git, just run the script and then `git diff` to see what's changed. 
If there's a value that dissappeared from the left profile it will be super obvious. Usually a big red line of text.

## Menu Bindings
There are actually 3 sections in the .SC2Hotkeys files.  

`[Settings]`  
This is a high-level section with things like `AllowSetConflicts`. It does not get translated using the `KeyMappings.ini` file. It just gets copied.

`[Commands]`  
These are the unit commands, like `morph baneling nest` or `attack`.
Everything in this section gets translated from the left profile to the right profile using the values from `[LeftToRightMaps]` in the `KeyMappings.ini` file.

`[Hotkeys]`  
This section has a stupid name, but it has higher level commands like `open chat`, `show fps`, along with things like `create control group` or `save camera location`.
Everything in this section is not translated from left to right, except for all the values found in the `[MenuValues]` section of `KeyMappings.ini`.

## Source Control
Localizations are all found in the `build` folder, and that folder can be distributed.
The `build` folder should not be checked into source control as it will clog up the git history, so it won't be there when you clone the repo for the first time.
Just run the script to generate it.

The files in `hotkey_sources` *should* be checked into source control since they're considered a source file. 
If you make a change to a hotkey profile then go ahead and commit it.
