
# The Nonagons
## Introduction
The Nonagons are an art project I started back in December of 2019 to fill the space on an empty wall in my living room. I had some LEDs and an old raspberry pi laying around that were put to good use in the nonagons.
## Parts
- Raspberry Pi 2b+
- 4 144 LED/m Dotstar Strips (only 434 LEDs total used and I bought mine from adafruit but you can find them cheaper as APA102 led strips)
- Mini USB Microphone
- Female DC Power adapter - 2.1mm jack to screw terminal block
- 74AHCT125 - Quad Level-Shifter (3V to 5V)
- 10a / 5V power supply
- 40 4pin strip-to-strip LED connectors 10mm wide (these were actually not wide enough but ended up working)
- A large assortment of jumpper wires of all types
- 4700uF 10v Capacitor
- 2 feet x 2 feet x 1/4 inch project board (https://www.homedepot.com/p/Columbia-Forest-Products-3-4-in-x-2-ft-x-2-ft-PureBond-Walnut-Plywood-Project-Panel-Free-Custom-Cut-Available-2731/204771202)
- A test board with the same dimensions as above made of something cheap like MDF
- Excess wood, preferably also 1/4in thick (used for gluing to the main project board, screwing the screw eyes into and hanging from)
- 2 Screw Eyes
- Picture Hanging Wire
- Wood Stain
- Spray on Lacquer
- Gorilla Glue
- 8ft of Quarter Round (size doesn't matter a ton, it's just to increase the surface area the aluminum can be glued to)
- Slightly more than 8ft of Aluminum that is 2 inches wide (one of these and maybe another that is at least 4 ft https://www.lowes.com/pd/Steelworks-0-125-ft-x-2-in-Aluminum-Solid/3058163)
- A thin sheet of cork (optional for coasters)

## Tools
- An exacto knife preferably with a couple different attachments for different jobs
- A CNC Router (I used an x-carve with a 1/8th inch drill  bit for the whole project)
- A 3D Printer with clear filament
- Clamps
- A hacksaw with a blade for cutting metal
- Soldering Iron & Solder
- Gloves
- A Tarp 
- Something to spread wood stain with
- A respirator if you use spray on lacquer
- Sandpaper of varyings grits (Some for wood, some very fine for the aluminum pieces)

## 3D Printing
The plastic nonagons were first designed in Blender as a flat surface with walls to keep the LEDs inside. Then I printed them with transparent filament.<br>
![3D Print Design](./readme-content/small/3DPrintDesign.jpg)
![3D Printing](./readme-content/small/3DPrinting.jpg)<br>

At this point there was no plan for the board and after seeing that they managed to fit some LEDs comfortably inside, then the rest of the board was planned around their size<br>
![First Nonagon](./readme-content/small/CoasterFirstLight.jpg)
![Several Nonagons](./readme-content/small/Coasters.jpg)
![Nonagons Upside Down](./readme-content/small/CoastersUpsidedown.jpg)

## CNC Routing
The design for the CNC cut were created in the Inventables Easel program, it's super easy to use. There are little tails on each nonagon so that there is room for wires sticking out of each nonagon</br> 
![CNC Design](./readme-content/small/CNCRouterDesigns.jpg)<br>

Test cuts were made in an MDF board to get the size right holes for the plastic nonagons. I had to pause the cut and turn off the drill as soon as each nonagon was cut completely out in order to remove the cut out piece of wood. Without removing the wood the drill bit could potentially fling it across the work surface.<br>
![CNC MDF](./readme-content/small/CNCRouterMDF.jpg)
![CNC Pause](./readme-content/small/CNCRouterPauseToRemoveWood.jpg)
![CNC MDF Fit](./readme-content/small/CNCRouterMDFTest.jpg)<br>

After getting the right sized nonagon cutouts determined, it was time to move on to using actual wood.<br>
![CNC Router Wood](./readme-content/small/CNCRouter.jpg)<br>

Unfortunately one of the wood boards ended up not laying as flat as the MDF and the drill went through in places it shouldn't have. Luckily I had another.<br>
![CNC Router Failed](./readme-content/small/CNCRouterFailedCut.jpg)<br>

The wooden cutouts are a good size for coasters so I saved them<br>
![CNC Router Coaster](./readme-content/small/Coaster.jpg)<br>
## Assembly
Somewhere along the way I realized I could only fit 31 LEDs on a strip inside the nonagons if I had plastic connectors and wires on both ends of the strip. Originally I hadn't planned to do all the LEDs in series but it was the path of least resistance. In order to have the wires sit comfortably in the nonagon I needed to cut a rectangle out of the plastic nonagon walls. This seemed very difficult to do at first but a simple method I discovered was heating up my exacto knife blade and then quickly cutting/melting through the portion of the nonagon I wanted to remove.<br>
![Melted Nonagon Edge And Strips](./readme-content/small/meltedNonagonEdgeAndStrips.jpg)<br>

Next the rough edges of the board needed to be sanded and then the board was stained. After the stain dried the board was coated several times in spray on lacquer (make sure to do this in a well ventilated area and wear a respirator)<br>
![Unsanded Edges](./readme-content/small/unsandedEdges.jpg)
![Staining](./readme-content/small/Staining.jpg)
### Gluing
Throughout the gluing process I was using small clamps to hold the pieces in place and also random heavy objects to hold the board flat and in place. 
Next the wooden quarter round was cut to size and glued onto the wood so that there was a larger surface area on the sides of the project board which the aluminum frame could be glued to.<br>
![Clamping on quarter round](./readme-content/small/ClampingWood.jpg)<br>

Next the aluminum strips were cut to size. 2 of them were 2ft exactly and the other two were 2ft and a quarter or half inch so that the aluminum could make a perfect box around the edges of the project board. The aluminum was sanded with increasingly higher grit sandpaper to remove blemishes and make it look polished.<br>
![Cut Aluminum Strips](./readme-content/small/cutAluminum.jpg)
![Unsanded vs Sanded Aluminum](./readme-content/small/sandedVsUnsandedAluminum.jpg)<br>

Next two rectanlges of wood were glued onto the back of the main board and screw eyes were installed so that picture hanging wire could hang the whole project on the wall. The extra layer of wood was added so that the screw eyes would not piece or warp the main board in any way.<br>
![Installing screw eyes](./readme-content/small/screwEyes.jpg)<br>

Next the aluminum edges were glued onto the board<br>
![Gluing and clamping aluminum to board](./readme-content/small/clampingAluminum.jpg)<br>

About an hour after gluing once the glue is set but not 100% dried, I flipped the project over to remove any excess glue from the front of the board while it was still ever so slightly malleable. When completely dried the glue can also be removed very carefully using an exacto knife.<br>
![Edges](./readme-content/small/edges.jpg)
![Edges 2](./readme-content/small/edgesGlue.jpg)<br>

One of the final steps of assembling the board itself was gluing in the plastic nonagons<br>
![Some nonagons glued to the board](./readme-content/small/pre-nonagonGluing.jpg)
![Final Board](./readme-content/small/nonagonGluing2.jpg)
### Coasters
The wooden cutouts from the board can be easily turned into coasters. I carved names into some of them for my girlfriend and her roommates as well as for Ken's 50th.<br>
![CNC Router Coaster](./readme-content/small/Coaster.jpg)<br>

I stained the cutouts and then sprayed them with lacquer before cutting very thin cork to glue onto the back of the coasters. Before doing this I wish I had attached something heavy to the back of the coasters because the surface tension from water can easily pick them up due to being super light. The cork cutouts are definitely just forbidden pringles.<br>
![Cork and Coasters](./readme-content/small/CorkForCoasters.jpg)
![Forbidden Pringles](./readme-content/small/CorkCutouts.jpg)
<br><br>I broke at least one exacto knife blade because I accidentally glued a couple of these to some excess MDF. The coasters work pretty well!<br>
![Broken Exacto](./readme-content/small/brokenExacto.jpg)
![Coasters supporting a wineglass of chocolate milk](./readme-content/small/coastersWorking.jpg)


### Wiring
![The Back Of The Board](./readme-content/small/TheBack.jpg)


## Software
### Libraries
Python libraries

### Architecture

### Setup
Adding to your crontab to start the program in the background 30 seconds after startup. This could be modified to start immediately and then the python could check for a network connection.

```
sudo crontab -e
>
@reboot (sleep 30 && sudo python3 /home/pi/Desktop/ennea-LED/main.py) &   
>
ctrl+x > y
```

### Making Patterns
![Nonagon Edge Reference Sheet](./readme-content/small/NonagonEdgeReference.jpg)

## Similar Patterns
After making this I couldn't stop seeing similar patterns, for example:<br>
![Chicago Flag](./readme-content/small/Inspiration2.jpg)
![Work Bathroom Tiles](./readme-content/small/Inspiration.jpg)
![](./readme-content/small/.jpg)

## Finished Product
![Finished Product Off](./readme-content/small/FinishedOff.jpg)
![Finished Product Rainbow Sparkle](./readme-content/small/FinishedRainbowSparkle.jpg)
![Finished Product Rainbow at Night](./readme-content/small/FinishedRainbow.jpg)
![Finished Product Rainbow Circles Gif](./readme-content/small/rainbowCircles.jpg)


