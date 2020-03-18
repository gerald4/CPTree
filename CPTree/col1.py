#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:31:33 2019

@author: labogeraldo
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy as np


### This function is taken from sklearn 
### Source https://github.com/scikit-learn/scikit-learn/blob/7b136e9/sklearn/tree/export.py#L75
def _color_brew(n):
    """Generate n colors with equally spaced hues.
    Parameters
    ----------
    n : int
        The number of colors required.
    Returns
    -------
    color_list : list, length n
        List of n tuples of form (R, G, B) being the components of each color.
    """
    color_list = []

    # Initialize saturation & value; calculate chroma & value shift
    s, v = 0.75, 0.9
    c = s * v
    m = v - c

    for h in np.arange(25, 385, 360. / n).astype(int):
        # Calculate some intermediate values
        h_bar = h / 60.
        x = c * (1 - abs((h_bar % 2) - 1))
        # Initialize RGB with same hue & chroma as our color
        rgb = [(c, x, 0),
               (x, c, 0),
               (0, c, x),
               (0, x, c),
               (x, 0, c),
               (c, 0, x),
               (c, x, 0)]
        r, g, b = rgb[int(h_bar)]
        # Shift the initial RGB values to match value and store
        rgb = [(int(255 * (r + m))),
               (int(255 * (g + m))),
               (int(255 * (b + m)))]
        color_list.append(rgb)

    return color_list

def get_color(value,n_classes):
	# Find the appropriate color & intensity for a node
        # Classification tree
    colors={}
    colors['rgb'] = _color_brew(n_classes)
    color = list(colors['rgb'][np.argmax(value)])
    sorted_values = sorted(value, reverse=True)
    if len(sorted_values) == 1:
        alpha = 0
    else:
        alpha = int(np.round(255 *(sorted_values[0]-sorted_values[1])/(1+sorted_values[0]),0))
    color.append(alpha)
    hex_codes = [str(i) for i in range(10)]
    hex_codes.extend(['a', 'b', 'c', 'd', 'e', 'f'])
    color = [hex_codes[c // 16] + hex_codes[c % 16] for c in color]
    return '#' + ''.join(color)
