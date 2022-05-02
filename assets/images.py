import pygame

player_image = pygame.image.load("assets\\images\\player.png")

dirt_image = pygame.image.load("assets\\images\\dirt_1.png")

grass_1_image = pygame.image.load("assets\\images\\grass_1.png")
grass_2_image = pygame.image.load("assets\\images\\grass_2.png")
grass_3_image = pygame.image.load("assets\\images\\grass_3.png")
grass_4_image = pygame.image.load("assets\\images\\grass_4.png")
grass_5_image = pygame.image.load("assets\\images\\grass_5.png")
grass_6_image = pygame.image.load("assets\\images\\grass_6.png")

tree_1_image = pygame.image.load("assets\\images\\tree_1.png")
tree_2_image = pygame.image.load("assets\\images\\tree_2.png")
tree_3_image = pygame.image.load("assets\\images\\tree_3.png")
tree_4_image = pygame.image.load("assets\\images\\tree_4.png")

grass_top_1_image = pygame.image.load("assets\\images\\grass_top_1.png")
grass_top_2_image = pygame.image.load("assets\\images\\grass_top_2.png")
mushroom_1_image = pygame.image.load("assets\\images\\mushroom_1.png")
mushroom_2_image = pygame.image.load("assets\\images\\mushroom_2.png")
mushroom_3_image = pygame.image.load("assets\\images\\mushroom_3.png")
sign_1_image = pygame.image.load("assets\\images\\sign_1.png")
statue_1_image = pygame.image.load("assets\\images\\statue_1.png")

devil_image = pygame.image.load("assets\\images\\devil.png")
minotaur_image = pygame.image.load("assets\\images\\minotaur.png")
goblin_image = pygame.image.load("assets\\images\\goblin.png")
zombie_image = pygame.image.load("assets\\images\\zombie.png")
knight_image = pygame.image.load("assets\\images\\knight.png")

battleaxe_image = pygame.image.load("assets\\images\\item_battleaxe.png")
mace_image = pygame.image.load("assets\\images\\item_mace.png")
silversword_image = pygame.image.load("assets\\images\\item_silversword.png")
trident_image = pygame.image.load("assets\\images\\item_trident.png")
warhammer_image = pygame.image.load("assets\\images\\item_warhammer.png")

grass_images = [grass_1_image, grass_2_image, grass_3_image,
                grass_4_image, grass_5_image, grass_6_image]

# find the largest height of the grass images
_max_height = max([image.get_height() for image in grass_images])

# create a list of grass images that are the same height as the largest
# grass image by adding a transparent background to the top of each image
for image in grass_images.copy():
    transparent_image = pygame.Surface((image.get_width(), _max_height), pygame.SRCALPHA)
    transparent_image.blit(image, (0, _max_height - image.get_height()))
    grass_images.append(transparent_image)

grass_images = grass_images[len(grass_images)//2:]

tree_images = [tree_1_image, tree_2_image, tree_3_image, tree_4_image]

_max_height = max([image.get_height() for image in tree_images])

for image in tree_images.copy():
    transparent_image = pygame.Surface((image.get_width(), _max_height), pygame.SRCALPHA)
    transparent_image.blit(image, (0, _max_height - image.get_height()))
    tree_images.append(transparent_image)

tree_images = tree_images[len(tree_images)//2:]


foliage_images = [
  mushroom_1_image, mushroom_2_image, mushroom_3_image,
  grass_top_1_image, grass_top_2_image
]

decor_images = [
  sign_1_image, statue_1_image
]