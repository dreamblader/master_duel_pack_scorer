import datetime
from models.enums import DateRuleSet
class SecretPackData:

    def __init__(self, name, date) -> None:
        self.name = name
        self.date = date
        self.cards = []
        self.ocg_score = 0
        self.tcg_score = 0
        self.max_tcg_cards = []
        self.min_tcg_cards = []
        self.max_ocg_cards = []
        self.min_ocg_cards = []
    

    def add_card(self, card):
        self.cards.append(card)


    def calculate_score(self):
        max_score = [0] * 2
        min_score = [float("inf")] * 2
        for card in self.cards:
            self.ocg_score += card.ocg_score
            self.tcg_score += card.tcg_score
            max_score[DateRuleSet.OCG] = max(max_score[DateRuleSet.OCG], card.ocg_score)
            max_score[DateRuleSet.TCG] = max(max_score[DateRuleSet.TCG], card.tcg_score)
            min_score[DateRuleSet.OCG] = min(min_score[DateRuleSet.OCG], card.ocg_score)
            min_score[DateRuleSet.TCG] = min(min_score[DateRuleSet.TCG], card.tcg_score)
        
        for card in self.cards:
            if card.ocg_score == min_score:
                self.min_ocg_cards.append(card.name)
            if card.ocg_score == max_score:
                self.max_ocg_cards.append(card.name)
            if card.tcg_score == min_score:
                self.min_ocg_cards.append(card.name)
            if card.tcg_score == max_score:
                self.max_tcg_cards.append(card.name)
    

    def __str__(self):
        date_str = self.date.strftime("%d/%m/%Y")
        return f"Secret Pack: {self.name} [{date_str}] || SCORE -> ({self.ocg_score})({self.tcg_score})"