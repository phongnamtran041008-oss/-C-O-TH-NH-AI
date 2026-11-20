"""Every string the player sees (spec 0: Vietnamese UI, kept separate from code)."""

TITLE = "Toán Tu Tiên"
TAGLINE = "Giải một bài, thu một tia linh khí"

MENU_START = "Bắt đầu"
MENU_SETTINGS = "Cài đặt"
MENU_CREDITS = "Ghi công"
MENU_QUIT = "Thoát"

LOGIN = "Đăng nhập"
REGISTER = "Đăng ký"
RECOVER = "Quên mật khẩu"
USERNAME = "Tên đăng nhập"
PASSWORD = "Mật khẩu"
PASSWORD_AGAIN = "Nhập lại mật khẩu"
RECOVERY_CODE = "Mã khôi phục"
NEW_PASSWORD = "Mật khẩu mới"
PASSWORDS_DIFFER = "Hai mật khẩu không giống nhau."
CONNECTING = "Đang kết nối máy chủ..."
CANNOT_CONNECT = ("Không kết nối được máy chủ {url}. Hãy mở chay_server.bat, để cửa sổ đó chạy và xem nó có "
                  "báo lỗi không. Game sẽ tự thử lại...")
SERVER_STARTING = "Máy chủ đang khởi động, chờ khoảng 1 phút..."
OFFLINE = "Mất kết nối máy chủ, đang thử lại..."
VERSION_MISMATCH = "Phiên bản game đã cũ, hãy tải bản mới để chơi tiếp."
DOWNLOAD_AT = "Tải bản mới ở: {url}"
NEW_VERSION = "Đã có bản v{version} — tải ở trang máy chủ hoặc GitHub Releases."
UPDATE_TITLE = "Có bản cập nhật!"
UPDATE_TEXT = "Đã có Toán Tu Tiên v{v} (bạn đang dùng v{cur})."
UPDATE_HOW = ("Cách cập nhật: bấm Tải về → tắt game → giải nén file vừa tải ĐÈ lên thư mục game cũ "
              "(Windows hỏi thì chọn Replace / Thay thế). Thế giới và tài khoản vẫn giữ nguyên.")
UPDATE_DOWNLOAD = "Tải về"
UPDATE_LATER = "Để sau"
UPDATE_OPENED = "Đang tải trong trình duyệt..."
UPDATE_TOAST = "Đã có bản mới v{v} — xem ở màn hình chính"
UPDATE_MENU = "Có bản mới v{v} — bấm để tải"
MAINTENANCE = "Bảo trì: {text}"
ANNOUNCEMENT = "Thông báo: {text}"
CRASHED = "Game gặp lỗi và phải đóng.\nChi tiết đã lưu ở:\n{path}\nHãy gửi file này cho người làm game nhé."
SERVER = "Máy chủ"
BACK = "Quay lại"
OK = "Đồng ý"
CANCEL = "Hủy"
CLOSE = "Đóng"

RECOVERY_TITLE = "Mã khôi phục của bạn"
RECOVERY_SAVED = "Tôi đã chép lại"
RECOVERY_HINT = ("Đây là lần duy nhất mã được hiển thị. Hãy chép ra giấy hoặc lưu ở nơi an toàn: "
                 "khi quên mật khẩu, bạn cần tên đăng nhập và mã này để đặt lại.")

CREATE_TITLE = "Tạo nhân vật"
CHAR_NAME = "Đạo hiệu (tên nhân vật)"
BODY = "Dáng người"
CREATE_NOTE = "Mọi người đều bắt đầu với bộ Áo Vải Phàm Nhân. Còn lại, tự tu luyện mà có!"
CREATE_GO = "Nhập môn"

REALMS = {"pham_nhan": "Phàm Nhân", "luyen_khi": "Luyện Khí", "truc_co": "Trúc Cơ",
          "kim_dan": "Kết Đan", "nguyen_anh": "Nguyên Anh", "hoa_than": "Hóa Thần", "luyen_hu": "Luyện Hư",
          "hop_the": "Hợp Thể", "dai_thua": "Đại Thừa"}

HUD_BAG = "Túi đồ"
HUD_BOOK = "Các phổ"
HUD_GACHA = "Thiên Cơ"
HUD_MENU = "Cài đặt"
HUD_FRIENDS = "Bạn bè"
PRESS_E = "[E] {action}"
ACTIONS = {"gacha": "Thiên Cơ Đài", "meditate": "Bàn đả tọa", "exit": "Xuống Trúc Lâm Thôn",
           "talk": "Nói chuyện", "hive": "Linh Phong Sào", "alchemy": "Đan Lô (luyện đan)"}


QUIZ_SUBMIT = "Trả lời"
QUIZ_CORRECT = "Chính xác!"
QUIZ_WRONG = "Chưa đúng"
QUIZ_TIMEOUT = "Hết giờ!"
QUIZ_ANSWER_WAS = "Đáp án: {a}"

GACHA_ROLL1 = "Quay 1 ({p})"
GACHA_ROLL10 = "Quay 10 ({p})"
GACHA_FREE = "Quay miễn phí"

BAG_TITLE = "Túi đồ"
EMPTY_LIST = "Chưa có gì ở đây."



SETTINGS_TITLE = "Cài đặt"
SCALE = "Phóng to"
SCALE_AUTO = "Tự động"
FULLSCREEN = "Toàn màn hình"
SFX_VOLUME = "Âm lượng hiệu ứng"
LOGOUT = "Đăng xuất"
SAVE = "Lưu"

CREDITS_TITLE = "Ghi công"
CREDITS_TEXT = (
    "Phông chữ: VT323 và Noto Sans SC (SIL OFL 1.1) · Hình công thức toán: MathJax (Apache 2.0). "
    "Hình vẽ và âm thanh hiệu ứng của game được làm bằng code."
)

# ---------------------------------------------------------------- Trúc Lão
MASTER = "Trúc Lão"
MASTER_IDLE = ["Trà nguội rồi... con có thấy cái chén của ta đâu không?",
               "Ôn đúng lúc quan trọng hơn ôn nhiều. Tu luyện cũng thế, người cũng thế.",
               "Ngồi bàn đả tọa mà giải bài, linh khí tự khắc tụ về.",
               "Hồi trẻ ta cũng muốn giữ hết bí kíp cho riêng mình... à mà thôi, chuyện cũ rồi.",
               "Sai một bài thì nhớ lâu một đời. Đừng sợ sai, chỉ sợ không thử."]


# ---------------------------------------------------------------- stage 3: the shared world
ZONE_NAMES = {"abode": "Động Phủ", "truc_lam_thon": "Trúc Lâm Thôn", "rung_muc_loang": "Mê Đồ Lâm",
              "ho_nghien_muc": "Vạn Tượng Trạch", "loan_so_coc": "Kiếm Trủng Sơn",
              "luu_van_coc": "Lưu Vân Cốc", "thien_cong_phuong": "Thiên Công Phường",
              "linh_xa_nguyen": "Linh Xạ Nguyên", "loi_kiep_dai": "Lôi Kiếp Đài",
              "bi_canh": "Bí Cảnh"}
# where a player may be standing when they log out, so the game sends them back there
WORLD_ZONES = ("truc_lam_thon", "rung_muc_loang", "ho_nghien_muc", "loan_so_coc",
               "luu_van_coc", "thien_cong_phuong", "linh_xa_nguyen", "loi_kiep_dai")
# Thiên Địa Đồ: the weapons lying in the lands (GET /weapons, the weapon system draws the rest)
WEAPON_SPOT = "Binh khí"
WEAPON_SPOT_TAKEN = "Binh khí này đã có chủ."
WEAPON_SPOT_LOCKED = "Chưa đủ tu vi để cầm binh khí này."
WEAPON_SPOT_CLAIMED = "Đã nhặt {name}."
ENTERING = "Đang đến {zone}..."
CONNECTING_WORLD = "Đang kết nối thế giới..."
CHANNEL = "Kênh {n}"
CHANNELS_TITLE = "Chọn kênh"
CHANNEL_ROW = "Kênh {n} · {p}/{cap} người"
CHANNEL_NEW = "Mở kênh mới"
CHANNEL_HINT = "Mỗi kênh là một bản sao của vùng đất, tối đa 40 người."
HP = "Sinh Lực"
QI = "Linh Lực"
WORLD_ACTIONS = {"talk_master": "Nói chuyện", "talk_guide": "Hỏi đường", "gacha": "Thiên Cơ Các",
                 "math_craft": "Lò Toán",
                 "library": "Tàng Thư Các", "shop": "Mua bán", "alchemy": "Lò luyện đan", "forge": "Lò rèn",
                 "quests": "Bảng nhiệm vụ", "td": "Cổng Thủ Thành", "player": "Đạo hữu", "monster": "Mặc Quái",
                 "fisher": "Ngư Ông", "fish_book": "Ngư Phổ", "cloth": "Sạp Vải", "realm": "Cổng Bí Cảnh",
                 "rift": "Khe Nứt Mực", "seal": "Phong Ấn Phù"}
COMING = {
    "cloth": "Sạp vải hôm nay đóng cửa. Bà Chủ Sạp ở Sạp Tạp Hóa bên cạnh có bán đồ Phàm, Linh.",
    "monster": "{name} lườm con một cái rồi lẩn vào sương mực. Vấn Đạo (đánh quái bằng câu đố) sẽ mở ở bản cập nhật tới.",
}
MASTER_VILLAGE = ["Ồ, con xuống làng rồi à? Trúc Lâm Thôn đông vui lắm, đạo hữu khắp nơi kéo về.",
                  "Phía đông là Mê Đồ Lâm, rừng của Thuật Toán. Lối đi ở đó chằng chịt, đừng đi một mình lúc tối nhé.",
                  "Ra cổng Tây là Vạn Tượng Trạch. Lão Ngư Ông câu cá ở Hồ Nghiên Mực trong đầm từ hồi ta còn trẻ.",
                  "Mỗi vùng đất quanh làng luyện một nhánh toán. Lôi Kiếp Đài ở góc tây bắc chỉ mở khi con xong cả Luyện Khí.",
                  "Về động phủ thì nhớ ngồi bàn đả tọa. Bài không ôn là bài bay mất!"]
GUIDE_NAME = "Tiểu Lan"
GUIDE_LINES = ["Chào đạo hữu! Ta là Tiểu Lan, chuyên chỉ đường cho người mới.",
               "Bấm Enter để chat. Thế giới là nói với mọi người, Khu vực thì chỉ người trong kênh này nghe.",
               "Mỗi vùng có nhiều kênh, mỗi kênh tối đa 40 người. Bấm vào tên kênh trên đầu màn hình để đổi.",
               "Cổng phía đông dẫn tới Mê Đồ Lâm, cổng phía tây ra Vạn Tượng Trạch, cổng phía bắc lên Kiếm Trủng Sơn. Đường phía nam đưa con về động phủ.",
               "Cổng đông bắc ra Lưu Vân Cốc. Thiên Công Phường và Linh Xạ Nguyên chỉ mở khi Đạo Thụ của con đủ tầng.",
               "Kết bạn rồi thì nhắn riêng được, lại rủ nhau lập tổ đội (phím Y) cùng vào bí cảnh."]
