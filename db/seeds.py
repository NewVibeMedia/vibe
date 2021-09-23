from django_seed import Seed

seeder = Seed.seeder()

# from myapp.models import Game, Player
# seeder.add_entity(Game, 5)
# seeder.add_entity(Player, 10)

inserted_pks = seeder.execute()