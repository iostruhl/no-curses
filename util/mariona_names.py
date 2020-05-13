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
    'Mozambique', 'Macedonia', 'Matriarchy', 'Mudblood', 'Martingetti',
    'Margrave', 'Maple Glaze', 'Misanthropy', 'Medication', 'Monopoly',
    'Marionette', 'Morbidezza', 'Metadata', 'Megabyte', 'Mafioso', 'Manicotti',
    'Mario', 'Martinelli', 'Lil\' Trash', 'Mysterio', 'Mahershala', 'Mandingo',
    'Musk Ox', 'Magdalena', 'Masaccio', 'Misbeliever', 'Minesweeper',
    'Monteverdi', 'Mustachioed', 'Macadamia', 'Misbegotten', 'Memorandum',
    'Maravilla', 'Monolingual', 'Malapropos', 'Millenial', 'Melliferous',
    'Mamoncillo', 'Meshuggeneh', 'Midsemester', 'Malocchio', 'Manichaean',
    'Malthusian', 'Manzanilla', 'Mexicali', 'Miscitation', 'Montevideo',
    'Miscellany', 'Majordomo', 'Misestimate', 'Marathoner', 'Mugwumpery',
    'Mitigator', 'Moneymonger', 'Methuselah', 'Machismo', 'Mogadishu',
    'Muscle Milk', 'Mowgli', 'Mogul', 'Mammogram', 'Marmaduke',
    'Melissandra', 'Marc Antony', 'Manishewitz', 'Matza Ball',
    'Negotiator', 'Manbun', 'Marblehead', 'Madonna', 'Macklemore',
    'Melatonin', 'Malpractice', 'Marmalade', "MARIOVID-19"
]

def get_mariona_name():
    return random.choice(mariona_names)
