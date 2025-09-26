class Topic:
    id_counter = 1

    def __init__(self, name: str):
        self.id = Topic.id_counter
        Topic.id_counter += 1
        
        self.name = name

    def __repr__(self):
        return f"Topic(id={self.id}, name='{self.name}')"
