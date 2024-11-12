"""
IMPORTANT NOTE:
The XPATH solution will not work in masterduelmeta.com/secret-packs because the current page html is not a valid XML
"""

#URLS
master_duel_meta_url = "https://www.masterduelmeta.com"
secret_pack_endpoint = "/secret-packs"
ygo_pro_api_endpoint = "https://db.ygoprodeck.com/api/v7/cardinfo.php?misc=yes&name="
ygo_db_endpoint = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid="


#SELECTORS
load_button_text = "Load more..."
cards_in_pack_master_duel_page = "a.image-wrapper"
date_in_ygo_db = ".t_body > .t_row:first-child > .inside > .time"


#EXTRA
ocg_locale = "&request_locale=ja"
tcg_locale = "&request_locale=en"

#first t_row child of t_body class .time child of .inside