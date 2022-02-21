# Mealie Integration
This repository contains a mealie integration for home assistant. This project is still under construction. You can set up your own mealie integration using [this guide](https://hay-kot.github.io/mealie/documentation/getting-started/introduction/).

## Included sensors
* Total number of recipies
* Number of untagged recipies
* Number of uncategorized recipes
* Current meal plan
  * Start and and date
* Today's recipe
  * Url to the recipe

## TODO
* [x] Create API client
  * [x] Authorization
  * [x] Store credentials
  * [x] Add first endpoint (meal plan for this week)
  * [x] Tests
* [ ] Add Home Assistant configuration
  * [x] Hook up API client to home assistant code
  * [x] Fix names of sensors
  * [ ] Figure out how to test integration
* [ ] Translations for sensor names / units
* [ ] Integration tests
* [x] Add more endpoints / sensors
* [ ] Extract mealie code to separate api wrapper
* [ ] [Optional] switch to pydantic for models
* [ ] ...
