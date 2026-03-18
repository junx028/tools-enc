import base64
import zlib
import os
import re
import py_compile
import binascii

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def baca_file(nama_file):
    try:
        with open(nama_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"\n[-] ERROR membaca file: {e}")
        return None

def tulis_file(nama_file, konten, mode='w'):
    try:
        with open(nama_file, mode, encoding='utf-8') as f:
            f.write(konten)
        print(f"\n[+] SUKSES! File tersimpan di: {nama_file}")
    except Exception as e:
        print(f"\n[-] ERROR menulis file: {e}")

def encode_zlib_b64():
    print("\n--- 1. ENCODE TINGKAT TINGGI (Zlib + Base64) ---")
    file_in = input("File asli: ")
    file_out = input("File hasil: ")
    
    kode = baca_file(file_in)
    if kode:
        # Kompresi lalu encode
        terkompresi = zlib.compress(kode.encode('utf-8'))
        kode_b64 = base64.b64encode(terkompresi).decode('utf-8')
        
        # Payload satu baris
        payload = f"import zlib,base64;exec(zlib.decompress(base64.b64decode('{kode_b64}')))"
        tulis_file(file_out, payload)

def decode_zlib_b64():
    print("\n--- 2. BONGKAR KODE (Zlib/Base64) ---")
    file_in = input("File yang terkunci: ")
    file_out = input("File hasil bongkaran: ")
    
    kode = baca_file(file_in)
    if kode:
        # Cari pola Base64 di dalam script
        pencarian = re.search(r"b64decode\(['\"]([^'\"]+)['\"]\)", kode)
        if pencarian:
            kode_b64 = pencarian.group(1)
            try:
                # Coba dekompresi zlib dulu, kalau gagal langsung decode base64
                data_mentah = base64.b64decode(kode_b64)
                try:
                    kode_asli = zlib.decompress(data_mentah).decode('utf-8')
                except:
                    kode_asli = data_mentah.decode('utf-8')
                tulis_file(file_out, kode_asli)
            except Exception as e:
                print(f"\n[-] Gagal membongkar: {e}")
        else:
            print("\n[-] Pola tidak ditemukan. Mungkin file ini menggunakan metode lain.")

def encode_hex():
    print("\n--- 3. ENCODE KE HEXADECIMAL ---")
    file_in = input("File asli: ")
    file_out = input("File hasil: ")
    
    kode = baca_file(file_in)
    if kode:
        kode_hex = binascii.hexlify(kode.encode('utf-8')).decode('utf-8')
        payload = f"import binascii;exec(binascii.unhexlify('{kode_hex}'))"
        tulis_file(file_out, payload)

def kunci_file_pyc():
    print("\n--- 4. KUNCI FILE (Compile ke .pyc Bytecode) ---")
    print("Catatan: File hasil (.pyc) tidak bisa diedit, hanya bisa dijalankan (python namafile.pyc)")
    file_in = input("File asli (.py): ")
    
    if os.path.exists(file_in):
        try:
            # Mengkompilasi file python menjadi bytecode
            nama_file_pyc = file_in.replace('.py', '_locked.pyc')
            py_compile.compile(file_in, cfile=nama_file_pyc)
            print(f"\n[+] SUKSES! File terkunci berhasil dibuat: {nama_file_pyc}")
        except Exception as e:
            print(f"\n[-] Gagal mengunci file: {e}")
    else:
        print("\n[-] File tidak ditemukan!")

# --- PROGRAM UTAMA ---
while True:
    bersihkan_layar()
    print("==========================================")
    print("  TOOLS SECURITY & OBFUSCATION SCRIPT  ")
    print("==========================================")
    print("1. Obfuscate Kuat (Zlib Compress + Base64)")
    print("2. Bongkar Obfuscate (Zlib/Base64)")
    print("3. Obfuscate Hexadecimal")
    print("4. KUNCI FILE (Compile ke Bytecode .pyc)")
    print("5. Keluar")
    print("==========================================")
    
    pilihan = input("Pilih menu (1-5): ")

    if pilihan == '1':
        encode_zlib_b64()
    elif pilihan == '2':
        decode_zlib_b64()
    elif pilihan == '3':
        encode_hex()
    elif pilihan == '4':
        kunci_file_pyc()
    elif pilihan == '5':
        print("\nKeluar dari program. Stay secure!")
        break
    else:
        print("\nPilihan tidak valid!")
    
    if pilihan in ['1', '2', '3', '4']:
        input("\nTekan Enter untuk kembali ke menu...")
