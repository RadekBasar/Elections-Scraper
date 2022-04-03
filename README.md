Závěrečný projekt
-
# Úvod
Výstupem posledního projektu v rámci kurzu bylo naprogramování scraperu výsledků voleb z roku 2017, který získává data z webu.

# Popis programu
Program podle zadané URL stáhne stránku, ze které získá kód a název obce a URL na stránku okrsku.
Následně stáhne stránku okrsku. V případě, že obec obsahuje pouze jeden okrsek, obsahuje stránka výsledky voleb. V opačném případě (obec obsahuje více okrsků) stránka obsahuje jednotlivé odkazy, které směřují na jejich výsledky voleb.
Poté se výsledky voleb u jednotlivých obcí v okrsku propojí s kódem a názvem obce. Ty se nakonec ve formátu CSV uloží do souboru podle uživatelem vloženého názvu.

# Postup
1. uživatel spustí program se 2 vstupními argumenty v pořadí: **URL** a **název CSV souboru** (bez přípony), do kterého se výsledky mají uložit
2. program vytvoří z dat stažených z webu (1. argument) konsolidované výsledky ve formátu CSV a uloží je do souboru (2. argument)

# Použité knihovny
## requests
Knihovna pro HTTP komunikaci. Pro její instalaci je potřeba v příkazové řádce spustit příkaz `pip install requests`.
## beautifulsoup4
Knihovna pro parsování HTML stránek. Pro její instalaci je potřeba v příkazové řádce spustit příkaz `pip install beautifulsoup4`.

# Ukázka
Uživatel upraví konfiguraci Projektu v PyCharm v části Edit configuration / Parameters zadáním URL adresy a názvu souboru. Pak spustí program pomocí tlačítka Run. Program vytvoří soubor podle zadaného argumentu ("Volby.csv") s výsledky voleb pro jednotlivé obce, např.: 565423,Bdín,51,34,34,1,0,0,7,0,1,1,1,0,0,0,0,3,0,0,1,15,0,0,0,0,0,0,0,4,0.