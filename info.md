[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
[![Project Maintenance][maintenance-shield]][user_profile]
[![License][license-shield]][license]
[![GitHub Activity][commits-shield]][commits]

{% if prerelease %}

# This is a Beta version!

{% endif %}

# Mealie Integration

This repository contains a mealie integration for home assistant. This project is still under construction. You can set up your own mealie integration using [this guide](https://hay-kot.github.io/mealie/documentation/getting-started/introduction/).

**This integration will set up the following platforms.**

| Platform | Description         |
| -------- | ------------------- |
| `sensor` | Show info from API. |

## Installation

1. Install via HACS
2. Configure via UI

## Included sensors

- Total number of recipies
- Number of untagged recipies
- Number of uncategorized recipes
- Current meal plan
  - Start and and date
- Today's recipe
  - Url to the recipe

[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
[releases-shield]: https://img.shields.io/github/release/marvingfx/home-assistant-mealie-integration.svg
[releases]: https://github.com/marvingfx/home-assistant-mealie-integration/releases
[user_profile]: https://github.com/marvingfx
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40marvingfx-blue.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/marvingfx/home-assistant-mealie-integration.svg
[commits]: https://github.com/marvingfx/marvingfx/home-assistant-mealie-integration/commits/main
[license]: https://github.com/marvingfx/home-assistant-mealie-integratio/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/marvingfx/home-assistant-mealie-integration.svg
