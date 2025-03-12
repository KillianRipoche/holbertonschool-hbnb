import uuid


class InMemoryRepository:
    """
    Simple in-memory repository for storing objects.
    """

    def __init__(self):
        self.storage = {}

    def add(self, obj):
        if not obj.id:
            obj.id = str(uuid.uuid4())
        self.storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def delete(self, obj_id):
        return self.storage.pop(obj_id, None)

    def update(self, obj_id, new_obj):
        if obj_id in self.storage:
            self.storage[obj_id] = new_obj
            return new_obj
        return None

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self.storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None

    def get_all(self):
        return list(self.storage.values())
