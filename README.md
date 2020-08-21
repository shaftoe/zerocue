# zerocue - zeros-out your CUE sheet file

Python-based command-line utility (CLI) to remove first leading `INDEX` track time from any subsequent `INDEX` timestamps in a CUE sheet file.

## Install

`pip install zerocue`

## Requirements

- Python >= 3.8.x

NOTE: this is the version I used to develop and test it but it should work with any version of Python above 3.x

## Usage

```text
usage: zerocue [-h] [-v] [-o OUTPUT | -w] cuefile

remove first INDEX track time from every following INDEXes in a CUE sheet file

positional arguments:
  cuefile               source CUE file (e.g playlist.cue)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         send informative logs to STDERR
  -o OUTPUT, --output OUTPUT
                        write to OUTPUT file instead of STDOUT
  -w, --inline          overwrite source CUE file
```

`zerocue` reads content from a [CUE sheet](https://en.wikipedia.org/wiki/Cue_sheet_(computing)) file (which name is the only accepted and required CLI argument) and prints the content of the same CUE sheet file with updated `INDEX` time values, i.e. set the first `INDEX` timestamp to `00:00:00` and remove the initial first `INDEX` track elapsed time from every subsequent `INDEX` record in the sheet.

## Examples

Assuming `playlist.cue` is a file in the current working directory which has the following example content (CUE sheet excerpt taken from <https://kodi.wiki/view/Cue_sheets>):

```cue
REM GENRE Ska
REM DATE 1991
REM DISCID D00DA810
REM COMMENT "ExactAudioCopy v0.95b4"
PERFORMER "The Specials"
TITLE "Singles"
FILE "The Specials - Singles.wav" WAVE
  TRACK 01 AUDIO
    TITLE "Gangsters"
    PERFORMER "The Specials"
    INDEX 01 01:57:31
  TRACK 02 AUDIO
    TITLE "Rudi, A Message To You"
    PERFORMER "The Specials"
    INDEX 00 02:47:74
    INDEX 01 02:48:27
  TRACK 03 AUDIO
    TITLE "Nite Klub"
    PERFORMER "The Specials"
    INDEX 00 05:41:50
    INDEX 01 05:42:27
```

than running `zerocue playlist.cue` will print the following output:

```cue
REM GENRE Ska
REM DATE 1991
REM DISCID D00DA810
REM COMMENT "ExactAudioCopy v0.95b4"
PERFORMER "The Specials"
TITLE "Singles"
FILE "The Specials - Singles.wav" WAVE
  TRACK 01 AUDIO
    TITLE "Gangsters"
    PERFORMER "The Specials"
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "Rudi, A Message To You"
    PERFORMER "The Specials"
    INDEX 00 00:50:43
    INDEX 01 00:50:71
  TRACK 03 AUDIO
    TITLE "Nite Klub"
    PERFORMER "The Specials"
    INDEX 00 03:44:19
    INDEX 01 03:44:71
```

To create a new CUE sheet you can either redirect `STDIN` to a (new) file, use the `--output` option to create a new file, or use the `--inline` option to update the source file.

These two commands should be equivalent and will replace `new_playlist.cue` content if already present:

- `zerocue playlist.cue > new_playlist.cue`
- `zerocue --output=new_playlist.cue playlist.cue`

while this will overwrite the content of `playlist.cue`:

- `zerocue --inline playlist.cue`

## Unit Tests

To run unit tests: `make dependencies tests`

NOTE: `make dependencies` will install `pytest` and `pylint` in your current environment. Probably you want to initialize a new Python _Virtualenv_ first:

```bash
git clone https://github.com/shaftoe/zerocue
cd zerocue
make install-venv
source .env/bin/activate
```

## Contribute

Contributions are welcome, just open an issue/pull request or [get in touch with me directly](https://a.l3x/in/contact) if you prefer.
