KEYBINDINGS = {
    'transport': {
        'play': 'Space',
        'stop': 'Shift+Space',
        'record': 'Ctrl+R'
    },
    'navigation': {
        'next_track': 'Ctrl+Right',
        'prev_track': 'Ctrl+Left'
    },
    'editing': {
        'cut': 'Ctrl+X',
        'copy': 'Ctrl+C',
        'paste': 'Ctrl+V'
    }
}

MIDI_CC_MAPPINGS = {
    1: 'filter_cutoff',
    2: 'resonance',
    3: 'drive_amount'
}

MIDI_SETUP_PROTOCOLS = {
    'list_devices': 'aconnect -i -o',
    'list_amidi_devices': 'amidi -l',
    'connect_devices': 'aconnect <input_id> <output_id>',
    'recording_choices': {
        'list_recording_devices': 'arecord -l',
        'set_recording_format_bitrate': 'arecord -D plughw:<card_number>,<device_number> -f <format> -r <bitrate> -d <duration> <output_file>'
    },
    'list_all_midi_devices': 'aconnect -l'
}
