import socket
import requests
import winsound
import os
import subprocess
import platform
import psutil
import datetime
import time 
import threading
import versionInfo
import ui
from scriptHandler import script

def check_top_processes():
    """Menampilkan proses yang sedang berjalan"""
    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        try:
            processes.append((proc.info['name'], proc.info['cpu_percent'], proc.info['memory_info'].rss / (1024 * 1024)))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    sorted_processes = sorted(processes, key=lambda p: (p[1], p[2]), reverse=True)[:5]

    if sorted_processes:
        for proc in sorted_processes:
            ui.message(f"Proses {proc[0]}, CPU {proc[1]} persen, RAM {proc[2]:.2f} MB.")
    else:
        ui.message("Tidak ada proses yang berjalan.")

def check_ram():
    """Memeriksa penggunaan RAM secara detail"""
    ram_info = psutil.virtual_memory()
    
    total_ram = ram_info.total / (1024 ** 3)  # Konversi ke GB
    used_ram = ram_info.used / (1024 ** 3)   # Konversi ke GB
    available_ram = ram_info.available / (1024 ** 3)  # Konversi ke GB
    ram_usage_percent = ram_info.percent  # Penggunaan RAM dalam persen

    message = (
        f"RAM Total: {total_ram:.2f} GB\n"
        f"RAM Digunakan: {used_ram:.2f} GB\n"
        f"RAM Tersedia: {available_ram:.2f} GB\n"
        f"Penggunaan RAM: {ram_usage_percent} persen"
    )
    
    ui.message(message)



def check_cpu():
    """Memeriksa penggunaan CPU"""
    cpu_usage = psutil.cpu_percent(interval=1)
    ui.message(f"Penggunaan CPU: {cpu_usage} persen")


def tampilkan_info_sistem():
    # Informasi Sistem Operasi dan Platform
    jenis_os = platform.system()
    versi_os = platform.version()
    arsitektur = platform.architecture()[0]
    nama_komputer = platform.node()
    prosesor = platform.processor()
    
    # Informasi CPU
    core_fisik = psutil.cpu_count(logical=False)
    core_logis = psutil.cpu_count(logical=True)
    
    # Waktu Boot
    waktu_boot = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    
    # Menyusun Pesan
    pesan = (
        f"Sistem Operasi: {jenis_os}\n"
        f"Versi OS: {versi_os}\n"
        f"Arsitektur: {arsitektur}\n"
        f"Nama Komputer: {nama_komputer}\n"
        f"Prosesor: {prosesor}\n"
        f"Jumlah Core Fisik CPU: {core_fisik}\n"
        f"Jumlah Core Logis CPU: {core_logis}\n"
        f"Waktu Boot: {waktu_boot}"
    )
    
    # Menampilkan pesan dengan NVDA
    ui.message(pesan)


def check_usb_devices():
    """Memeriksa perangkat USB yang terhubung ke komputer."""
    try:
        # Memberi tahu pengguna bahwa proses sedang berjalan
        ui.message("Silakan tunggu, sedang memeriksa perangkat USB...")

        # Menjalankan perintah PowerShell untuk mendapatkan daftar perangkat USB
        result = subprocess.run(
            ["powershell", "-Command", "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'USB' } | Select-Object -Property FriendlyName"],
            capture_output=True,
            text=True,
            shell=True
        )

        output = result.stdout.strip()

        # Jika output kosong, tidak ada perangkat USB yang terdeteksi
        if not output:
            ui.message("Tidak ada perangkat USB yang terhubung.")
        else:
            ui.message("Perangkat USB yang terhubung:")
            for line in output.splitlines():
                if line.strip():
                    ui.message(line.strip())

    except Exception as e:
        ui.message(f"Terjadi kesalahan saat memeriksa perangkat USB: {str(e)}")


def check_windows_update():
    """Memeriksa apakah ada update Windows yang tersedia."""
    try:
        # Memberi tahu pengguna bahwa proses sedang berjalan
        ui.message("Silakan tunggu, sedang memeriksa update Windows...")

        # Menjalankan perintah PowerShell untuk mengecek update
        result = subprocess.run(
            ["powershell", "-Command", "Get-WindowsUpdate | Select-Object -Property Title, KBArticle"],
            capture_output=True,
            text=True,
            shell=True
        )

        output = result.stdout.strip()

        # Jika output kosong, tidak ada update
        if not output:
            ui.message("Tidak ada update Windows yang tersedia.")
        else:
            ui.message("Tersedia update Windows berikut:")
            for line in output.splitlines():
                ui.message(line)

    except Exception as e:
        ui.message(f"Terjadi kesalahan saat memeriksa update: {str(e)}")


