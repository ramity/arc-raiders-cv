import os
import re
import sys
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

# 2025-11-21-01-26

# URLS sourced from using steps at docs/scrape-loot-steps.md

URLS = [
  "https://arcraiders.wiki/wiki/Advanced_ARC_Powercell",
  "https://arcraiders.wiki/wiki/Advanced_Electrical_Components",
  "https://arcraiders.wiki/wiki/Advanced_Mechanical_Components",
  "https://arcraiders.wiki/wiki/Agave",
  "https://arcraiders.wiki/wiki/Air_Freshener",
  "https://arcraiders.wiki/wiki/Alarm_Clock",
  "https://arcraiders.wiki/wiki/Antiseptic",
  "https://arcraiders.wiki/wiki/Apricot",
  "https://arcraiders.wiki/wiki/ARC_Alloy",
  "https://arcraiders.wiki/wiki/ARC_Circuitry",
  "https://arcraiders.wiki/wiki/ARC_Coolant",
  "https://arcraiders.wiki/wiki/ARC_Flex_Rubber",
  "https://arcraiders.wiki/wiki/ARC_Motion_Core",
  "https://arcraiders.wiki/wiki/ARC_Performance_Steel",
  "https://arcraiders.wiki/wiki/ARC_Powercell",
  "https://arcraiders.wiki/wiki/ARC_Synthetic_Resin",
  "https://arcraiders.wiki/wiki/ARC_Thermo_Lining",
  "https://arcraiders.wiki/wiki/Assorted_Seeds",
  "https://arcraiders.wiki/wiki/Bastion_Cell",
  "https://arcraiders.wiki/wiki/Battery",
  "https://arcraiders.wiki/wiki/Bicycle_Pump",
  "https://arcraiders.wiki/wiki/Bloated_Tuna_Can",
  "https://arcraiders.wiki/wiki/Blue_Gate_Communication_Tower_Key",
  "https://arcraiders.wiki/wiki/Blue_Gate_Confiscation_Room_Key",
  "https://arcraiders.wiki/wiki/Blue_Gate_Cellar_Key",
  "https://arcraiders.wiki/wiki/Blue_Gate_Village_Key",
  "https://arcraiders.wiki/wiki/Bombardier_Cell",
  "https://arcraiders.wiki/wiki/Breathtaking_Snow_Globe",
  "https://arcraiders.wiki/wiki/Broken_Flashlight",
  "https://arcraiders.wiki/wiki/Broken_Guidance_System",
  "https://arcraiders.wiki/wiki/Broken_Handheld_Radio",
  "https://arcraiders.wiki/wiki/Broken_Taser",
  "https://arcraiders.wiki/wiki/Buried_City_Hospital_Key",
  "https://arcraiders.wiki/wiki/Buried_City_JKV_Employee_Access_Card",
  "https://arcraiders.wiki/wiki/Buried_City_Residential_Mastery_Key",
  "https://arcraiders.wiki/wiki/Buried_City_Town_Hall_Key",
  "https://arcraiders.wiki/wiki/Burned_ARC_Circuitry",
  "https://arcraiders.wiki/wiki/Camera_Lens",
  "https://arcraiders.wiki/wiki/Candle_Holder",
  "https://arcraiders.wiki/wiki/Canister",
  "https://arcraiders.wiki/wiki/Cat_Bed",
  "https://arcraiders.wiki/wiki/Chemicals",
  "https://arcraiders.wiki/wiki/Coffee_Pot",
  "https://arcraiders.wiki/wiki/Complex_Gun_Parts",
  "https://arcraiders.wiki/wiki/Coolant",
  "https://arcraiders.wiki/wiki/Cooling_Coil",
  "https://arcraiders.wiki/wiki/Cooling_Fan",
  "https://arcraiders.wiki/wiki/Cracked_Bioscanner",
  "https://arcraiders.wiki/wiki/Crude_Explosives",
  "https://arcraiders.wiki/wiki/Crumpled_Plastic_Bottle",
  "https://arcraiders.wiki/wiki/Dam_Control_Tower_Key",
  "https://arcraiders.wiki/wiki/Dam_Staff_Room_Key",
  "https://arcraiders.wiki/wiki/Dam_Surveillance_Key",
  "https://arcraiders.wiki/wiki/Dam_Testing_Annex_Key",
  "https://arcraiders.wiki/wiki/Dam_Utility_Key",
  "https://arcraiders.wiki/wiki/Damaged_ARC_Motion_Core",
  "https://arcraiders.wiki/wiki/Damaged_ARC_Powercell",
  "https://arcraiders.wiki/wiki/Damaged_Fireball_Burner",
  "https://arcraiders.wiki/wiki/Damaged_Heat_Sink",
  "https://arcraiders.wiki/wiki/Damaged_Hornet_Driver",
  "https://arcraiders.wiki/wiki/Damaged_Rocketeer_Driver",
  "https://arcraiders.wiki/wiki/Damaged_Snitch_Scanner",
  "https://arcraiders.wiki/wiki/Damaged_Tick_Pod",
  "https://arcraiders.wiki/wiki/Damaged_Wasp_Driver",
  "https://arcraiders.wiki/wiki/Dart_Board",
  "https://arcraiders.wiki/wiki/Deflated_Football",
  "https://arcraiders.wiki/wiki/Degraded_ARC_Rubber",
  "https://arcraiders.wiki/wiki/Diving_Goggles",
  "https://arcraiders.wiki/wiki/Dog_Collar",
  "https://arcraiders.wiki/wiki/Dried-Out_ARC_Resin",
  "https://arcraiders.wiki/wiki/Duct_Tape",
  "https://arcraiders.wiki/wiki/Durable_Cloth",
  "https://arcraiders.wiki/wiki/Electrical_Components",
  "https://arcraiders.wiki/wiki/Empty_Wine_Bottle",
  "https://arcraiders.wiki/wiki/Exodus_Modules",
  "https://arcraiders.wiki/wiki/Expired_Pasta",
  "https://arcraiders.wiki/wiki/Expired_Respirator",
  "https://arcraiders.wiki/wiki/Explosive_Compound",
  "https://arcraiders.wiki/wiki/Fabric",
  "https://arcraiders.wiki/wiki/Faded_Photograph",
  "https://arcraiders.wiki/wiki/Fertilizer",
  "https://arcraiders.wiki/wiki/Film_Reel",
  "https://arcraiders.wiki/wiki/Fine_Wristwatch",
  "https://arcraiders.wiki/wiki/Fireball_Burner",
  "https://arcraiders.wiki/wiki/Frequency_Modulation_Box",
  "https://arcraiders.wiki/wiki/Fried_Motherboard",
  "https://arcraiders.wiki/wiki/Frying_Pan",
  "https://arcraiders.wiki/wiki/Garlic_Press",
  "https://arcraiders.wiki/wiki/Geiger_Counter",
  "https://arcraiders.wiki/wiki/Great_Mullein",
  "https://arcraiders.wiki/wiki/Headphones",
  "https://arcraiders.wiki/wiki/Heavy_Gun_Parts",
  "https://arcraiders.wiki/wiki/Hornet_Driver",
  "https://arcraiders.wiki/wiki/Household_Cleaner",
  "https://arcraiders.wiki/wiki/Humidifier",
  "https://arcraiders.wiki/wiki/Ice_Cream_Scooper",
  "https://arcraiders.wiki/wiki/Impure_ARC_Coolant",
  "https://arcraiders.wiki/wiki/Industrial_Battery",
  "https://arcraiders.wiki/wiki/Industrial_Charger",
  "https://arcraiders.wiki/wiki/Industrial_Magnet",
  "https://arcraiders.wiki/wiki/Ion_Sputter",
  "https://arcraiders.wiki/wiki/Laboratory_Reagents",
  "https://arcraiders.wiki/wiki/Lance%27s_Mixtape_(5th_Edition)",
  "https://arcraiders.wiki/wiki/Lemon",
  "https://arcraiders.wiki/wiki/Leaper_Pulse_Unit",
  "https://arcraiders.wiki/wiki/Light_Bulb",
  "https://arcraiders.wiki/wiki/Light_Gun_Parts",
  "https://arcraiders.wiki/wiki/Magnet",
  "https://arcraiders.wiki/wiki/Magnetic_Accelerator",
  "https://arcraiders.wiki/wiki/Magnetron",
  "https://arcraiders.wiki/wiki/Matriarch_Reactor",
  "https://arcraiders.wiki/wiki/Mechanical_Components",
  "https://arcraiders.wiki/wiki/Medium_Gun_Parts",
  "https://arcraiders.wiki/wiki/Metal_Brackets",
  "https://arcraiders.wiki/wiki/Metal_Parts",
  "https://arcraiders.wiki/wiki/Microscope",
  "https://arcraiders.wiki/wiki/Mini_Centrifuge",
  "https://arcraiders.wiki/wiki/Mod_Components",
  "https://arcraiders.wiki/wiki/Moss",
  "https://arcraiders.wiki/wiki/Motor",
  "https://arcraiders.wiki/wiki/Mushroom",
  "https://arcraiders.wiki/wiki/Music_Album",
  "https://arcraiders.wiki/wiki/Music_Box",
  "https://arcraiders.wiki/wiki/Number_Plate",
  "https://arcraiders.wiki/wiki/Oil",
  "https://arcraiders.wiki/wiki/Olives",
  "https://arcraiders.wiki/wiki/Painted_Box",
  "https://arcraiders.wiki/wiki/Patrol_Car_Key",
  "https://arcraiders.wiki/wiki/Plastic_Parts",
  "https://arcraiders.wiki/wiki/Playing_Cards",
  "https://arcraiders.wiki/wiki/Polluted_Air_Filter",
  "https://arcraiders.wiki/wiki/Pop_Trigger",
  "https://arcraiders.wiki/wiki/Portable_TV",
  "https://arcraiders.wiki/wiki/Poster_Of_Natural_Wonders",
  "https://arcraiders.wiki/wiki/Pottery",
  "https://arcraiders.wiki/wiki/Power_Bank",
  "https://arcraiders.wiki/wiki/Power_Cable",
  "https://arcraiders.wiki/wiki/Power_Rod",
  "https://arcraiders.wiki/wiki/Prickly_Pear",
  "https://arcraiders.wiki/wiki/Processor",
  "https://arcraiders.wiki/wiki/Projector",
  "https://arcraiders.wiki/wiki/Queen_Reactor",
  "https://arcraiders.wiki/wiki/Radio",
  "https://arcraiders.wiki/wiki/Radio_Relay",
  "https://arcraiders.wiki/wiki/Raider_Hatch_Key",
  "https://arcraiders.wiki/wiki/Red_Coral_Jewelry",
  "https://arcraiders.wiki/wiki/Remote_Control",
  "https://arcraiders.wiki/wiki/Resin",
  "https://arcraiders.wiki/wiki/Ripped_Safety_Vest",
  "https://arcraiders.wiki/wiki/Rocket_Thruster",
  "https://arcraiders.wiki/wiki/Rocketeer_Driver",
  "https://arcraiders.wiki/wiki/Roots",
  "https://arcraiders.wiki/wiki/Rope",
  "https://arcraiders.wiki/wiki/Rosary",
  "https://arcraiders.wiki/wiki/Rotary_Encoder",
  "https://arcraiders.wiki/wiki/Rubber_Duck",
  "https://arcraiders.wiki/wiki/Rubber_Pad",
  "https://arcraiders.wiki/wiki/Rubber_Parts",
  "https://arcraiders.wiki/wiki/Ruined_Accordion",
  "https://arcraiders.wiki/wiki/Ruined_Augment",
  "https://arcraiders.wiki/wiki/Ruined_Baton",
  "https://arcraiders.wiki/wiki/Ruined_Handcuffs",
  "https://arcraiders.wiki/wiki/Ruined_Parachute",
  "https://arcraiders.wiki/wiki/Ruined_Tactical_Vest",
  "https://arcraiders.wiki/wiki/Ruined_Riot_Shield",
  "https://arcraiders.wiki/wiki/Rusted_Bolts",
  "https://arcraiders.wiki/wiki/Rusted_Gear",
  "https://arcraiders.wiki/wiki/Rusted_Shut_Medical_Kit",
  "https://arcraiders.wiki/wiki/Rusted_Tools",
  "https://arcraiders.wiki/wiki/Rusty_ARC_Steel",
  "https://arcraiders.wiki/wiki/Sample_Cleaner",
  "https://arcraiders.wiki/wiki/Sensors",
  "https://arcraiders.wiki/wiki/Sentinel_Firing_Core",
  "https://arcraiders.wiki/wiki/Shredder_Gyro",
  "https://arcraiders.wiki/wiki/Signal_Amplifier",
  "https://arcraiders.wiki/wiki/Silver_Teaspoon_Set",
  "https://arcraiders.wiki/wiki/Simple_Gun_Parts",
  "https://arcraiders.wiki/wiki/Snitch_Scanner",
  "https://arcraiders.wiki/wiki/Spaceport_Container_Storage_Key",
  "https://arcraiders.wiki/wiki/Spaceport_Control_Tower_Key",
  "https://arcraiders.wiki/wiki/Spaceport_Trench_Tower_Key",
  "https://arcraiders.wiki/wiki/Spaceport_Warehouse_Key",
  "https://arcraiders.wiki/wiki/Speaker_Component",
  "https://arcraiders.wiki/wiki/Spectrometer",
  "https://arcraiders.wiki/wiki/Spectrum_Analyzer",
  "https://arcraiders.wiki/wiki/Spring_Cushion",
  "https://arcraiders.wiki/wiki/Spotter_Relay",
  "https://arcraiders.wiki/wiki/Statuette",
  "https://arcraiders.wiki/wiki/Steel_Spring",
  "https://arcraiders.wiki/wiki/Stella_Montis_Archives_Key",
  "https://arcraiders.wiki/wiki/Stella_Montis_Assembly_Admin_Key",
  "https://arcraiders.wiki/wiki/Stella_Montis_Medical_Storage_Key",
  "https://arcraiders.wiki/wiki/Stella_Montis_Security_Checkpoint_Key",
  "https://arcraiders.wiki/wiki/Surveyor_Vault",
  "https://arcraiders.wiki/wiki/Synthesized_Fuel",
  "https://arcraiders.wiki/wiki/Syringe",
  "https://arcraiders.wiki/wiki/Tattered_ARC_Lining",
  "https://arcraiders.wiki/wiki/Tattered_Clothes",
  "https://arcraiders.wiki/wiki/Telemetry_Transceiver",
  "https://arcraiders.wiki/wiki/Thermostat",
  "https://arcraiders.wiki/wiki/Tick_Pod",
  "https://arcraiders.wiki/wiki/Toaster",
  "https://arcraiders.wiki/wiki/Torn_Book",
  "https://arcraiders.wiki/wiki/Torn_Blanket",
  "https://arcraiders.wiki/wiki/Turbo_Pump",
  "https://arcraiders.wiki/wiki/Unusable_Weapon",
  "https://arcraiders.wiki/wiki/Vase",
  "https://arcraiders.wiki/wiki/Very_Comfortable_Pillow",
  "https://arcraiders.wiki/wiki/Volcanic_Rock",
  "https://arcraiders.wiki/wiki/Voltage_Converter",
  "https://arcraiders.wiki/wiki/Wasp_Driver",
  "https://arcraiders.wiki/wiki/Water_Filter",
  "https://arcraiders.wiki/wiki/Water_Pump",
  "https://arcraiders.wiki/wiki/Wires"
]

