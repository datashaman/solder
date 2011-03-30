from base import BaseWelder

class GridWelder(BaseWelder):
    model = None
    columns = []

    def weld(self):
        all_objects = self.model.objects.all()

        self['#users thead th'] = [label for _, label in self.columns]
        self['#users tbody th'] = [fromstring('<span class="%s"/>' % key) for key, _ in self.columns]
        self['#users tr'] = [obj.attributes_dict for obj in all_objects]
        self['#select option'] = [fromstring('<option value="%s">%s</option>'\
                % (obj.id, obj)) for obj in all_objects]
