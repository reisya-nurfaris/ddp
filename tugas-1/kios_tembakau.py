#========= modules =========#
from prettytable import PrettyTable
from pwinput import pwinput


#========= dict =========#
data_kios = {
    "user": {
        "jojon": {
            "password": "12345",
            "saldo":1000000,
            "e-money": 90000,
            "vip": True,
            "keranjang": {}
        },
        "kipli": {
            "password": "kipluy",
            "saldo": 500000,
            "e-money": 0,
            "vip": False,
            "keranjang": {}
        }
    },
    "produk": {
        "tembakau": {
            "gayo aceh": {"harga": 25000, "tipe": "lokal"},
            "esse change grape": {"harga": 20000, "tipe": "lokal"},
            "virginia": {"harga": 20000, "tipe": "impor"},
            "barrack lemon": {"harga": 20000, "tipe": "lokal"},
            "captain black": {"harga": 28000, "tipe": "impor"},
            "black cavendish": {"harga": 30000, "tipe": "impor"}
        },
        "kertas": {
            "kertas buffalo 100lbr": {"harga": 5000, "tipe": "tawar"},
            "kertas esse coffee 100lbr": {"harga": 5000, "tipe": "manis"},
            "kertas mascotte zig-zag 100lbr": {"harga": 10000, "tipe": "tawar"}
        },
        "roller": {
            "roller plastik 110mm": {"harga": 15000},
            "roller kain serap 110mm": {"harga": 20000},
            "roller otomatis 80mm": {"harga": 100000},
            "roller raw classic 80mm": {"harga": 18000},
            "roller OCB metal 110mm": {"harga": 25000}
        },
        "filter": {
            "filter menthol 50g": {"harga": 20000},
            "filter reguler 50g": {"harga": 15000},
            "filter esse menthol 50g": {"harga": 25000}
        }
    },
    "voucher": {
        "gacor50": {"diskon": 50, "dipakai": False},
        "linting22": {"diskon": 22,"dipakai": False}
    }
}


#========= vars =========#
daftar_kategori = list(data_kios["produk"].keys())


#========= funcs =========#
def intinput(prompt):
    while True:
        try:
            parsed_input = int(input(prompt))
            if parsed_input > 0:
                return parsed_input
            elif parsed_input <= 0:
                print("Input harus lebih dari 0\n")
        except:
            print("Input hanya bisa berupa angka\n")

def format_uang(nominal):
    return f"Rp{nominal:,.0f}".replace(',','.')


def menu_akun():
    print(f"\n{'='*10} Akun {'='*10}")
    print(f"{username} | Member {'VIP' if user['vip'] else 'biasa'}")
    print(f"\nSaldo: {user['saldo']}")
    print(f"e-money: {user['e-money']}")
    if not user["vip"]:
        print("\n[1] Upgrade ke VIP")
        print("[2] Kembali")
        while True:
            pilihan = intinput("Masukkan pilihan anda: ")
            if pilihan == 1:
                print(f"\n{'='*10} Upgrade ke VIP {'='*10}")
                print("Keuntungan menjadi member VIP:")
                print("- Potongan harga sebesar 30% di setiap pembelian tanpa menggunakan voucher")
                print("- Metode pembayaran cashless")
                print("\nHarga VIP per bulan: Rp100.000\n")
                pilihan = input("Apakah anda ingin menjadi member VIP? [y/n]: ")
                while True:
                    if pilihan == 'y':
                        if user["saldo"] >= 50000:
                            user["vip"] = True
                            user["saldo"] -= 50000
                            print("Anda telah menjadi member VIP")
                            menu_akun()
                            break
                        else:
                            print("Saldo anda tidak mencukupi")
                    elif pilihan == 'n':
                        menu_akun()
                        break
                    else:
                        print("Pilihan tidak valid")
            elif pilihan == 2:
                menu_utama()
                break
    else:
        print("[1] Tambah e-money")
        print("[2] Kembali")
        while True:
            pilihan = intinput("Masukkan pilihan anda: ")
            if pilihan == 1:
                jumlah = intinput("Masukkan jumlah yang diinginkan: ")
                if jumlah <= user["saldo"]:
                    user["saldo"] -= jumlah
                    user["e-money"] += jumlah
                    print(f"Berhasil menambahkan {format_uang(jumlah)} ke e-money anda")
                    menu_akun()
                    break
                else:
                    print("Saldo anda tidak mencukupi")
            elif pilihan == 2:
                menu_utama()
                break
            else:
                print("Pilihan tidak valid")

