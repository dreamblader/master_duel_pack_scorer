import datetime

ygo_start_date = datetime.date(1999, 2, 4)
class SecretPackData:

    def __init__(self, name, date) -> None:
        self.name = name
        self.date = date
        self.cards = []
        self.ocg_score = 0
        self.tcg_score = 0
    

    def add_card(self, card):
        self.cards.append(card)


    def calculate_score(self):
        for card in self.cards:
            self.ocg_score += (card.ocg_date - ygo_start_date).days
            self.tcg_score += (card.tcg_date - ygo_start_date).days

    

    def __str__(self):
        date_str = self.date.strftime("%d/%m/%Y")
        return f"Secret Pack: {self.name} [{date_str}] || SCORE -> ({self.ocg_score})({self.tcg_score})"