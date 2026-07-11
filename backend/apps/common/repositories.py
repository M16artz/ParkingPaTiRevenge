class BaseRepository:
    model = None

    def get_by_id(self, object_id):
        return self.model.objects.filter(id=object_id).first()

    def all(self):
        return self.model.objects.all()

