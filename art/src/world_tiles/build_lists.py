"""Names and sheet order shared by scene.py (Blender side) and build.py / wt_preview.py (venv side)."""
SIDES = ["nw", "n", "ne", "w", "e", "sw", "s", "se", "in_nw", "in_ne", "in_sw", "in_se"]
TERRAIN_ORDER = (
    [f"grass_path_{r}" for r in SIDES] + [f"grass_dirt_{r}" for r in SIDES] + [f"shore_{r}" for r in SIDES] +
    ["cliff_nw", "cliff_n", "cliff_ne", "cliff_w", "cliff_e",
     "cliff_face_a_l", "cliff_face_a", "cliff_face_a2", "cliff_face_a_r", "stairs_a",
     "cliff_face_b_l", "cliff_face_b", "cliff_face_b2", "cliff_face_b_r", "stairs_b",
     "cliff_shadow_l", "cliff_shadow", "cliff_shadow_r",
     "plateau_top_0", "plateau_top_1", "plateau_top_2",
     "bridge_h", "bridge_v", "bridge_h_w", "bridge_h_e", "bridge_v_n", "bridge_v_s", "snow_0", "snow_1", "sand_0", "sand_1", "lava_rock_0", "lava_rock_1", "cloud_0", "cloud_1"])
# only these terrain tiles are seamless with themselves (plain ground); everything else is an edge or a transition
TERRAIN_WRAP = {"plateau_top_0", "plateau_top_1", "plateau_top_2", "snow_0", "snow_1", "sand_0", "sand_1", "lava_rock_0", "lava_rock_1", "cloud_0", "cloud_1"}

# walk-blocking footprint of each prop in px, relative to its pivot: (dx, dy up is negative, w, h); None = walkable
PROP_SOLID = {
    "bamboo_1": (-6, -4, 12, 4), "bamboo_2": (-6, -4, 12, 4), "bamboo_3": (-5, -4, 10, 4), "pine_1": (-3, -4, 6, 4),
    "pine_2": (-3, -4, 6, 4), "tree_1": (-4, -5, 8, 5), "tree_2": (-4, -5, 8, 5), "peach_tree": (-4, -5, 8, 5),
    "dead_tree": (-4, -5, 8, 5), "bush_1": (-8, -5, 16, 5), "bush_2": (-8, -5, 16, 5), "rock_1": (-8, -5, 16, 5),
    "rock_2": (-9, -6, 18, 6), "rock_3": (-7, -5, 14, 5), "boulder": (-14, -8, 28, 8), "stump": (-6, -4, 12, 4),
    "log": (-15, -5, 30, 5), "crystal_1": (-7, -4, 14, 4), "crystal_2": (-7, -4, 14, 4),
}
PROP_NAME_VI = {
    "bamboo_1": "Trúc cao", "bamboo_2": "Khóm trúc", "bamboo_3": "Trúc thấp", "pine_1": "Cây tùng cao", "pine_2": "Cây tùng",
    "tree_1": "Cây lá rộng", "tree_2": "Cây lá vàng", "peach_tree": "Cây đào", "dead_tree": "Cây khô", "bush_1": "Bụi cây",
    "bush_2": "Bụi quả đỏ", "rock_1": "Đá nhỏ", "rock_2": "Đá vừa", "rock_3": "Đá rêu", "boulder": "Tảng đá lớn",
    "linh_thao_1": "Lam Tinh Thảo", "linh_thao_2": "Thanh Lộ Thảo", "linh_thao_3": "Dạ Quang Nấm", "linh_thao_4": "Kim Tuệ Thảo",
    "tall_grass": "Cỏ cao", "lotus": "Lá sen", "stump": "Gốc cây", "log": "Thân cây đổ", "crystal_1": "Tinh thạch lam",
    "crystal_2": "Tinh thạch tím", "cloud_puff_1": "Cụm mây nhỏ", "cloud_puff_2": "Cụm mây lớn", "mushroom_ring": "Vòng nấm",
}

# 32 px sheets: the same names, plus the isolated-cell tiles for path and dirt
EXTRA_ROLES = ["island", "h", "v", "cap_n", "cap_s", "cap_e", "cap_w"]
TERRAIN32_ORDER = TERRAIN_ORDER + [f"{p}_{r}" for p in ("grass_path", "grass_dirt") for r in EXTRA_ROLES]

_ALL = SIDES + ["in_nw", "in_ne", "in_sw", "in_se"][:0]
_FULL = ["nw", "n", "ne", "w", "e", "sw", "s", "se", "in_nw", "in_ne", "in_sw", "in_se"]
TERRAIN32_ORDER = TERRAIN32_ORDER + [f"{p}_{r}" for p in ("grass_stone", "grass_plaza", "grass_dark", "dark_ink") for r in _FULL + EXTRA_ROLES] \
    + [f"realm_edge_{r}" for r in _FULL]
