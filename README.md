
# pgengine
pgengine is basicly a bunch of support code for making games using pygame.

## Installing
Project is installed as an package. First clone pgengine to the project root.

    git clone https://github.com/cmdtvt/pgengine
Next you can use this import the needed classes to start pgengine project up.

    import sys
    import pygame
    
    from pgengine import engine,gui,utilities,render,structure,world_management


# Project structure

## engine
engine has many of the main classes inside of it. These include dataclasses for handling Spritesheets, animations and other implementations of concepts you can find often being used in gamedevelopment like points and paths.
## gui
gui is basicly a dynamic system from generating user interfaces. Each Gui has a wrapper called `Gui()` this wrapper can store only one element inside of it.

### gui.pack(element) 
When you have created a layout of elements you can pack them into main Gui class. Gui class accepts only one element because this is the main wrapper for handling multiple Elements.
#### Example: packing Elements to a gui
Next example creates a Gui where there are two columns inside each other and the innermost column has a Text element inside of it.

    from pgengine import gui
    
    temp_gui = Gui()
    temp_column = gui.Column()
    temp_column2 = gui.Column()
    temp_column2.add_child(gui.Text("This is a text"))
    temp_column.add_child(temp_column2)
    temp_gui.pack(temp_column)
To render any Gui you can use `render_gui(gui)` from Render class.

### Element
Element is a core part of the Gui system. If class inherits Element class it gives the class ability to apply different styles to itself and work as part of the Gui system.
#### Style
Style() is basically a data class which is used by the Element class to keep track of the style setting for the Element.
From element values of style can be accessed by calling `Element().style.STYLENAME`
### Column
Column handles placing elements on evenly sized areas depending on passes `style.display`
### Row
(This might not be implemented)
### Grid
adadad
### Text
adada


## utilities
adad
## render
adadad
## structure
adadad
## world_management
adadad