LIBRARIAN_NAME = "Thủ Thư"
LIBRARIAN_LINES = ["Chào mừng con tới Tàng Thư Các. Ở đây cất kinh thư toán của mọi tầng Đạo Thụ: công thức, "
                   "lời giải mẫu và những chỗ người tu hay vấp.",
                   "Gặp bài nào khó thì tới đây đọc lại kinh thư của tầng ấy. Các phổ của con và kệ đan phương cũng ở đây."]
LIBRARIAN_IDLE = ["Kinh thư không chạy đi đâu, chỉ sợ người đọc vội.",
                  "Đọc một trang kinh thư rồi hẵng luyện, công lực tăng nhanh hơn.",
                  "Một công thức hiểu tận gốc hơn mười công thức học vẹt."]
SIGN_READ = "Biển chỉ đường"

CHAT_TABS = {"all": "Tất cả", "world": "Thế giới", "zone": "Khu vực", "party": "Tổ đội", "friend": "Bạn bè"}
CHAT_PREFIX = {"world": "[TG]", "zone": "[KV]", "party": "[TĐ]", "friend": "[BB]", "system": "[!]"}
CHAT_PLACEHOLDER = "Nhập tin nhắn, Enter để gửi"
CHAT_HINT = "[Enter] chat"
CHAT_NEED_TARGET = "Nhắn riêng: gõ /w Tên-bạn nội dung, hoặc bấm Nhắn trong danh sách bạn bè."
CHAT_TO = "→ {name}"
CHAT_OFFLINE = "Chưa kết nối máy chủ thế giới, chưa chat được."
CHAT_ZONE_ONLY = "Kênh Khu vực chỉ dùng được khi ở ngoài thế giới."

FRIENDS_TITLE = "Đạo hữu"
FRIENDS_TAB = "Bạn bè ({n})"
REQUESTS_TAB = "Lời mời ({n})"
BLOCKED_TAB = "Đã chặn"
FRIEND_ADD_PH = "Đạo hiệu của người muốn kết bạn"
FRIEND_ADD = "Kết bạn"
FRIEND_SENT = "Đã gửi lời mời tới {name}."
FRIEND_NOW = "{name} và con đã là bạn bè!"
FRIEND_ONLINE = "{name} vừa lên mạng"
FRIEND_LEFT = "{name} vừa rời mạng"
FRIEND_REQUEST = "{name} muốn kết bạn (mở Bạn bè để đồng ý)"
ONLINE_IN = "Đang ở {zone}"
OFFLINE_LABEL = "Ngoại tuyến"
MSG = "Nhắn"
REMOVE = "Xóa"
ACCEPT = "Đồng ý"
DECLINE = "Từ chối"
BLOCK = "Chặn"
UNBLOCK = "Bỏ chặn"
REPORT = "Báo cáo"
REMOVE_CONFIRM = "Xóa {name} khỏi danh sách bạn bè?"
BLOCK_CONFIRM = "Chặn {name}? Hai bạn sẽ không còn là bạn bè và con sẽ không thấy tin nhắn của người này nữa."
REPORT_CONFIRM = "Báo cáo {name} vì lời lẽ không phù hợp? Tin nhắn gần nhất của người này sẽ được gửi kèm."
REPORT_DONE = "Đã gửi báo cáo, quản trị viên sẽ xem xét. Cảm ơn con!"
NO_FRIENDS = "Chưa có đạo hữu nào. Gõ đạo hiệu để kết bạn, hoặc bấm vào người chơi khác trong làng."
NO_REQUESTS = "Không có lời mời nào."
NO_BLOCKED = "Chưa chặn ai."
PLAYER_REALM = "Cảnh giới: {realm}"


KICKED_ELSEWHERE = "Tài khoản của con vừa đăng nhập ở máy khác, nên máy này đã thoát ra."
KICKED = "Máy chủ đã ngắt kết nối: {msg}"

# ---------------------------------------------------------------- stage 4: Vấn Đạo and cultivation
TU_VI = "Tu Vi"
HUD_CHAR = "Tu luyện"
HUD_QUESTS = "Nhiệm vụ"
ATTACK_HINT = "[Chuột trái / Space] đánh · [1-6] chiêu thức · [Q] đan"
MONSTER_RANK = {"normal": "", "elite": "Tinh anh", "boss": "Thủ lĩnh"}
HOI_THE = "Hộ Thể"
COMBAT_INTRO = "Mặc Thuẫn chặn đòn! Trả lời đúng để phá khiên."
SHIELD_BROKEN = "Phá Mặc Thuẫn!"
NGO_DAO = "Ngộ Đạo"
MAC_KICH = "Mặc Kích"
SHIELD_BACK = "Mặc Thuẫn hồi lại!"
# the open-world rule (world_plan.json "combat"): a question only when a monster's blow lands
PARRY_INTRO = "Bị đánh trúng thì phải trả lời: đúng là Phản Đòn, sai là trúng đòn. [Shift] để né."
PARRY_HEADER = "{monster} đánh trúng! Đúng để Phản Đòn (đòn: -{dmg})"
PARRY = "Phản Đòn!"
PARRY_RESULT = "Phản Đòn! Không mất máu · quái nhận -{n} và choáng {s} giây · +{qi} Linh Lực"
PARRY_RESULT_GONE = "Phản Đòn! Không mất máu · +{qi} Linh Lực"
GUARD_BREAK = "Trúng đòn"
GUARD_BREAK_RESULT = "Trúng đòn -{n}. Xem lời giải bên trên."
PARRY_REST = "Nghỉ {s} giây: đòn trúng chỉ nửa sát thương, không hỏi"
DODGE_OK = "Né!"
DODGE_LOCKED = "Né Đòn mở ở Luyện Khí tầng 1."
DODGE_HINT = "[Shift] Né Đòn"
# linh thú và thần thông Luyện Khí (Thiên Địa Đồ: thu phục, pháp trận, Đạp Kiếm Lướt, cưỡi linh thú)
BEAST_RANK = "Linh thú"
BEAST_TAME_COUNT = "Phản Đòn {n}/{need}"
BEAST_TAME_PANEL = "Thu phục {name}: Phản Đòn {n}/{need}"
BEAST_YIELDED = "Chịu phục"
BEAST_YIELDED_TOAST = "{name} chịu phục! Đứng gần, bấm E để dùng Phong Ấn Phù."
BEAST_SEAL = "Phong Ấn Phù"
BEAST_SNIFF = "Linh Hồ đánh hơi: {name} ở {way}, cách {d} ô"
BEAST_SNIFF_NONE = "Linh Hồ đánh hơi: quanh đây không còn binh khí nào"
PARRY_FIRE = "Hỏa!"
ABILITY_KEYS = {"phap_tran": "T", "dap_kiem_luot": "G", "cuoi_linh_thu": "R"}
ABILITY_LOCKED = "{name} mở ở Luyện Khí tầng {stage} trên Đạo Thụ."
ABILITY_TIP = "{name} ({key}): {desc}"
ABILITY_DESC = {"phap_tran": "đặt pháp trận dưới chân, quái trong trận ra đòn chậm lại.",
                "dap_kiem_luot": "lướt trên kiếm qua vực và mặt nước theo hướng đang đi.",
                "cuoi_linh_thu": "cưỡi linh thú đang đeo (Tiểu Long) để đi nhanh; bấm lại để xuống."}
GLIDE_NO_LANDING = "Không có chỗ đặt chân trong tầm lướt."
RIDE_NO_MOUNT = "Cần đeo một linh thú cưỡi được (Tiểu Long)."
RIDE_ON = "Cưỡi {name}"
STUNNED = "Choáng"
LOOT_STONES = "+{n} Linh Thạch"
LOOT_XP = "+{n} Tu Vi"
LOOT_ITEM = "Nhận {name} ×{qty}"
LOOT_GEAR = "Nhặt được {name} ({rarity})"
LOOT_LOCKED = "Tu vi chưa đủ: {items}"
LOOT_LOCKED_ONE = "{name} (cần {need})"


def locked_text(locked: list | None) -> str:
    """One short line for the drops a loot payload lists under `locked` (rơi đồ theo tu vi);
    "" when there are none."""
    if not locked:
        return ""
    return LOOT_LOCKED.format(items=", ".join(LOOT_LOCKED_ONE.format(name=x.get("name_vi", ""),
                                                                      need=x.get("need_vi", ""))
                                              for x in locked[:3]))
QUEST_DONE = "Nhiệm vụ hoàn thành: {title} — mở Nhiệm vụ (J) để nhận thưởng"
STAGE_UP = "Đột phá: {label}!"
BOTTLENECK = "Tu Vi đã đầy. Cần {pill} và vượt Thiên Kiếp để vào {realm}."
DEAD_TITLE = "Trọng thương!"
DEAD_TEXT = "Mực tràn vào kinh mạch... Trúc Lão kéo con về làng. Mất một chút Tu Vi, không mất đồ."
XP_LOST = "Mất {n} Tu Vi"
SKILL_FAIL = {"cooldown": "Chiêu đang hồi", "no_qi": "Không đủ Linh Lực", "no_target": "Chưa chọn quái",
              "too_far": "Quá xa", "answering": "Đang trả lời câu hỏi", "not_learned": "Chưa học chiêu này"}

CHAR_TITLE = "Tu luyện"
STATS_VI = {"max_hp": "Sinh Lực", "max_qi": "Linh Lực", "atk": "Công", "def": "Thủ", "crit": "Bạo kích %",
            "ink_res": "Kháng Mực %"}
SKILLS_TITLE = "Chiêu thức"
SKILL_LOCKED = "chưa mở"
BREAKTHROUGH = "Vượt Thiên Kiếp"
NEED_PILL = "Cần {pill}"
TRIB_WAIT = "Thi lại sau {t}"
XP_FULL = "Tu Vi đầy"
GEAR_SLOTS = {"weapon": "Vũ khí", "body": "Áo", "hat": "Mũ", "shoes": "Giày", "jade": "Ngọc Bội", "ring": "Nhẫn"}
NO_WEAPON = "Tay không"

BAG_ITEMS = "Vật phẩm"
BAG_GEAR = "Trang bị"
# Binh khí của Thiên Địa Đồ: tab Binh Khí trong túi đồ
BAG_WEAPONS = "Binh Khí"
WPN_MINE = "Binh khí của con"
WPN_NONE = "Chưa có binh khí nào. Học trên Đạo Thụ rồi đi nhặt ở các vùng đất."
WPN_PLACED = "Rải rác ở các vùng đất"
WPN_LINE = "{type} · bậc {grade} · {quality} · Công {atk}"
WPN_TIP = "{name} · {quality}\n{effect}\nNhánh {branch}.\n{why}"
WPN_STATE = {"available": "Nhặt được", "taken": "Đã nhặt", "locked": "Chưa mở"}
WPN_WHERE = "{land}: {spot}"
WPN_HAND = "Trong tay"
WPN_EQUIPPED = "Đang cầm"
WPN_TU_VI = "Đạo Thụ: {realm} tầng {stage}"
USE = "Dùng"
EQUIP = "Mặc"
UNEQUIP = "Tháo"

