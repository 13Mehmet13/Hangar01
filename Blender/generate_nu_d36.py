"""
Hangar 01 - Nu.D36 (1930'lardan cift kanatli egitim ucagi) - dusuk-poligonlu model uretici
BMU1421 - Dijital Oyun Tasarimi - Hafta 01 lab foyune gore hazirlanmistir.

KULLANIM:
1) Blender 5.2 LTS'i ac (yeni/bos bir sahne).
2) Ust menuden "Scripting" sekmesine gec.
3) "New" ile yeni bir metin dosyasi olustur, bu dosyanin TUM icerigini icine yapistir.
4) Ust kisimdaki "Run Script" (uclu ok / Play) butonuna bas.
5) Script; govdeyi, kanatlari, kuyrugu, inis takimini, motoru ve pervaneyi olusturur,
   renklendirir, pervane haric hepsini "Nu_D36" adiyla birlestirir, pervaneyi ona
   parent yapar ve asagidaki OUTPUT_DIR klasorune Nu_D36.blend + Nu_D36.fbx olarak kaydeder.

NOT: Bu script govdenin ana hacmini, gercek olcekteki boyutlarini, kanat/kuyruk/inis
takimi/motor/pervane yerlesimini, malzemeleri, birlestirmeyi ve dogru FBX disa aktarim
ayarlarini otomatik yapar (foydeki en cok hata yapilan/en can sikici kisimlar). Kokpit
cukurlari Boolean ile otomatik acilir. BONUS gorevlerden ikisi de dahil edildi: arka
kokpitte basit bir pilot basi + ruzgarda ucusan atki, ve motorun onunde 9 silindirlik
bir yildiz motor halkasi.

Yon (Blender -Y = burun) veya pervane donus ekseni ters gorunurse, foydeki "Sik
karsilasilan hatalar" tablosundaki gibi normaldir; asagidaki rotation_euler
degerlerinin isaretini (90 <-> -90) degistirerek ya da Unity'de Donus Ekseni'ni
(0,1,0)/(1,0,0) deneyerek duzeltebilirsin.
"""

import bpy
import bmesh
import os
import math
from mathutils import Vector

# ---------------------------------------------------------------------------
# Ayarlanabilir cikti klasoru
# ---------------------------------------------------------------------------
OUTPUT_DIR = os.path.expanduser("~/Desktop/Hangar01")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 02) Birim sistemi: metrik, olcek 1.0
# ---------------------------------------------------------------------------
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# Baslangictaki varsayilan kupu sil (kamera ve isik kalsin)
default_cube = bpy.data.objects.get("Cube")
if default_cube is not None:
    bpy.data.objects.remove(default_cube, do_unlink=True)


def make_cube(name, size_x, size_y, size_z, loc):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = (size_x, size_y, size_z)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def make_cylinder(name, radius, depth, loc, rot_euler=(0, 0, 0), vertices=18):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = rot_euler
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return obj


def make_cone(name, radius1, radius2, depth, loc, rot_euler=(0, 0, 0), vertices=4):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2,
                                     depth=depth, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = rot_euler
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return obj


def set_material(obj, name, rgb):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
    mat.diffuse_color = (rgb[0], rgb[1], rgb[2], 1.0)
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is not None:
            bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def make_strut_between(name, p1, p2, radius=0.05, vertices=8):
    p1 = Vector(p1)
    p2 = Vector(p2)
    mid = (p1 + p2) / 2
    direction = p2 - p1
    length = direction.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=mid)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return obj


