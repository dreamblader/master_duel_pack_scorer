from models.enums import DateRuleSet
from models.card_data import CardData
class SecretPackData:

    def __init__(self, name, date) -> None:
        self.name = name
        self.date = date
        self.cards = []
        self.max_card = [None] * 2
        self.min_card = [None] * 2
        self.total_score = [0] * 2
        self.average_score = [0] * 2


    def add_card(self, card):
        self.cards.append(card)


    def calculate_score(self):
        max_score = [0] * 2
        min_score = [float("inf")] * 2
        for card in self.cards:
            self.total_score[DateRuleSet.OCG.value] += card.ocg_score
            self.total_score[DateRuleSet.TCG.value] += card.tcg_score
            for rule in DateRuleSet:
                card_score = card.ocg_score if rule == DateRuleSet.OCG else card.tcg_score
                if(card_score >= max_score[rule.value]):
                    max_score[rule.value] = card_score
                    self.max_card[rule.value] = card
                if(card_score <= min_score[rule.value]):
                    min_score[rule.value] = card_score
                    self.min_card[rule.value] = card
        for rule in DateRuleSet:
            self.average_score[rule.value] = round(self.total_score[rule.value]/len(self.cards), 2)


    def get_unlock_cards(self) -> str:
        ur = "Ultra Rare"
        sr = "Super Rare"
        unlock_cards = filter(lambda card: card.rarity == ur or card.rarity == sr, self.cards)
        return self.__get_names(unlock_cards)


    def get_max_cards_name(self, rule_set:DateRuleSet) -> str:
        return self.max_card[rule_set.value].name


    def get_min_cards_name(self, rule_set:DateRuleSet) -> str:
        return self.min_card[rule_set.value].name


    def __get_names(self, cards:list[CardData]) -> str:
        return ", ".join(card.name for card in cards)


    def __str__(self):
        date_str = self.date.strftime("%d/%m/%Y")
        return f"Secret Pack: {self.name} [{date_str}] \
              || AVERAGE SCORE -> ({self.average_score[DateRuleSet.OCG.value]}) ({self.average_score[DateRuleSet.TCG.value]}) \
              || TOTAL SCORE -> ({self.total_score[DateRuleSet.OCG.value]}) ({self.total_score[DateRuleSet.TCG.value]})"