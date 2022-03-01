# GENOCC
**GENOCC** is a project to extract bilingual or multilingual parallel data from Wikipedia balanced in gender within occupations.

### Data Collection

The first step in our pipeline is to extract data from Wikidata along Wikipedia. Mainly, we collect a set of people *(from now on entities)*  with their occupation(s), gender, and Wikipedia links in all available languages. Afterwards, the user can decide which languages are of their interest to adapt the monolingual extraction phase to their needs. 

[**As of now**] To make it run, we just have to execute the following command from the `/collection` directory - within the file you can modify the configuration:

```bash
python3 manager.py
```

[**TODO**] To make it run, we just have to execute the following command after configuring `config.json` file with the corresponding paths (*if default configuration isn't desired*):

```bash
sh manager.sh
```

The following explains how to taylor and run each part of the project individually.

#### Information Extraction 

1. `collection/information/get_occupations.py`: extracts all the occupations present in Wikidata.
2. `collection/information/get_entities_for_occupations.py`: for each occupation, we gather the data of every entity that works in the related occupation.
3. `collection/information/get_languages.py` & `collection/information/get_gender.py`: for each entity from the previous step, we determine the gender information and related Wikipedia links in all available languages

![](./static/img/extraction.png)

You can execute the whole **information extraction** step by running: `python3 pipeline.py`.

#### Language and Gender specification

#### Entity Biography Scraping

We scrape all the monolingual data from the corresponding Wikipedia biography, only for entities with a link for all of the given languages.

[**TODO**] To make it run...  

#### Preprocessing 



### Requirements

All steps requires **Python >= 3.6**. One can install all requiremets executing:

```
pip3 install -r requirements.txt
```

