<div align="center">
  <a href="https://github.com/tom-bartk/tuicub">
    <img src="https://static.tuicub.com/img/tuicub-logo.png" alt="Logo" width="335" height="115">
  </a>

<div align="center">
<a href="https://jenkins.tombartk.com/job/tuicub/">
  <img alt="Jenkins" src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Ftuicub">
</a>
<a href="https://jenkins.tombartk.com/job/tuicub/lastCompletedBuild/testReport/">
  <img alt="Jenkins tests" src="https://img.shields.io/jenkins/tests?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Ftuicub">
</a>
<a href="https://jenkins.tombartk.com/job/tuicub/lastCompletedBuild/coverage/">
  <img alt="Jenkins Coverage" src="https://img.shields.io/jenkins/coverage/apiv4?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Ftuicub%2F">
</a>
<a href="https://www.gnu.org/licenses/agpl-3.0.en.html">
  <img alt="PyPI - License" src="https://img.shields.io/pypi/l/tuicub">
</a>
<a href="https://pypi.org/project/tuicubserver/">
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/tuicub">
</a>
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>
</div>

  <p align="center">
    <b><a href="https://tuicub.com">tuicub</a></b> - online multiplayer board game in your terminal.
  </p>
   <p align="center">
    <a href="https://tuicub.com"><strong>Website</strong></a>
    ·
    <a href="https://github.com/tom-bartk/tuicub"><strong>Server</strong></a>
  </p>
</div>


## Screenshots

#### Gameplay
![Screenshot showing gameplay](https://static.tuicub.com/img/tuicub_screenshot_1.png)

#### Public gamerooms
![Screenshot showing starting screen](https://static.tuicub.com/img/tuicub_screenshot_2.png)

#### Gameroom
![Screenshot showing starting screen](https://static.tuicub.com/img/tuicub_screenshot_5.png)

#### Gameplay
![Screenshot showing starting screen](https://static.tuicub.com/img/tuicub_screenshot_3.png)


## Features

### Application

- Simple and intuitive controls,
- Public gamerooms,
- Modern user interface,
- Free and open-source.

### Code

- Fully typed code ([PEP-484](https://peps.python.org/pep-0484/)),
- Testable, clean layered architecture,
- 100% tests coverage,
- Most public interfaces documented with [Google style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

## Installation

### Using `pip`

Tuicub is available as [`tuicub`](https://pypi.org/project/tuicub/) on PyPI:
```sh
pip install tuicub
```

### Manually

Start by cloning the repository:

```sh
git clone https://github.com/tom-bartk/tuicub.git
cd tuicub
```

Then, install the project's dependencies:

```sh
python -m pip install -e .
```

You can now launch the game by running:

```
$ python -m src.tuicub --help

Usage: src.tuicub [-h] [-d] [-u URL] [--events-host HOST] [--events-port PORT] [--logfile PATH] [--theme PATH]

An online multiplayer board game in your terminal.

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug mode. (default: False)
  -u URL, --api-url URL
                        Base URL for the API. (default: https://api.tuicub.com)
  --events-host HOST    Hostname of the events server. (default: api.tuicub.com)
  --events-port PORT    Port of the events server. (default: 23432)
  --logfile PATH        If debug is enabled, write logs to file at this path. (default: /tmp/tuicub.log)
  --theme PATH          Path to the file containing the custom color theme. (default: None)
```

## Configuration

#### Color theme

Tuicub uses a modified [gruvbox](https://github.com/morhetz/gruvbox) color theme. A custom color theme can be configured using a `toml` file with the following structure and default values:

```toml
fg_black = "#191b1c"
fg0 = "#fbf1c7"
fg1 = "#ebdbb2"
fg2 = "#d5c4a1"
fg3 = "#bdae93"
fg4 = "#a89984"
fg5 = "#857a6b"
bg0 = "#191b1c"
bg1 = "#1d2021"
bg2 = "#232425"
bg3 = "#282828"
bg4 = "#2d2c2c"
bg5 = "#32302f"
bg6 = "#3c3836"
bg7 = "#504945"
bg8 = "#665c54"
gray = "#928374"
aqua = "#8ec07c"
aqua_dim = "#343d34"
purple = "#d3869b"
purple_dim = "#413339"
red = "#fb4934"
red_dark = "#cc241d"
red_dim = "#462726"
blue = "#83a598"
blue_dim = "#304142"
yellow = "#fabd2f"
yellow_light = "#fac74d"
yellow_dark = "#d79921"
yellow_dim = "#67552a"
green = "#b8bb26"
green_light = "#c5c646"
green_dark = "#98971a"
green_dim = "#454528"
orange = "#fe8109"
orange_dark = "#d65d0e"
tile_fg_selected = "#fbf1c7"
tile_bg_light = "#ede6cd"
tile_bg = "#ddd1ba"
tile_blue = "#00abc8"
tile_yellow = "#f39300"
tile_red = "#d6070f"
tile_black = "#0c0a05"
tile_black_selected = "#747474"
tile_selected_border = "#504945"
```

You can change only some of the colors - omitted colors will fall back to default values.

To use a custom theme, set the `--theme` option to the path of your theme file when running the game:

```sh
tuicub --theme ~/mytuicub/theme.toml
```


## Running

```
Usage: tuicub [-h] [-d] [-u URL] [--events-host HOST] [--events-port PORT] [--logfile PATH] [--theme PATH]

An online multiplayer board game in your terminal.

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug mode. (default: False)
  -u URL, --api-url URL
                        Base URL for the API. (default: https://api.tuicub.com)
  --events-host HOST    Hostname of the events server. (default: api.tuicub.com)
  --events-port PORT    Port of the events server. (default: 23432)
  --logfile PATH        If debug is enabled, write logs to file at this path. (default: /tmp/tuicub.log)
  --theme PATH          Path to the file containing the custom color theme. (default: None)
```

Following example starts the game with a custom API and events server:

```sh
tuicub --api-url http://localhost:8080 --events-host localhost
```

## Rules

Tuicub is inspired by the popular tile-based game [_Rummikub&reg;_](https://rummikub.com). Most of the game rules
of _Rummikub&reg;_ apply also to tuicub.

[**Rules of _Rummikub&reg;_.**](https://en.wikipedia.org/wiki/Rummikub#Rules)


## See also

* [tom-bartk/tuicub-server](https://github.com/tom-bartk/tuicub-server) - the server for tuicub,
* [tom-bartk/tuicub-website](https://github.com/tom-bartk/tuicub-website) - the tuicub's website.

#### Packages used in `tuicub`
* [tom-bartk/pydepot](https://github.com/tom-bartk/pydepot) - strongly-typed, scalable state container for Python,
* [tom-bartk/pyllot](https://github.com/tom-bartk/pyllot) - application routing with event-driven finite-state machine,
* [tom-bartk/httperactor](https://github.com/tom-bartk/httperactor) - async interactor for HTTP requests using a template method.
* [tom-bartk/eventoolkit](https://github.com/tom-bartk/eventoolkit) - client-side toolkit for abstract events.
* [tom-bartk/asockit](https://github.com/tom-bartk/asockit) - client-side toolkit for async sockets. 



## License
![AGPLv3](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)
```monospace
Copyright (C) 2023 tombartk 

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU Affero General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.
If not, see https://www.gnu.org/licenses/.
```
