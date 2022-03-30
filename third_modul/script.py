from models import Region

region = Region("Xorazm1")
region.save()

print('*' * 30)
for item in Region.objects():
    print(item)

name = 'Xorazm'
region.name = name
region.save()

print('*' * 30)
for item in Region.objects():
    print(item)