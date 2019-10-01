# coding: utf-8
from __future__ import unicode_literals

import bz2
import json
import logging

from bin.wiki_entity_linking.wiki_namespaces import WD_META_ITEMS

logger = logging.getLogger(__name__)


def read_wikidata_graph(wikidata_file):
    with bz2.open(wikidata_file, mode='rb') as file:
        for cnt, line in enumerate(file):
            clean_line = line.strip()
            if clean_line.endswith(b","):
                clean_line = clean_line[:-1]
            if len(clean_line) > 1:
                obj = json.loads(clean_line)
                entry_type = obj["type"]
                if entry_type != "item":
                    print(line)


def read_wikidata_entities_json(wikidata_file, limit=None, to_print=False, lang="en", parse_descriptions=True):
    # Read the JSON wiki data and parse out the entities. Takes about 7u30 to parse 55M lines.
    # get latest-all.json.bz2 from https://dumps.wikimedia.org/wikidatawiki/entities/

    site_filter = '{}wiki'.format(lang)

    # filter: currently defined as OR: one hit suffices to be removed from further processing
    exclude_list = WD_META_ITEMS

    # years, months, days, ordinial numbers, ...
    exclude_list.append(["Q577", "Q3186692", "Q19828", "Q3311614", "Q6743362", "Q47018901", "Q47018478",
                         "Q47150325", "Q1790144", "Q21199", "Q13366104", "Q50707"])
    neg_prop_filter = {'P31': exclude_list}

    title_to_id = dict()
    id_to_descr = dict()

    # parse appropriate fields - depending on what we need in the KB
    parse_properties = False
    parse_sitelinks = True
    parse_labels = False
    parse_aliases = False
    parse_claims = True

    cnt = 0

    with bz2.open(wikidata_file, mode='rb') as file:
        for cnt, line in enumerate(file):
            if limit and cnt >= limit:
                break
            if cnt % 500000 == 0 and cnt > 0:
                logger.info("processed {} lines of WikiData JSON dump".format(cnt))
            clean_line = line.strip()
            if clean_line.endswith(b","):
                clean_line = clean_line[:-1]
            if len(clean_line) > 1:
                obj = json.loads(clean_line)
                entry_type = obj["type"]

                if entry_type == "item":
                    keep = True

                    claims = obj["claims"]
                    if parse_claims:
                        for prop, value_set in neg_prop_filter.items():
                            claim_property = claims.get(prop, None)
                            if claim_property:
                                for cp in claim_property:
                                    cp_id = (
                                        cp["mainsnak"]
                                        .get("datavalue", {})
                                        .get("value", {})
                                        .get("id")
                                    )
                                    cp_rank = cp["rank"]
                                    if cp_rank != "deprecated" and cp_id in value_set:
                                        keep = False

                    if not keep:
                        print("removed:", obj["id"], obj["labels"])
                    else:
                        unique_id = obj["id"]

                        if to_print:
                            print("ID:", unique_id)
                            print("type:", entry_type)

                        # parsing all properties that refer to other entities
                        if parse_properties:
                            for prop, claim_property in claims.items():
                                cp_dicts = [
                                    cp["mainsnak"]["datavalue"].get("value")
                                    for cp in claim_property
                                    if cp["mainsnak"].get("datavalue")
                                ]
                                cp_values = [
                                    cp_dict.get("id")
                                    for cp_dict in cp_dicts
                                    if isinstance(cp_dict, dict)
                                    if cp_dict.get("id") is not None
                                ]
                                if cp_values:
                                    if to_print:
                                        print("prop:", prop, cp_values)

                        found_link = False
                        if parse_sitelinks:
                            site_value = obj["sitelinks"].get(site_filter, None)
                            if site_value:
                                site = site_value["title"]
                                if to_print:
                                    print(site_filter, ":", site)
                                title_to_id[site] = unique_id
                                found_link = True

                        if parse_labels:
                            labels = obj["labels"]
                            if labels:
                                lang_label = labels.get(lang, None)
                                if lang_label:
                                    if to_print:
                                        print(
                                            "label (" + lang + "):", lang_label["value"]
                                        )

                        if found_link and parse_descriptions:
                            descriptions = obj["descriptions"]
                            if descriptions:
                                lang_descr = descriptions.get(lang, None)
                                if lang_descr:
                                    if to_print:
                                        print(
                                            "description (" + lang + "):",
                                            lang_descr["value"],
                                        )
                                    id_to_descr[unique_id] = lang_descr["value"]

                        if parse_aliases:
                            aliases = obj["aliases"]
                            if aliases:
                                lang_aliases = aliases.get(lang, None)
                                if lang_aliases:
                                    for item in lang_aliases:
                                        if to_print:
                                            print(
                                                "alias (" + lang + "):", item["value"]
                                            )

                        if to_print:
                            print()

    # log final number of lines processed
    logger.info("Finished. Processed {} lines of WikiData JSON dump".format(cnt))
    return title_to_id, id_to_descr


def write_entity_files(entity_def_output, title_to_id):
    with entity_def_output.open("w", encoding="utf8") as id_file:
        id_file.write("WP_title" + "|" + "WD_id" + "\n")
        for title, qid in title_to_id.items():
            id_file.write(title + "|" + str(qid) + "\n")


def write_entity_description_files(entity_descr_output, id_to_descr):
    with entity_descr_output.open("w", encoding="utf8") as descr_file:
        descr_file.write("WD_id" + "|" + "description" + "\n")
        for qid, descr in id_to_descr.items():
            descr_file.write(str(qid) + "|" + descr + "\n")
