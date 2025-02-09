from __future__ import annotations
import pygame


#Maybe create a manager class that passes correct rendering functions to the classes.

class Element:
    def __init__(self,element_type="undefined"):
        self.children = []
        self.style_hide = False
        self.style_hover = False
        self.click_allow = False
        self.click_action = None

        self.element_type = element_type

    # Possiby allow **args and pass them to the clicked binded function
    def action_click(self,):
        pass

    def add_child(self,element:Element):
        self.children.append(element)
        return self.get_children()

    def remove_element(self,index):
        pass

    def get_children(self,):
        return self.children


# Wrapper for all gui elements
class Gui():
    def __init__(self, gui_type:str="flex",width:int=200, height:int=150):
        #Types to be implemented, flex, static, 
        self.elements = []
        self.width = width
        self.height = height

    def add_element(self, element:Element):
        self.elements.append(element)


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



