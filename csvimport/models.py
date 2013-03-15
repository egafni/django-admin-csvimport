from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
import csv
fs = FileSystemStorage(location=settings.MEDIA_ROOT)
from django.contrib import messages

class CSVImport(models.Model):
    """ Logging model for importing files """
    model = models.ForeignKey(ContentType)
    file = models.FileField(upload_to='csv', storage=fs)

    def __unicode__(self):
        return u'CSVImport[{0.id}]'.format(self)

def update_from_csv(sender, **kwargs):
    csvimport = kwargs['instance']
    object_klass = csvimport.model.model_class()
    dr = csv.DictReader(csvimport.file)
    for row in dr:
        row2 = dict( [ (k, None if v == '' else v) for k, v in row.items() ] )
        id = row2.setdefault('id',None)
        instance, created = object_klass.objects.get_or_create(pk=id)
        del row2['id'] # don't want to reset id in next line
        instance.__dict__.update(**row2)
        instance.save()


post_save.connect(update_from_csv, sender=CSVImport)