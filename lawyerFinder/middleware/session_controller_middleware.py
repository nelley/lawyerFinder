from django.core.handlers.wsgi import logger
from django.contrib.auth.views import logout
from lawyerFinder.settings import SESSION_FRONT_AGE, SESSION_BACK_AGE
import datetime

class SessionControllerMiddleware(object):
    # session timeout checker
    def process_request(self, request):
        # check whether frontend or backend by domain(frontend 60min, backend 15min)
        logger.debug(request.get_full_path())
        if request.user.is_authenticated():
            logger.debug('logged in user!')
            if 'lastRequest' in request.session:
                elapsedTime = datetime.datetime.now() - \
                              request.session['lastRequest']
                if elapsedTime.seconds > SESSION_FRONT_AGE:
                    del request.session['lastRequest'] 
                    logout(request)

            request.session['lastRequest'] = datetime.datetime.now()
        else:
            logger.debug('not yet logged in user!')
            if 'lastRequest' in request.session:
                del request.session['lastRequest'] 

        return None
   