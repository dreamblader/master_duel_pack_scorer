-- Some Cards are missing the OCG_DATE value from YGO PRO API
-- Because of that the log spill any Warning of any missing value from dates 
-- This SQL file is a fix command that update the missing values by grabing the "closest" release date value of this cards
-- This happens because this cards are not present in the official English(Asia) DB of Konami 
-- However they do have dates of the other OCG ruleset countries

--Cards with no OCG Dates List:

--Zalamander Catalyzer
UPDATE Cards 
SET OCG_DATE="2023-09-23", OCG_SCORE="8997" 
WHERE NAME="Zalamander Catalyzer";
--Flowerdino
UPDATE Cards 
SET OCG_DATE="2022-09-10", OCG_SCORE="8619" 
WHERE NAME="Flowerdino";
--The%20Great%20Double%20Casted%20Caster
--Salamandra%20with%20Chain
--Salamandra%20Fusion
--Flame%20Swordsrealm
-- THERE IS A LOT NEED TO FIX THIS