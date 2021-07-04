def id_num(x):
    return int(x)


def mmr(x):
    return int(x)


def money(x):
    return round(float(x), 2)


def rating(x):
    return round(float(x), 1)


def string(x):
    return str(x)


def nullable(serializer):
    def serialize(x):
        return None if x is None else serializer(x)
    return serialize


def non_null(serializer):
    def serialize(x):
        assert(x is not None)
        return serializer(x)
    return serialize


def serializer(schema):
    def serialize(x):
        return {
            key: ser(getattr(x, key))
            for key, ser in schema.items()
        }
    return serialize


serialize_company_details = serializer({
    'cid': non_null(id_num),
    'company_name': non_null(string),
    'company_mmr': non_null(mmr),
    'company_min_salary': nullable(money),
    'company_avg_salary': nullable(money),
    'company_max_salary': nullable(money),
    'company_avg_rating': nullable(rating),
})

serialize_job_details = serializer({
    'cid': non_null(id_num),
    'company_name': non_null(string),
    'company_mmr': non_null(mmr),
    'jid': non_null(id_num),
    'job_title': non_null(string),
    'company_min_salary': nullable(money),
    'company_avg_salary': nullable(money),
    'company_max_salary': nullable(money),
    'company_avg_rating': nullable(rating),
    'job_min_salary': nullable(money),
    'job_avg_salary': nullable(money),
    'job_max_salary': nullable(money),
    'job_avg_rating': nullable(rating),
})

serialize_tag = serializer({
    'tid': non_null(string),
    'label': non_null(string),
})