FORGE_TITLE = "Lò Rèn · Cường hóa"
FORGE_HINT = "Cường hóa +1 đến +10. Thất bại không mất đồ, chỉ mất nguyên liệu."
FORGE_GO = "Cường hóa"
FORGE_COST = "{p}% · {s} Linh Thạch · {q} {m}"
FORGE_MAX = "Đã tối đa"
FORGE_OK = "Thành công! {name} +{lv}"
FORGE_FAIL = "Thất bại... nguyên liệu tan thành khói, trang bị vẫn còn."
FORGE_EMPTY = "Chưa có trang bị nào. Đánh quái ở các vùng đất quanh làng để nhặt."

QUESTS_TITLE = "Nhiệm vụ"
QUEST_CLAIM = "Nhận thưởng"
QUEST_REWARDS = "Thưởng: {r}"
QUEST_PROGRESS = "{n}/{c}"
QUESTS_NONE = "Đã xong mọi nhiệm vụ chính hiện có. Sắp có thêm!"

MONSTER_BOOK = "Yêu Quái Phổ"
MB_KILLS = "Đã hạ: {n}"
MB_MISTAKE = "Hay sai: {m}"
MB_WEAK = "Điểm yếu: {w}"
MB_DROPS = "Rơi: {d}"
MB_UNKNOWN = "Chưa gặp"

MEDITATE_TITLE = "Đả tọa"
MEDITATE_TEXT = ("Tĩnh tâm, giải một câu toán ở tầng con đang tu. Câu đúng cho Tu Vi theo bậc của câu. "
                 "Không trả lời thì không có Tu Vi.")
MEDITATE_GO = "Ôn một câu"
MEDITATE_WAIT = "Câu tiếp theo sau {t}"

TRIB_TITLE = "Thiên Kiếp"
TRIB_INTRO = ("Thiên Kiếp gồm {n} câu toán khó nhất mà con đã đủ sức giải ở tầng mình đang tu, "
              "mỗi câu có thời gian riêng theo dạng câu. "
              "Đúng từ {p}% thì đột phá. Trượt mất 10% Tu Vi và phải chờ mới thi lại, đan dược không mất.")
TRIB_START = "Bắt đầu"
TRIB_PROGRESS = "Câu {n}/{total} · đúng {c}"
TRIB_PASS = "Vượt kiếp thành công! Nay đã là {label}."
TRIB_FAIL = "Thiên Kiếp chưa qua ({c}/{total}). Mất {xp} Tu Vi, nghỉ ngơi rồi thử lại."
TRIB_REWARD = "+{n} Tiên Ngọc"
MASTER_QUEST_LINES = ["Đến rồi à? Cây bút này ta dùng hồi trẻ. Mực của nó phá được Mặc Thuẫn... à không, là lời giải của con phá chứ!",
                      "Nhớ: đánh thường chỉ làm xước khiên. Muốn phá Mặc Thuẫn thì phải trả lời đúng."]

# ---------------------------------------------------------------- stage 5: Linh Phong
HUD_HIVE = "Tổ ong"
HIVE_TITLE = "Linh Phong Sào"
HIVE_LEVEL = "Tổ cấp {lv}/{mx}"
HIVE_HONEY = "Linh Mật {h}/{cap}"
HIVE_RATE = "{r}/giờ"
HIVE_WAX = "Sáp Ong {w}"
HIVE_COLLECT = "Thu mật"
HIVE_COLLECTED = "Thu được {h} Linh Mật, {w} Sáp Ong"
HIVE_UPGRADE = "Nâng cấp tổ"
HIVE_UPGRADE_COST = "Cấp {lv}: {s} Linh Thạch, {items}. Mật đầy tới {cap}, làm mật ×{m}. Mở: {deco}"
HIVE_UPGRADED = "Tổ ong lên cấp {lv}!"
HIVE_MAX = "Tổ đã nâng cấp tối đa"
HIVE_UNLOCK = "Mở ô ({s})"
HIVE_UNLOCK_TIP = "Mở thêm ô thứ {n} cho tổ ong: {s} Linh Thạch"
HIVE_UNLOCK_NEED = "Ô thứ {n} cần phát hiện {k} loài trong Ong Phổ (đang có {f})"
HIVE_CELLS = "Ô tổ: {n}/{mx}"
HIVE_LOCKED_CELL = "Ô chưa mở"
HIVE_PICK = "Bấm vào một con ong để xem. Kéo thả (hoặc bấm ong rồi bấm ô) để đổi chỗ."
HIVE_NO_BEES = "Tổ còn trống. Ấp một quả trứng ong để bắt đầu!"
HIVE_EGGS = "Trứng ong"
HIVE_HATCH = "Ấp"
HIVE_NEW_SPECIES = "Loài mới! Đã ghi vào Ong Phổ."
HIVE_HATCHED = "{name} vừa nở!"
HIVE_GUARDS = "Hộ vệ {n}/{mx}"
HIVE_INTRO = ["Linh Phong Sào đây! Ong linh nở từ trứng, mỗi con một ô trong tổ.",
              "Để ong ở tổ thì chúng làm Linh Mật và Sáp Ong. Tổ đầy mật thì bấm Thu mật mà lấy về túi.",
              "Từ Luyện Khí, vài con có thể làm Hộ vệ, bay theo con ra ngoài và đánh những con quái đã bị con phá "
              "Mặc Thuẫn. Cho ăn đúng món chúng thích thì chúng quý con hơn."]
BEE_ROLE = {"hive": "Ở tổ", "guard": "Hộ vệ"}
BEE_ROLE_TIP = {"hive": "Làm Linh Mật và Sáp Ong trong tổ",
                "guard": "Bay theo con ra thế giới, đánh quái đã mất Mặc Thuẫn"}
BEE_LEVEL = "Cấp {lv}"
BEE_XP = "Kinh nghiệm {x}/{n}"
BEE_XP_MAX = "Cấp tối đa"
BEE_BOND = "Thân thiết {b}/{mx}"
BEE_STATS = "Mật {h}/giờ · Sinh Lực {hp} · Công {atk}"
BEE_RESONANCE = "Đồng hệ cộng hưởng +{p}%"
BEE_FAV = "Món thích: {f}"
BEE_FAV_HINT = "Món thích: ??? — {h}"
BEE_FEED = "Cho ăn"
BEE_FEED_TITLE = "Cho {name} ăn gì?"
BEE_NO_FOOD = "Chưa có gì cho ong ăn. Thu Linh Mật ở tổ, câu cá, hoặc mua dược thảo ở Sạp Tạp Hóa."
BEE_FED = "+{xp} kinh nghiệm"
BEE_FED_FAV = "Món nó thích! +{xp} kinh nghiệm, thân thiết +{b}"
BEE_FAV_FOUND = "Phát hiện món {name} thích: {food}"
BEE_LEVEL_UP = "{name} lên cấp {lv}!"
BEE_RELEASE = "Thả ong"
BEE_RELEASE_CONFIRM = "Thả {name} (cấp {lv}) về rừng? Con nhận lại {wax} Sáp Ong. Không thể hoàn tác."
BEE_RELEASED = "Đã thả ong về rừng: +{w} Sáp Ong"
BEE_DOWN = "{name} bị thương, bay về tổ nghỉ 60 giây"
BEE_STUN = "choáng"
BEE_HUD_TIP = "{name} · Sinh Lực {hp}/{mx}"
BEE_HUD_DOWN = "{name} đang nghỉ trong tổ ({t} giây)"

BEE_BOOK = "Ong Phổ"
BEE_BOOK_FOUND = "Đã phát hiện {f}/{t} loài"
BEE_BOOK_HATCHED = "Đã nở: {n} · Cấp cao nhất: {lv} · Đang nuôi: {o}"
BEE_BOOK_UNKNOWN = "Chưa phát hiện"
BEE_BOOK_STATS = "Gốc: mật {h}/giờ · Sinh Lực {hp} · Công {atk}"
BEE_MILESTONE_GOT = "Mốc Ong Phổ {n} loài: nhận {r}"

STARTER_EGG_HINT = "Trúc Lão để lại một quả Trứng Ong trong túi con. Bấm H để mở Linh Phong Sào."

GACHA_TAB_BEES = "Trứng Ong"
GACHA_BEES_TITLE = "Thiên Cơ Các · Trứng Ong"
GACHA_BEE_RATES = "Tỉ lệ: Phàm 60% · Linh 27% · Huyền 9% · Địa 3% · Thiên 1%"
GACHA_BEE_PITY = "Bảo hiểm: lượt thứ 30 chắc chắn Huyền trở lên, lượt thứ 90 chắc chắn Thiên. 10 lượt có ít nhất 1 trứng Linh."
GACHA_BEE_PITY_NOW = "Đã quay {h}/30 lượt chưa có Huyền, {t}/90 lượt chưa có Thiên"
GACHA_BEE_EFFECTIVE = "Tỉ lệ thực tế khi tính bảo hiểm: Thiên ≈ {t}%, Huyền trở lên ≈ {h}%"
GACHA_BEE_DONE = "Trứng đã vào túi. Mang đến Linh Phong Sào trong động phủ để ấp!"
JADE = "Tiên Ngọc"
SELL_ITEM = "Bán ({p})"
EGG_HINT = "Ấp ở tổ ong"


