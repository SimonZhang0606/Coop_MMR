def id_num(x, obj):
    return int(x)


def mmr(x, obj):
    return int(x)


def rank(field):
    def serialize(x, obj):
        return None if getattr(obj, field) is None else x
    return serialize


def money(x, obj):
    return round(float(x), 2)


def rating(x, obj):
    return round(float(x), 1)


def string(x, obj):
    return str(x)


def nullable(serializer):
    def serialize(x, obj):
        return None if x is None else serializer(x, obj)
    return serialize


def non_null(serializer):
    def serialize(x, obj):
        assert(x is not None)
        return serializer(x, obj)
    return serialize


def serializer(schema):
    def serialize(obj):
        return {
            key: ser(getattr(obj, key), obj)
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
    'company_salary_rank': rank('company_avg_salary'),
    'company_rating_rank': rank('company_avg_rating'),
    'company_mmr_rank': rank('company_mmr'),
})

serialize_job_details = serializer({
    'cid': non_null(id_num),
    'company_name': non_null(string),
    'company_mmr': non_null(mmr),
    'company_min_salary': nullable(money),
    'company_avg_salary': nullable(money),
    'company_max_salary': nullable(money),
    'company_avg_rating': nullable(rating),
    'company_salary_rank': rank('company_avg_salary'),
    'company_rating_rank': rank('company_avg_rating'),
    'company_mmr_rank': rank('company_mmr'),
    'jid': non_null(id_num),
    'job_title': non_null(string),
    'job_min_salary': nullable(money),
    'job_avg_salary': nullable(money),
    'job_max_salary': nullable(money),
    'job_avg_rating': nullable(rating),
    'job_salary_rank': rank('job_avg_salary'),
    'job_rating_rank': rank('job_avg_rating'),
})

serialize_review = serializer({
    'cid': non_null(id_num),
    'jid': non_null(id_num),
    'rid': non_null(id_num),
    'headline': non_null(string),
    'review_body': non_null(string),
    'rating': nullable(rating),
})

serialize_tag = serializer({
    'tid': non_null(string),
    'label': non_null(string),
})
