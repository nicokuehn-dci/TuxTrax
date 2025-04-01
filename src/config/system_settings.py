import configparser

config = configparser.ConfigParser()

# Default settings
config['Audio'] = {
    'sample_rate': '44100',
    'buffer_size': '512',
    'default_path': '~/samples'
}

config['MIDI'] = {
    'default_port': '0',
    'velocity_curve': 'exponential'
}

config['GUI'] = {
    'theme': 'dark',
    'default_scale': 'C Major'
}

config['AI'] = {
    'magenta_studio_path': '/usr/local/bin/magenta-studio'
}

# Write default settings to file
with open('system_settings.ini', 'w') as configfile:
    config.write(configfile)

def read_settings():
    config.read('system_settings.ini')
    return config

def write_settings(section, option, value):
    config.set(section, option, value)
    with open('system_settings.ini', 'w') as configfile:
        config.write(configfile)
