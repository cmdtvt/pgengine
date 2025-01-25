import pygame

class Gui:
    def __init__(self, render_management):
        self.elements = []
        self.render_management = render_management

    def add_element(self, element):
        """Add rows or other elements to the GUI."""
        self.elements.append(element)

    def render(self, screen):

        """Render all elements."""
        for e in self.elements:
            e.render(screen, self.render_management)

    def create_window(self):
        # TODO: use subsurface to make movable windows that can look around their assigned surface.
        pass


class Row:
    def __init__(self, y_position, spacing=10):
        self.columns = []
        self.y_position = y_position
        self.spacing = spacing  # Space between columns

    def add_column(self, column):
        """Add a column to this row."""
        self.columns.append(column)

    def render(self, screen, render_management):
        """Render each column within the row with correct spacing."""
        x_position = 0
        total_width = screen.get_width() - (self.spacing * (len(self.columns) - 1))
        for column in self.columns:
            col_width = int((column.width / 12) * total_width)
            column.render(screen, render_management, x_position, self.y_position, col_width)
            x_position += col_width + self.spacing


class Column:
    def __init__(self, element, width=1):
        self.element = element  # GUI element, e.g., a button or text box
        self.width = width  # Width in terms of Bootstrap-like columns (1-12)

    def render(self, screen, render_management, x, y, width):
        """Render the contained element with a specified width and position."""
        self.element.render(screen, render_management, x, y, width)


class Element:
    def __init__(self, color=(0, 0, 0)):
        self.color = color

    def render(self, screen, render_management, x, y, width):
        """Draw a simple rectangle as a placeholder for any GUI element."""
        pygame.draw.rect(screen, self.color, pygame.Rect(x, y, width, 50))  # Height fixed at 50 for simplicity




class UiBox(Element):
    def __init__(self, ):
        super().__init__("UiBox")
        self.width = 2
        self.height = 2