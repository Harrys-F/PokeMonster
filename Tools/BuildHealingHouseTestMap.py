"""Run once with Unreal's PythonScript commandlet after building PokeMonsterEditor.

Creates only Dev_HealingHouseTestMap. Refuses to overwrite an existing map.
Existing materials/sprites are referenced, never edited or re-saved.
"""
import unreal

MAP = "/Game/Maps/Dev_HealingHouseTestMap"
if unreal.EditorAssetLibrary.does_asset_exist(MAP):
    raise RuntimeError("Healing-house map already exists; edit it in the editor instead.")

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world = unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
if not world:
    raise RuntimeError("Could not create healing-house map")

materials = {}
for name in ("Grass", "Path", "Wood", "Wall", "Roof", "Stone", "Water", "Leaves"):
    path = "/Game/Environment/Prototype/Materials/MI_Slice_" + name
    materials[name] = unreal.load_asset(path)
    if not materials[name]:
        raise RuntimeError("Missing existing material: " + path)
cube_mesh = unreal.load_asset("/Engine/BasicShapes/Cube")


def spawn(cls, name, location, folder, rotation=(0, 0, 0), tags=()):
    actor = actors.spawn_actor_from_class(cls, unreal.Vector(*location),
        unreal.Rotator(pitch=rotation[0], yaw=rotation[1], roll=rotation[2]))
    actor.set_actor_label(name)
    actor.set_folder_path(folder)
    actor.set_editor_property("tags", list(tags))
    return actor


def cube(name, location, size, material, folder, block=False, rotation=(0, 0, 0), tags=()):
    actor = spawn(unreal.StaticMeshActor, name, location, folder, rotation, tags)
    mesh = actor.static_mesh_component
    mesh.set_static_mesh(cube_mesh)
    mesh.set_material(0, materials[material])
    actor.set_actor_scale3d(unreal.Vector(*(v / 100.0 for v in size)))
    mesh.set_cast_shadow(False)
    mesh.set_collision_profile_name("BlockAll" if block else "NoCollision")
    if not block:
        mesh.set_editor_property("generate_overlap_events", False)
    return actor


# One continuous ground collision surface: no threshold, raised floor or hidden step.
cube("Ground", (0, 0, -30), (4000, 4000, 60), "Grass", "HealingHouse/Forecourt", True)
cube("Forecourt", (-850, 0, 0.5), (650, 680, 1), "Path", "HealingHouse/Forecourt")
cube("ApproachPath", (-1450, 0, 0.6), (750, 230, 1), "Path", "HealingHouse/Forecourt")
cube("InteriorFloor", (0, 0, 1), (870, 970, 2), "Wood", "HealingHouse/Interior")

# 9 x 10 m floor, 2.6 m walls, 2.4 m open door for the existing 56 cm capsule.
occluders = []
for y in (-310, 310):
    wall = cube("EntranceWall_" + str(y), (-450, y, 130), (30, 380, 260),
                "Wall", "HealingHouse/Body", True, tags=("HealingHouse_EntranceWall",))
    occluders.append(wall)
occluders.append(cube("DoorLintel", (-450, 0, 245), (30, 240, 30), "Wall", "HealingHouse/Door", True))
cube("RearWall", (450, 0, 130), (30, 1000, 260), "Wall", "HealingHouse/Body", True)
cube("FarSideWall", (0, -500, 130), (900, 30, 260), "Wall", "HealingHouse/Body", True)
occluders.append(cube("CameraSideWall", (0, 500, 130), (900, 30, 260), "Wall", "HealingHouse/Body", True))
for y in (-135, 135):
    occluders.append(cube("DoorPost_" + str(y), (-468, y, 120), (18, 20, 240), "Wood", "HealingHouse/Door"))
occluders.append(cube("DoorBeam", (-468, 0, 245), (18, 300, 22), "Wood", "HealingHouse/Door"))

# Two simple sloping roof sections, distinct from the colliding walls.
for y, angle in ((-260, -20), (260, 20)):
    occluders.append(cube("Roof_" + str(y), (0, y, 360), (1020, 570, 24),
                          "Roof", "HealingHouse/Roof", rotation=(0, 0, angle)))
occluders.append(cube("Ridge", (0, 0, 458), (1040, 25, 25), "Wood", "HealingHouse/Roof"))

# Window surfaces and frames are decoration, not extra collision hulls.
for y in (-315, 315):
    occluders.append(cube("FrontWindow_" + str(y), (-467, y, 158), (3, 100, 82),
                          "Water", "HealingHouse/Windows"))
    for offset in (-57, 57):
        occluders.append(cube("FrontWindowFrame_" + str(y) + "_" + str(offset),
                              (-470, y + offset, 158), (8, 10, 100), "Wood", "HealingHouse/Windows"))
    occluders.append(cube("FrontWindowSill_" + str(y), (-472, y, 111), (12, 124, 10),
                          "Stone", "HealingHouse/Windows"))
for x in (-230, 230):
    cube("FarWindow_" + str(x), (x, -483, 158), (100, 3, 82), "Water", "HealingHouse/Windows")

