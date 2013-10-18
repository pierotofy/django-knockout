from django.template.loader import render_to_string

def koModel(model, field_names=None, data=None):

    if type(model) == str:
        modelName = model
    else:
        modelName = model.__name__

    if field_names:
        fields = field_names
    else:
        if hasattr(model, "knockout_fields"):
            fields = model.knockout_fields()
        else:
            fields = model.to_dict().keys()

    modelViewString = render_to_string("knockout_modeler/model.html", {'modelName': modelName, 'fields': fields, 'data': data} )

    return modelViewString

def koData(queryset, field_names):

    modelName = queryset[0].__class__.__name__    
    modelNameData = []

    if field_names:
        fields = field_names
    else:
        if hasattr(model, "knockout_fields"):
            fields = model.knockout_fields()
        else:
            fields = model.to_dict().keys()

    for obj in queryset:
        temp_dict = dict()
        for field in fields:
            temp_dict[field] = getattr(obj, field)
        modelNameData.append(temp_dict)

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
    return "var " + modelName + "Data = " + json.dumps(modelNameData, default=dthandler) + ';'

def ko(queryset, field_names):

    koDataString = koData(queryset, field_names)
    koModelString = koModel(queryset[0].__class__.__name__, field_names, data=True)

    koString = koDataString + '\n' + koModelString

    return koString
