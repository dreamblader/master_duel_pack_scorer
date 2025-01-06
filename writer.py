import csv
import logging
from models.secret_pack_data import SecretPackData
from models.enums import DateRuleSet


def generate_csv(packs:list[SecretPackData]):
    for rule in DateRuleSet:
        __generate(packs, rule)
    #TODO THE MIN AND MAX CARDS IS EMPTY ????


def __generate(packs:list[SecretPackData], rule_set:DateRuleSet):
    my_score_header = ""
    packs.sort(key= lambda pack : (pack.date, pack.average_score[rule_set.value]))
    my_score_header = f"Total {rule_set.name} Score"
    file_id = rule_set.name.lower()
    filename = f"data/master-duel-progression-{file_id}.csv"
    logging.info(f"Generating {rule_set} CSV File at {filename}")
    
    with open(filename, 'w', newline='') as csvfile:
        stream_w = csv.writer(csvfile)
        stream_w.writerow(["Pack Name", "Release Date", my_score_header, "Pack Score Average", "Unlock Cards", "Most Older Cards", "Most Recent Cards"])
        for pack in packs:
            stream_w.writerow([pack.name, pack.date, pack.total_score[rule_set.value], pack.average_score[rule_set.value], pack.get_unlock_cards(), pack.get_min_cards_name(rule_set), pack.get_max_cards_name(rule_set)])
    