def shear_top_y(obj, shear_amount):
    """Ustteki (Z'si yuksek) verteksleri +Y'ye kaydirarak egimli/sweptback bir siluet verir."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    max_z = max(v.co.z for v in bm.verts)
    min_z = min(v.co.z for v in bm.verts)
    mid_z = (max_z + min_z) / 2
    for v in bm.verts:
        if v.co.z > mid_z:
            v.co.y += shear_amount
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')


def boolean_cut(obj, cutter):
    mod = obj.modifiers.new(name="cut_" + cutter.name, type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


RED = (0.55, 0.05, 0.05)
CREAM = (0.85, 0.78, 0.6)
GRAY = (0.35, 0.35, 0.35)
DERI = (0.3, 0.18, 0.1)
ATKI = (0.75, 0.55, 0.1)

# ---------------------------------------------------------------------------
# 03) Govde: ana kutu + inceltilmis kuyruk konisi (toplam ~6.4 m, burun -Y yonunde)
# ---------------------------------------------------------------------------
FUSE_CENTER_Z = 1.05
govde_ana = make_cube("Govde_Ana", 0.9, 5.4, 1.1, (0, 0, FUSE_CENTER_Z))

kuyruk_konisi = make_cone("Govde_KuyrukKonisi", 0.5, 0.08, 1.0,
                           (0, 3.2, FUSE_CENTER_Z), rot_euler=(math.radians(-90), 0, 0))

# Kokpitler: Boolean ile iki cukur ac (on koltuk + arka koltuk)
fuse_top = FUSE_CENTER_Z + 0.55
for cockpit_name, y_pos in (("Kokpit_On", -0.6), ("Kokpit_Arka", 0.6)):
    cutter = make_cube(cockpit_name + "_Kesici", 0.55, 0.7, 0.35,
                        (0, y_pos, fuse_top - 0.175))
    boolean_cut(govde_ana, cutter)

set_material(govde_ana, "Govde_Kirmizi", RED)
set_material(kuyruk_konisi, "Govde_Kirmizi", RED)

# ---------------------------------------------------------------------------
# 04) Kanatlar: farkli acikliktaki cift kanat + dikmeler (stagger uygulanmis)
# ---------------------------------------------------------------------------
UST_KANAT_Z = fuse_top + 0.7
ALT_KANAT_Z = FUSE_CENTER_Z - 0.55 + 0.15

ust_kanat = make_cube("UstKanat", 9.74, 1.5, 0.15, (0, -0.3, UST_KANAT_Z))
alt_kanat = make_cube("AltKanat", 8.5, 1.3, 0.15, (0, 0, ALT_KANAT_Z))
set_material(ust_kanat, "Kanat_Krem", CREAM)
set_material(alt_kanat, "Kanat_Krem", CREAM)

strut_len = UST_KANAT_Z - ALT_KANAT_Z
strut_mid_z = (UST_KANAT_Z + ALT_KANAT_Z) / 2
strut_y = -0.15
dikmeler = []
for x in (-3.0, 3.0):
    d = make_cylinder(f"Dikme_Kanat_{x}", 0.04, strut_len, (x, strut_y, strut_mid_z), vertices=8)
    dikmeler.append(d)

cabin_len = UST_KANAT_Z - fuse_top
cabin_mid_z = (UST_KANAT_Z + fuse_top) / 2
for x in (-0.5, 0.5):
    d = make_cylinder(f"Dikme_Kabin_{x}", 0.04, cabin_len, (x, -0.3, cabin_mid_z), vertices=8)
    dikmeler.append(d)
for d in dikmeler:
    set_material(d, "Govde_Kirmizi", RED)

# ---------------------------------------------------------------------------
# 05) Kuyruk yuzeyleri ve inis takimi
# ---------------------------------------------------------------------------
yatay_stab = make_cube("YatayStabilizor", 3.0, 0.9, 0.08, (0, 3.5, FUSE_CENTER_Z + 0.15))
dikey_stab = make_cube("DikeyStabilizor", 0.08, 1.0, 1.0, (0, 3.5, FUSE_CENTER_Z + 0.6))
shear_top_y(dikey_stab, 0.35)  # ust on kenari geriye cekilmis, egimli bir dumen
set_material(yatay_stab, "Govde_Kirmizi", RED)
set_material(dikey_stab, "Govde_Kirmizi", RED)

WHEEL_R = 0.4
FUSE_BOTTOM = FUSE_CENTER_Z - 0.55
tekerlekler = []
for x in (-1.8, 1.8):
    tekerlek = make_cylinder(f"Tekerlek_{x}", WHEEL_R, 0.15, (x, 0, WHEEL_R),
                              rot_euler=(0, math.radians(90), 0))
    wheel_pos = (x, 0, WHEEL_R)
    # V bicimli inis takimi: tekerlekten govde tabanina, biri one biri arkaya yaslanan iki dikme
    strut_a = make_strut_between(f"IskeleDikmesi_{x}_On", wheel_pos, (x * 0.15, -0.35, FUSE_BOTTOM), radius=0.05)
    strut_b = make_strut_between(f"IskeleDikmesi_{x}_Arka", wheel_pos, (x * 0.15, 0.35, FUSE_BOTTOM), radius=0.05)
    tekerlekler += [tekerlek, strut_a, strut_b]

kuyruk_kizagi = make_cube("KuyrukKizagi", 0.1, 0.3, 0.1, (0, 3.5, 0.45))
for o in tekerlekler + [kuyruk_kizagi]:
    set_material(o, "Motor_Gri", GRAY)

# ---------------------------------------------------------------------------
# 06) Motor ve pervane: pervane AYRI bir nesne olarak kalir
# ---------------------------------------------------------------------------
motor = make_cylinder("Motor", 0.55, 0.45, (0, -2.925, FUSE_CENTER_Z),
                       rot_euler=(math.radians(90), 0, 0), vertices=18)
set_material(motor, "Motor_Gri", GRAY)

# BONUS: Yildiz motor - motorun onune cember seklinde 9 kucuk silindir
motor_on_y = -2.925 - 0.225
yildiz_motor = []
YM_R = 0.42
for i in range(9):
    angle = 2 * math.pi * i / 9
    cx = YM_R * math.cos(angle)
    cz = FUSE_CENTER_Z + YM_R * math.sin(angle)
    silindir = make_cylinder(f"YildizMotor_{i}", 0.09, 0.14, (cx, motor_on_y, cz),
                              rot_euler=(math.radians(90), 0, 0), vertices=10)
    yildiz_motor.append(silindir)
for o in yildiz_motor:
    set_material(o, "Motor_Gri", GRAY)

# BONUS: Pilot basi + ruzgarda ucusan atki (arka kokpitte)
pilot_kafa = bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.16,
                                                    location=(0, 0.6, fuse_top + 0.13))
pilot_kafa = bpy.context.active_object
pilot_kafa.name = "PilotKafasi"
set_material(pilot_kafa, "Pilot_Deri", DERI)

atki_1 = make_cube("Atki_1", 0.32, 0.28, 0.05, (0, 0.62 + 0.24, fuse_top + 0.18))
atki_1.rotation_euler = (math.radians(-18), 0, 0)
bpy.context.view_layer.objects.active = atki_1
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

atki_2 = make_cube("Atki_2", 0.24, 0.22, 0.04, (0.08, 0.62 + 0.46, fuse_top + 0.3))
atki_2.rotation_euler = (math.radians(-34), 0, math.radians(10))
bpy.context.view_layer.objects.active = atki_2
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

for o in (atki_1, atki_2):
    set_material(o, "Atki_Sari", ATKI)

pervane = make_cube("Pervane", 2.2, 0.08, 0.18, (0, -3.21, FUSE_CENTER_Z))
set_material(pervane, "Motor_Gri", GRAY)
bpy.context.view_layer.objects.active = pervane
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

# ---------------------------------------------------------------------------
# 07) Renkler zaten verildi -> Pervane disindaki her seyi "Nu_D36" olarak birlestir
# ---------------------------------------------------------------------------
hull_parts = ([govde_ana, kuyruk_konisi, ust_kanat, alt_kanat, yatay_stab, dikey_stab,
               kuyruk_kizagi] + dikmeler + tekerlekler + [motor] + yildiz_motor +
              [pilot_kafa, atki_1, atki_2])

bpy.ops.object.select_all(action='DESELECT')
for o in hull_parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = govde_ana
bpy.ops.object.join()
nu_d36 = bpy.context.active_object
nu_d36.name = "Nu_D36"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

# Origin'i govde ortasindan yer (Z=0, tekerlek tabani) seviyesine tasi.
# Boylece Unity'de Position (0,0,0) verildiginde tekerlekler tam zemine oturur;
# aksi halde govde-merkezli pivot yuzunden ucagin alt kismi (tekerlek, pervane)
# eklenen Ground Plane'in altina gomulur.
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.context.view_layer.objects.active = nu_d36
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

# Pervaneyi Nu_D36'nin altina parent yap (Unity Hierarchy'de Nu_D36 > Pervane olsun)
bpy.ops.object.select_all(action='DESELECT')
pervane.select_set(True)
nu_d36.select_set(True)
bpy.context.view_layer.objects.active = nu_d36
bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

# ---------------------------------------------------------------------------
# 08) Disa aktar: Nu_D36.blend + Nu_D36.fbx (foydeki tam ayarlarla)
# ---------------------------------------------------------------------------
blend_path = os.path.join(OUTPUT_DIR, "Nu_D36.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

bpy.ops.object.select_all(action='DESELECT')
nu_d36.select_set(True)
pervane.select_set(True)
bpy.context.view_layer.objects.active = nu_d36

fbx_path = os.path.join(OUTPUT_DIR, "Nu_D36.fbx")
bpy.ops.export_scene.fbx(
    filepath=fbx_path,
    use_selection=True,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_ALL',
    axis_forward='-Z',
    axis_up='Y',
    bake_space_transform=True,
    object_types={'MESH'},
)

# BONUS: Tarayicida (three.js editor) gostermek icin glTF olarak da disa aktar
glb_path = os.path.join(OUTPUT_DIR, "Nu_D36.glb")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    use_selection=True,
    export_format='GLB',
)

print("Bitti! Dosyalar su klasorde:", OUTPUT_DIR)
print(" -", blend_path)
print(" -", fbx_path)
print(" -", glb_path)
