def before_all(context):
    context.base_url = context.config.userdata.get('base_url', None)
