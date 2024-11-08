import csv
from models.secret_pack_data import SecretPackData
from models.enums import DateRuleSet


def generate_csv(packs:SecretPackData):
    for rule in DateRuleSet:
        __generate(packs, rule)


def __generate(packs, rule_set):
    filename = f"master-duel-progression-{rule_set}.csv"
    with open(filename, 'w', newline='') as csvfile:
        stream_w = csv.writer(csvfile)
        #TODO