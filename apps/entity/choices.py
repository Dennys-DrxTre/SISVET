# Nacionalidad

nat = "V-"
juri = "J-"
ex = "E-"
type_client = [(nat, 'V-'), (juri, 'J-'), (ex, 'E-')]

# Codigo de area Movil
Digitel1 = "0412"
Movilnet1 = "0416"
Movilnet2 = "0426"
Movistar1 = "0414"
Movistar2 = "0424"
cod_mobile = [
    (Digitel1, "0412"), 
    (Movilnet1, "0416"), 
    (Movilnet2, "0426"), 
    (Movistar1, "0414"), 
    (Movistar2, "0424") 
]

gender_choices = (
    ('Masculino','Masculino'),
    ('Femenino','Femenino'),
)

gender_pet = (
    ('Hembra','Hembra'),
    ('Macho','Macho')
)

species_pet = (
    ('Gato','Gato'),
    ('Perro','Perro'),
    ('oveja','oveja'),
    ('cerdo','cerdo'),
    ('vaca','vaca'),
    ('cabra','cabra'),
    ('toro','toro'),
    ('gallo','gallo'),
    ('gallina','gallina'),
    ('alce','alce'),
    ('burro','burro'),
)

unidad_product = (
    ('Litro(s)','Litro(s)'),
    ('Unidad(es)','Unidad(es)'),
    ('cm','cm'),
    ('g','g'),
    ('galon(es)','galon(es)'),
    ('kg','kg'),
    ('Libra(s)','Libra(s)'),
    ('onza(s)','onza(s)'),
    ('μg','μg'),
    ('mg','mg'),
    ('ml,','ml'),
)

type_sale_buy = (
    ('Compra','Compra'),
    ('Venta','Venta')
)