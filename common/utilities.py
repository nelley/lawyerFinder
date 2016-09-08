from django.db.models import FileField, ImageField
from django.forms import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext as _
from datetime import datetime
from django.template.loader import render_to_string
from hashlib import sha1
from accounts.models import *
from lawyerFinder.settings import *
import boto
from boto.sqs.message import Message
from boto.regioninfo import RegionInfo
from lawyerFinder.settings import SITE_URL
from datetime import datetime

def gen_tokens(id):
    time = datetime.now().isoformat()
    plain = id + '\0' + time
    token = sha1(plain)
    return token.hexdigest()

def aws_ses_config():
    cusRegion = RegionInfo()
    cusRegion.endpoint='email.us-west-2.amazonaws.com'
    cusRegion.name='us-west-2'
    
    connection = boto.connect_ses(
                      aws_access_key_id=AWS_ACC_KEY_ID,
                      aws_secret_access_key=AWS_SEC_ACC_KEY,
                      region=cusRegion,)
    return connection

def userInquirySender(userObj, inquiryContent):
    logger.debug('mail to %s' % userObj.email)
    mail_html = render_to_string('email/user_inquiry.html', {'lawyer_firstname': userObj.first_name,
                                                             'lawyer_lastname': userObj.last_name,
                                                             'userInquiry': inquiryContent},
                                )
    connection = aws_ses_config()
    
    #mail_html = render_to_string('email/_base.html', {'user': 'NELLEY'})

    # complaint@simulator.amazonses.com
    # bounce@simulator.amazonses.com
    result = connection.send_email(
                        source='dragonbrucelee@gmail.com' # from
                       ,subject='Inquiry Mail'
                       ,body=mail_html
                       ,to_addresses=userObj.email # to
                       ,cc_addresses=['dragonbrucelee@gmail.com']
                       ,bcc_addresses=[]
                       ,format='html'
                       ,reply_addresses=''
                       ,return_path=''
                       )


def user_regist_mailSender(mail_to=None, token=None):#used in repw_view, user_register_view
    mail_context=''
    URL = SITE_URL + 'accounts/registConfirm/'
    MAIL_TITLE=_('New Member Verification')
    
    verify_link=URL + token
    mail_html = render_to_string('email/reverify.html',
                                 {'verify_link': verify_link,},
                                )
        
    connection = aws_ses_config()
    
    result = connection.send_email('dragonbrucelee@gmail.com' # from
                       ,MAIL_TITLE
                       ,mail_html
                       ,mail_to # to
                       ,cc_addresses=[]
                       ,bcc_addresses=[]
                       ,format='html'
                       ,reply_addresses=''
                       ,return_path=''
                       )
    logger.debug('New Member Verification Mail Sent')
    logger.debug(result)

def mailSender(mail_to=None, pw=None, token=None):#used in repw_view
    mail_context=''
    URL = SITE_URL + 'accounts/registConfirm/'
    MAIL_TITLE = ''
    #mail_to='doublenunchakus@gmail.com'
    
    if pw:
        logger.debug('repassword mail resend')
        MAIL_TITLE=_('repassword mail resend')
        mail_html = render_to_string('email/repassword.html', 
                                     {'new_pw': pw,},
                                )
    else:
        logger.debug('verify mail resend')
        verify_link=URL + token
        MAIL_TITLE=_('verify mail resend')
        mail_html = render_to_string('email/reverify.html',
                                    {'verify_link': verify_link,},
                                )
        
    connection = aws_ses_config()
    
    result = connection.send_email('dragonbrucelee@gmail.com' # from
                       ,MAIL_TITLE
                       ,mail_html
                       ,mail_to # to
                       ,cc_addresses=[]
                       ,bcc_addresses=[]
                       ,format='html'
                       ,reply_addresses=''
                       ,return_path=''
                       )
    
    logger.debug(result)


def ajax_session_check(request):
    logger.debug(request.get_full_path())
    if request.user.is_authenticated():
        logger.debug('logged in user!')
        if 'lastRequest' in request.session:
            elapsedTime = datetime.now() - \
                          request.session['lastRequest']
            if elapsedTime.seconds > SESSION_FRONT_AGE:
                del request.session['lastRequest'] 
                logout(request)
                return False

        request.session['lastRequest'] = datetime.now()
        return True
    else:
        logger.debug('not yet logged in user!')
        if 'lastRequest' in request.session:
            del request.session['lastRequest']
            
        return False


def get_email_by_userid(req):
    u = User.objects.get(id=req.session['_auth_user_id'])
    return u.email

def pwPolicyValidator(pw):
    if re.search(r'\d', pw) and re.search(r'[A-Z]', pw) and re.search(r'[a-z]', pw):
        return True
    else:
        return False


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
                
                
