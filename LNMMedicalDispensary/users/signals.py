# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

# from django.contrib.auth.models import User
# from .models import Doctor, Chemist

# def createDocChem(sender, instance, created, **kwargs):
#     user = instance
#     print('Signal Triggered')
#     if created:
#         print('Created')
#         if user.is_doctor:
#             print('Doctor')
#             doctor = Doctor.objects.create(
#                 # user = user,
#                 # username = user.username,
#                 age=user.age,
#                 name = user.first_name + ' ' + user.last_name,
#                 gender = user.gender,
#             )
#             doctor.save()
#         if user.is_chemist:
#             print('Chemist')
#             chemist = Chemist.objects.create(
#                 name = user.first_name + ' ' + user.last_name,
#                 age = user.age,
#                 gender = user.gender,
#             )
#             chemist.save()
#     else:
#         # user = instance
#         print('Not created')
#         if user.is_doctor:
#             print('Doctor')
#             doctor = Doctor.objects.get(
#                 Did = user.Did
#             )
#             doctor.name = user.first_name + ' ' + user.last_name,
#             doctor.age = user.age,
#             doctor.gender = user.gender,
#             doctor.save()
#         if user.is_chemist:
#             print('Chemist')
#             chemist = Chemist.objects.get(
#                 Cid = user.Cid
#             )
#             chemist.name = user.first_name + ' ' + user.last_name,
#             chemist.age = user.age,
#             chemist.gender = user.gender,
#             chemist.save()

# def deleteUser(sender, instance, **kwargs):
#     user = instance.user
#     user.delete()


# post_save.connect(createDocChem, sender = User, dispatch_uid="create_DocChem_instance")

# post_delete.connect(deleteUser, sender = Doctor)
# post_delete.connect(deleteUser, sender = Chemist)

# # post_delete.connect(deleteChemUser, sender = Chemist)