# ---------------------------------------------------------------- stage 6: câu cá (spec 11)
RARITY_NAMES = {"pham": "Phàm", "linh": "Linh", "huyen": "Huyền", "dia": "Địa", "thien": "Thiên"}
RARITY_COLORS = {"pham": "#7D7468", "linh": "#6A994E", "huyen": "#4A7CC8", "dia": "#8E5AC8", "thien": "#C99A3A"}
PRESS_F = "[F] Câu cá"
FISH_CASTING = "Quăng câu..."
FISH_WAITING = "Chờ cá cắn... Phao chìm thì bấm F / Space để giật!"
FISH_BITE = "Cá cắn! Giật ngay!"
FISH_EARLY = "Giật sớm quá, cá hoảng bơi mất rồi."
FISH_LATE = "Chậm tay quá, cá ăn mất mồi rồi."
FISH_REEL_HINT = "Giữ chuột (hoặc Space) để kéo, nhả để thả dây. Giữ móc câu trong vùng xanh!"
FISH_QUIZ_HINT = "Cá {r} cắn câu! Trả lời đúng thì vùng xanh rộng hơn (sai cũng không mất máu)."
FISH_QUIZ_TWO = "Cá Thiên: phải đúng 2 câu liên tiếp ({n}/2)."
FISH_ZONE_WIDE = "Đúng rồi! Vùng xanh rộng ra."
FISH_ZONE_NARROW = "Sai mất rồi, vùng xanh hẹp lại. Cố lên!"
FISH_CAUGHT = "Câu được rồi!"
FISH_ESCAPED = "Cá giãy tuột mất rồi..."
FISH_SNAPPED = "Phựt! Dây căng quá nên đứt."
FISH_STRAIN = "Dây"
FISH_PROGRESS = "Bắt"
FISH_CANCEL = "Thu cần (Esc)"
FISH_NEW = "Loài mới trong Ngư Phổ!"
FISH_RECORD = "Kỷ lục của con!"
FISH_SERVER_RECORD = "KỶ LỤC TOÀN MÁY CHỦ!"
FISH_SMALL = "Con này nhỏ quá, thành Cá Nhỏ (ong ăn được)."
FISH_SIZE = "Dài {cm} cm"
FISH_GOT = "Nhận: {items}"
FISH_MILESTONE = "Mốc Ngư Phổ {n} loài: {r}"
FISH_FICTIONAL = "(cá do Ngư Ông tưởng tượng ra)"
FISH_MYTHICAL = "(cá trong truyền thuyết)"
FISH_CONDITIONS = "{zone} · {time} · {weather}"
FISH_DAY, FISH_NIGHT, FISH_RAIN, FISH_CLEAR = "ban ngày", "ban đêm", "trời mưa", "trời quang"
FISH_NO_BAIT = "không mồi"
SHOP_FISH_TITLE = "Ngư Ông · Cần câu & Mồi"
SHOP_FISH_HINT = "Câu không mồi chỉ ra cá Phàm và Linh. Mồi tốt dụ được cá hiếm."
SHOP_RODS = "Cần câu"
SHOP_BAITS = "Mồi câu"
SHOP_USE = "Dùng"
SHOP_IN_USE = "Đang dùng"
SHOP_BUY10 = "Mua 10 ({p})"
SHOP_CRAFT = "Làm ({n} {src} → {m})"
SHOP_NOT_SOLD = "Không bán"
ROD_STATS = "Kéo ×{pull} · Dây ×{line} · May +{luck} · Cắn nhanh {bite}% · Vùng +{zone}%"
ROD_LEVEL = "cấp {lv}"
ROD_PRICE = "{s} Linh Thạch"
ROD_PRICE_SCALES = "{s} Linh Thạch + {v} Vảy"
ROD_PRICE_SILK = " + {n} Thiên Tằm Ti"
ROD_NEED_REALM = "Cần {realm}"
ROD_FORGE = "Cần câu"
ROD_FORGE_TITLE = "Lò Rèn · Nâng cấp cần câu"
ROD_FORGE_HINT = "Mỗi cấp tăng lực kéo, độ bền dây và may mắn. Vảy Linh Ngư có từ cá Linh trở lên."
ROD_UPGRADE = "Nâng cấp ({s} LT, {v} Vảy)"
ROD_MAX = "Cấp tối đa"
ROD_UPGRADED = "{name} lên {lv}!"
SCALES_HAVE = "Vảy Linh Ngư: {n}"
FISH_BOOK = "Ngư Phổ"
FISH_BOOK_TITLE = "Tàng Thư Các · Ngư Phổ"
FISH_BOOK_FOUND = "Đã câu {f}/{t} loài"
FISH_BOOK_RECORDS = "Kỷ lục"
FISH_BOOK_SPECIES = "Các loài"
FISH_BOOK_ENTRY = "Đã câu {n} con · to nhất {cm} cm"
FISH_BOOK_HINT_UNKNOWN = "Chưa câu được. Gợi ý: {hint}"
FISH_RECORDS_EMPTY = "Chưa ai câu được con nào. Con sẽ là người đầu tiên!"
FISHER_NAME = "Ngư Ông"
FISHER_LINES = ["Hồ này tên là Nghiên Mực, vì đêm đêm Mực Nang phun mực đen cả mặt nước.",
                "Đứng sát mép nước hoặc ra cuối bến gỗ, bấm F để quăng câu. Phao chìm thì giật ngay!",
                "Cá hiếm cắn câu sẽ hỏi con một câu. Trả lời đúng thì dễ kéo hơn. Sai cũng chẳng sao, câu cá là để thư thả.",
                "Mỗi loài có giờ của nó: cá này thích đêm, cá kia đợi mưa, có con chỉ đớp đúng một loại mồi."]
FISHER_IDLE = ["Hôm nay nước lặng, cá ăn mồi đều tay.",
               "Nghe nói đêm mưa có con cá chép mọc sừng. Lão đợi nó bốn mươi năm rồi...",
               "Giun Đất thì lão bán, còn Bánh Mật phải có Linh Mật mới làm được."]

# ---------------------------------------------------------------- Thủ Thành Toán: bàn cờ chung (giai đoạn 7, M10)
TD_GATE_LINES = ["Mặc Quái đang kéo về từ cổng mực, nhắm thẳng vào Linh Mạch của thôn!",
                 "Mỗi tòa tháp giữ thành là một mảng toán. Muốn dựng hay nâng tháp nào thì phải trả lời đúng một câu "
                 "của mảng ấy; tầng con đã tới trên Đạo Thụ càng cao, càng nhiều loại tháp.",
                 "Dựng tháp tốn Linh Khí. Giữa các đợt có câu Linh Khí Vấn Đạo, trong đợt bấm Tụ Khí để hỏi thêm."]
TD_MONSTERS = "Quái trong ải"
TD_FIRST_REWARDS = "Thưởng lần đầu: 1 sao {a} · 2 sao {b} · 3 sao {c}"
TD_DAILY = "Lượt nhận thưởng chơi lại hôm nay: {n}/{m}"
TD_START = "Vào ải"
TD_RESUME = "Chơi tiếp"
TD_DROP_RUN = "Bỏ lượt"
TD_RESUME_TEXT = "Lượt dở ở {name} (đã tới đợt {n}). Vào ải khác thì lượt này bị bỏ."
TD_WAVE = "Đợt {n}/{t}"
TD_CORE = "Linh Mạch {n}/{m}"
TD_QI = "Linh Khí {n}"
TD_START_WAVE = "Bắt đầu đợt"
TD_TU_KHI = "Tụ Khí"
TD_TU_KHI_WAIT = "Tụ Khí ({n}s)"
TD_SPEED = "Tốc độ ×{n}"
TD_LEAVE = "Rời ải"
TD_LEAVE_CONFIRM = "Rời ải bây giờ thì lượt này bỏ dở, không có thưởng. Rời thật chứ?"
TD_UPGRADE = "Nâng cấp ({c})"
TD_UPGRADE_MAX = "Cấp tối đa"
TD_LEVEL = "Cấp {n}"
TD_ON_PATH = "Tháp chặn đường dựng ngay trên đường để chặn quái."
TD_OFF_PATH = "Tháp này dựng cạnh đường, không dựng trên đường."
TD_NO_QI = "Không đủ Linh Khí."
TD_CANT_PLACE = "Không dựng được ở đây."
TD_STATS_DMG = "Sát thương {d} · tầm {r} ô · {cd}s/lần"
TD_STATS_MOC = "Máu {hp} · gai {t}/giây"
TD_STATS_QI = "+{q} Linh Khí mỗi {cd}s"
TD_STATS_SUPPORT = "Tháp kề bên: bắn nhanh +{h}%, tháp chặn đường hồi {hl} máu/giây"
TD_MONSTER_HP = "Máu {hp} · tốc {sp} · lọt vào mất {lk} điểm"
TD_CHECKING = "Đang gửi nhật ký ải cho máy chủ kiểm tra..."
TD_WON = "Giữ vững Linh Mạch!"
TD_LOST = "Linh Mạch thất thủ..."
TD_RESULT_STARS = "Linh Mạch còn {hp}/{m} điểm"
TD_RESULT_REWARDS = "Nhận: {r}"
TD_RESULT_REPLAY = "(thưởng chơi lại, còn {n} lượt hôm nay)"
TD_RESULT_NO_REWARD = "Không có thưởng lần này."
TD_RESULT_NEXT = "Ải tiếp"
TD_RESULT_RETRY = "Chơi lại"
TD_RESULT_MAP = "Về bản đồ ải"
TD_ROLE_COLORS = {"hoa": "#E07A3F", "thuy": "#4A90C8", "moc": "#6A994E", "son": "#9C7B4E", "kim": "#C99A3A",
                  "quang": "#E9C46A", "sinh_khi": "#8DB360", "ho_tro": "#E89AB0", "thanh_ngu": "#8E5AC8"}

# ---------------------------------------------------------------- Tàng Thư Các: kệ các phổ
BOOKS_TITLE = "Tàng Thư Các · Kệ Phổ"
BOOKS_HINT = "Các phổ của con. Mỗi mốc 25/50/75/100% có quà."
BOOKS_SCROLLS = "Kinh thư toán"
LIBRARY_OPEN = "Mở"
LIBRARY_CLAIMED = "Đã nhận"
LIBRARY_BOOK_ROW = "{f}/{t} · {p}%"
LIBRARY_GOT = "Nhận thưởng mốc {p}% {book}: {r}"
LIBRARY_NONE = "Không"
LIBRARY_TITLE_PICK = "Danh hiệu:"
LIBRARY_FRAME_PICK = "Khung:"
LIBRARY_SHOP = "Đan phương"
LIBRARY_SHOP_TITLE = "Tàng Thư Các · Kệ đan phương"
LIBRARY_SHOP_HINT_RECIPES = ("Đan phương giữ trong túi là luyện được mãi ở Đan Lô (động phủ) hoặc lò của Đan Sư. "
                             "Mỗi loại chỉ cần mua một lần.")
LIBRARY_SHOP_OWNED = "Đã có"
LIBRARY_SHOP_FAR = "Thủ Thư đang ở Tàng Thư Các trong làng. Tới gặp bà ấy để mua."
LIBRARY_SHOP_BUY = "Mua ({p} LT)"
LIBRARY_BOUGHT = "Đã mua {name}. Đan phương nằm trong Túi đồ."
TREASURE_TITLE = "Tàng Thư Các · Bảo Vật Phổ"
TREASURE_FOUND = "Đã có {f}/{t} bảo vật"
TREASURE_UNKNOWN = "Chưa từng có"
FRAME_COLORS = {"khung_muc": "#2B2B2B", "khung_song": "#4A90C8", "khung_vang": "#E9C46A", "khung_giap": "#BC4749"}


# ---------------------------------------------------------------- stage 8: luyện đan, Linh Thú, kinh tế
HUD_PETS = "Linh Thú"
ALCHEMIST_NAME = "Đan Sư"
ALCHEMIST_LINES = ["Lại đây, lại đây! Lò của lão vừa đỏ lửa.",
                   "Luyện đan cốt ở canh lửa: kim chạy qua lại, con bấm đúng lúc kim vào vùng văn hỏa, ba lần.",
                   "Bấm càng sát giữa vùng văn hỏa thì đan ra càng tốt. Lệch ra ngoài thì lửa hỏng, đan kém đi.",
                   "Đây, cầm lấy đan phương Hồi Huyết Đan. Đan phương giữ trong túi là luyện được mãi."]
