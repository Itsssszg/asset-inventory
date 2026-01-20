import re
from sqlalchemy.orm import sessionmaker
from app.db.session import engine
from app.schemas.asset import AssetCreate
from app.crud.asset import create_asset

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def parse_inventory_data(data):
    assets = []
    category = "Network Devices"
    subcategory = None
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('- '):
            # Item with quantity
            match = re.match(r'- (.+) - \((\d+|Too many to count.*)\)', line)
            if match:
                name = match.group(1).strip()
                qty_str = match.group(2).strip()
                if 'Too many to count' in qty_str:
                    qty = 100  # Default for too many
                else:
                    qty = int(qty_str.replace('x', ''))
                for i in range(qty):
                    asset_tag = f"{name.replace(' ', '_').upper()}_{i+1:03d}"
                    assets.append(AssetCreate(
                        asset_tag=asset_tag,
                        name=name,
                        category=category,
                        subcategory=subcategory,
                        asset_type="Hardware"
                    ))
        elif not line.startswith('Cables') and not line.startswith('Cords') and not line.startswith('Battery') and not line.startswith('Power Supply') and not line.startswith('Wireless Router') and not line.startswith('Charger') and not line.startswith('Crimping Tool') and not line.startswith('RJ45') and not line.startswith('Box of staples') and not line.startswith('Screws and Washers') and not line.startswith('Finisar USB Optical Transceiver') and not line.startswith('Pencil') and not line.startswith('RAM') and not line.startswith('STORAGE') and not line.startswith('Dell USB Port Replicator') and not line.startswith('Air Quality Device') and not line.startswith('DELL Server Caddy') and not line.startswith('DELL 16GB iDRAC Flash') and not line.startswith('Cable Tester') and not line.startswith('Flash drives'):
            subcategory = line
    return assets

def main():
    inventory_data = """
Network Devices

Cables
- Optical Fiber Cable 50/125 ZIPCORD 115304 type OFNP (ETL) C(ETL) - (1x)
- AMP Incorporated Optical Fiber Cable 62 5/125 Type OFNR (UL) C(UL) - (3x)
- OFNP RoHS PLENUM 2.0 Cable 033274FT 1231 E207090 (UL) C(UL) PLUS CORN1NG SMF-28 ULTRA - (1x)
- TYCO Electronic OPTICAL FIBER CABLE 50/125 XG 2.0Mm ZIPCORD - (1x)
- TYPE C Cable - (1x)
- CAT6 Cable - (16x)
- CAT5 Cable - (1x)
- CAT6 Premium - (1x)
- Black Cable - (1x)

Cords
- WALTHER Electric 211 3 06 - (1x)


Battery
- AA Battery - (4x)
- AAA Battery - (1x)
- Laptop Lenovo Battery - (1x)


Power Supply PW118 KA0502N59 - (1x)
DELL Front Bezel - (4x)
Heat Sink - (1x)

Wireless Router BELKIN - (1x)

Charger
- DELL Laptop Charger - (3x)
- AD/DC Adapter - (1x)
- HP Laptop Charger - (1x)
- CISCO ASA 5505 - (1x)
- Switching Adapter - (1x)

HDI 2VG Adapter - (1x)

Crimping Tool
- CD-R KING DA Series MODEL: DC-CRP-315 - (1x)
- KOION HY-210C FOR CORD 8P8C USE (1x)
- EAGLE Modular Crimping Tool (3 in 1) - (2x)
- UNISO UUT-001 - (1x)
- Ratcheting Modular Crimping Tool with Wire Stripper - (1x)

RJ45
Big - (68x)
Small - (193x)
Rubber Covers - (Too many to count)

Box of staples - (2x)

Screws and Washers - (Too many to count, let's say 420x)
Finisar USB Optical Transceiver - (Too many to count, Let's say 120x)
Pencil - (1x)

RAM
- Hynix 2GB 2Rx8 PC3-10600R-9-10-80 - (13x)
- SK Hynix 16GB 4Rx4-8500R-7-12-F0 - (4x)
- SAMSUNG 8GB 2Rx4 PC3L-10600R-09-11-E2-P2 - (8x)
- SAMSUNG 1GB 1Rx8 PC3-10600R-09-10-A0 - (6x)
- SAMSUNG 2GB 2Rx8-10600R-09-11-B1-D3 - (6x)
- Kingston 1GB KVR533D2N4/1G - (2x)
- Kingston 4GB KTD-XPS730A/4G - (1x)
- IBM 256MB P/N 38L4786 - (3x)
- ID11410B2G 256MB - (2x)
- SMART 4GB - (2x)
- CRUCIAL - (3x)

STORAGE
- SEAGATE 250GB Barracuda 7200.12 - (3x)
- SEAGATE 6GBs SAVVIO 10K.6 - (1x)
- DELL 900GB - (1x)



Dell USB Port Replicator - (6x)
Air Quality Device - (1x)
DELL Server Caddy - (2x)
DELL 16GB iDRAC Flash - (1x)

Cable Tester
- 189


Flash drives
- KINGSTON 16GB - (2x)
- MICRO SV USB 2.0 - (1x)
- DWA-131 - (1x)
"""

    assets = parse_inventory_data(inventory_data)
    db = SessionLocal()
    try:
        for asset in assets:
            create_asset(db, asset)
        print(f"Inserted {len(assets)} assets into the database.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
