# Atmos

Atmos is an adjustable atmospheric controller that can be used to monitor and control the atmosphere of any closed area.
it has been developped with an open source aspect, allowing people to provide more functionnality to the sytem. Since the sytem is not based on a specific hardware, it can be run on any linux computer board that provided a GPIO and can, with the appropriate electronic components, control a very wide range of system, from the smallest 30x30x30cm terrarium to a 40 m² room. **However it has been developped for a big sized (300 liters) terrarium in mind**

## Features
- ###### A basic on / off controller, allowing the use of any on / off machine like : 
  - Pump, Mist machine, Light bulb, UV light, heating wire, heating plate, peltier module
  
- ###### A more advanced controller allowing the use to PWR to control intensity of some devices :
  - Control the light intensity, fan intensity, heating wire intensity, etc ...
  - Basic animation system (accuracy to the seconds)
  
- ###### A SW2801 controller without led limit and few functionnalities
  - Plain color
  - Repeating sample for the whole strip
  - Set individual led color
  - Basic animation system (accuracy to the seconds)

## Fast Doc
Atmos is divided in three parts
- ### The Core :
  The main part of Atmos, his role is to
  
  - Check for errors in the settings file
  - Launch controller that doesn't have any error
  - Execute all differents system commands
  - Control the GPIO of the computer board

- ### The controllers
  Controllers are threads executed along the Core and in charge of following the timer list provide by the settings file. Those timers are independant for each controllers and must follow few rules (explain in rules section).
  For an on / off controller, this timers list is written that way :
  ``` json
  "timers": [
      {
        "on": "14:17:00",
        "off": "14:17:10"
      },

      {
        "on": "14:02:00",
        "off": "14:02:30"
      }
    ]
   ```
   
  - ### The settings.json file
  This file provided all the information that the system need to operate.
  - The `rules` representing the maximum number of second the devices can run in a row and the minimum seconds it needs to rest/cool down.
  - The `mapping` representing the pin(s) used by the device
  - The `timers` reprensenting a list of timer that define the running period of the device during a day
    The timer must have at least on entry that have at least two entries :
    - `on` following by a date hh:mm:ss
    - `off` following by a date hh:mm:ss
    
    It can also have an other entry `update` to define basic animation or provide more complex informations
  Since Atmos has been developped to control the atmosphere of a wide terrarium, the settings files provide information for six differents systems in used called :
    - **water** to control the wattering sysyem
    - **mist** to control smoke machine
    - **heat** to control a heating wire
    - **cold** to control two peltier module
    - **light** to control a WS2801 60 leds strip
    - **wind** to control two three wired fan (fan speed control)
    
# TO DO
- [ ] A WS281x controller for more advanced strip led
- [ ] A easiest way for user to set their system
- [ ] Add animation feature for PWM devices
