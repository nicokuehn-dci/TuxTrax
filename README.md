# TuxTrax: Unleash Your Inner Penguin DJ

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Ubuntu-First](https://img.shields.io/badge/Platform-Linux%20(Ubuntu)-brightgreen)
![Python](https://img.shields.io/badge/Language-Python-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-orange)

## Jam Like a Penguin: The Ubuntu-First Live Performance Sampler & Mixer

**TuxTrax** is a powerful, open-source live performance sampler and mixer, built from the ground up for Ubuntu and the vibrant Linux audio community. Embrace the spirit of Tux, the Linux penguin, and unleash your creativity with this powerful and versatile tool. Whether you're a seasoned DJ or just starting your musical journey, TuxTrax combines intuitive sampling, mixing, and performance features with cutting-edge AI-powered tools, providing everything you need to create captivating live soundscapes.

## Core Features - Assembled By Penguins

*   **Sampler Section:** Effortlessly import, slice, and manipulate samples with MIDI mapping for full expressive control.
*   **Mixer Section:** Craft polished mixes with analog-style channel strips, a pro-grade effects rack, and dynamic sidechain compression.
*   **Ubuntu-First Focus:** Experience exceptional low-latency performance thanks to our JACK Audio integration.

## Feature Highlights: From Ice Floe to Stage

### Sampler Section: Your Palette of Sound

*   **Multi-Sample Import:** Drag and drop WAV, MP3, and FLAC files, then automatically slice loops for rhythmic perfection.
*   **Smart Pitch/Time:** Manipulate tempo and pitch with ease. The Paulstretch algorithm delivers pristine time-stretching, while auto-tune helps lock your samples into perfect harmony.
*   **Sampler Modes:** Explore a range of modes:
    *   **One-Shot:** Perfect for percussive hits and short samples.
    *   **ADSR Envelopes:** Sculpt the dynamics of your sounds.
    *   **Loop Modes:** Create evolving textures and soundscapes.
*   **MIDI Mapping:** Assign samples to notes or pads for expressive play with drum pads and melodic instruments.

### Mixer Section: Sculpt Your Sonic Landscape

*   **Analog-Style Channel Strips:** Tweak levels, pan, and EQ on each channel for a polished, balanced mix. Choose from a variety of EQ styles to impart character and shape to your tracks.
*   **Pro Effects Rack:** Elevate your mixes with high-quality effects:
    *   **Inserts:** Inject warmth and character with the Tube Saturator, capture vintage vibes with Tape Emulation, or add digital grit with the Bitcrusher.
    *   **Sends:** Generate immersive sonic spaces with Convolution Reverb, build hypnotic rhythms with Analog Delay, or add swirling movement with Phaser, Chorus, Flanger, and Stutter effects.
*   **Sidechain Compression:** Add rhythmic pumping to your mix by ducking channels with kick drums or basslines.

## Pro Features: Evolve Your Sound

### AI-Powered Workflow: The Future of Sound

*   **Auto-Tag Samples:** Spend less time organizing and more time creating, thanks to ML-driven tagging for genre, instrument type, key, and BPM.
*   **Smart Sample Matching:** Uncover hidden sonic gems by finding harmonically compatible samples.
*   **AI Mastering:** Achieve a professional, polished sound with one-click EQ, limiter, and stereo widening.
*   **Style Transfer:** Transform your audio between genres. Want to turn a rock riff into a DnB banger? TuxTrax has you covered! (Experimental feature)

### Sample Library Integration: Dive Into Your Sound Collection

*   **Deep Library Scanning:** Automatically index your Splice, Loopmasters, or other sample folders.
*   **Cloud Sync:** Access your samples from anywhere by linking TuxTrax to your cloud storage provider (Splice, Noiiz, Google Drive, Dropbox).
*   **Auto-Fill Channels:** Spark inspiration with:
    *   **Style-Based Channel Population:** Quickly create complete kits based on genre (e.g., "Hip-Hop Kit").
    *   **"Surprise Me" Randomization:** Embrace the unexpected and discover new sounds.

### MIDI & Sequencing: Sequence Your Way

*   **MIDI Style Library:** Jumpstart your creativity with:
    *   **Genre Templates:** Load pre-made templates for House, Trap, Techno, Lo-fi, and more.
    *   **Humanization:** Inject groove and swing into your MIDI sequences with realistic humanization templates.
*   **MIDI Drag & Drop:** Seamlessly export MIDI clips to your favorite DAWs or hardware for further refinement.
*   **MIDI Learn:** Take hands-on control by mapping hardware knobs and faders to TuxTrax parameters.

### Modulation & Automation: Bring Your Sounds to Life

*   **LFO Tool:** Add dynamic movement by modulating FX parameters like filter cutoff or tremolo depth.
*   **Automation Lanes:** Precisely control volume, pan, and FX parameters over time with custom-drawn automation curves.

### Hardware Integration: Bridge the Digital and Analog Worlds

*   **Eurorack Sync:** Integrate with modular synthesizers using CV/Gate support via `python-osc`.
*   **DAW Controller Support:** Enjoy tactile control with popular controllers like Akai APC and Ableton Push.

### Collaboration: Create Together

*   **Cloud Projects:** Collaborate with other penguins by syncing your projects with Google Drive or Dropbox, complete with versioning.
*   **Live Collaboration (Experimental):** Jam with musicians in real-time with our WebSockets + Firebase-powered live editing feature.

### Visual Feedback: See the Sound

*   **Spectrogram View:** Analyze the frequency content of your audio with real-time spectrogram visualization powered by `pyqtgraph`.
*   **Phase Correlation Meter:** Prevent mono compatibility issues with real-time phase monitoring.

## Unique Selling Points: Why Choose TuxTrax?

*   **Vintage Mode:** Add the warmth and character of classic analog gear with tape hiss and vinyl crackle emulation.
*   **Modular FX Grid:** Design your own custom effects chains with drag-and-drop routing (inspired by Bitwig).
*   **Live Looping:** Overdub and layer sounds in real-time with our intuitive live looping functionality (inspired by Boss RC-505).
*   **Ubuntu-First:** Optimized for low-latency performance and a smooth user experience on Linux. **This isn't just cross-platform, it's built for Linux first.**

## Tech Stack: Under the Hood

TuxTrax is built on a foundation of powerful, open-source technologies:

*   **Python Libraries:**
    *   **Audio Engine:** `pedalboard`, `sounddevice`, `pydub`
    *   **AI/ML:** `librosa`, `tensorflow-lite`
    *   **GUI:** `PyQt5`, `DearPyGui`, `pyqtgraph`
    *   **Cloud:** `boto3`, `firebase-admin`, `websockets`
    *   **MIDI/CV:** `mido`, `python-rtmidi`, `python-osc`
*   **Performance Optimizations:**
    *   **Real-Time Audio:** JACK Audio (`jackd`)
    *   **C Extensions:** `cython`/`numba` for blazing-fast DSP.
    *   **Multicore Processing:** Harness the power of modern CPUs with `ray`/`multiprocessing`.

## Getting Started: Let's Make Some Noise!

1.  **Clone the repository:**

    ```
    git clone git@github.com:nicokuehn-dci/TuxTrax.git
    cd TuxTrax
    ```

2.  **Dive into the [Setup Guide](docs/SETUP.md) for detailed installation and configuration instructions.**

## Contributing: Join the Penguin Party

We welcome contributions from the open-source community! Whether you're a seasoned developer, a talented sound designer, or just eager to help, there's a place for you in the TuxTrax community. Check out our [Contribution Guidelines](CONTRIBUTING.md) for more information.

## License: Open Source, Open Minds

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support: We're Here to Help

Encounter a bug? Have a feature request? Let us know by opening an issue on GitHub!

## Roadmap: The Future of TuxTrax

*   [ ] **Implement Style Transfer:** Expand our AI-powered style transfer capabilities.
*   [ ] **Expand the MIDI Style Library:** Provide even more genre-specific MIDI templates.
*   [ ] **Improve Cloud Collaboration Features:** Make real-time jamming even more seamless.
*   [ ] **Native Plugin Support**: Host VST/AU plugins within TuxTrax.

## Show Your Support: Give a Penguin a Fish

If you find TuxTrax useful, please give this project a ⭐ to show your support! And don't forget to share your creations with the world!

## Connect with the Community:

*   [ ] Discord: (Add a link to a Discord server if you have one)
*   [ ] Forum: (Add a link to a forum or discussion board)

---

Made with ❤️ for the love of music and open source by Nico Kühn.



