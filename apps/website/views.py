from django.shortcuts import render_to_response
from django.template import RequestContext
from merengue.base.models import BaseContent
from merengue.pluggable.utils import get_plugin


def index(request):
    """ Index page """
    # put here your staff
    core_config = get_plugin('core').get_config()
    main_content_index = int(core_config['home_initial_content'].get_value())
    content = BaseContent.objects.get(pk=main_content_index).get_real_instance()
    return render_to_response([content._meta.content_view_template,
                               'website/index.html'],
                              {'content': content},
                              context_instance=RequestContext(request))
