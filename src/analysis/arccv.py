import cv2
import numpy
import sys
import time
import pickle
import requests
import json
from tqdm import tqdm
import matplotlib.pyplot as plt

DEBUG = False

class ARCCV:

    OCR_SERVICE_URL = "http://arc_raiders_ocr:8000/ocr"

    # In-Raid UI

    COMPASS_SUBREGION = (675, 16, 550, 24)
    COMPASS_BEARING_VALUE_SUBREGION = (936, 16, 48, 24)
    COMPASS_OBJECTIVES_SUBREGION = (675, 40, 550, 32)
    COMPASS_TEXT_SUBREGION = (783, 73, 371, 26)
    MATCH_TIMER_SUBREGION = (930, 100, 60, 24)
    AUTOMATIC_EXTRACTION_TIMER_SUBREGION = (810, 103, 299, 18)
    RETURN_POINT_SHUTDOWN_NOTICE_REGION = (712, 184, 503, 88)

    QUICKWHEEL_BOUNDING_BOX = (649, 230, 622, 620)
    QUICKWHEEL_TEXT_SUBREGION = (883, 520, 154, 32)

    FRAME_RATE_COUNTER_SUBREGION = (1866, 0, 54, 21)

    LOCATION_TEXT_SUBREGION = (22, 389, 392, 87)

    XP_LOGS_SUBREGION = (23, 308, 355, 118)

    PLAYER_PROXIMITY_VOICE_SUBREGION = (21, 592, 288, 39)

    PLAYER_CHAT_SUBREGION = (36, 704, 448, 70)

    PLAYER_2_BOUNDING_BOX = (39, 876, 271, 68)
    PLAYER_2_COLOR_SUBREGION = (45, 895, 6, 20)

    PLAYER_1_BOUNDING_BOX = (40, 944, 270, 90)

    PLAYER_1_VOICE_ICON_SUBREGION = (268, 944, 20, 19)

    PLAYER_1_SHIELD_NW_POINT = (40, 994)
    PLAYER_1_SHIELD_NE_POINT = (309, 966)
    PLAYER_1_SHIELD_SE_POINT = (309, 981)
    PLAYER_1_SHIELD_SW_POINT = (40, 1011)
    PLAYER_1_SHIELD_BOUNDING_BOX = (40, 966, 269, 46)
    PLAYER_1_SHIELD_SLICE_SUBREGION = (4, 20, 261, 1)

    PLAYER_1_HEALTH_NW_POINT = (40, 1016)
    PLAYER_1_HEALTH_NE_POINT = (309, 986)
    PLAYER_1_HEALTH_SE_POINT = (309, 1001)
    PLAYER_1_HEALTH_SW_POINT = (40, 1033)
    PLAYER_1_HEALTH_BOUNDING_BOX = (40, 986, 269, 46)
    PLAYER_1_HEALTH_SLICE_SUBREGION = (4, 20, 261, 1)

    OVER_ENCUMBERED_ICON_REGION = (946, 936, 28, 24)

    STAMINA_BAR_SUBREGION = (857, 968, 206, 16)
    STAMINA_BAR_SLICE_SUBREGION = (3, 7, 200, 1)

    INVENTORY_OVERLAY_SUBREGION = (923, 639, 72, 108)

    PATCH_SERVER_LOBBY_REGION = (1731, 1060, 160, 20)

    RELOAD_INDICATOR_SUBREGION = (940, 520, 40, 40)

    QUICK_ITEM_1_SUBREGION = (1536, 909, 64, 92)
    QUICK_ITEM_2_SUBREGION = (1608, 914, 64, 94)

    UNSELECTED_SECONDARY_WEAPON_BOUNDING_BOX = (1680, 980, 200, 55)
    SELECTED_PRIMARY_WEAPON_BOUNDING_BOX = (1680, 883, 200, 112)
    SELECTED_PRIMARY_WEAPON_CURRENT_AMMO_SUBREGION = (1698, 924, 53, 28)
    SELECTED_PRIMARY_WEAPON_RESERVE_AMMO_SUBREGION = (1720, 952, 32, 17)

    FLASHLIGHT_TOOL_TIP_REGION = (1743, 821, 140, 37)
    UNARMED_TOOL_TIP_REGION = (1743, 784, 140, 37)

    DIALOGUE_CAPTION_SUBREGION = (587, 985, 751, 95)

    RECHARGE_OWN_SHIELD_SUBREGION = (1176, 678, 219, 32)
    RECHARGE_OTHER_SHIELD_SUBREGION = (1176, 726, 233, 32)

    PLAYER_ZONE_BOUNDING_BOX = (469, 398, 980, 682)

    # Shared overlay UI

    OVERLAY_NAVIGATION_SUBREGION = (634, 23, 648, 42)

    # Looting UI

    LOOTING_INVENTORY_LOADOUT_DETAILS_SUBREGION = (661, 158, 306, 69)
    LOOTING_EQUIPMENT_AUGMENT_SUBREGION = (661, 295, 146, 98)
    LOOTING_EQUIPMENT_SHIELD_SUBREGION = (821, 295, 146, 98)
    LOOTING_EQUIPMENT_PRIMARY_WEAPON_SUBREGION = (661, 415, 306, 202)
    LOOTING_EQUIPMENT_SECONDARY_WEAPON_SUBREGION = (661, 631, 306, 202)
    LOOTING_BACKPACK_LABEL_SUBREGION = (1013, 255, 156, 17)
    LOOTING_BACKPACK_BOUNDING_BOX = (1013, 295, 410, 514)
    LOOTING_QUICK_USE_LABEL_SUBREGION = (1473, 255, 142, 17)
    LOOTING_QUICK_USE_BOUNDING_BOX = (1473, 295, 306, 202)
    LOOTING_AUGMENTED_SLOTS_LABEL_SUBREGION = (1473, 527, 218, 17)
    LOOTING_AUGMENTED_SLOTS_BOUNDING_BOX = (1473, 567, 306, 98)
    LOOTING_SAFE_POCKET_LABEL_SUBREGION = (1473, 695, 155, 17)
    LOOTING_SAFE_POCKET_BOUNDING_BOX = (1473, 735, 306, 98)
    LOOTING_CONTAINER_BOUNDING_BOX = (141, 295, 410, 410)
    LOOTING_KEYBINDS_BOUNDING_BOX = (51, 1017, 764, 34)

    LOOTING_SALVAGE_BOUNDING_BOX = (570, 313, 780, 454)

    # Map UI

    MAP_BOUNDING_BOX = (48, 112, 1824, 856)
    MAP_PLAYER_POSITION_SUBREGION = (949, 531, 21, 21)
    MAP_LEGEND_BOUNDING_BOX = (1506, 128, 350, 815)
    MAP_DETAILS_SUBREGION = (1506, 128, 350, 86)
    MAP_QUESTS_BOUNDING_BOX = (48, 128, 466, 824)
    MAP_KEYBINDS_BOUNDING_BOX = (51, 1017, 1231, 34)

    # Weapon localization

    POSSIBLE_WEAPON_NAMES = [
        "Kettle",
        "Rattler",
        "arpeggio",
        "Tempest",
        "Bettina",
        "Ferro",
        "Renegade",
        "Aphelion",
        "Stitcher",
        "Bobcat",
        "Il Toro",
        "Vulcano",
        "Hairpin",
        "Burletta",
        "Anvil",
        "Venator",
        "Torrente",
        "Osprey",
        "Jupiter",
        "Hullcracker",
        "Equalizer"
    ]

    POSSIBLE_MAP_NAMES = [
        "Dam Battlegrounds",
        "Burried City",
        "Spaceport",
        "The Blue Gate",
        "Stella Montis",
        "Practice Range"
    ]

    POSSIBLE_MAP_MODIFIERS = [
        "Lust Blooms",
        "Prospecting Probes",
        "Husk Graveyard",
        "Uncovered Caches",
        "Launch Tower Loot",
        "Harvester",
        "Matriarch",
        "Night Raid",
        "Electromagnetic Storm",
        "Hidden Bunker",
        "Locked Gate",
        # "Snow Variant" # Planned December 2025 release
    ]

    POSSIBLE_QUEST_NAMES = [
        "Picking Up The Pieces",
        "Trash Into Treasure",
        "Clearer Skies",
        "Off The Radar",
        "A Bad Feeling",
        "A Balanced Harvest",
        "A Better Use",
        "A Lay Of The Land",
        "A New Type Of Plant",
        "A Reveal in Ruins",
        "A Symbol Of Unification",
        "A Warm Place To Rest",
        "After Rain Comes",
        "Armored Transports",
        "Back On Top",
        "Bees!",
        "Broken Monument",
        "Building A Library",
        "Celeste's Journals",
        "Communication Hideout",
        "Digging Up Dirt",
        "Doctor's Orders",
        "Dormant Barons",
        "Down To Earth",
        "Echoes Of Victory Ridge",
        "Espresso",
        "Eyes In The Sky",
        "Eyes On The Prize",
        "Flickering Threat",
        "Greasing Her Palms",
        "Hatch Repairs",
        "Industrial Espionage",
        "Into The Fray",
        "Keeping The Memory",
        "Life Of A Pharmacist",
        "Lost In Transmission",
        "Marked For Death",
        "Market Correction",
        "Medical Merchandise",
        "Mixed Signals",
        "Our Presence Up There",
        "Out Of The Shadows",
        "Power Out",
        "Prescriptions Of The Past",
        "Safe Passage",
        "Source Of The Contamination",
        "Sparks Fly",
        "Straight Record",
        "Switching The Supply",
        "The Right Tool",
        "The Root Of The Matter",
        "The Major's Footlocker",
        "The Trifecta",
        "Tribute to Toledo",
        "Turnabout",
        "Unexpected Initiative",
        "Untended Garden",
        "Water Troubles",
        "What Goes Around",
        "What We Left Behind",
        "A First Foothold",
        "Reduced to Rubble",
        "With A Trace",
        "In My Image",
        "Cold Storage",
        "Snap And Salvage"
    ]

    POSSIBLE_AMMO_TYPES = [
        "Light Ammo",
        "Medium Ammo",
        "Heavy Ammo",
        "Shotgun Ammo",
        "Launcher Ammo",
        "Energy Clip"
    ]

    def __init__(self):
        
        self.statistics = {}

    def process_vod(self, vod_path):

        capture = cv2.VideoCapture(vod_path)

        if not capture.isOpened():
            raise FileNotFoundError(f"Could not open video file: {vod_path}")

        # Get video properties
        capture_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        capture_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = capture.get(cv2.CAP_PROP_FPS)
        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # Define process overrides

        # 2608011038.mp4 Framestamps:
        # PROCESS_START_FRAME = 84120 # In Raid UI example
        # PROCESS_START_FRAME = 71160 # Looting UI example
        # PROCESS_START_FRAME = 6 # Map UI example
        # PROCESS_START_FRAME = 89040 # Map UI example
        # PROCESS_START_FRAME = 73920 # Dynamic In Raid UI example for stamina/shield/health
        # PROCESS_START_FRAME = 10500 # Shield and health with grey example
        # PROCESS_START_FRAME = 9960 # Shield grey and health yellow example

        # PROCESS_START_FRAME = (8 * 60 * 60) + (42.5 * 60)
        PROCESS_START_FRAME = 0

        # frame_video_out = cv2.VideoWriter(
        #     './frame_video.mp4',
        #     cv2.VideoWriter_fourcc(*'avc1'),
        #     60,
        #     (1920, 1080),
        #     3
        # )

        PROCESS_FRAME_COUNT = total_frames - PROCESS_START_FRAME
        capture.set(cv2.CAP_PROP_POS_FRAMES, PROCESS_START_FRAME)

        for offset in tqdm(range(PROCESS_FRAME_COUNT)):

            ret, frame = capture.read()
            if not ret:
                raise ValueError(f"Could not read frame {PROCESS_START_FRAME + offset} from video.")

            # raid_ui_frame = frame.copy()
            # self._draw_in_raid_ui(raid_ui_frame)
            # cv2.imwrite(f"/usr/src/analysis/frame/inraid_frame_{int(PROCESS_START_FRAME + offset):07d}.jpg", raid_ui_frame)

            # looting_ui_frame = frame.copy()
            # self._draw_looting_ui(looting_ui_frame)
            # cv2.imwrite(f"/usr/src/analysis/frame/looting_frame_{int(PROCESS_START_FRAME + offset):07d}.jpg", looting_ui_frame)

            # map_ui_frame = frame.copy()
            # self._draw_map_ui(map_ui_frame)
            # cv2.imwrite(f"/usr/src/analysis/frame/map_frame_{int(PROCESS_START_FRAME + offset):07d}.jpg", map_ui_frame)

            # cv2.imwrite(f"/usr/src/analysis/frame/processed_frame_{int(PROCESS_START_FRAME + offset):07d}.jpg", frame)

            stamina_results = self._stamina_calculation(frame)
            shield_results = self._shield_calculation(frame)
            health_results = self._health_calculation(frame)

            self.statistics[PROCESS_START_FRAME + offset] = {}
            self.statistics[PROCESS_START_FRAME + offset]['stamina'] = stamina_results
            self.statistics[PROCESS_START_FRAME + offset]['shield'] = shield_results
            self.statistics[PROCESS_START_FRAME + offset]['health'] = health_results

            # frame_video_out.write(frame)

            # Determine scene
            # scene = self._determine_scene(frame)
    
        # write statistics to json file
        with open('/usr/src/analysis/frame/statistics.json', 'w') as f:
            json.dump(self.statistics, f)

    def _load_and_plot_saved_statistics(self):

        with open('/usr/src/analysis/frame/statistics.json', 'r') as f:
            self.statistics = json.load(f)

        frames = list(self.statistics.keys())
        stamina_values = [self.statistics[frame]['stamina']['stamina'] for frame in frames]
        shield_values = [self.statistics[frame]['shield']['shield'] for frame in frames]
        health_values = [self.statistics[frame]['health']['health'] for frame in frames]

        plt.figure(figsize=(20, 5))
        plt.plot(frames, stamina_values, label='Stamina', color='black')
        plt.plot(frames, shield_values, label='Shield', color='blue')
        plt.plot(frames, health_values, label='Health', color='green')
        plt.ylabel('Value')
        plt.xlabel('Frame Number')
        plt.xticks(ticks=range(0, len(frames), len(frames)//20))
        plt.title('Player Stamina, Shield, and Health Over Time')
        plt.legend()
        plt.savefig('/usr/src/analysis/frame/player_stats_over_time.png')
        plt.close()
    
    def _load_and_multi_plot_saved_statistics(self):

        with open('/usr/src/analysis/frame/statistics.json', 'r') as f:
            self.statistics = json.load(f)
        
        frames = list(self.statistics.keys())
        stamina_values = [self.statistics[frame]['stamina']['stamina'] for frame in frames]
        shield_values = [self.statistics[frame]['shield']['shield'] for frame in frames]
        shield_damage_values = [self.statistics[frame]['shield']['damage'] for frame in frames]
        health_values = [self.statistics[frame]['health']['health'] for frame in frames]
        health_damage_values = [self.statistics[frame]['health']['damage'] for frame in frames]
        fig, axs = plt.subplots(5, 1, figsize=(20, 15), sharex=True)
        axs[0].plot(frames, stamina_values, label='Stamina', color='black')
        axs[0].set_ylabel('Stamina Value')
        axs[1].plot(frames, shield_values, label='Shield', color='blue')
        axs[1].set_ylabel('Shield Value')
        axs[2].plot(frames, shield_damage_values, label='Shield Damage', color='red')
        axs[2].set_ylabel('Shield Damage')
        axs[3].plot(frames, health_values, label='Health', color='green')
        axs[3].set_ylabel('Health Value')
        axs[4].plot(frames, health_damage_values, label='Health Damage', color='red')
        axs[4].set_ylabel('Health Damage')
        axs[4].set_xlabel('Frame Number')
        fig.suptitle('Player Stamina, Shield, Shield Damage, Health, and Health Damage Over Time')
        plt.xticks(ticks=range(0, len(frames), len(frames)//20))
        plt.savefig('/usr/src/analysis/frame/player_stats_over_time_multi.png')
        plt.close()

    def _load_and_multi_plot_complete_saved_statistics(self):

        with open('/usr/src/analysis/frame/statistics.json', 'r') as f:
            self.statistics = json.load(f)
        
        frames = list(self.statistics.keys())

        stamina_values = [self.statistics[frame]['stamina']['stamina'] for frame in frames]

        shield_values = [self.statistics[frame]['shield']['shield'] for frame in frames]
        shield_damage_values = [self.statistics[frame]['shield']['damage'] for frame in frames]
        shield_queued_values = [self.statistics[frame]['shield']['queued'] for frame in frames]
        shield_charging_values = [self.statistics[frame]['shield']['charging'] for frame in frames]
        shield_missing_values = [self.statistics[frame]['shield']['missing'] for frame in frames]

        health_values = [self.statistics[frame]['health']['health'] for frame in frames]
        health_damage_values = [self.statistics[frame]['health']['damage'] for frame in frames]
        health_queued_values = [self.statistics[frame]['health']['queued'] for frame in frames]
        health_charging_values = [self.statistics[frame]['health']['charging'] for frame in frames]
        health_missing_values = [self.statistics[frame]['health']['missing'] for frame in frames]

        fig, axs = plt.subplots(11, 1, figsize=(18, 18), sharex=True)
        axs[0].plot(frames, stamina_values, label='Stamina', color='black')
        axs[0].set_ylabel('Stamina Value')

        axs[1].plot(frames, shield_values, label='Shield', color='blue')
        axs[1].set_ylabel('Shield Value')
        axs[2].plot(frames, shield_damage_values, label='Shield Damage', color='red')
        axs[2].set_ylabel('Shield Damage')
        axs[3].plot(frames, shield_queued_values, label='Shield Queued', color='orange')
        axs[3].set_ylabel('Shield Queued')
        axs[4].plot(frames, shield_charging_values, label='Shield Charging', color='grey')
        axs[4].set_ylabel('Shield Charging')
        axs[5].plot(frames, shield_missing_values, label='Shield Missing', color='brown')
        axs[5].set_ylabel('Shield Missing')

        axs[6].plot(frames, health_values, label='Health', color='green')
        axs[6].set_ylabel('Health Value')
        axs[7].plot(frames, health_damage_values, label='Health Damage', color='red')
        axs[7].set_ylabel('Health Damage')
        axs[8].plot(frames, health_queued_values, label='Health Queued', color='orange')
        axs[8].set_ylabel('Health Queued')
        axs[9].plot(frames, health_charging_values, label='Health Charging', color='grey')
        axs[9].set_ylabel('Health Charging')
        axs[10].plot(frames, health_missing_values, label='Health Missing', color='brown')
        axs[10].set_ylabel('Health Missing')
        axs[10].set_xlabel('Frame Number')

        fig.suptitle('Player Stamina, Shield, Shield Damage, Shield Queued, Shield Charging, Shield Missing, Health, Health Damage, Health Queued, Health Charging, and Health Missing Over Time', weight='bold')
        plt.xticks(ticks=range(0, len(frames), len(frames)//20))
        plt.tight_layout(pad=1.5)
        plt.savefig('/usr/src/analysis/frame/complete_player_stats_over_time_multi.png')
        plt.close()

    def _perform_ocr_and_draw_text(self, frame, output_path):
        results = self._perform_ocr(frame)
        result_frame = frame.copy()

        for item in results["results"]:
            # [[p1,p2], [p3,p4], [p5,p6], [p7,p8]]
            points = item['bbox']

            cv2.rectangle(result_frame, (points[0][0], points[0][1]), (points[2][0], points[2][1]), (0, 255, 0), 2)
            cv2.putText(result_frame, item['text'], (points[0][0], points[0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imwrite(output_path, result_frame)

    def _determine_scene(self, frame):

        # Check if scene is in-raid UI
        compass_bearing = self._perform_ocr(self._extract_subregion(frame, self.COMPASS_BEARING_VALUE_SUBREGION))
        match_timer = self._perform_ocr(self._extract_subregion(frame, self.MATCH_TIMER_SUBREGION))
        selected_primary_weapon_details = self._perform_ocr(self._extract_subregion(frame, self.SELECTED_PRIMARY_WEAPON_BOUNDING_BOX))
        if any(weapon_name in selected_primary_weapon_details for weapon_name in self.POSSIBLE_WEAPON_NAMES):
            return "INRAID"

        # Check if scene is looting UI
        looting_inventory_loadout = self._perform_ocr(self._extract_subregion(frame, self.LOOTING_INVENTORY_LOADOUT_DETAILS_SUBREGION))
        if "LOADOUT" in looting_inventory_loadout:
            return "LOOTING"

        # Check if overlay is visible
        overlay_navigation = self._perform_ocr(self._extract_subregion(frame, self.OVERLAY_NAVIGATION_SUBREGION))
        if "INVENTORY" in overlay_navigation or "CRAFTING" in overlay_navigation or "MAP" in overlay_navigation or "LOGBOOK" in overlay_navigation or "SYSTEM" in overlay_navigation:
            # Scene is an overlay related
            # TODO: ensure this isn't shared with out of raid UI
            # TODO: determine state machine for UI scenes
            pass

        # Check if scene is map UI
        map_legend = self._perform_ocr(self._extract_subregion(frame, self.MAP_LEGEND_BOUNDING_BOX))
        if any(map_name in map_legend for map_name in self.POSSIBLE_MAP_NAMES):
            return "MAP"

        return "UNKNOWN"

    def _extract_subregion(self, frame, subregion):
        x, y, w, h = subregion
        return frame[y:y+h, x:x+w]

    def _perform_ocr(self, image):
        _, img_encoded = cv2.imencode('.jpg', image)
        files = {"file": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}
        response = requests.post(self.OCR_SERVICE_URL, files = files)
        response.raise_for_status()
        return response.json()

    def _draw_in_raid_ui(self, frame):
        # Shared UI
        cv2.rectangle(frame, self.FRAME_RATE_COUNTER_SUBREGION[:2], (self.FRAME_RATE_COUNTER_SUBREGION[0] + self.FRAME_RATE_COUNTER_SUBREGION[2], self.FRAME_RATE_COUNTER_SUBREGION[1] + self.FRAME_RATE_COUNTER_SUBREGION[3]), (0, 0, 255), 1)

        # In-raid UI specific
        cv2.rectangle(frame, self.COMPASS_SUBREGION[:2], (self.COMPASS_SUBREGION[0] + self.COMPASS_SUBREGION[2], self.COMPASS_SUBREGION[1] + self.COMPASS_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.COMPASS_BEARING_VALUE_SUBREGION[:2], (self.COMPASS_BEARING_VALUE_SUBREGION[0] + self.COMPASS_BEARING_VALUE_SUBREGION[2], self.COMPASS_BEARING_VALUE_SUBREGION[1] + self.COMPASS_BEARING_VALUE_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.COMPASS_OBJECTIVES_SUBREGION[:2], (self.COMPASS_OBJECTIVES_SUBREGION[0] + self.COMPASS_OBJECTIVES_SUBREGION[2], self.COMPASS_OBJECTIVES_SUBREGION[1] + self.COMPASS_OBJECTIVES_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.COMPASS_TEXT_SUBREGION[:2], (self.COMPASS_TEXT_SUBREGION[0] + self.COMPASS_TEXT_SUBREGION[2], self.COMPASS_TEXT_SUBREGION[1] + self.COMPASS_TEXT_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.MATCH_TIMER_SUBREGION[:2], (self.MATCH_TIMER_SUBREGION[0] + self.MATCH_TIMER_SUBREGION[2], self.MATCH_TIMER_SUBREGION[1] + self.MATCH_TIMER_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.AUTOMATIC_EXTRACTION_TIMER_SUBREGION[:2], (self.AUTOMATIC_EXTRACTION_TIMER_SUBREGION[0] + self.AUTOMATIC_EXTRACTION_TIMER_SUBREGION[2], self.AUTOMATIC_EXTRACTION_TIMER_SUBREGION[1] + self.AUTOMATIC_EXTRACTION_TIMER_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.RETURN_POINT_SHUTDOWN_NOTICE_REGION[:2], (self.RETURN_POINT_SHUTDOWN_NOTICE_REGION[0] + self.RETURN_POINT_SHUTDOWN_NOTICE_REGION[2], self.RETURN_POINT_SHUTDOWN_NOTICE_REGION[1] + self.RETURN_POINT_SHUTDOWN_NOTICE_REGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.QUICKWHEEL_BOUNDING_BOX[:2], (self.QUICKWHEEL_BOUNDING_BOX[0] + self.QUICKWHEEL_BOUNDING_BOX[2], self.QUICKWHEEL_BOUNDING_BOX[1] + self.QUICKWHEEL_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.QUICKWHEEL_TEXT_SUBREGION[:2], (self.QUICKWHEEL_TEXT_SUBREGION[0] + self.QUICKWHEEL_TEXT_SUBREGION[2], self.QUICKWHEEL_TEXT_SUBREGION[1] + self.QUICKWHEEL_TEXT_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOCATION_TEXT_SUBREGION[:2], (self.LOCATION_TEXT_SUBREGION[0] + self.LOCATION_TEXT_SUBREGION[2], self.LOCATION_TEXT_SUBREGION[1] + self.LOCATION_TEXT_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.XP_LOGS_SUBREGION[:2], (self.XP_LOGS_SUBREGION[0] + self.XP_LOGS_SUBREGION[2], self.XP_LOGS_SUBREGION[1] + self.XP_LOGS_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PLAYER_PROXIMITY_VOICE_SUBREGION[:2], (self.PLAYER_PROXIMITY_VOICE_SUBREGION[0] + self.PLAYER_PROXIMITY_VOICE_SUBREGION[2], self.PLAYER_PROXIMITY_VOICE_SUBREGION[1] + self.PLAYER_PROXIMITY_VOICE_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PLAYER_CHAT_SUBREGION[:2], (self.PLAYER_CHAT_SUBREGION[0] + self.PLAYER_CHAT_SUBREGION[2], self.PLAYER_CHAT_SUBREGION[1] + self.PLAYER_CHAT_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PLAYER_2_BOUNDING_BOX[:2], (self.PLAYER_2_BOUNDING_BOX[0] + self.PLAYER_2_BOUNDING_BOX[2], self.PLAYER_2_BOUNDING_BOX[1] + self.PLAYER_2_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PLAYER_1_BOUNDING_BOX[:2], (self.PLAYER_1_BOUNDING_BOX[0] + self.PLAYER_1_BOUNDING_BOX[2], self.PLAYER_1_BOUNDING_BOX[1] + self.PLAYER_1_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PLAYER_1_VOICE_ICON_SUBREGION[:2], (self.PLAYER_1_VOICE_ICON_SUBREGION[0] + self.PLAYER_1_VOICE_ICON_SUBREGION[2], self.PLAYER_1_VOICE_ICON_SUBREGION[1] + self.PLAYER_1_VOICE_ICON_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PLAYER_1_SHIELD_BOUNDING_BOX[:2], (self.PLAYER_1_SHIELD_BOUNDING_BOX[0] + self.PLAYER_1_SHIELD_BOUNDING_BOX[2], self.PLAYER_1_SHIELD_BOUNDING_BOX[1] + self.PLAYER_1_SHIELD_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PLAYER_1_HEALTH_BOUNDING_BOX[:2], (self.PLAYER_1_HEALTH_BOUNDING_BOX[0] + self.PLAYER_1_HEALTH_BOUNDING_BOX[2], self.PLAYER_1_HEALTH_BOUNDING_BOX[1] + self.PLAYER_1_HEALTH_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.OVER_ENCUMBERED_ICON_REGION[:2], (self.OVER_ENCUMBERED_ICON_REGION[0] + self.OVER_ENCUMBERED_ICON_REGION[2], self.OVER_ENCUMBERED_ICON_REGION[1] + self.OVER_ENCUMBERED_ICON_REGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.INVENTORY_OVERLAY_SUBREGION[:2], (self.INVENTORY_OVERLAY_SUBREGION[0] + self.INVENTORY_OVERLAY_SUBREGION[2], self.INVENTORY_OVERLAY_SUBREGION[1] + self.INVENTORY_OVERLAY_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.STAMINA_BAR_SUBREGION[:2], (self.STAMINA_BAR_SUBREGION[0] + self.STAMINA_BAR_SUBREGION[2], self.STAMINA_BAR_SUBREGION[1] + self.STAMINA_BAR_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PATCH_SERVER_LOBBY_REGION[:2], (self.PATCH_SERVER_LOBBY_REGION[0] + self.PATCH_SERVER_LOBBY_REGION[2], self.PATCH_SERVER_LOBBY_REGION[1] + self.PATCH_SERVER_LOBBY_REGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.RELOAD_INDICATOR_SUBREGION[:2], (self.RELOAD_INDICATOR_SUBREGION[0] + self.RELOAD_INDICATOR_SUBREGION[2], self.RELOAD_INDICATOR_SUBREGION[1] + self.RELOAD_INDICATOR_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.QUICK_ITEM_1_SUBREGION[:2], (self.QUICK_ITEM_1_SUBREGION[0] + self.QUICK_ITEM_1_SUBREGION[2], self.QUICK_ITEM_1_SUBREGION[1] + self.QUICK_ITEM_1_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.QUICK_ITEM_2_SUBREGION[:2], (self.QUICK_ITEM_2_SUBREGION[0] + self.QUICK_ITEM_2_SUBREGION[2], self.QUICK_ITEM_2_SUBREGION[1] + self.QUICK_ITEM_2_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.UNSELECTED_SECONDARY_WEAPON_BOUNDING_BOX[:2], (self.UNSELECTED_SECONDARY_WEAPON_BOUNDING_BOX[0] + self.UNSELECTED_SECONDARY_WEAPON_BOUNDING_BOX[2], self.UNSELECTED_SECONDARY_WEAPON_BOUNDING_BOX[1] + self.UNSELECTED_SECONDARY_WEAPON_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.SELECTED_PRIMARY_WEAPON_BOUNDING_BOX[:2], (self.SELECTED_PRIMARY_WEAPON_BOUNDING_BOX[0] + self.SELECTED_PRIMARY_WEAPON_BOUNDING_BOX[2], self.SELECTED_PRIMARY_WEAPON_BOUNDING_BOX[1] + self.SELECTED_PRIMARY_WEAPON_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.SELECTED_PRIMARY_WEAPON_CURRENT_AMMO_SUBREGION[:2], (self.SELECTED_PRIMARY_WEAPON_CURRENT_AMMO_SUBREGION[0] + self.SELECTED_PRIMARY_WEAPON_CURRENT_AMMO_SUBREGION[2], self.SELECTED_PRIMARY_WEAPON_CURRENT_AMMO_SUBREGION[1] + self.SELECTED_PRIMARY_WEAPON_CURRENT_AMMO_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.SELECTED_PRIMARY_WEAPON_RESERVE_AMMO_SUBREGION[:2], (self.SELECTED_PRIMARY_WEAPON_RESERVE_AMMO_SUBREGION[0] + self.SELECTED_PRIMARY_WEAPON_RESERVE_AMMO_SUBREGION[2], self.SELECTED_PRIMARY_WEAPON_RESERVE_AMMO_SUBREGION[1] + self.SELECTED_PRIMARY_WEAPON_RESERVE_AMMO_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.FLASHLIGHT_TOOL_TIP_REGION[:2], (self.FLASHLIGHT_TOOL_TIP_REGION[0] + self.FLASHLIGHT_TOOL_TIP_REGION[2], self.FLASHLIGHT_TOOL_TIP_REGION[1] + self.FLASHLIGHT_TOOL_TIP_REGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.UNARMED_TOOL_TIP_REGION[:2], (self.UNARMED_TOOL_TIP_REGION[0] + self.UNARMED_TOOL_TIP_REGION[2], self.UNARMED_TOOL_TIP_REGION[1] + self.UNARMED_TOOL_TIP_REGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.DIALOGUE_CAPTION_SUBREGION[:2], (self.DIALOGUE_CAPTION_SUBREGION[0] + self.DIALOGUE_CAPTION_SUBREGION[2], self.DIALOGUE_CAPTION_SUBREGION[1] + self.DIALOGUE_CAPTION_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.RECHARGE_OWN_SHIELD_SUBREGION[:2], (self.RECHARGE_OWN_SHIELD_SUBREGION[0] + self.RECHARGE_OWN_SHIELD_SUBREGION[2], self.RECHARGE_OWN_SHIELD_SUBREGION[1] + self.RECHARGE_OWN_SHIELD_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.RECHARGE_OTHER_SHIELD_SUBREGION[:2], (self.RECHARGE_OTHER_SHIELD_SUBREGION[0] + self.RECHARGE_OTHER_SHIELD_SUBREGION[2], self.RECHARGE_OTHER_SHIELD_SUBREGION[1] + self.RECHARGE_OTHER_SHIELD_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.PLAYER_ZONE_BOUNDING_BOX[:2], (self.PLAYER_ZONE_BOUNDING_BOX[0] + self.PLAYER_ZONE_BOUNDING_BOX[2], self.PLAYER_ZONE_BOUNDING_BOX[1] + self.PLAYER_ZONE_BOUNDING_BOX[3]), (0, 0, 255), 1)

    def _draw_looting_ui(self, frame):
        # Shared UI
        cv2.rectangle(frame, self.FRAME_RATE_COUNTER_SUBREGION[:2], (self.FRAME_RATE_COUNTER_SUBREGION[0] + self.FRAME_RATE_COUNTER_SUBREGION[2], self.FRAME_RATE_COUNTER_SUBREGION[1] + self.FRAME_RATE_COUNTER_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.OVERLAY_NAVIGATION_SUBREGION[:2], (self.OVERLAY_NAVIGATION_SUBREGION[0] + self.OVERLAY_NAVIGATION_SUBREGION[2], self.OVERLAY_NAVIGATION_SUBREGION[1] + self.OVERLAY_NAVIGATION_SUBREGION[3]), (0, 0, 255), 1)

        # Lotting UI specific
        cv2.rectangle(frame, self.LOOTING_INVENTORY_LOADOUT_DETAILS_SUBREGION[:2], (self.LOOTING_INVENTORY_LOADOUT_DETAILS_SUBREGION[0] + self.LOOTING_INVENTORY_LOADOUT_DETAILS_SUBREGION[2], self.LOOTING_INVENTORY_LOADOUT_DETAILS_SUBREGION[1] + self.LOOTING_INVENTORY_LOADOUT_DETAILS_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_EQUIPMENT_AUGMENT_SUBREGION[:2], (self.LOOTING_EQUIPMENT_AUGMENT_SUBREGION[0] + self.LOOTING_EQUIPMENT_AUGMENT_SUBREGION[2], self.LOOTING_EQUIPMENT_AUGMENT_SUBREGION[1] + self.LOOTING_EQUIPMENT_AUGMENT_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_EQUIPMENT_SHIELD_SUBREGION[:2], (self.LOOTING_EQUIPMENT_SHIELD_SUBREGION[0] + self.LOOTING_EQUIPMENT_SHIELD_SUBREGION[2], self.LOOTING_EQUIPMENT_SHIELD_SUBREGION[1] + self.LOOTING_EQUIPMENT_SHIELD_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_EQUIPMENT_PRIMARY_WEAPON_SUBREGION[:2], (self.LOOTING_EQUIPMENT_PRIMARY_WEAPON_SUBREGION[0] + self.LOOTING_EQUIPMENT_PRIMARY_WEAPON_SUBREGION[2], self.LOOTING_EQUIPMENT_PRIMARY_WEAPON_SUBREGION[1] + self.LOOTING_EQUIPMENT_PRIMARY_WEAPON_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_EQUIPMENT_SECONDARY_WEAPON_SUBREGION[:2], (self.LOOTING_EQUIPMENT_SECONDARY_WEAPON_SUBREGION[0] + self.LOOTING_EQUIPMENT_SECONDARY_WEAPON_SUBREGION[2], self.LOOTING_EQUIPMENT_SECONDARY_WEAPON_SUBREGION[1] + self.LOOTING_EQUIPMENT_SECONDARY_WEAPON_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_BACKPACK_LABEL_SUBREGION[:2], (self.LOOTING_BACKPACK_LABEL_SUBREGION[0] + self.LOOTING_BACKPACK_LABEL_SUBREGION[2], self.LOOTING_BACKPACK_LABEL_SUBREGION[1] + self.LOOTING_BACKPACK_LABEL_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_BACKPACK_BOUNDING_BOX[:2], (self.LOOTING_BACKPACK_BOUNDING_BOX[0] + self.LOOTING_BACKPACK_BOUNDING_BOX[2], self.LOOTING_BACKPACK_BOUNDING_BOX[1] + self.LOOTING_BACKPACK_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_QUICK_USE_LABEL_SUBREGION[:2], (self.LOOTING_QUICK_USE_LABEL_SUBREGION[0] + self.LOOTING_QUICK_USE_LABEL_SUBREGION[2], self.LOOTING_QUICK_USE_LABEL_SUBREGION[1] + self.LOOTING_QUICK_USE_LABEL_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_QUICK_USE_BOUNDING_BOX[:2], (self.LOOTING_QUICK_USE_BOUNDING_BOX[0] + self.LOOTING_QUICK_USE_BOUNDING_BOX[2], self.LOOTING_QUICK_USE_BOUNDING_BOX[1] + self.LOOTING_QUICK_USE_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_AUGMENTED_SLOTS_LABEL_SUBREGION[:2], (self.LOOTING_AUGMENTED_SLOTS_LABEL_SUBREGION[0] + self.LOOTING_AUGMENTED_SLOTS_LABEL_SUBREGION[2], self.LOOTING_AUGMENTED_SLOTS_LABEL_SUBREGION[1] + self.LOOTING_AUGMENTED_SLOTS_LABEL_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_AUGMENTED_SLOTS_BOUNDING_BOX[:2], (self.LOOTING_AUGMENTED_SLOTS_BOUNDING_BOX[0] + self.LOOTING_AUGMENTED_SLOTS_BOUNDING_BOX[2], self.LOOTING_AUGMENTED_SLOTS_BOUNDING_BOX[1] + self.LOOTING_AUGMENTED_SLOTS_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_SAFE_POCKET_LABEL_SUBREGION[:2], (self.LOOTING_SAFE_POCKET_LABEL_SUBREGION[0] + self.LOOTING_SAFE_POCKET_LABEL_SUBREGION[2], self.LOOTING_SAFE_POCKET_LABEL_SUBREGION[1] + self.LOOTING_SAFE_POCKET_LABEL_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_SAFE_POCKET_BOUNDING_BOX[:2], (self.LOOTING_SAFE_POCKET_BOUNDING_BOX[0] + self.LOOTING_SAFE_POCKET_BOUNDING_BOX[2], self.LOOTING_SAFE_POCKET_BOUNDING_BOX[1] + self.LOOTING_SAFE_POCKET_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_CONTAINER_BOUNDING_BOX[:2], (self.LOOTING_CONTAINER_BOUNDING_BOX[0] + self.LOOTING_CONTAINER_BOUNDING_BOX[2], self.LOOTING_CONTAINER_BOUNDING_BOX[1] + self.LOOTING_CONTAINER_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_KEYBINDS_BOUNDING_BOX[:2], (self.LOOTING_KEYBINDS_BOUNDING_BOX[0] + self.LOOTING_KEYBINDS_BOUNDING_BOX[2], self.LOOTING_KEYBINDS_BOUNDING_BOX[1] + self.LOOTING_KEYBINDS_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.LOOTING_SALVAGE_BOUNDING_BOX[:2], (self.LOOTING_SALVAGE_BOUNDING_BOX[0] + self.LOOTING_SALVAGE_BOUNDING_BOX[2], self.LOOTING_SALVAGE_BOUNDING_BOX[1] + self.LOOTING_SALVAGE_BOUNDING_BOX[3]), (0, 0, 255), 1)

    def _draw_map_ui(self, frame):
        # Shared UI
        cv2.rectangle(frame, self.FRAME_RATE_COUNTER_SUBREGION[:2], (self.FRAME_RATE_COUNTER_SUBREGION[0] + self.FRAME_RATE_COUNTER_SUBREGION[2], self.FRAME_RATE_COUNTER_SUBREGION[1] + self.FRAME_RATE_COUNTER_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.OVERLAY_NAVIGATION_SUBREGION[:2], (self.OVERLAY_NAVIGATION_SUBREGION[0] + self.OVERLAY_NAVIGATION_SUBREGION[2], self.OVERLAY_NAVIGATION_SUBREGION[1] + self.OVERLAY_NAVIGATION_SUBREGION[3]), (0, 0, 255), 1)

        # Map UI specific
        cv2.rectangle(frame, self.MAP_BOUNDING_BOX[:2], (self.MAP_BOUNDING_BOX[0] + self.MAP_BOUNDING_BOX[2], self.MAP_BOUNDING_BOX[1] + self.MAP_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.MAP_PLAYER_POSITION_SUBREGION[:2], (self.MAP_PLAYER_POSITION_SUBREGION[0] + self.MAP_PLAYER_POSITION_SUBREGION[2], self.MAP_PLAYER_POSITION_SUBREGION[1] + self.MAP_PLAYER_POSITION_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.MAP_LEGEND_BOUNDING_BOX[:2], (self.MAP_LEGEND_BOUNDING_BOX[0] + self.MAP_LEGEND_BOUNDING_BOX[2], self.MAP_LEGEND_BOUNDING_BOX[1] + self.MAP_LEGEND_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.MAP_DETAILS_SUBREGION[:2], (self.MAP_DETAILS_SUBREGION[0] + self.MAP_DETAILS_SUBREGION[2], self.MAP_DETAILS_SUBREGION[1] + self.MAP_DETAILS_SUBREGION[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.MAP_QUESTS_BOUNDING_BOX[:2], (self.MAP_QUESTS_BOUNDING_BOX[0] + self.MAP_QUESTS_BOUNDING_BOX[2], self.MAP_QUESTS_BOUNDING_BOX[1] + self.MAP_QUESTS_BOUNDING_BOX[3]), (0, 0, 255), 1)
        cv2.rectangle(frame, self.MAP_KEYBINDS_BOUNDING_BOX[:2], (self.MAP_KEYBINDS_BOUNDING_BOX[0] + self.MAP_KEYBINDS_BOUNDING_BOX[2], self.MAP_KEYBINDS_BOUNDING_BOX[1] + self.MAP_KEYBINDS_BOUNDING_BOX[3]), (0, 0, 255), 1)

    # Extract the stamina bar from the complete frame and calculate its value
    def _stamina_calculation(self, frame):
        stamina_bar_region = self._extract_subregion(frame, self.STAMINA_BAR_SUBREGION)
        stamina_bar_slice = self._extract_subregion(stamina_bar_region, self.STAMINA_BAR_SLICE_SUBREGION)
        slice_values = []
        for pixel in stamina_bar_slice[0]:
            white = [255, 255, 255]
            distance = abs(pixel - white).sum()
            if distance < 100:
                slice_values.append("W")
            else:
                slice_values.append("X")

        stamina_string = "".join(slice_values)
        total = len(stamina_string)
        stamina = stamina_string.count("W")

        if DEBUG:
            print(f"Raw stamina output: {stamina_string}")
            print(f"Stamina: {stamina}, Total: {total}")

        return {"stamina": stamina, "total": total}

    def _shield_calculation(self, frame):
        x, y, w, h = self.PLAYER_1_SHIELD_BOUNDING_BOX
        src_points = numpy.float32([self.PLAYER_1_SHIELD_NW_POINT, self.PLAYER_1_SHIELD_NE_POINT, self.PLAYER_1_SHIELD_SW_POINT, self.PLAYER_1_SHIELD_SE_POINT]) 
        dst_points = numpy.float32([[0, 0], [w, 0], [0, h], [w, h]])
        M = cv2.getPerspectiveTransform(src_points, dst_points)
        unwarped_image = cv2.warpPerspective(frame, M, (w, h))

        # calculate the numerical value of the shield
        slice_roi = self._extract_subregion(unwarped_image, self.PLAYER_1_SHIELD_SLICE_SUBREGION)
        slice_values = []
        for pixel in slice_roi[0]:
            blue = [167, 150, 63]
            red = [79, 77, 213]
            yellow = [54, 164, 205]
            grey = [127, 125, 122]
            black = [85, 73, 72]

            blue_delta = abs(pixel - blue).sum()
            red_delta = abs(pixel - red).sum()
            yellow_delta = abs(pixel - yellow).sum()
            grey_delta = abs(pixel - grey).sum()
            black_delta = abs(pixel - black).sum()

            min_diff = min(blue_delta, red_delta, yellow_delta, grey_delta, black_delta)

            if (blue_delta == min_diff).all():
                slice_values.append("B")
            elif (red_delta == min_diff).all():
                slice_values.append("R")
            elif (yellow_delta == min_diff).all():
                slice_values.append("Y")
            elif (grey_delta == min_diff).all():
                slice_values.append("G")
            elif (black_delta == min_diff).all():
                slice_values.append("X")
            else:
                print("No shield pixel detected")

        shield_string = "".join(slice_values)
        shield = shield_string.count("B")
        damage = shield_string.count("R")
        queued = shield_string.count("Y")
        charging = shield_string.count("G")
        total = len(shield_string)
        missing = total - len(shield_string.rstrip("X"))

        if DEBUG:
            print(f"Raw shield output: {shield_string}")
            print(f"Shield: {shield}, Damage: {damage}, Queued: {queued}, Charging: {charging}, Missing: {missing}, Total: {total}")
            print(f"Shield value: {shield}")

        return {"shield": shield, "damage": damage, "queued": queued, "charging": charging, "missing": missing, "total": total}

    def _health_calculation(self, frame):
        x, y, w, h = self.PLAYER_1_HEALTH_BOUNDING_BOX
        src_points = numpy.float32([self.PLAYER_1_HEALTH_NW_POINT, self.PLAYER_1_HEALTH_NE_POINT, self.PLAYER_1_HEALTH_SW_POINT, self.PLAYER_1_HEALTH_SE_POINT]) 
        dst_points = numpy.float32([[0, 0], [w, 0], [0, h], [w, h]])
        M = cv2.getPerspectiveTransform(src_points, dst_points)
        unwarped_image = cv2.warpPerspective(frame, M, (w, h))

        # calculate the numerical value of the health
        slice_roi = self._extract_subregion(unwarped_image, self.PLAYER_1_HEALTH_SLICE_SUBREGION)
        slice_values = []
        for pixel in slice_roi[0]:
            white = [248, 245, 246]
            red = [79, 77, 213]
            yellow = [54, 164, 205]
            grey = [127, 125, 122]
            black = [85, 73, 72]

            white_delta = abs(pixel - white).sum()
            red_delta = abs(pixel - red).sum()
            yellow_delta = abs(pixel - yellow).sum()
            grey_delta = abs(pixel - grey).sum()
            black_delta = abs(pixel - black).sum()
            min_diff = min(white_delta, red_delta, yellow_delta, grey_delta, black_delta)

            if (white_delta == min_diff).all():
                slice_values.append("W")
            elif (red_delta == min_diff).all():
                slice_values.append("R")
            elif (yellow_delta == min_diff).all():
                slice_values.append("Y")
            elif (grey_delta == min_diff).all():
                slice_values.append("G")
            elif (black_delta == min_diff).all():
                slice_values.append("X")

        health_string = "".join(slice_values)
        health = health_string.count("W")
        damage = health_string.count("R")
        queued = health_string.count("Y")
        charging = health_string.count("G")
        total = len(health_string)
        missing = total - len(health_string.rstrip("X"))

        if DEBUG:
            print(f"Raw health output: {health_string}")
            print(f"Health: {health}, Damaged: {damage}, Queued: {queued}, Charging: {charging}, Missing: {missing}, Total: {total}")

        return {"health": health, "damage": damage, "queued": queued, "charging": charging, "missing": missing, "total": total}
