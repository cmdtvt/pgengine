

# Game Object can be interacted with rendering and other engine movements etc...
#TODO: Later we might want to implement network synced gameobject using pnetwork library.
class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.identifier = None

# Represents all kind of data in the system for standardized access.
class Resource:
    def __init__(self, resource, resource_type="image",description:str = ""):
        self.resource_type = resource_type
        self.resource = resource
        self.description = description

    def __repr__(self):
        has_resource = False
        if self.resource:
            has_resource = True
        if self.description == "":
            return "<Resource resource_type={resource_type} has_resource={has_resource}>".format(resource_type=self.resource_type, has_resource=has_resource)
        return "<Resource resource_type={resource_type} has_resource={has_resource} description={description}>".format(resource_type=self.resource_type, has_resource=has_resource, description=description)

        