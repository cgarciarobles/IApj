import webcolors

primeraetapa = (
'darkolivegreen',
'olivedrab',
'yellowgreen',
'limegreen',
'lime',
'lawngreen',
'chartreuse',
'greenyellow',
'springgreen',
'mediumspringgreen',
'lightgreen',
'palegreen',
'darkseagreen',
'mediumaquamarine',
'mediumseagreen',
'seagreen',
'forestgreen',
'green',
'darkgreen'
)


etapamedia = (
'yellow',
'lightyellow',
'lemonchiffon',
'lightgoldenrodyellow',
'papayawhip',
'moccasin',
'peachpuff',
'palegoldenrod',
'khaki',
'darkkhaki'
)


etapafinal = (
'darkgoldenrod',
'peru',
'chocolate',
'saddlebrown',
'sienna',
'brown',
'maroon',
'silver',
'darkgray',
'gray',
'dimgray',
'lightslategray',
'slategray',
'darkslategray',
'black'
)





def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

requested_colour = (238, 232, 170)
actual_name, closest_name = get_colour_name(requested_colour)

print ("Actual colour name:", actual_name, ", closest colour name:", closest_name)
