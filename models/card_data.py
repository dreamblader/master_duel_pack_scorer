class CardData:

    def __init__(self, name) -> None:
        self.name = name
    

    def __str__(self):
        date_str = self.date.strftime("%d/%m/%Y")
        return f"Banner: {self.name}({self.link})[{date_str}]"