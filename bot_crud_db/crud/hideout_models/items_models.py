# placeholder
class Item:
    installed: bool
    resource: int

    def __init__(self, installed=False, resource=None) -> None:
        self.installed = installed
        self.resource = resource

    # should deprecate this idea of own full inventory backend surely
    def tick_resource(self):
        if self.installed:
            if self.resource:
                self.resource -= 1
            else:
                pass