def menu_keranjang():
    tabel_keranjang = PrettyTable()
    tabel_keranjang.title = "Keranjang"
    tabel_keranjang.field_names = ["Nama Produk", "Harga", "Jumlah", "Total"]
    harga_total = 0
    for nama_item in list(user['keranjang'].keys()):
        item = user["keranjang"][nama_item]
        harga_total += item["jumlah"]*item["harga"]
        if item["kategori"] == "tembakau":
            harga_item = f"{format_uang(item['harga'])}/50g"
            jumlah = f"{item['jumlah']*50:.0f}g"
        else:
            jumlah = item['jumlah']
            harga_item = format_uang(item["harga"])

        tabel_keranjang.add_row([f"{nama_item}".title(), harga_item, jumlah, format_uang(item["jumlah"]*item["harga"])])

    tabel_keranjang.add_row(['-'*10, '-'*10, '-'*10, '-'*10])
    tabel_keranjang.add_row(['','',"Subtotal:", format_uang(harga_total)])
    print(tabel_keranjang)
    print("[1] Bayar")
    print("[2] Kembali")
    pilihan = intinput("masukkan pilihan anda: ")
    if pilihan == 1:
        if user["vip"]:
            print("[1] Cash")
            print("[2] e-money")
            pilihan = intinput("Masukkan plihan anda: ")

            if pilihan == 1:
                metode = "saldo"
            elif pilihan == 2:
                metode = "e-money"
            diskon = 30
        else:
            metode = "saldo"
            kode_voucher = input("Masukkan kode voucher. Tekan [n] untuk tidak pakai voucher: ")
            if kode_voucher in list(data_kios["voucher"].keys()):
                diskon = data_kios["voucher"][kode_voucher]["diskon"]
                data_kios["voucher"][kode_voucher]["dipakai"] = True
            elif kode_voucher == 'n':
                diskon = 0
            else:
                print("Kode voucher tidak ditemukan")

        harga_potongan = harga_total - (harga_total * (diskon / 100))

        if user[metode] >= harga_potongan:
            tabel_keranjang.add_row(['','',"Potongan:", f"{diskon}% (-{format_uang(harga_total * (diskon / 100))})"])
            tabel_keranjang.add_row(['','',"Total:", format_uang(harga_potongan)])
            tabel_keranjang.add_row(['','',f"{metode.replace('saldo','Cash')}:", format_uang(user[metode])])
            tabel_keranjang.add_row(['','',"Kembali:", format_uang(user[metode] - harga_potongan)])
            user[metode] -= harga_potongan
            user["keranjang"] = {}
            tabel_keranjang.title = "Kios Tembakau Kretek Bacco"
            print(tabel_keranjang)
            print("Terima kasih telah belanja di kios kami")
            print("[1] Kembali ke menu produk")
            print("[2] Log out")
            pilihan = intinput("Masukkan pilihan anda: ")
            if pilihan == 1:
                menu_produk()
            elif pilihan == 2:
                menu_awal()
        else:
            print(f"{metode.title()} anda tidak mencukupi")
    elif pilihan == 2:
        menu_produk()

