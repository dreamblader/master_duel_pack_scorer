class SecretBannerData:

    def __init__(self, name, link, date) -> None:
        self.name = name
        self.link = link
        self.date = date
    
    def __str__(self):
        date_str = self.date.strftime("%d/%m/%Y")
        return f"Banner: {self.name}({self.link})[{date_str}]"