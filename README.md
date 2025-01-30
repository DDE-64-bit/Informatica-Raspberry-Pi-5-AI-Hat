# Informatica Raspberry Pi 5 AI-hat
Hier geef ik informatie over de raspberry pi 5 AI hat en laat zien hoe de hat gebruikt kan worden.

**Gevolgde Documentatie:** https://www.raspberrypi.com/documentation/accessories/m2-hat-plus.html

Doosje rpi ai kit:
- 3 onderdelen:
  - rpi m2 hat+ 
  - pin ding 
  - schroefjes
  


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
Om te updaten wanneer nodig.