def check_disk_usage():
    """Memeriksa penggunaan storage pada disk utama (C:\)."""
    try:
        # Mengambil informasi disk C:
        disk_usage = psutil.disk_usage("C:\\")
        
        total = disk_usage.total / (1024 ** 3)       # Total kapasitas (GB)
        used = disk_usage.used / (1024 ** 3)         # Kapasitas terpakai (GB)
        free = disk_usage.free / (1024 ** 3)         # Kapasitas tersedia (GB)
        percent_used = disk_usage.percent            # Persentase terpakai

        # Menampilkan informasi disk
        ui.message(
            f"Total kapasitas: {total:.2f} GB. "
            f"Terpakai: {used:.2f} GB ({percent_used} persen). "
            f"Tersedia: {free:.2f} GB."
        )
        
    except Exception as e:
        ui.message(f"Terjadi kesalahan saat memeriksa storage: {str(e)}")

# Variabel global untuk menyimpan status koneksi terakhir
last_status = None  

def check_connection_status():    
    global last_status

    while True:
        try:
            # Coba membuat koneksi ke Google untuk memeriksa koneksi
            response = requests.get("https://www.google.com", timeout=10)
            response.raise_for_status()
            connected = True
        except (requests.RequestException, OSError):
            connected = False

        # Jika status berubah dari terakhir kali, panggil checkInternet()
        if connected != last_status:
            last_status = connected  # Perbarui status terakhir
            checkInternet()  # Panggil fungsi utama

        time.sleep(10)  

# Jalankan pemeriksaan di latar belakang
thread = threading.Thread(target=check_connection_status, daemon=True)
thread.start()


def checkInternet():
    """Memeriksa status koneksi internet dan menampilkan informasi jaringan Wi-Fi."""
    try:
        response = requests.get("https://www.google.com", timeout=10)
        response.raise_for_status()
        
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            shell=True
        )
        output = result.stdout
        ssid = "Tidak terdeteksi"
        signal = "Tidak diketahui"

        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":", 1)[1].strip()
            if "Signal" in line:
                signal = line.split(":", 1)[1].strip()

        ui.message(f"Terhubung ke jaringan {ssid} dengan kekuatan sinyal {signal}.")
        
        connected_sound = os.path.join(os.path.dirname(os.path.abspath(__file__)), "connected.wav")
        if os.path.exists(connected_sound):
            winsound.PlaySound(connected_sound, winsound.SND_FILENAME)
        else:
            ui.message("File suara tidak ditemukan: connected.wav")
        
    except (requests.RequestException, OSError):
        ui.message("Perangkat tidak terhubung ke internet")
        disconnected_sound = os.path.join(os.path.dirname(os.path.abspath(__file__)), "disconnected.wav")
        if os.path.exists(disconnected_sound):
            winsound.PlaySound(disconnected_sound, winsound.SND_FILENAME)
        else:
            ui.message("File suara tidak ditemukan: disconnected.wav")



def check_battery_status():
    notified = False  # Variabel untuk memastikan notifikasi hanya dikirim sekali per kondisi
    while True:
        battery = psutil.sensors_battery()
        if battery is None:
            ui.message("Perangkat Anda tidak menggunakan baterai.")
            break
        else:
            percent = battery.percent
            if battery.power_plugged:
                ui.message(f"Baterai sedang diisi, {percent} persen.")
                notified = False  # Reset status notifikasi jika baterai sedang diisi
            else:
                if percent <= 20 and not notified:
                    ui.message("Peringatan: Baterai lemah, segera isi ulang!")
                    winsound.PlaySound("disconnected.wav", winsound.SND_FILENAME)
                    notified = True  # Hindari pengulangan notifikasi untuk kondisi yang sama
                elif percent > 20:
                    notified = False  # Reset notifikasi jika baterai kembali di atas 20%

        time.sleep(60)  # Tunggu 60 detik sebelum melakukan pengecekan lagi

# Jalankan fungsi untuk memeriksa status baterai
check_battery_status()
# fungsi check versi NVDA
def nvdaVersion():    
    ui.message(f"versi NVDA kamu {versionInfo.version}")

