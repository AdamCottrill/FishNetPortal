def get_create_update_delete(model, filters, data):
    """given a model, a set of filters and an array of data dictionaries,
    return the list of slugs for database entries that need to be
    deleted (are in the database but not in the data), created (are in
    the data but do not exist in the database), and updated (are in
    both the database and data)

    """
    in_glis = set([x[0] for x in model.objects.filter(**filters).values_list("slug")])
    # get the set of slugs in our upload:
    in_upload = set([x["slug"] for x in data])

    update = list(in_glis.intersection(in_upload))
    create = list(in_upload - in_glis)
    delete = list(in_glis - in_upload)

    return [create, update, delete]


def create_update_delete(data, model, filters, parent_key, parent_map, parent_inverse):
    """A function to syncronyze the data in the database with the data
    passed in for each model.  It first compares the passed in data
    with the values in the database to determine which objects need to
    be created, updated, or deleted.  It then removes records that
    should be deleted, and compiles list of objects to create or
    update using django bulk update and bulk create functionality.

    NOTE: this function is only suitable for models that have single
    foreign keys, require anykind of pre-processing, and do not rely
    on custom save functionality.  For example, it cannot be used for
    FN121 objects as they have multiple foreign keys to each of the
    design tables and use a custom save method to associate each
    record with the spatial polygons.

    """

    create_slugs, update_slugs, delete_slugs = get_create_update_delete(
        model, filters, data
    )
    model.objects.filter(slug__in=delete_slugs).delete()
    to_be_created = []
    updates = {}
    for item in [x for x in data if x["slug"] in create_slugs + update_slugs]:
        # call preprocessor here to make any necessary transformation to each item
        # what needs to be done depends on the current model.
        tmp = item[parent_key]
        item[parent_key] = parent_map[parent_inverse[tmp]]
        if item["slug"] in create_slugs:
            to_be_created.append(model(**item))
        else:
            updates[item["slug"]] = item
    model.objects.bulk_create(to_be_created)
    batch_update_model(model, update_slugs, updates)


def batch_update_model(model, update_slugs, updates):
    """Given a FN Portal model, a list of slugs corresponding to records
    that need to be updated, and a list of dictionaries containing the
    updates, fetch the corresponding model objects from the database
    using the slugs,

    To prevent updating all fields for all records (which are unlikely
    to have changed), we need to update just those records that have
    changed, and only those fields that are different.

    for each object, find the corresponding updated dictionary and
    compare the attributes of the object with the values in the
    updated dictionary. If there are no differences, pop this object
    off the list of objects. If there are differences, findout which
    fields/atts are differet and add those fields to the field list.

    Arguments:
    - `model`: fn_portal model

    - `update_slugs`: list of slugs for records that need to be updated

    - `updates`: a list of dictionaries containing data that will be
      used for updates.

    """

    if len(updates):
        objs = [x for x in model.objects.filter(slug__in=update_slugs)]
        for obj in objs:
            attrs = updates[obj.slug]
            keep = False
            fields = set()
            for attr in attrs:
                if getattr(obj, attr) != attrs[attr]:
                    keep = True
                    fields.add(attr)
                    setattr(obj, attr, attrs[attr])
            if keep is False:
                objs.remove(obj)
        if len(objs) and len(list(fields)):
            model.objects.bulk_update(objs, fields=list(fields), batch_size=1000)
