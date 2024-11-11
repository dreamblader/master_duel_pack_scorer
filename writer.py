import csv
from models.secret_pack_data import SecretPackData
from models.enums import DateRuleSet


def generate_csv(packs:SecretPackData):
    for rule in DateRuleSet:
        __generate(packs, rule)


def __generate(packs, rule_set):
    my_score = ""
    other_score = ""
    match rule_set:
        case DateRuleSet.OCG:
            packs.sort(key= lambda pack : (pack.date, pack.ocg_score))
            my_score = "OCG Score"
            other_score = "TCG Score"
        case DateRuleSet.TCG:
            packs.sort(key= lambda pack : (pack.date, pack.tcg_score))
            my_score = "TCG Score"
            other_score = "OCG Score"
    
    filename = f"master-duel-progression-{rule_set}.csv"
    with open(filename, 'w', newline='') as csvfile:
        stream_w = csv.writer(csvfile)
        stream_w.writerow("Pack Name", "Release Date", my_score, other_score, "Unlock Cards", "Min Score Card", "Max Score Card")
        #TODO