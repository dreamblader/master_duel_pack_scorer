import csv
import logging
from models.secret_pack_data import SecretPackData
from models.enums import DateRuleSet


def generate_csv(packs:SecretPackData):
    for rule in DateRuleSet:
        __generate(packs, rule)


def __generate(packs, rule_set):
    my_score_heaeder = ""
    
    match rule_set:
        case DateRuleSet.OCG:
            packs.sort(key= lambda pack : (pack.date, pack.ocg_score))
            my_score_heaeder = "OCG Score"
            file_id = "ocg"
        case DateRuleSet.TCG:
            packs.sort(key= lambda pack : (pack.date, pack.tcg_score))
            my_score_heaeder = "TCG Score"
            file_id = "tcg"
    
    filename = f"data/master-duel-progression-{file_id}.csv"
    logging.info(f"Generating {rule_set} CSV File at {filename}")
    with open(filename, 'w', newline='') as csvfile:
        stream_w = csv.writer(csvfile)
        stream_w.writerow(["Pack Name", "Release Date", my_score_heaeder, "Pack Score Average", "Unlock Cards", "Most Older Cards", "Most Recent Cards"])
        for pack in packs:
            my_score = pack.ocg_score if rule_set == DateRuleSet.OCG else pack.tcg_score
            avg = my_score/len(pack.cards)
            stream_w.writerow([pack.name, pack.date, my_score, avg, pack.get_unlock_cards(), pack.get_min_cards_name(rule_set), pack.get_max_cards_name(rule_set)])
    