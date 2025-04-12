# Informatica Raspberry Pi 5 AI-hat
Hier geef ik informatie over de raspberry pi 5 AI hat en laat zien hoe de hat gebruikt kan worden.

# 1. OS
Via raspberry pi imager installeer de laatste 32 bit raspberry pi os voor de raspberry pi 5. Het is aan te raden om dit te doen op een SD kaart met minimaal 64GB.

# 2. Tools en Firmware updaten
Hieronder vind je een lijst met commands die je kunt uitvoeren om alles up to date te krijgen.

``` bash
sudo apt update && sudo apt full-upgrade
```
Alles updaten.


``` bash
sudo rpi-eeprom-update
```
Kijken of je raspberry firmware is up to date.


``` bash
sudo rpi-eeprom-update -a
```
Om de firmware te updaten wanneer nodig.

``` bash
sudo reboot
```
Tot slot moet je de pi rebooten, dat kan je doen met dit command.

# 3. Aansluiten van de M.2 HAT en AI HAT
De AI hat heeft een M.2 hat nodig om aangesloten te kunnen worden aan de pi. In de meeste gevallen wordt deze meegegeven. 

**Let op:** Als eerste moet je de pi van de stroom loskoppelen.

## Active Cooler aansluiten (Optioneel)
Als je de hats met Active Cooling wilt gebruiken. Dan moet je die eerst op de pi installeren. Volg daarvoor de meegeleverde instructies.

## 3.1. Spacers en GPIO stacking header aansluiten
Plaats de spacers (relatief lange zwarte balkjes) op het bord van de pi. Schroef ze via de onderkant vast. Plaats daarna ook de GPIO* stacking header op de GPIO* pinnen van de pi.

*GPIO staat voor General Purpose Input/Output.

## 3.2 Aansluiten lintkabel
Om de lintkabel to kunnen aansluiten moet je eerst voorzichtig de kabel losmaken van de hat. Waneer dat is gebeurd kan je de losse lintkabel weer voorzichtig vastmaken, deze keer aan de pi zelf.

## 3.3 Hat aansluiten
Nu moet je de hat voorzichtig op de spacers plaatsen, en vast schroeven met de overige schroeven. Als laatste moet je de lintkabel weer aan de hat vast maken. Wees daar weer voorzichtig mee.


Dit was het aansluiten van de hat op de pi 5.

# 3. Software

Nu heb je de juiste software nodig, [hier](https://www.raspberrypi.com/documentation/computers/ai.html) kan je een goede uitleg daarvoor vinden.


# Programmeren met Hailo

Ik heb al 2 programma's gemaakt die zitten in de scripts folder. Daar kan je mee doorgaan of nieuwe scripts maken.

Hieronder nog een paar ideeen die ik nog had maar nog niet had kunnen uitwerken.
* Met reinforcement learning de raspberry pi een simpel spel laten spelen (flappy bird, tetris) 
* Iets met MCP (zie [anthropic](https://www.anthropic.com/news/model-context-protocol), [mcp github](https://github.com/modelcontextprotocol))
* Custom objecten herkennen (gezichten, kleuren)
* AI NIDS (Network Intrusion Detection System)
* Een slimme honeypot met AI

<hr>

Als je vragen hebt kan je mij zo bereiken:
- Discord: dde88
- Mail: olivier.hartsuiker@gmail.com


Mocht je andere goede script hebben kan je altijd een pull request sturen.
