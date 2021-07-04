def serialize(x, as_type=None, nullable=False):
    if nullable:
        return None if x is None else as_type(x)
    else:
        assert(x is not None)
        return as_type(x)


def serialize_company_details(cd):
    return {
        'cid': serialize(cd.cid, as_type=int),
        'name': cd.name,
        'avg_salary': serialize(cd.avg_salary, as_type=float, nullable=True),
        'avg_rating': serialize(cd.avg_rating, as_type=float, nullable=True),
    }


def serialize_job_details(jd):
    return {
        'cid': serialize(jd.cid, as_type=int),
        'jid': serialize(jd.jid, as_type=int),
        'company_name': jd.company_name,
        'job_title': jd.job_title,
        'avg_salary': serialize(jd.avg_salary, as_type=float, nullable=True),
        'avg_rating': serialize(jd.avg_rating, as_type=float, nullable=True),
    }


def serialize_tag(tag):
    return {
        'tid': serialize(tag.tid, as_type=int),
        'label': tag.label,
    }
