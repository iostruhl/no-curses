import random

# Maximum name length is 11 characters
#   '***********'
mariona_names = [
    'Mariona', 'Mitsubishi', 'Marga-RE-ti', 'Mr. Miyagi', 'Madagascar',
    'Mariposa', 'Masahiro', 'Missandei', 'Mordecai', 'Moriarty', 'Macaroni',
    'Marsupial', 'Montenegro', 'Missouri', 'Mississippi', 'Marlboro',
    'Meningitis', 'Mathematica', 'Motorcycle', 'Missionary', 'Maleficent',
    'Mozzarella', 'Magnesium', 'Montesquieu', 'Matrimony', 'Marinara',
    'Mujahedeen', 'Malodorous', 'Mariachi', 'Melanoma', 'Macerator',
    'Methylamine', 'Mussolini', 'Mauritius', 'Manchurian', 'Mankey',
    'Maraschino', 'Misdemeanor', 'Megohmmeter', 'Maharajah', 'Motorboat',
    'Moneymaker', 'Masochist', 'Manifesto', 'Metonymy', 'Mongolia',
    'Mozambique', 'Macedonia', 'Matriarchy', 'Mudblood'
]


def get_mariona_name():
    return random.choice(mariona_names)
