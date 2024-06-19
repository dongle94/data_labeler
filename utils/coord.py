

def get_box_point(pt1, pt2):
    """
    return box point xyxy with 2 points
    :param pt1:
    :param pt2:
    :return new_pt1, new_pt2:
    """
    x1, y1 = pt1
    x2, y2 = pt2
    new_pt1 = (min(x1, x2), min(y1, y2))
    new_pt2 = (max(x1, x2), max(y1, y2))
    return new_pt1, new_pt2