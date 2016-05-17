'''
from django.db.models import FileField, ImageField
from django.forms import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext as _


class RestrictedImageField(ImageField):
    content_type = None
    max_upload_size = None
    """
        Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", None)
        self.max_upload_size = kwargs.pop("max_upload_size", None)
        super(RestrictedImageField, self).__init__(*args, **kwargs)
        
    def clean(self, *args, **kwargs):
        data = super(RestrictedImageField, self).clean(*args, **kwargs)
        image = data.file
        if self.content_types and hasattr(image, 'content_type') and image.content_type not in self.content_types:
            raise ValidationError(_('Filetype not supported.'))
        if self.max_upload_size and image.size > self.max_upload_size:
            raise ValidationError(_('Keep filesize under %(max_size)s. Current filesize %(current_size)s.') % {'max_size': filesizeformat(self.max_upload_size), 'current_size': filesizeformat(image.size)})
        return data
    
    def save_form_data(self, instance, data):
        if data is not None:
            file = getattr(instance, self.attname)
            if file != data:
                file.delete(save=False)
                super(RestrictedImageField, self).save_form_data(instance, data)
                
                
'''