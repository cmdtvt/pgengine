from __future__ import annotations
import pygame


#Maybe create a manager class that passes correct rendering functions to the classes.

class Style:
    def __init__(self,):
        self.hide = False
        self.hover = False
        self.margin = 10
        self.padding = 10
        self.border = 0
        self.border_color = (125, 121, 121)
        self.background_color = (181,181,181)
        self.width = 0
        self.height = 0
        self.width_min = 200
        self.height_min = 50

        #TODO: The should be automaticaly set to the size of the window
        self.width_max = 500
        self.height_max = 500

        #auto = starts from min size and scales to the max size depending on elements
        #fluid = takes all space untill max size
        #fixed = takes fixed amount of pixel from the window
        #responsive = takes precentage from the window and scales to it
        self.display = "" #auto, fluid or fixed, responsive



class Element:
    def __init__(self,element_type="undefined"):
        self.children = []
        self.style = Style()

        self.click_allow = False
        self.click_action = None
        self.element_type = element_type

    # Possiby allow **args and pass them to the clicked binded function
    def action_click(self,):
        pass

    def add_child(self,element:Element):
        self.children.append(element)
        return self

    def remove_element(self,index):
        pass

    def get_children(self,):
        return self.children

    # This is a way to send size information from the child to the parent
    def signal_parent(self,signal_name,signal_data):
        print(f"Received signal: {signal_name} | {signal_data}")


# Wrapper for all gui elements
class Gui():
    def __init__(self, gui_type:str="flex",width:int=200, height:int=150):
        #Types to be implemented, flex, static, 
        self.elements = []
        self.width = width
        self.height = height

    def add_element(self, element:Element):
        self.elements.append(element)

    def parse_xml(self,):
        raise NotImplementedError


class Column(Element):
    def __init__(self, ):
        super().__init__(element_type="column")


class Row(Element):
    def __init__(self, ):
        super().__init__(element_type="row")


class Grid(Element):
    def __init__(self, max_width:int=5, max_height:int = 5):
        super().__init__(element_type="grid")


class Text(Element):
    def __init__(self, text:str=""):
        super().__init__(element_type="text")
        self.text = text