ALCHEMIST_IDLE = ["Lửa vũ thì cháy đan, lửa văn mới thành đan. Từ từ thôi con.",
                  "Lò trong động phủ con nâng cấp được, vùng văn hỏa sẽ rộng ra.",
                  "Thiếu Trúc Diệp Thảo thì ghé Sạp Tạp Hóa, Bà Chủ Sạp có bán."]
ALCHEMY_TITLE = "Luyện Đan"
ALCHEMY_HOME = "Đan Lô trong động phủ · {name} (cấp {lv})"
ALCHEMY_PUBLIC = "Lò công cộng của Đan Sư (cấp 1)"
ALCHEMY_FAR = "Hãy đứng cạnh một lò luyện đan để luyện."
ALCHEMY_FEE = "Phí lò {n} LT"
ALCHEMY_YIELD = "Ra: hạ {h} · trung {m} · thượng {t} viên"
ALCHEMY_BREW = "Nhóm lửa"
ALCHEMY_RESUME = "Luyện tiếp"
ALCHEMY_UNKNOWN = "Chưa có đan phương"
ALCHEMY_SOURCES = "Tìm ở: {s}"
ALCHEMY_REALM = "Cần {r}"
ALCHEMY_HAVE = "Đang có {n} viên"
ALCHEMY_UPGRADE = "Nâng lò ({p} LT)"
ALCHEMY_UPGRADE_NEED = "Lên {name}: {m}"
ALCHEMY_UPGRADED = "Lò đã thành {name}!"
ALCHEMY_BUFFS = "Đang có: {b}"
FIRE_TITLE = "Canh lửa · {name}"
FIRE_HINT = "Bấm Space (hoặc chuột) khi kim vào vùng văn hỏa. Giữa vùng sáng là đẹp nhất."
FIRE_PRESS = "Lần {n}/{t}"
FIRE_NEXT = "Tiếp"
FIRE_HITS = {"perfect": "Văn hỏa tuyệt hảo!", "good": "Văn hỏa", "miss": "Lửa lệch rồi"}
FIRE_SENDING = "Mở nắp lò..."
FIRE_RESULT = "{q}: {n} viên {name}"
FIRE_RESULT_NONE = "Phế đan... nguyên liệu cháy thành tro."
FIRE_EXTRA = "Lò tốt cho thêm 1 viên!"
FIRE_DONE = "Xong"
SHOP_TITLE = "Sạp Tạp Hóa · Bà Chủ Sạp"
SHOP_NAME = "Bà Chủ Sạp"
SHOP_LINES = ["Mua gì cứ chọn, sạp có đan dược, dược thảo, Mực Tinh, cả mồi câu.",
              "Mỗi thứ một ngày ta chỉ bán cho mỗi người một ít thôi, để ai cũng có phần.",
              "Đồ dư thì mang lại đây, ta mua lại. Rẻ thôi, nhưng không để con thiệt."]
SHOP_TAB_BUY = "Hàng ngày"
SHOP_TAB_GEAR = "Trang bị"
SHOP_TAB_SELL = "Bán lại"
SHOP_LEFT = "còn {n}/{d} hôm nay"
SHOP_BUY = "Mua ({p})"
SHOP_BUY5 = "×5"
SHOP_BOUGHT = "Đã mua {name} ×{n}"
SHOP_FAR = "Bà Chủ Sạp đang ở Sạp Tạp Hóa trong Trúc Lâm Thôn. Tới gặp bà để mua."
SHOP_SELL = "Bán ({p})"
SHOP_SOLD = "Đã bán: +{n} Linh Thạch"
SHOP_NOTHING = "Không có gì để bán."
SHOP_GEAR_BUY = "Mua ({p} LT)"
PETS_TITLE = "Linh Thú"
PETS_HINT = "Đeo một linh thú: nó đi theo con, thêm chút chỉ số và một kỹ năng. Quay ở Thiên Cơ Các."
PETS_NONE = "Chưa có linh thú nào. Ghé Thiên Cơ Các (tab Linh Thú) để quay."
PETS_WEAR = "Đeo"
PETS_WORN = "Đang đeo"
PETS_TAKE_OFF = "Tháo"
PETS_LEVEL = "Cấp {l}/{m}"
PETS_BOOK = "Linh Thú Phổ"
PETS_BOOK_TITLE = "Tàng Thư Các · Linh Thú Phổ"
PETS_FOUND = "Đã gặp {f}/{t} linh thú"
PETS_UNKNOWN = "Chưa gặp"
PETS_EQUIPPED = "{name} đã theo con."
PETS_TAMED = "Đã thu phục"
PETS_TAMED_FROM = "Linh thú"
PETS_PAGE = "Trang {a}/{b}"
GACHA_TAB_PETS = "Linh Thú"
GACHA_PET_TITLE = "Thiên Cơ Các · Linh Thú"
GACHA_PET_RATES = "Tỉ lệ: Thường 55% · Hiếm 30% · Quý 12% · Huyền thoại 3%. 12 con giáp, mỗi con một kỹ năng."
GACHA_PET_PITY = "Bảo hiểm: 20 lượt chắc chắn có Quý, 60 lượt chắc chắn có Huyền thoại. 10 lượt có ít nhất 1 Hiếm."
GACHA_PET_PITY_NOW = "Đã quay chưa ra: Quý {e}/20 · Huyền thoại {l}/60"
GACHA_PET_DONE = "Linh thú đã về. Mở bảng Linh Thú (phím O) để đeo!"
GACHA_PET_NEW = "Mới!"
GACHA_PET_LEVEL = "Lên cấp {l}"
GACHA_PET_STONES = "+{n} LT"
QUESTS_TAB_MAIN = "Cốt truyện"
QUESTS_TAB_DAILY = "Hằng ngày"
QUESTS_DAILY_BONUS = "Xong cả hôm nay: {r}"
QUESTS_DAILY_BONUS_GOT = "Đã nhận quà xong cả ngày."
QUEST_BONUS = "Xong hết việc hôm nay! +{r}"
GIFT_BUTTON = "Tặng quà"
GIFT_TITLE = "Tặng quà cho {name}"
GIFT_HINT = "Đồ không ràng buộc, tối đa 5 cái mỗi lần, 5 lần mỗi ngày."
GIFT_GIVE = "Tặng {n}"
GIFT_SENT = "Đã tặng {name} ×{n}"
GIFT_GOT = "{name} tặng con {item} ×{n}"
GIFT_NONE = "Không có gì tặng được."

# ---- stage 9: tổ đội and bí cảnh
PARTY_TITLE = "Tổ đội"
PARTY_NONE = "Bạn chưa ở trong tổ đội nào. Mời đạo hữu bằng đạo hiệu, hoặc bấm vào người chơi khác rồi chọn Mời vào tổ đội."
PARTY_INVITE_PH = "Đạo hiệu người muốn mời"
PARTY_INVITE = "Mời vào tổ đội"
PARTY_INVITE_BTN = "Mời"
PARTY_INVITED = "Đã gửi lời mời tới {name}."
PARTY_INVITE_FROM = "{name} ({realm}) mời con vào tổ đội."
PARTY_INVITE_TOAST = "{name} mời con vào tổ đội (phím Y)"
PARTY_ACCEPT = "Vào đội"
PARTY_DECLINE = "Từ chối"
PARTY_DECLINED = "{name} đã từ chối lời mời."
PARTY_LEAVE = "Rời đội"
PARTY_KICK = "Mời ra"
PARTY_PROMOTE = "Nhường trưởng"
PARTY_LEADER = "Đội trưởng"
PARTY_OFFLINE = "ngoại tuyến"
PARTY_LEFT = {"leave": "Con đã rời tổ đội.", "kicked": "Đội trưởng đã mời con ra khỏi đội.",
              "disbanded": "Tổ đội đã giải tán.", "offline": "Con rời đội vì ngoại tuyến quá lâu."}
PARTY_PENDING = "Lời mời đang chờ"
PARTY_HINT = "Tối đa 5 người. Cùng đội thì thấy máu nhau, đánh quái gần nhau được chia Tu Vi, chat kênh Tổ Đội (/d)."
HUD_PARTY = "Đội"
NOTICE = "[Thông báo] {text}"
REALM_GATE_TITLE = "Cổng Bí Cảnh"
REALM_RIFT_TITLE = "Khe Nứt Mực"
REALM_TAB_REALMS = "Bí cảnh"
REALM_TAB_FORGE = "Ghép Bảo Vật"
REALM_OPEN = "Đang mở · còn {m} phút"
REALM_OPEN_ALWAYS = "Đang mở"
REALM_CLOSED = "Mở sau {t}"
REALM_RIFT_ONLY = "Chỉ vào được qua Khe Nứt Mực xuất hiện ngẫu nhiên ở Mê Đồ Lâm, Vạn Tượng Trạch."
REALM_INFO = "{p} gian trận nhãn rồi boss · {m} phút · tổ đội {n}-5 người"
REALM_ENTRIES = "Lượt hôm nay: {n}/{d}"
REALM_ENTER = "Vào cùng tổ đội"
REALM_QUEUE = "Hàng chờ ghép đội"
REALM_UNQUEUE = "Rời hàng chờ"
REALM_QUEUED = "Đang chờ ghép đội · {n} người"
REALM_NEED_LEADER = "Đội trưởng dẫn đội vào (2-5 người)."
REALM_ENTERING = "Đang mở cửa vào {name}..."
REALM_PARTY = "Tổ đội: {names}"
REALM_ROOM = "{name} · Phòng {i}/{n}: {room}"
REALM_TIME = "{m:02d}:{s:02d}"
REALM_LEAVE = "Rời bí cảnh"
REALM_LEAVE_CONFIRM = "Rời bí cảnh bây giờ? Con giữ phần thưởng các phòng đã qua, nhưng không nhận rương cuối và mất lượt vào hôm nay."
REALM_CLEARED = "Cửa đã mở! Sang phòng sau trong {n} giây."
REALM_GHOST = "Con đã thành hồn ma. Đi theo đội, qua phòng sau sẽ được hồi sinh."
REALM_REVIVED = "Hồi sinh! Sinh Lực {hp}."
REALM_MEMBER_LEFT = {"left": "{name} đã rời bí cảnh.", "disconnected": "{name} mất kết nối quá lâu, đã rời bí cảnh."}
REALM_RESULT = {"won": "Vượt bí cảnh!", "failed": "Cả đội gục ngã...", "timeout": "Hết giờ!", "abandoned": "Đã rời bí cảnh"}
REALM_RESULT_INFO = "Thời gian {m:02d}:{s:02d} · Gian không sai câu nào: {f}/{p}"
REALM_FAST = "Nhanh như gió: thêm Linh Thạch và một lần mở rương!"
REALM_FRAGMENTS = "Mảnh Bảo Vật chung cả đội: {n}"
REALM_YOUR_LOOT = "Phần thưởng của con"
REALM_LOOT_STONES = "{n} Linh Thạch"
REALM_LOOT_JADE = "{n} Tiên Ngọc"
REALM_BACK = "Về Trúc Lâm Thôn ({n})"
REALM_ROOM_LOOT = "Phòng {i}: +{n} Linh Thạch"
REALM_YOUR = "Của con"
REALM_BOSS_PHASE = "Nghiên Ma · pha {p}/4"
REALM_BOSS_SHIELD = "Mặc Thuẫn lớn: {n}/{need} người đã trả lời đúng"
REALM_BOSS_OPEN = "Khiên vỡ! Đánh đi!"
REALM_FAILS = "Sai: {n}"
REALM_RIFT_ENTER = "Vào khe nứt cùng tổ đội"
REALM_RIFT_QUEUE = "Chờ người cùng vào"
REALM_RIFT_LEFT = "Khép lại sau {t}"
REALM_FORGE_HAVE = "Mảnh Bảo Vật: {have}/{need} · {stones} Linh Thạch mỗi món"
REALM_FORGE_HINT = "Ghép đủ Mảnh Bảo Vật thành một món {set} phẩm {rarity}."
REALM_FORGE_BONUS = "Thưởng bộ: 2 món {b2} · 4 món {b4}"
REALM_FORGE_BTN = "Ghép"
REALM_FORGE_DONE = "Ghép xong {name} phẩm {rarity}!"
REALM_NEED_PARTY = "Cần tổ đội 2-5 người (phím Y), hoặc vào hàng chờ."

