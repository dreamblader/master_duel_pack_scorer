from models.enums import DateRuleSet
from models.card_data import CardData
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
            max_score[DateRuleSet.OCG.value] = max(max_score[DateRuleSet.OCG.value], card.ocg_score)
            max_score[DateRuleSet.TCG.value] = max(max_score[DateRuleSet.TCG.value], card.tcg_score)
            min_score[DateRuleSet.OCG.value] = min(min_score[DateRuleSet.OCG.value], card.ocg_score)
            min_score[DateRuleSet.TCG.value] = min(min_score[DateRuleSet.TCG.value], card.tcg_score)
        
        for card in self.cards:
            if card.ocg_score == min_score:
                self.min_ocg_cards.append(card.name)
            if card.ocg_score == max_score:
                self.max_ocg_cards.append(card.name)
            if card.tcg_score == min_score:
                self.min_ocg_cards.append(card.name)
            if card.tcg_score == max_score:
                self.max_tcg_cards.append(card.name)
    

    def get_unlock_cards(self) -> str:
        ur = "Ultra Rare"
        sr = "Super Rare"
        unlock_cards = filter(lambda card: card.rarity == ur or card.rarity == sr, self.cards)
        return self.__get_names(unlock_cards)


    def get_max_cards_name(self, rule_set:DateRuleSet) -> str:
        match rule_set:
            case DateRuleSet.OCG:
                return self.__get_names(self.max_ocg_cards)
            case DateRuleSet.TCG:
                return self.__get_names(self.max_tcg_cards)
    

    def get_min_cards_name(self, rule_set:DateRuleSet) -> str:
        match rule_set:
            case DateRuleSet.OCG:
                return self.__get_names(self.min_ocg_cards)
            case DateRuleSet.TCG:
                return self.__get_names(self.min_tcg_cards)
            

    def __get_names(self, cards:list[CardData]) -> str:
        return ", ".join(card.name for card in cards)


    def __str__(self):
        date_str = self.date.strftime("%d/%m/%Y")
        return f"Secret Pack: {self.name} [{date_str}] || SCORE -> ({self.ocg_score})({self.tcg_score})"