DOWNLOAD_DIR = "/root/assets/loot"
DOWNLOAD_ALL_IMAGES = False
REQUEST_TIMEOUT = 15

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(name):
    name = re.sub(r'[^A-Za-z0-9._-]', '_', name)
    return name[:250]  # keep length reasonable

def filename_from_url(url):
    p = urlparse(url)
    base = os.path.basename(p.path) or "image"
    return sanitize_filename(base)

def filename_from_cd(cd):
    # Content-Disposition: attachment; filename="fname.jpg"
    if not cd:
        return None
    m = re.search(r'filename\*?=(?:UTF-8\'\')?["\']?([^"\';]+)', cd)
    if m:
        return sanitize_filename(m.group(1))
    return None

def download_image(img_url, session, referer=None):
    if img_url.startswith("data:"):
        print("  - Skipping data URI image.")
        return None
    headers = {}
    if referer:
        headers['Referer'] = referer
    try:
        resp = session.get(img_url, stream=True, timeout=REQUEST_TIMEOUT, headers=headers)
        resp.raise_for_status()
    except Exception as e:
        print(f"  - Failed to download {img_url}: {e}")
        return None

    # Determine filename
    cd = resp.headers.get('content-disposition')
    fname = filename_from_cd(cd) or filename_from_url(img_url)
    # Add extension if missing and Content-Type provides one
    if "." not in fname or fname.endswith("image"):
        ctype = resp.headers.get('content-type', '')
        if '/' in ctype:
            ext = ctype.split('/')[-1].split(';')[0]
            if ext and not fname.lower().endswith(f".{ext}"):
                fname = f"{fname}.{ext}"
    fname = sanitize_filename(fname)
    path = os.path.join(DOWNLOAD_DIR, fname)
    # Ensure unique filename
    base, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f"{base}_{counter}{ext}"
        counter += 1
    try:
        with open(path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"  - Error saving {img_url} -> {path}: {e}")
        return None
    return path