# ---------------------------------------------------------------- LAN worlds (Minecraft style) + Firebase accounts
FB_TITLE = "Tài khoản Toán Tu Tiên"
FB_EMAIL = "Email"
FB_NEED_EMAIL = "Hãy nhập email."
FB_NEED_PASSWORD = "Hãy nhập mật khẩu."
FB_SEND_RESET = "Gửi email"
FB_RESET_HINT = "Nhập email đã đăng ký: Firebase sẽ gửi thư có đường dẫn để đặt mật khẩu mới."
FB_RESET_SENT = "Đã gửi thư đặt lại mật khẩu tới {email}. Xem cả mục Spam nhé."
FB_NOTE = "Tài khoản dùng chung cho mọi thế giới · cần Internet khi đăng nhập"
FB_NOT_SIGNED_IN = "chưa đăng nhập"
FB_SIGN_OUT = "Đăng xuất"
WORLD_TAB_MINE = "Thế giới của tôi"
WORLD_TAB_LAN = "Tham gia mạng LAN"
WORLD_NONE = "Chưa có thế giới nào. Đặt tên rồi bấm Tạo — thế giới được lưu ngay trên máy này."
WORLD_ROW = "{when} · {kb} KB"
WORLD_NEW_PLACEHOLDER = "Tên thế giới mới"
WORLD_CREATE = "Tạo"
WORLD_FOLDER = "Mở thư mục"
WORLD_OPEN = "Mở thế giới"
WORLD_NEED_NAME = "Hãy đặt tên cho thế giới."
WORLD_CREATED = "Đã tạo thế giới «{name}». Bấm Mở thế giới để vào."
WORLD_OPENING = "Đang mở «{name}»... (lần đầu mất khoảng nửa phút; Windows hỏi tường lửa thì bấm Allow)"
WORLD_JOINING = "Đang vào thế giới..."
WORLD_HOST_FAILED = "Không mở được thế giới: {err}"
WORLD_HOST_DIED = "Máy chủ của thế giới đã dừng. {log}"
WORLD_HOST_SLOW = "Thế giới mở quá lâu. Thử lại, hoặc xem server.log trong thư mục thế giới."
WORLD_UNREACHABLE = "Không kết nối được {url}. Kiểm tra cùng mạng LAN và tường lửa của máy mở thế giới."
WORLD_OTHER_VERSION = "Thế giới này chạy phiên bản game khác (v{v}). Hai máy cần cùng bản game."
WORLD_NOT_LAN = "Địa chỉ này là máy chủ riêng, không phải thế giới LAN."
WORLD_SESSION_ENDED = "Phiên chơi đã kết thúc, hãy vào lại thế giới."
WORLD_HOSTING = "Thế giới «{name}» đang mở cho mạng LAN. Bạn bè cùng mạng vào mục Tham gia, hoặc gõ: {addrs}"
WORLD_LAN_ADDR = "Bạn bè cùng mạng LAN vào bằng địa chỉ:"
WORLD_PLAYING_ON = "Đang chơi ở thế giới {url}"
WORLD_LEAVE = "Rời thế giới"
WORLD_SIGNED_IN = "Tài khoản: {email}"
LAN_SEARCHING = "Đang tìm thế giới trong mạng LAN"
LAN_HINT = "Người mở thế giới bấm Mở thế giới ở máy họ. Không thấy? Cho game qua tường lửa, hoặc gõ địa chỉ họ thấy trong Cài đặt (vd 192.168.1.5:8000)."
LAN_LISTEN_FAILED = "Không nghe được mạng LAN ({err}). Vẫn gõ địa chỉ được."
LAN_ROW = "{n} người · {addr}"
LAN_ADDR_PLACEHOLDER = "Địa chỉ, vd 192.168.1.5:8000"
LAN_CONNECT = "Kết nối"
LAN_JOIN = "Tham gia"

# ---------------------------------------------------------------- math question loop (M2)
HUD_MATH = "Toán"
MATH_TITLE = "Bí Cảnh Toán"
MATH_LOADING = "Đang mở bí cảnh..."
MATH_FLOOR = "Tầng {n}"
MATH_TIERS = "Bậc {lo}-{hi}"
MATH_TIER_ONE = "Bậc {lo}"
MATH_PLAY = "Luyện"
MATH_RESUME = "Luyện tiếp"
MATH_TIER_LABEL = "Bậc {n} · {name}"
MATH_SECONDS = "{n} giây"
MATH_TRUE = "Đúng"
MATH_FALSE = "Sai"
MATH_NUMBER_HINT = "Phân số viết a/b, số thập phân dùng dấu chấm, nhiều số cách nhau bằng dấu phẩy"
MATH_NUMBER_PLACEHOLDER = "vd 3/4 hoặc 1, 2, 3"
MATH_YOUR_ANSWER = "Bạn trả lời: {a}"
MATH_SOLUTION = "Lời giải từng bước"
MATH_XP = "Tu Vi +{n}"
MATH_TIER_UP = "Lên bậc {name}"
MATH_TIER_DOWN = "Xuống bậc {name}"
MATH_COMBO = "Chuỗi đúng: {n}"
MATH_SCORE = "Đúng {c}/{a}"
MATH_NEXT = "Câu tiếp"
MATH_STOP = "Nghỉ"
MATH_SUMMARY = "Kết thúc buổi luyện"
MATH_SUMMARY_SCORE = "Trả lời đúng {c}/{a} câu"
MATH_SUMMARY_COMBO = "Chuỗi đúng dài nhất: {n}"
MATH_SUMMARY_XP = "Tu Vi nhận được: {n}"
MATH_SUMMARY_TIER = "Bậc đang luyện: {name}"
MATH_BACK = "Chọn nút"
MATH_PARALLEL = "Tâm ma: ý vừa sai quay lại với số mới"
MATH_WILL_RETURN = "Ý này sẽ quay lại"
MATH_PARALLEL_CLEARED = "Đã phá tâm ma"

# Cổng thuần thục, Thiên kiếp nhỏ và ôn xoắn ốc (M5)
MATH_LOCKED = "Chưa mở"
MATH_CLEARED = "Đã qua"
MATH_GATE = "Cổng {n}/{t}"
MATH_GATE_HINT = "Cổng thuần thục: mỗi vi kỹ năng đúng {need}/{window} câu gần nhất ở bậc {tier}"
MATH_TRIAL = "Thiên kiếp"
MATH_TRIAL_PROGRESS = "Thiên kiếp nhỏ: câu {n}/{t}"
MATH_TRIAL_ALLOWED = "Được sai {n} câu"
MATH_TRIAL_PASSED = "Vượt Thiên kiếp nhỏ!"
MATH_TRIAL_FAILED = "Chưa qua Thiên kiếp nhỏ"
MATH_TRIAL_AGAIN = "Ôn lại vi kỹ năng yếu rồi thử lại ngay được."
MATH_REVIEW = "Ôn xoắn ốc: tầng {n}"
MATH_REVIEW_NODE = "Ôn lại: {name}"           # a review question: the node of Đạo Thụ it comes from
MATH_REVIEW_COUNT = "Câu ôn tầng dưới: {n}"
MATH_RESULT = "Xem kết quả"

# Bài tập lập trình (M6)
CODE_TITLE = "Bài tập lập trình"
CODE_SHORT = "Bài tập"
CODE_NONE = "Tầng này chưa có bài tập lập trình."
CODE_LOADING = "Đang mở đề..."
CODE_OPEN = "Làm bài"
CODE_RUN = "Chạy thử"
CODE_SUBMIT = "Nộp bài"
CODE_SAVE = "Lưu"
CODE_RUNNING = "Đang chạy bài làm..."
CODE_SENDING = "Đang chấm..."
CODE_INPUT = "Dữ liệu vào"
CODE_OUTPUT = "Kết quả ra"
CODE_LIMITS = "Giới hạn"
CODE_SAMPLE = "Ví dụ {n}"
CODE_HIDDEN_TESTS = "{n} test ẩn"
CODE_TIME_LIMIT = "{n} giây mỗi test"
CODE_FILE = "Bài làm: {path}"
CODE_SAVED = "Đã lưu bài làm"
CODE_NO_PYTHON = "Máy chưa có Python để chạy bài làm. Hãy cài Python, hoặc ghi đường dẫn vào config.json."
CODE_TEST_LINE = "Test {n}: {v}"
CODE_SAMPLE_LINE = "Ví dụ {n}: {v}"
CODE_PASSED = "Qua {p}/{t} test"
CODE_BEST = "Tốt nhất: {v}, {p}/{t} test"
CODE_RUN_HINT = "Chạy thử dùng ví dụ trong đề. Nộp bài chạy trên test ẩn và nhận Tu Vi."
CODE_VERDICTS = {
    "AC": "Đúng hết",
    "WA": "Sai kết quả",
    "TLE": "Quá thời gian",
    "RE": "Lỗi khi chạy",
    "CE": "Lỗi cú pháp",
    "-": "chưa chạy",
}
# Xạ Trường: bài Thực Chiến chấm theo phẩm (docs/THUC_CHIEN_TRONG_GAME.md)
XT_HIDDEN_SETS = "{n} bộ bia ẩn"
XT_TIME_LIMIT = "{n} giây mỗi bộ bia"
XT_PRACTICE = "Bia tập: {note}"
XT_ACCURACY = "Độ chính xác {v}"
XT_ERROR = "Sai số {v}"
XT_BARS = "Mốc hạ / trung / thượng phẩm: {bars}"
XT_SET_LINE = "Bộ {n}: {v}"
XT_SAMPLE_SET_LINE = "Ví dụ {n}: {v}"
XT_NO_SCORE = "không chấm được"
XT_BAD_COUNT = "in {got} dự đoán, cần {want}"
XT_NOT_NUMBER = "có dự đoán không phải số"
XT_TARGET_HIDDEN = "Bắn thật: bia ẩn"
XT_TARGET_PRACTICE = "Bắn tập: bia tập"
XT_LOSS_TITLE = "Đường mất mát ({where})"
XT_WHERE_SET = "bộ {n}"
XT_WHERE_SAMPLE = "ví dụ {n}"
XT_LOSS_RANGE = "mất mát {a} -> {b} sau {n} vòng"
XT_LOSS_NONE = "Chương trình không in dòng #loss nào ra stderr, nên không có đường mất mát để vẽ."
XT_LOSS_BLOWN = "Mất mát thành nan hay vô cùng: tẩu hỏa nhập ma, hãy giảm tốc độ học."
XT_LOSS_VAL = "đường nhạt: #val"
XT_LOSS_LOG = "thang log"
XT_SHOW_TARGET = "Xem bia"
XT_SHOW_STATEMENT = "Xem đề"
XT_BEST = "Tốt nhất: {g}"

