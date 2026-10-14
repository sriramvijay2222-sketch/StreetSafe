from math import asin, cos, radians, sin, sqrt

CATEGORY_WEIGHTS = {"exposed electrical wire": 60, "open drain": 40, "flooding": 35, "unsafe crossing": 35, "broken streetlight": 20, "other": 10}
SEVERITY_POINTS = {"low": 10, "medium": 25, "high": 40}

def priority(category: str, severity: str):
    weight, points = CATEGORY_WEIGHTS[category], SEVERITY_POINTS[severity]
    score = min(100, weight + points)
    return score, "low" if score < 40 else "medium" if score < 70 else "high", weight, points

def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000
    dlat, dlon = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*r*asin(sqrt(a))

def duplicate_ids(report, reports):
    return [r.incident_id for r in duplicate_reports(report, reports)]

def duplicate_reports(report, reports):
    return [r for r in reports if r.id != report.id and r.category == report.category and haversine_m(report.latitude, report.longitude, r.latitude, r.longitude) <= 150]
