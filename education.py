def create_educations(educations):
    out = []
    for e in educations:
        education = Education()
        for (k,v) in e.items():
            setattr(education, k, v)
        out.append(education)
    return out

class Education:
    pass
    
