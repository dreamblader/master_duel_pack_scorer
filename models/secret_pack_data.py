class SecretPackData:

    def __init__(self, name, date) -> None:
        self.name = name
        self.date = date
        self.cards = []
        self.ocg_score = 0
        self.tcg_score = 0
    

    def add_card(self, card):
        self.cards.append(card)


    def __str__(self):
        date_str = self.date.strftime("%d/%m/%Y")
        return f"Secret Pack: {self.name} [{date_str}] - {self.cards}"