def process_url(url, session):
    if not url or not url.strip():
        print("Skipping empty/invalid URL.")
        return []
    print(f"Processing: {url}")
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        print(f"  - Failed to fetch page: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    imgs = soup.find_all("img", class_="mw-file-element")
    if not imgs:
        print("  - No <img> tags found on page.")
        return []

    results = []
    targets = imgs if DOWNLOAD_ALL_IMAGES else imgs[:1]
    for i, img in enumerate(targets, start=1):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if not src:
            print(f"  - img #{i} has no src attribute, skipping.")
            continue
        full_url = urljoin(resp.url, src)  # resolves relative URLs, handles redirects
        print(f"  - Found img: {full_url}")
        saved = download_image(full_url, session, referer=resp.url)
        if saved:
            print(f"    -> saved to {saved}")
            results.append(saved)
    return results

def main():
    if not URLS or all(not u.strip() for u in URLS):
        print("No valid URLs provided in `URLS`. Please edit the URLS list in the script.")
        sys.exit(1)

    s = requests.Session()
    s.headers.update({
        "User-Agent": "img-downloader/1.0 (+https://example.com)"
    })

    all_saved = []
    for u in URLS:
        saved = process_url(u, s)
        all_saved.extend(saved)

    print("\nDone.")
    if all_saved:
        print("Downloaded files:")
        for p in all_saved:
            print(" -", p)
    else:
        print("No images were downloaded.")

if __name__ == "__main__":
    main()
