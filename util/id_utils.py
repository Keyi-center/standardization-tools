import uuid


def gen_work_id(namespace=None):
    # make a random UUID

    tmp_id = str(uuid.uuid4()).replace('-', '')[:16]
    if namespace is not None:
        return f'{namespace}-{tmp_id}'

    return tmp_id
