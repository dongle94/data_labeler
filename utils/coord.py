

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


def absxyxy_to_relxyxy(points, img_w, img_h):
    x1, y1, x2, y2 = points

    rel_x1, rel_y1 = round(x1 / img_w, 6), round(y1 / img_h, 6)
    rel_x2, rel_y2 = round(x2 / img_w, 6), round(y2 / img_h, 6)

    return rel_x1, rel_y1, rel_x2, rel_y2