# Free central aisle; the counter blocks walking but lets the interaction sweep reach the healer.
counter = cube("HealingCounter", (220, -80, 42), (80, 340, 84), "Wood", "HealingHouse/Interior", True,
               tags=("HealingHouse_Counter",))
counter.static_mesh_component.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,
                                                               unreal.CollisionResponseType.ECR_IGNORE)
cube("CounterTop", (220, -80, 88), (94, 350, 8), "Stone", "HealingHouse/Interior")
for x in (-50, 170):
    cube("RestBed_" + str(x), (x, 350, 24), (150, 95, 48), "Wood", "HealingHouse/Interior/RestArea", True)
    cube("RestBedCover_" + str(x), (x, 350, 51), (138, 83, 6), "Leaves", "HealingHouse/Interior/RestArea")
cube("SupplyShelf", (160, -415, 60), (300, 75, 120), "Wood", "HealingHouse/Interior/Supplies", True)
for x in (60, 155, 250):
    cube("HerbPot_" + str(x), (x, -415, 133), (22, 22, 26), "Leaves", "HealingHouse/Interior/Supplies")
cube("SpareCreatureBed", (-170, -345, 18), (160, 120, 36), "Stone", "HealingHouse/Interior/Reserve", True)

healer_class = unreal.load_class(None, "/Script/PokeMonster.PokeMonsterRestPoint")
healer = spawn(healer_class, "HouseHealer", (330, -80, 62), "HealingHouse/Functions",
               tags=("HealingHouse_Healer",))
healer.set_editor_property("display_name", unreal.Text("Hüterin der Ruhestätte"))
healer.set_editor_property("intro_text", unreal.Text(
    "Willkommen. Ruhe einen Moment aus: Ich heile dein ganzes Team und fülle alle Attacken auf. "
    "Diese Hüterstätte wird dein neuer Wiederkehrort. Weiter zum Ausruhen."))
healer.set_editor_property("save_after_rest", True)
healer.set_editor_property("activate_checkpoint", True)
healer.set_editor_property("checkpoint_id", "Dev_HealingHouse")
sprite = healer.get_editor_property("sprite")
sprite_asset = unreal.load_asset("/Game/Characters/Prototype2D/Sprites/S_Archivarin")
if not sprite_asset:
    raise RuntimeError("Missing existing healer sprite")
sprite.set_sprite(sprite_asset)
dimensions = sprite_asset.get_editor_property("source_dimension")
ppu = sprite_asset.get_editor_property("pixels_per_unreal_unit")
sprite.set_relative_scale3d(unreal.Vector(*(90.0 * ppu / dimensions.y for _ in range(3))))
sprite.set_relative_rotation(unreal.Rotator(pitch=0, yaw=45, roll=-55), False, True)
sprite.set_relative_location(unreal.Vector(0, 0, -62), False, True)
for label in healer.get_components_by_class(unreal.TextRenderComponent):
    label.set_hidden_in_game(True)

cutaway_class = unreal.load_class(None, "/Script/PokeMonster.PokeMonsterBuildingCutaway")
cutaway = spawn(cutaway_class, "HouseCutaway", (-40, 0, 150), "HealingHouse/Functions")
cutaway.set_editor_property("occluding_actors", occluders)

start = spawn(unreal.PlayerStart, "SafeExteriorStart", (-1000, 0, 50), "HealingHouse/Functions",
              rotation=(0, 0, 0), tags=("PokeMonsterSafeFallback",))
world.get_world_settings().set_editor_property("default_game_mode",
    unreal.load_class(None, "/Script/PokeMonster.PokeMonsterGameMode"))

# A few existing illustrated plants mark the forecourt, without blocking the doorway.
for index, (x, y) in enumerate(((-1100, -430), (-700, -455), (-920, 450), (-560, 650))):
    plant = spawn(unreal.PaperSpriteActor, "ForecourtPlant_" + str(index), (x, y, 2), "HealingHouse/Forecourt")
    component = plant.get_editor_property("render_component")
    component.set_sprite(unreal.load_asset("/Game/Environment/Prototype2D/Details/S_GrassCluster"))
    component.set_collision_profile_name("NoCollision")
    component.set_cast_shadow(False)
    plant.set_actor_rotation(unreal.Rotator(pitch=0, yaw=45, roll=-55), False)
    plant.set_actor_scale3d(unreal.Vector(0.45, 0.45, 0.45))

sun = spawn(unreal.DirectionalLight, "SoftDaylight", (0, 0, 900), "HealingHouse/Lighting", (-55, -25, 0))
sun.light_component.set_editor_property("intensity", 2.0)
sun.light_component.set_editor_property("light_color", unreal.Color(255, 242, 220, 255))
sun.light_component.set_cast_shadows(False)
sky = spawn(unreal.SkyLight, "SoftFill", (0, 0, 700), "HealingHouse/Lighting")
sky.light_component.set_editor_property("intensity", 0.6)
unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(
    unreal.Vector(-1400, 1400, 1800), unreal.Rotator(pitch=-41, yaw=-45, roll=0))
if not unreal.EditorLoadingAndSavingUtils.save_map(world, MAP):
    raise RuntimeError("Could not save healing-house map")
unreal.log("HEALING_HOUSE_CREATED " + MAP + " actors=" + str(len(actors.get_all_level_actors())))
