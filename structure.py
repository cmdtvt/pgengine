class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Resource:
    def __init__(self, resource, resource_type="image"):
        self.resource_type = resource_type
        self.resource = resource

    def __repr__(self):
        has_resource = False
        if self.resource:
            has_resource = True
        return "<Resource resource_type={resource_type} has_resource={has_resource}>".format(resource_type=self.resource_type, has_resource=has_resource)

        