import datetime

class CardData:

    def __init__(self, name) -> None:
        self.name = name
        self.type = ""
        self.rarity = ""
    
    def set_dates(self, ocg, tcg) -> None:
        self.ocg_date = datetime.datetime.strptime(ocg, "%Y-%m-%d").date()
        self.tcg_date = datetime.datetime.strptime(tcg, "%Y-%m-%d").date()

    def __str__(self):
        date_format = "%d/%m/%Y"
        ocg_date_str = self.ocg_date.strftime(date_format)
        tcg_date_str = self.tcg_date.strftime(date_format)
        return f"Card: {self.name} ({self.rarity}) - Type: {self.type} - Dates: OCG[{ocg_date_str}] TCG[{tcg_date_str}]"