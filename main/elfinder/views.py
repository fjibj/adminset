import json
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from exceptions import ElfinderErrorMessages
from elfinder.connector import ElfinderConnector
from elfinder.conf import settings as ls
from elfinder.volumes.storage import ElfinderVolumeStorage
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from cmdb.models import Host, Idc, HostGroup, ASSET_STATUS, ASSET_TYPE
from cmdb.api import get_object
import logging
from lib.log import log
from config.views import get_dir
#from webterminal.models import ServerInfor
"""
logger = logging.getLogger(__name__)
level = get_dir("log_level")
log_path = get_dir("log_path")
log("elfinder.log", level, log_path)
"""
class ElfinderConnectorView(View):
    """
    Default elfinder backend view
    """
    
    def render_to_response(self, context, **kwargs):
        """
        It returns a json-encoded response, unless it was otherwise requested
        by the command operation
        """
        kwargs = {}
        additional_headers = {}
        #create response headers
        if 'header' in context:
            for key in context['header']:
                if key == 'Content-Type':
                    kwargs['content_type'] = context['header'][key]
                elif key.lower() == 'status':
                    kwargs['status'] = context['header'][key]
                else:
                    additional_headers[key] = context['header'][key]
            del context['header']
        
        #return json if not header
        if not 'content_type' in kwargs:
            kwargs['content_type'] = 'application/json'
            
        if 'pointer' in context: #return file
            context['pointer'].seek(0)
            kwargs['content'] = context['pointer'].read()
            context['volume'].close(context['pointer'], context['info']['hash'])
        elif 'raw' in context and context['raw'] and 'error' in context and context['error']: #raw error, return only the error list
            kwargs['content'] = context['error']
        elif kwargs['content_type'] == 'application/json': #return json
            kwargs['content'] = json.dumps(context)
        else: #return context as is!
            kwargs['content'] = context
        
        response = HttpResponse(**kwargs)
        for key, value in additional_headers.items():
            response[key] = value

        return response
    
    def output(self, cmd, src):
        """
        Collect command arguments, operate and return self.render_to_response()
        """
        args = {}

        for name in self.elfinder.commandArgsList(cmd):
            if name == 'request':
                args['request'] = self.request
            elif name == 'FILES':
                args['FILES'] = self.request.FILES
            elif name == 'targets':
                args[name] = src.getlist('targets[]')
            else:
                arg = name
                if name.endswith('_'):
                    name = name[:-1]
                if name in src: 
                    try:
                        args[arg] = src.get(name).strip()
                    except:
                        args[arg] = src.get(name)
        args['debug'] = src['debug'] if 'debug' in src else False

        return self.render_to_response(self.elfinder.execute(cmd, **args))
    
    def get_command(self, src):
        """
        Get requested command
        """
        try:
            return src['cmd']
        except KeyError:
            return 'open'
        
    def get_optionset(self, **kwargs):
        set_ = ls.ELFINDER_CONNECTOR_OPTION_SETS[kwargs['optionset']]
        """
	if kwargs['start_path'] != 'default':
            for root in set_['roots']:
                root['startPath'] = kwargs['start_path']
        """
	return set_
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        if not kwargs['optionset'] in ls.ELFINDER_CONNECTOR_OPTION_SETS:
            raise Http404
        return super(ElfinderConnectorView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        used in get method calls
        """       
        logging.info("----1----start_path:"+kwargs['start_path']+"-----------")
        if kwargs['optionset'] == 'sftp':
            server_object = get_object(Host,hostname=kwargs['start_path'])
            logging.info("---1-----hostname:"+server_object.hostname+",ip:"+server_object.ip+"-----------")
            #optinon_sets = self.get_optionset(**kwargs)
            #logging.info("---1-----roots.len:"+str(len(optinon_sets['roots']))+"---------------------")
            #logging.info("---1-----alias:"+optinon_sets['roots'][0]['alias']+"---------------------")
            optinon_sets = {
				'debug' : True,
				'roots' : [
					{
						'id' : 'pdfid',
                        'rootRev' : server_object.ip,
						'alias' : '{0}-{1}'.format(server_object.hostname,server_object.ip),                        
						'driver' : ElfinderVolumeStorage,
						'storageClass': 'storages.backends.sftpstorage.SFTPStorage',
						'keepAlive' : False,
						'cache' : False
					} 
				]  
			}
            #optinon_sets['roots'][0]['alias'] = '{0}-{1}'.format(server_object.hostname,server_object.ip)
            logging.info("--------hostname:"+server_object.hostname+",ip:"+server_object.ip+"-----------")
            logging.info("---1-----alias:"+optinon_sets['roots'][0]['alias']+"---------------------")
            optinon_sets['roots'][0]['storageKwArgs'] = {'host':server_object.ip,
                                                         'params':{'port':22,	   												      'username':'root',
 					                 'password':'ztesoft123',
							 'timeout':30},
                                                         'root_path':'/','interactive':False}

            logging.info("---2-----alias:"+optinon_sets['roots'][0]['alias']+"---------------------")
            logging.info("---2-----hostname:"+server_object.hostname+",ip:"+server_object.ip+"-----------")
            self.elfinder = ElfinderConnector(optinon_sets, request.session)  
            logging.info("---3-----alias:"+optinon_sets['roots'][0]['alias']+"---------------------")
            logging.info("---3-----")
        else:
            optinon_sets = self.get_optionset(**kwargs)
            optinon_sets['roots'][0]['alias'] = 'hahahaha'
            self.elfinder = ElfinderConnector(optinon_sets, request.session)
        return self.output(self.get_command(request.GET), request.GET)

    def post(self, request, *args, **kwargs):
        """
        called in post method calls.
        It only allows for the 'upload' command
        """
        if kwargs['optionset'] == 'sftp':
            #server_object = get_object_or_404(ServerInfor,hostname=kwargs['start_path'])
            server_object = get_object_or_404(Host,hostname=kwargs['start_path'])
            optinon_sets = self.get_optionset(**kwargs)
            optinon_sets['roots'][0]['alias'] = '{0}-{1}'.format(server_object.hostname,server_object.ip)
            optinon_sets['roots'][0]['rootRev'] = server_object.ip
            optinon_sets['roots'][0]['storageKwArgs'] = {'host':server_object.ip,
                                                         'params':{'port':22,
 						         'username':'root', 
			    			         'password':'ztesoft123',
	 					         'timeout':30},
                                                         'root_path':'/','interactive':False}
            self.elfinder = ElfinderConnector(optinon_sets, request.session)
        else:
            optinon_sets = self.get_optionset(**kwargs)
            optinon_sets['roots'][0]['alias'] = 'hahahaha'
            self.elfinder = ElfinderConnector(optinon_sets, request.session)
        cmd = self.get_command(request.POST)
        
        if not cmd in ['upload']:
            self.render_to_response({'error' : self.elfinder.error(ElfinderErrorMessages.ERROR_UPLOAD, ElfinderErrorMessages.ERROR_UPLOAD_TOTAL_SIZE)})

        return self.output(cmd, request.POST)
