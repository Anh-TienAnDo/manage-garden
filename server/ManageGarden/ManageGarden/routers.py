class GardenRouter:
    route_app_labels = {"manhdat", "lichsu", "dieukhien"}
    db_name = "garden"
    # truy vấn đọc (SELECT)
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.db_name
        return 'default'
 # truy vấn ghi (INSERT, UPDATE, DELETE)
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.db_name
        return 'default'

# cho phép quan hệ (relationship) giữa hai đối tượng (obj1 và obj2
    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return 'default'

# thực hiện các migration trên database
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == self.db_name
        return 'default'