# Tàng Thư Các của bí cảnh toán (M4)
LIB_TITLE = "Tàng Thư Các"
LIB_READ = "Đọc"
LIB_OPEN = "Tàng Thư"
LIB_SECTIONS = "{n} mục"
LIB_SECTION = "Mục {n}/{t}: {name}"
LIB_PREV = "Mục trước"
LIB_NEXT = "Mục sau"
LIB_NOTE = "Trúc Lão nhắc: "
LIB_EMPTY = "Chưa có trang sách nào."

# ------------------------------------------------------------------ M7: quái lỗi sai, Lò Toán
CRAFT_TITLE = "Lò Toán"
CRAFT_EMPTY = "Chưa có công thức nào."
CRAFT_LOADING = "Đang nhóm lò..."
CRAFT_MAKES = "Rèn ra"
CRAFT_NEEDS = "Nguyên liệu"
CRAFT_NOTES = "Phải hiểu trước"
CRAFT_FEE = "Phí lò: {n} Linh Thạch"
CRAFT_DO = "Rèn"
CRAFT_DONE = "Rèn xong: {name}!"
CRAFT_HAVE = "{have}/{need}"
CRAFT_SLOT = {"weapon": "Vũ khí", "body": "Áo", "hat": "Mũ", "shoes": "Giày", "jade": "Ngọc Bội",
              "ring": "Nhẫn"}
CRAFT_TAB_RECIPES = "Rèn đồ"
CRAFT_TAB_UPGRADE = "Nâng phẩm"
UPG_TITLE = "{name}: {frm} → {to}"
UPG_NONE = "Chưa có binh khí {frm} nào. Nhặt binh khí ở các vùng đất rồi quay lại."
UPG_LOCKED = "Chưa mở. {why}"
UPG_DO = "Nâng phẩm"
UPG_DONE = "Nâng phẩm xong: {name} thành {quality}!"
UPG_ATK = "Công {a} → {b}"
NOTE_READ = "Đọc ghi chú"

# M9: chiêu thức gắn câu hỏi (thanh chiêu, thẻ câu hỏi) và hai kiểu câu mới
MSKILL_TIP = "{name} ({key}) · {kind}\nLoại câu: {qtype}\nLinh Lực {qi} · hồi {cd} giây\n{desc}"
MSKILL_TIP_LOCKED = "{name} (chưa mở)\n{why}"
MSKILL_MISS = "Chiêu hụt!"
MSKILL_COMBO = "Liên chiêu x{n}"
MSKILL_BADGE = "Chiêu: {name}"
MSKILL_LANDED = "Chiêu trúng! -{n}"
MSKILL_LANDED_CRIT = "Chiêu trúng, chí mạng! -{n}"
MSKILL_MISSED = "Chiêu hụt: không gây sát thương"
MSKILL_NEEDS_TARGET = "Chưa có quái trong tầm"
MATCH_KEYS = "Phím 1-5: vế trái · A-E: vế phải · Xóa lùi: bỏ cặp cuối · Enter: trả lời"
ORDER_KEYS = "Phím A-F: chọn bước · Xóa lùi: bỏ bước cuối · Enter: trả lời"
MQ_UNDO = "Hoàn tác"
MQ_CLEAR = "Làm lại"

# ------------------------------------------------------------------ M10: the math hub's doors
MATH_HUB_DUNGEON = "Hầm Ngục"
MATH_HUB_TD = "Thủ Thành"
MATH_HUB_FORTUNE = "Cơ Duyên"

# ------------------------------------------------------------------ M10: bí cảnh toán (agent REALM)
REALM_TAB_MATH = "Bí cảnh toán"
REALM_MATH_FLOOR = "Câu hỏi ở tầng {f} của con"
REALM_MATH_NO_FLOOR = "Con chưa có tầng toán nào có câu hỏi."
REALM_MATH_INFO = "{p} gian trận nhãn rồi boss · {m} phút · đi một mình hay cả đội"
REALM_MATH_SOLO = "Vào một mình"
REALM_MATH_PARTY = "Cả đội vào"
REALM_SEAL_COUNT = "Ấn đã phá: {n}/{need}"
REALM_SEAL_HOW = "Đứng lên một ấn đá để nhận câu hỏi."
REALM_SEAL_WAIT = "Còn chờ: {names}"
REALM_SEAL_MARK = "?"
REALM_SEAL_BROKEN = "vỡ"
REALM_SEAL_OK = "{by} phá được một ấn!"
REALM_SEAL_BAD = "{by} trả lời sai, ấn vẫn còn."
REALM_BOSS_TONG_HOP = "Mỗi người làm bài tổng hợp của mình."

# ------------------------------------------------------------------ M10: hầm ngục (agent DUNGEON)
DG_TITLE = "Hầm Ngục"
DG_LOADING = "Đang mở cửa hầm..."
DG_INTRO = ("Mỗi phòng một dạng câu, câu hỏi theo bậc của con. Trả lời sai hoặc hết giờ mất một tâm lực; "
            "hết tâm lực thì ra khỏi hầm, những gì đã nhận vẫn giữ nguyên.")
DG_FLOOR = "Tầng {n} · {title}"
DG_FLOOR_LOCKED = "Tầng {n}: {reason}"
DG_SEED = "Linh thạch số"
DG_SEED_HINT = "trống = ngẫu nhiên"
DG_SEED_BAD = "Số khắc trên linh thạch là một số từ 0 đến {n}."
DG_SEED_SHOWN = "Linh thạch số {n}"
DG_HEARTS = "Tâm lực"
DG_REWARDS_LEFT = "Hôm nay còn {n}/{t} hầm có thưởng."
DG_NO_REWARD = "Hôm nay đã hết lượt nhận thưởng: hầm này chỉ cho Tu Vi."
DG_START = "Vào hầm"
DG_ENTER = "Vào phòng"
DG_ABANDON = "Rời hầm"
DG_ROOM_N = "Phòng {i}/{n}"
DG_WARDEN = "Trấn Thủ"
DG_CHEST = "Rương"
DG_QTYPE = "Dạng câu: {name}"
DG_SKILL = "Hỏi về: {name}"
DG_SKILL_ALL = "Hỏi về: mọi vi kỹ năng của tầng, câu khó nhất con đã mở"
DG_GUARD = "{name}: {flavour}"
DG_PROGRESS = "Đúng {p}/{n} câu để qua phòng"
DG_ROOM_REWARD = "Mỗi phòng: +{n} Linh Thạch"
DG_CHEST_REWARD = "Cuối hầm: {name}"
DG_EARNED = "Đã nhận: {what}"
DG_STONES = "{n} Linh Thạch"
DG_ITEM = "{name} x{n}"
DG_NOTHING = "chưa có gì"
DG_LINE = "{room} · {name} · đúng {p}/{n} · tâm lực {h}/{m}"
DG_LINE_SHORT = "{room} · tâm lực {h}/{m}"
DG_ROOM_CLEARED = "Qua phòng!"
DG_HEART_LOST = "Mất một tâm lực."
DG_CHEST_OPEN = "Mở rương!"
DG_BACK_TO_MAP = "Về bản đồ"
DG_NEXT = "Câu tiếp"
DG_SEE_RESULT = "Xem kết quả"
DG_RESULT_TITLE = {"cleared": "Phá đảo hầm ngục!", "failed": "Cạn tâm lực", "abandoned": "Đã rời hầm"}
DG_RESULT_ROOMS = "Qua {c}/{t} phòng · đúng {x}/{y} câu"
DG_RESULT_XP = "Tu Vi +{n}"
DG_RESULT_LOOT = "Nhận được: {what}"
DG_RESULT_KEEP = "Không mất gì đã nhận."
DG_REPLAY = "Chơi lại linh thạch này"
DG_BACK = "Về"

# ------------------------------------------------------------------ M10: cơ duyên (agent FORTUNE)
FORTUNE_TITLE = "Cơ Duyên"
FORTUNE_LOADING = "Đang xem vận số…"
FORTUNE_TOAST = "Có cơ duyên: {name}! Mở Cơ Duyên ở Động Phủ để xem."
FORTUNE_NONE = "Chưa có cơ duyên nào tìm đến con."
FORTUNE_TODAY = "Hôm nay: {n}/{limit} cơ duyên"
FORTUNE_PROGRESS = "Câu đúng tích lũy: {n}/{need}"
FORTUNE_EXPIRES = "Còn {m}:{s:02d} nữa cơ duyên tan"
FORTUNE_ACCEPT = "Nhận"
FORTUNE_RESUME = "Tiếp tục"
FORTUNE_DECLINE = "Bỏ qua"
FORTUNE_ELDER = "Lão nhân ra đề"
FORTUNE_CHEST = "Rương đề"
FORTUNE_QUESTIONS = "{n} câu, phải đúng hết"
FORTUNE_ONE_QUESTION = "Một câu khó nhất con gặp được"
FORTUNE_CARD = "Cơ duyên: {name}  ·  câu {n}/{t}"
FORTUNE_WON = "Cơ duyên đã thành!"
FORTUNE_LOST = "Cơ duyên không thành."
FORTUNE_STONES = "+{n} Linh Thạch"
FORTUNE_ITEM = "+{n} {name}"
FORTUNE_RARE = "(hiếm)"
FORTUNE_LOG = "Những cơ duyên gần đây"
FORTUNE_LOG_EMPTY = "Chưa có gì."
FORTUNE_OUTCOME = {"won": "thành", "lost": "không thành", "declined": "bỏ qua", "expired": "tan mất",
                   "timeout": "hết giờ"}
FORTUNE_CLOSE = "Đóng"

# ------------------------------------------------------------------ M10: thủ thành toán (agent TD)
MTD_TITLE = "Thủ Thành Toán"
MTD_INTRO = ("Mỗi tháp là một mảng toán. Trả lời đúng một câu của mảng ấy thì tháp mới dựng lên hay lên cấp; "
             "sai thì Linh Khí bỏ ra không hoàn lại, ngoài ra không mất gì.")
