import os
import sys

# Tambahkan folder root ke path Python
sys.path.insert(0, os.getcwd())

# Import buildVars
import buildVars
# Tentukan lokasi file yang akan dikemas
AddonFiles = [
    "manifest.ini",
    "globalPlugins/deviceMonitoring/__init__.py",
        "globalPlugins/deviceMonitoring/functions.py",
        "globalPlugins/deviceMonitoring/connected.wav",
        "globalPlugins/deviceMonitoring/disconnected.wav",
]

# Nama file hasil build
AddonPackage = f"{buildVars.addon_name}-{buildVars.addon_version}.nvda-addon"

# Proses build
env = Environment()
env.Zip(AddonPackage, AddonFiles)

print(f"Addon berhasil dibuat: {AddonPackage}")
