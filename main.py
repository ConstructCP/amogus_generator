from app.amogus_generator import AmogusFactory
from app.image_generator import AmogusImageGenerator


amogus = AmogusFactory().generate_amogus()
image = AmogusImageGenerator(amogus.name).generate_image()
image.save('image.png')
print(amogus.name)