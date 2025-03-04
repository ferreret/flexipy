class ConfigModel:
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            description=data.get("description", "")
        )