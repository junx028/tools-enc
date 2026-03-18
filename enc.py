import base64

# 1. Tentukan nama file target dan nama file hasil output
file_target = 'enforcer.py' 
file_hasil = 'script_hasil.py'

try:
    # 2. Baca isi file Python mentah
    with open(file_target, 'r', encoding='utf-8') as f:
        kode_mentah = f.read()

    # 3. Ubah kode menjadi Base64
    kode_b64 = base64.b64encode(kode_mentah.encode('utf-8')).decode('utf-8')

    # 4. Susun menjadi satu baris menyamping dengan pemisah titik koma
    kode_sebaris = f"import base64;exec(base64.b64decode('{kode_b64}'))"

    # 5. Simpan hasilnya ke file baru
    with open(file_hasil, 'w', encoding='utf-8') as f:
        f.write(kode_sebaris)
        
    print(f"[+] Sukses! Kode berhasil dijadikan satu baris dan disimpan di {file_hasil}")

except FileNotFoundError:
    print(f"[-] Ups, file '{file_target}' tidak ditemukan. Pastikan ada di folder yang sama ya!")
