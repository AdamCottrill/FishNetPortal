PRECIP_CHOICES = [
    ("00", "none"),
    ("10", "mist"),
    ("40", "fog"),
    ("51", "slight drizzle"),
    ("55", "heavy drizzle"),
    ("61", "light rain"),
    ("65", "heavy rain"),
    ("71", "light snow"),
    ("75", "heavy snow"),
    ("80", "light rain shower"),
    ("85", "heavy rain shower"),
    ("95", "thunder storm"),
]

PRECIP_DURAITON_CHOICES = [
    (1, "no precipitation"),
    (2, "< 4 hours of precipitation"),
    (3, "> 4 hours of precipitation"),
    (4, "constant precipitation"),
]

WAVE_DURAITON_CHOICES = [
    (1, "no precipitation"),
    (2, "< 4 hours of precipitation"),
    (3, "> 4 hours of precipitation"),
    (4, "constant precipitation"),
]

VEGETATION_CHOICES = [
    (1, "None"),
    (2, "Sparse (1-25%)"),
    (3, "Moderate (25-75%)"),
    (4, "Dense (>75%)"),
]

VESSEL_DIRECTION_CHOICES = [
    (0, "Variable"),
    (1, "Northeast"),
    (2, "East"),
    (3, "Southeast"),
    (4, "South"),
    (5, "Southwest"),
    (6, "West"),
    (7, "Northwest"),
    (8, "North"),
    (9, "Not Definable"),
]


# Move this to common as a lookup
ORIENT_CHOICES = [
    ("1", "Perpendicular"),
    ("2", "Paralell"),
    ("3", "Other"),
    ("9", "Unknown"),
    ("U", "Upstream"),
    ("D", "Downstream"),
]