MTD_LEVELS = "Ải giữ thành"
MTD_TOWERS = "Các loại tháp"
MTD_AREA = "{subject} · tầng {floor}"
MTD_COST = "{c} Linh Khí"
MTD_LOCKED = "Khóa"
MTD_WAVES = "{n} đợt quái"
MTD_PLACE_CARD = "Dựng {name}: trả lời đúng thì tháp đứng lên (Linh Khí bỏ ra không hoàn lại)"
MTD_UPGRADE_CARD = "Nâng {name}: trả lời đúng thì tháp lên cấp (Linh Khí bỏ ra không hoàn lại)"
MTD_BREAK_CARD = "Linh Khí Vấn Đạo: đúng thì +{q} Linh Khí"
MTD_TU_KHI_CARD = "Tụ Khí: đúng thì +{q} Linh Khí, sai không mất gì"
MTD_PLACE_WRONG = "Chưa đúng: tháp chưa dựng được."
MTD_UP_WRONG = "Chưa đúng: tháp chưa lên cấp."
MTD_PLACE_HINT = "Bấm vào ô cạnh đường để dựng {name}. Chuột phải để thôi."
MTD_PICK_HINT = "Chọn tháp ở dưới rồi bấm vào ô cạnh đường. Mỗi tháp cần một câu đúng của mảng toán ấy."
MTD_SELL = "Dỡ (+{c})"
MTD_CONTINUE = "Tiếp"
MTD_ROLE_NAMES = {"hoa": "Nổ vùng", "thuy": "Làm chậm", "kim": "Bắn mạnh", "son": "Choáng vùng",
                  "quang": "Soi sáng", "ho_tro": "Hỗ trợ", "sinh_khi": "Sinh Linh Khí", "moc": "Chặn đường"}


# ---- M11: tìm chỗ sai (agent ENGINE)
FIND_KEYS = "Phím 1-6: chọn bước · Xóa lùi: bỏ chọn · Enter: trả lời"
FM_STEP = "Bước {n}"


# ---- M11: sảnh toán và kiểm tra đầu vào (agent HUB)
MATH_LIST_MORE = "{a}-{b} trong {t} · lăn chuột hoặc phím lên/xuống để xem thêm"
MATH_PLACE_BUTTON = "Kiểm tra đầu vào"
MATH_PLACE_CONTINUE = "Làm tiếp kiểm tra"
MATH_PLACE_TITLE = "Kiểm tra đầu vào"
MATH_PLACE_RESUME_INTRO = "Bài kiểm tra đầu vào đang dở: đã trả lời {a}/{t} câu."
MATH_PLACE_START = "Bắt đầu"
MATH_PLACE_GO_ON = "Làm tiếp"
MATH_PLACE_LATER = "Để sau"
MATH_PLACE_ABANDON = "Bỏ dở"
MATH_PLACE_PROGRESS = "Kiểm tra đầu vào: câu {n}/{t}"
MATH_PLACE_RESULT = "Kết quả kiểm tra đầu vào"
MATH_PLACE_START_AT = "Con bắt đầu ở tầng {n}."
MATH_PLACE_SKIPPED = "Được miễn: {floors}."
MATH_PLACE_WHY_STOP = "Tầng {n} chưa đạt: cần {need}/{planned} câu đúng."
MATH_PLACE_WHY_TOP = "Mọi tầng đều đạt; tầng {n} là tầng cao nhất đã có câu hỏi."
MATH_PLACE_ABANDONED = "Bài đã bỏ dở: con bắt đầu từ tầng {n}, không tầng nào được miễn."
MATH_PLACE_FLOOR = "Tầng {n}: đúng {c}/{a} câu (cần {need}/{planned})"
MATH_PLACE_FLOOR_NOT_ASKED = "Tầng {n}: chưa hỏi tới"
MATH_PLACE_MET = "đạt"
MATH_PLACE_NOT_MET = "chưa đạt"
MATH_PLACE_GATE_NOTE = "Ở tầng {n}, cổng thuần thục và Thiên kiếp nhỏ vẫn áp dụng như mọi người."
MATH_PLACE_BACK = "Về sảnh"

# ---- M11 đợt 2: thiên kiếp (agent TRIB)
TRIB_PART = "Phần {k} / {n}"                 # k is the part's letter
TRIB_PREV = "Phần trước"
TRIB_NEXT = "Phần sau"
TRIB_KEYS = "Trái/Phải: đổi phần · Lên/Xuống: cuộn đề"
TRIB_NEED_ALL = "Trả lời đủ mọi phần mới nộp được"
TRIB_PART_RIGHT = "{k}) Đúng: {a}"
TRIB_PART_WRONG = "{k}) Sai. Đáp án: {a}"
TRIB_PART_GIVEN = "con trả lời: {a}"
TRIB_PART_BLANK = "{k}) Chưa trả lời. Đáp án: {a}"

# ---- M11 đợt 2: bậc thang và kiểm tra đầu vào (agent LADDER)
MATH_LADDER_STEP = "Bậc thang {n}/{t} dẫn tới câu vừa sai"
MATH_LADDER_OPENED = "Tiếp theo: {t} bậc thang dẫn tới câu này"
MATH_LADDER_COUNT = "Bậc thang đã leo: {n}"
MATH_PLACE_INTRO_CLIMB = (
    "Bài kiểm tra đầu vào đặt điểm xuất phát của con trong bí cảnh {name}.",
    "Nhiều nhất {n} câu, mỗi tầng vài câu từ bậc dễ tới bậc khó; hết giờ tính là sai.",
    "Đạt {pct}% thì nhảy lên tầng cao hơn, chưa đạt thì dừng (có khi lùi một tầng để chắc). Con bắt đầu ở tầng thấp nhất chưa đạt.",
    "Không bắt buộc: không làm thì con bắt đầu từ tầng 1.",
    "Ở tầng xuất phát, cổng thuần thục và Thiên kiếp nhỏ vẫn chờ con như mọi người.",
    "Mỗi bí cảnh làm một lần. Bỏ dở thì coi như bắt đầu từ tầng 1.",
)


# ---- Đạo Thụ: sảnh toán đọc cây giáo trình (nút, tầng tu vi, nhánh)
TREE_STAGE = "{realm} tầng {n}/{t}"
TREE_STAGE_NONE = "{realm}: chưa qua tầng nào"
TREE_STAGE_PROGRESS = "đã xong {d}/{t} nút của tầng {n}"     # inside the stage being worked on
TREE_STAGE_PROGRESS_SHORT = "xong {d}/{t} nút tầng {n}"
TREE_TAB_NEXT = "Nên học"
TREE_TAB_SHORT = {"ds": "Đại Số", "gt": "Giải Tích", "xs": "Xác Suất", "tr": "Thuật Toán", "lt": "Lập Trình",
                  "ud": "Thực Chiến"}
TREE_ROW_STAGE = "Tầng {n}"
TREE_OPTIONAL = "Bàng môn"
TREE_PART = "({i}/{n})"
TREE_NEEDS = "Cần xong: {name}"
TREE_VACANT = "Đang biên soạn"
TREE_CODE_ONLY = "Chỉ có bài tập"
TREE_NODE_DONE = "Đã xong"
TREE_EMPTY = "Chưa có nút nào ở đây."
TREE_NEXT_EMPTY = "Không còn nút chính đạo nào đang mở."
TREE_SCROLL_MORE = "Dòng {a}-{b} trong {t} · lăn chuột hoặc phím lên/xuống"
TREE_OPENED = "Nút mới mở: {names}"
TREE_NODE_DONE_LINE = "Nút {name} đã xong"
NODE_CARD_TITLE = "Nút của Đạo Thụ"
NODE_STATE = {"open": "đang mở", "done": "đã xong", "locked": "chưa mở", "vacant": "đang biên soạn"}
NODE_OPTIONAL_TAG = "bàng môn, không chặn đường"
NODE_REQUIRES = "Cần xong trước"
NODE_NO_REQUIRES = "Không cần gì: học được ngay."
NODE_REQ_DONE = "đã xong"
NODE_REQ_TODO = "chưa xong"
NODE_REINFORCES = "Ôn lại"
NODE_TOPICS = "Học gì"
NODE_PROBLEMS = "Bài tập lập trình"
NODE_PROBLEM_SOLVED = "đã giải"
NODE_PROBLEM_TODO = "chưa giải"
NODE_SOURCE = "Nên học từ"
NODE_SRC_NONE = "Chưa có nguồn gợi ý cho nút này."
NODE_SRC_AUTHOR = "Tác giả: {a}"
NODE_SRC_WHERE = "Xem phần: {w}"
NODE_SRC_LANG = "Ngôn ngữ: {lang} · {kind}"
NODE_SRC_URL = "Đường dẫn: {u}"
NODE_SRC_OPEN = "Mở trang"
NODE_DO_PROBLEMS = "Làm bài"                   # opens the node's programming exercises
NODE_SRC_FAILED = "Không mở được trình duyệt. Hãy chép đường dẫn trong thẻ."
NODE_LANG = {"vi": "tiếng Việt", "en": "tiếng Anh"}
NODE_KIND = {"bai_viet": "bài viết", "video": "video", "sach": "sách", "khoa_hoc": "khoá học",
             "tuong_tac": "bài tương tác", "code": "mã nguồn", "bai_tap": "bài tập", "bai_bao": "bài báo"}


# ---- Lộ Trình tân thủ (guide): the board, the HUD box and the welcome
GUIDE_TITLE = "Lộ Trình Tu Tiên"
GUIDE_TAB_ROAD = "Lộ trình"
GUIDE_TAB_BOOK = "Cẩm nang"
GUIDE_LOADING = "Đang tải lộ trình..."
GUIDE_STUDYING = "Đang học"
GUIDE_STUDY_NONE = "Chưa có nút nào đang mở. Hãy xem Đạo Thụ (phím M)."
GUIDE_STAGE = "{realm} tầng {n}/{t}"
GUIDE_MARK_CLAIM = "Nhận"
GUIDE_MARK_DONE = "Xong"
GUIDE_OPTIONAL = "(tuỳ chọn)"
GUIDE_BONUS_ROW = "Thưởng chương"
GUIDE_BONUS_DESC = "Làm xong mọi bước bắt buộc của chương thì nhận thêm phần thưởng này."
GUIDE_REWARDS = "Thưởng: {r}"
GUIDE_REMAINING = "Còn: {names}"
GUIDE_GOTO = "Đi tới"
GUIDE_HELP = "Cẩm nang"
GUIDE_CLAIM = "Nhận thưởng"
GUIDE_STATE = {"active": "đang làm", "done": "xong, chờ nhận thưởng", "claimed": "đã nhận thưởng"}
GUIDE_CLAIMABLE = "Nhận thưởng: {n}"
GUIDE_CLAIMED = "Đã nhận: {r}"
GUIDE_NOTHING = "Chọn một bước để xem."
GUIDE_HUD_NEXT = "Việc tiếp theo · F1"
GUIDE_HUD_STUDY = "Đang học · F1"
GUIDE_HUD_CLAIM = "Nhận thưởng ({n}) · F1"
GUIDE_HUD_ALL_DONE = "Con đã làm hết lộ trình hiện có. Cứ luyện tiếp trên Đạo Thụ nhé."
GUIDE_STEP_DONE_TOAST = "Xong: {title}"       # short: in the world it sits beside the HUD box, which says F1
