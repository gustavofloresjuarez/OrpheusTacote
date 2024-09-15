<!-- PROJECT INTRO -->

OrpheusDL - Qobuz-MOD 🦑💿
=================

A Qobuz-MOD module for the OrpheusDL modular archival music program

[Report Bug](https://github.com/yarrm80s/orpheusdl/issues)
·
[Request Feature](https://github.com/yarrm80s/orpheusdl/issues)


## Table of content 📊

- [About OrpheusDL - Qobuz-MOD](#about-orpheusdl---qobuz-mod-ℹ%EF%B8%8F)
- [Getting Started](#getting-started-)
    - [Prerequisites](#prerequisites-%EF%B8%8F)
    - [Installation](#installation-)
- [Usage](#usage-)
- [Configuration](#configuration-%EF%B8%8F)
    - [Global](#global-%EF%B8%8F)
    - [Qobuz-MOD](#qobuz-mod-)
- [Contact](#contact-)


<!-- ABOUT ORPHEUS -->
## About OrpheusDL - Qobuz-MOD ℹ️

OrpheusDL - Qobuz-MOD is a module written in Python which allows archiving from **Qobuz** for the modular music archival program.


<!-- GETTING STARTED -->
## Getting Started 🚀

Follow these steps to get a local copy of Orpheus up and running:

### Prerequisites ⚠️📜

* Already have [OrpheusDL](https://github.com/yarrm80s/orpheusdl) installed

### Installation 💻

* ⚠️ NOTE: If you download the repository manually, when you unzip the module folder, please rename it to `qobuz`.
1. Clone the repo inside the folder `orpheusdl/modules/` ⬇️.
   ```sh
   git clone https://github.com/Jun-LLYLM-01/orpheusdl-qobuz-mod.git qobuz
   ```
2. Execute: ▶️
   ```sh
   python orpheus.py
   ```
3. Now the `config/settings.json` file should be updated with the Qobuz settings 🔄📝

<!-- USAGE EXAMPLES -->
## Usage 📱

Just call `orpheus.py` with any link you want to archive ⬇️🎶:

```sh
python orpheus.py https://open.qobuz.com/album/n0qk1ywkb9z3a
```

<!-- CONFIGURATION -->
## Configuration ⚙️

You can customize every module from Orpheus individually and also set general/global settings which are active in every
loaded module. You'll find the configuration file here: `config/settings.json`

### Global 🌎⚙️

```json5
"global": {
    "general": {
        // ...
        "download_quality": "hifi"
    },
    "formatting": {
        "album_format": "{album_name}{quality}{explicit}",
        // ...
    }
    // ...
}
```

`download_quality`: Choose one of the following settings:
* "hifi": FLAC up to 192/24
* "lossless": FLAC with 44.1/16
* "high": MP3 320 kbit/s

`album_format`:
* `{quality}` will add the format which you can specify under `quality_format` (see below), default:
    ```
     [192kHz 24bit]
    ```
  depending on the maximum available album quality and the chosen `download_quality` setting
* `{explicit}` will add
    ```
     [E]
    ```
  to the album path 

### Qobuz-MOD 💿
```json5
"qobuz": {
    "app_id": "",
    "app_secret": "",
    "quality_format": "{sample_rate}kHz {bit_depth}bit",
    "auth_with_tokens": true,
    "username_or_UserID": "",
    "password_or_Token": ""
}
```
`app_id`: Enter a valid mobile app id 🆔

`app_secret`: Enter a valid mobile app secret 🔒

`quality_format`: How the quality is formatted when `{quality}` is present in `album_format`, possible values are 
`{sample_rate}` and `bit_depth`.

**NOTE: Set the `"quality_format": ""` to remove the quality string even if `{quality}` is present in `album_format`. 
Square brackets `[]` will always be added before and after the `quality_format` in the album path.**

Authenticate with tokens or authenticate with username/password. 🔐 🔑

`username_or_UserID`: Enter your qobuz email address or UserID here

`password_or_Token`: Enter your qobuz password or UserAuthToken here

**NOTE: also support md5 password.**

<!-- Contact -->
 ## Contact 🔗

Yarrm80s - [@yarrm80s](https://github.com/yarrm80s)

Dniel97 - [@Dniel97](https://github.com/Dniel97)

Original Project Link: [OrpheusDL Qobuz Public GitHub Repository](https://github.com/yarrm80s/orpheusdl-qobuz)
