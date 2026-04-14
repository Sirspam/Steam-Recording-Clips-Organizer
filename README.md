# Steam Recording Clips Organizer

A simple Python script for bulk organizing clips saved by Steam Recording.
Can be used directly in clips directory or from the command line.

## Features
- Moving clips into game folders
- Converting clip names from 12 hour format to 24 hour format

## Requirements
- Python 3.14

## Usage
Download [organize_steam_clips.py](https://github.com/Sirspam/Steam-Recording-Clips-Organizer/blob/main/organize_steam_clips.py) from repository

The script's intended usage is to be saved in the clips directory and run with Python, this will organize files in the same directory as the script with all of the features enabled.

Alternatively, the script can be ran in the command line.

Example:

```bash
py organize_steam_clips.py
```

Additionally, the command line accepts the following optional arguments:
### Command Line Arguments
|Argument|Short|Parameter|Description|
|---|---|---|---|
|--path|-p|Path|Path to Steam Recording clips|
|--output-path|-o|Path|Path to output organized clips to|
|--no-organize| | |Do not organize clips into folders|
|--no-24hr-rename| | |Do not convert 12 hour file names to 24 hour|
|--dry-run| | |Print the changes that would be made without actually modifying files|