def menu_produk():
    while True:
        print(f"\n{'='*10} Kategori Produk {'='*10}")
        print("[1] Tembakau")
        print("[2] Kertas")
        print("[3] Roller")
        print("[4] Filter")
        print("[5] Kembali")
        pilihan = intinput("masukkan pilihan anda: ")
        if pilihan <= len(daftar_kategori):
            kategori = daftar_kategori[pilihan-1]

            daftar_nama_produk = list(data_kios["produk"][kategori].keys())
            tabel_produk = PrettyTable()
            tabel_produk.title = kategori.title()
            if kategori == "tembakau":
                tabel_produk.field_names = ["No", "Nama", "Harga/50g", "Tipe"]
                has_type = True
            elif "tipe" in data_kios["produk"][kategori][daftar_nama_produk[0]]:
                tabel_produk.field_names = ["No", "Nama", "Harga", "Tipe"]
                has_type = True
            else:
                has_type = False
                tabel_produk.field_names = ["No", "Nama", "Harga"]

            for i, nama_produk in enumerate(daftar_nama_produk, start=1):
                produk = data_kios["produk"][kategori][nama_produk]
                if has_type:
                    tabel_produk.add_row([i, nama_produk.title(), format_uang(produk["harga"]), produk["tipe"]])
                else:
                    tabel_produk.add_row([i, nama_produk.title(), format_uang(produk["harga"])])
            print(tabel_produk)

            print("[1] Tambah barang ke keranjang")
            print("[2] Kembali ke kategori")
            while True:
                pilihan = intinput("masukkan pilihan anda: ")
                if pilihan == 1:
                    while True:
                        no = intinput("\nNomor barang: ")
                        
                        ada = False
                        for i, nama_produk in enumerate(daftar_nama_produk, start=1):
                            if i == no:
                                ada = True
                                if kategori == "tembakau":
                                    while True:
                                        jumlah = intinput("Berapa gram?: ") / 50
                                        if jumlah < 1:
                                            print("\nMinimal 50 gram\n")
                                        else:
                                            break
                                else:
                                    while True:
                                        jumlah = intinput("jumlah: ")
                                        if jumlah < 1:
                                            print("\nMinimal 1\n")
                                        else:
                                            break
                                
                                if kategori == "tembakau":
                                    pak = f"{jumlah*50:.0f}g"
                                elif kategori == "kertas":
                                    pak = f"{jumlah} buku"
                                elif kategori == "filter":
                                    pak = f"{jumlah} bungkus"
                                else:
                                    pak = jumlah

                                if nama_produk in list(user["keranjang"].keys()):
                                    user["keranjang"][nama_produk]["jumlah"] += jumlah
                                else:
                                    user["keranjang"].update({nama_produk:{"kategori": kategori, "harga": produk["harga"], "jumlah": jumlah}})
                                    
                                print(f"\n{pak} {nama_produk} telah ditambahkan ke keranjang\n")

                                print("[1] Tambah barang lagi")
                                print("[2] Lihat Keranjang")
                                print("[3] Kembali ke kategori")
                                while True:
                                    pilihan = intinput("Masukkan pilihan: ")
                                    if pilihan == 1:
                                        break
                                    elif pilihan == 2:
                                        menu_keranjang()
                                        break
                                    elif pilihan == 3:
                                        menu_produk()
                                        break
                                    else:
                                        print("Pilihan tidak valid")
                        if not ada:
                            print("\nNomor barang tidak valid\n")

                elif pilihan == 2:
                    menu_produk()
                else:
                    print("Pilihan tidak valid")
        elif pilihan == 5:
            menu_utama()
        else:
            print("Pilihan tidak valid")

def register():
    print(f"\n{'='*10} Register {'='*10}")
    while True:
        username = input("Masukkan username anda: ").strip()
        if username in data_kios["user"]:
            print("Username sudah dipakai, silahkan pilih username lain\n")
        elif len(username) < 4:
            print("Username harus memiliki minimal 4 karakter\n")
        else:
            break

    while True:
        password = pwinput("Masukkan password anda: ").strip()
        if len(password) < 4:
            print("Password harus memiliki minimal 4 karakter\n")
        else:
            break
    
    data_kios["user"][username] = {
        "password": password,
        "saldo": 500000,
        "e-money": 0,
        "vip": False,
        "keranjang": {}
    }
    print(f"\nRegistrasi berhasil. Selamat datang {username}!")
    menu_utama()
    
def login():
    print(f"\n{'='*10} Login {'='*10}")
    while True:
        global username
        username = input("Masukkan username anda: ")
        password = pwinput("Masukkan password anda: ")
        if username in data_kios["user"] and data_kios["user"][username]["password"] == password:
            global user
            user = data_kios["user"][username]
            print("Login Berhasil. Selamat datang " + username + "!")
            menu_utama()
        else:
            print("Login gagal")

def menu_utama():
    print(f"\n{'='*10} Menu Utama {'='*10}")
    print("[1] Lihat produk")
    print("[2] Keranjang")
    print("[3] Akun")
    print("[4] Log out")
    while True:
        pilihan = intinput("masukkan pilihan anda: ")
        if pilihan == 1:
            menu_produk()
        elif pilihan == 2:
            if user["keranjang"] != {}:
                menu_keranjang()
            else:
                print("\nKeranjang anda kosong")
                menu_utama()
                break
        elif pilihan == 3:
            menu_akun()
        elif pilihan == 4:
            menu_awal()
        else:
            print("Pilihan tidak valid\n")

def menu_awal():
    print(f"\n{'='*5} Selamat Datang di Kios Tembakau Kretek Bacco {'='*5}")
    print("[1] Login")
    print("[2] Register")
    while True:
        pilihan = intinput("Masukkan pilihan anda: ")
        if pilihan == 1:
            login()
            break
        elif pilihan == 2:
            register()
            break
        else:
            print("Pilihan tidak valid\n")


#========= main call =========#
menu_awal()
