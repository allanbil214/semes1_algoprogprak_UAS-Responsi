import datetime as dt
import sqlite3 as db
from prettytable import PrettyTable as pt

print("\n[ TOKO SUMBER JAYA ]")

conn = db.connect("sumberjaya_data.db")
cur = conn.cursor()

def sumberjaya():
    main_menu = ["[1] MASUK KE MENU ITEM", 
                "[2] MASUK KE MENU KATEGORI", 
                "[3] KELUAR DARI APP"]

    def squek(): 
        def createTable():
            cur.execute("""CREATE TABLE IF NOT EXISTS "category" (
                        	"ID"	INTEGER,
                        	"name"	TEXT NOT NULL,
                        	PRIMARY KEY("ID" AUTOINCREMENT)
                        );""")
               
            cur.execute("""CREATE TABLE IF NOT EXISTS "item" (
                        	"ID"	INTEGER,
                        	"name"	TEXT NOT NULL,
                            "catID" INTEGER NOT NULL,
                        	"stock"	INTEGER NOT NULL,
                        	"price"	INTEGER NOT NULL,
                        	"inputdate"	TEXT NOT NULL,
                        	PRIMARY KEY("ID" AUTOINCREMENT),
                            FOREIGN KEY("catID") REFERENCES [category] (ID)
                        );""")
            exampleData()
            
        def exampleData():
            cur.execute("select count(*) as count from category")
            for r2 in cur.fetchall():
                count2 = r2[0]   
            if(count2 == 0):
                cur.execute("""insert into category (name)
                                values('Beverage'), ('Food'), ('Cleaner'), ('Personal Care'), ('Other')
                            """)                   
                conn.commit()
        createTable()

    def showCat():
        colCat = ['Id', 'Nama Kategori']
        print("\n[i] Nama Kategori\n")
        cur.execute("""select ID as 'Id', name as 'Nama Kategori' from category""")
        newPT = pt()
        newPT.field_names = colCat
        for r in cur.fetchall():
            newPT.add_row(r)
        print(newPT)

    def item():
        item.catid = 0
        item.ct = 0
        item_menu = ["[1] LIHAT DATA ITEM", 
                     "[2] TAMBAH DATA ITEM", 
                     "[3] EDIT DATA ITEM",
                     "[4] HAPUS DATA ITEM",
                     "[5] KELUAR DARI MENU ITEM"]
        
        def showMenu():
            for i in item_menu:
                print(i)

        def checkTable():
            cur.execute("select count(*) as count from item")
            for r in cur.fetchall():
                item.ct = r[0]
               
        def showItem():
            colItems = ['Id', 'Nama Barang', 'Kategori', 'Stok', 'Harga', 'Tanggal Input']
            print("\n[i] Daftar Barang\n")
            cur.execute("""select 
                            item.ID as 'Id', item.name, category.name, item.stock, item.price,item.inputdate
                            from item left join category on item.catID = category.ID
                        """)
            
            newPT = pt()
            newPT.field_names = colItems
            for r in cur.fetchall():
                newPT.add_row(r)
            print(newPT)
        
        def getCat():
            print("\n[i] Untuk memasukkan kategori anda bisa mengisinya dengan Id maupun Nama dari kategori tersebut.")
            inpCat = input("\n[=] Masukkan Id/Nama Kategori : ")
            if(inpCat == ""):
                return getCat()
            elif(inpCat.isdigit()):
                cur.execute("select * from category where ID=?", (inpCat,))
                row = cur.fetchone()
                if row == None:
                    print("\n[i] Tidak ada kategori yang ber-ID " + inpCat)
                    return getCat()
                else:
                    item.catid = row[0]
                    print("\n[i] Kategori yang anda pilih adalah " + row[1])
            else:
                cur.execute("select * from category where name like ?", (inpCat,))
                row = cur.fetchone()
                if row == None:
                    print("\n[i] Tidak ada kategori yang bernama " + inpCat)
                    return getCat()
                else:
                    item.catid = row[0]
                    print("\n[i] ID Kategori yang anda pilih adalah " + str(row[0]))
        
        def createItem():
            print("\n[i] Anda akan memasukkan barang baru ke server.")
            print("[i] Masukkan 0 atau Exit untuk kembali ke Menu Pilihan.")
            inpName = input("[=] Masukkan Nama Barang : ")
            showCat()
            getCat()
            inpStock = input("\n[=] Masukkan Stock Barang : ")               
            inpPrice = input("[=] Masukkan Harga Barang : ")
            if(inpName == "" or inpStock == "" or inpPrice == ""):
                return createItem()
            elif(inpName == "0" or inpName == "exit" or inpName == "Exit" or inpName == "EXIT"):
                return
            elif(inpStock.isdigit() and inpPrice.isdigit()):
                cur.execute("""insert into item (name, catID, stock, price, inputdate) 
                            values(?, ?, ?, ?, ?)""", (inpName, item.catid, inpStock, inpPrice, dt.date.today()),)
                conn.commit()
                print("\n[i] Data berhasil ditambahkan.")
            else:
                print("\n[!] Ada kesalahan ketika menginput data!")
                return createItem()
        
        def updateItem():
            showItem()
            print("\n[i] Anda akan mengubah beberapa atribut barang.")
            print("[i] Jika anda tidak ingin memperbarui beberapa atribut, silahkan kosongi inputan tersebut.")
            print("\n[i] Masukkan ID atau Nama barang untuk mengganti atribut barang.")
            print("[i] Masukkan 0 atau Exit untuk kembali ke Menu Pilihan.")
            inpID = input("[=] Masukkan ID atau Nama barang : ")
            
            if(inpID == ""):
                return updateItem()
            elif(inpID == "0" or inpID == "exit" or inpID == "Exit" or inpID == "EXIT"):
                return
            elif(inpID.isdigit()):
                cur.execute("""select item.ID, item.name, category.name , item.stock, item.price, category.id 
                                from item left join category on item.catID = category.ID where item.ID=?
                            """, (inpID,) )           
                getData = cur.fetchone()
                if getData == None:
                    print("\n[i] Tidak ada barang yang ber-ID " + inpID)
                    return updateItem()
                else:
                    inpID = getData[0]
                    print("\n[i] Barang yang anda pilih adalah " + getData[1])
            else:
                cur.execute("""select item.ID, item.name, category.name , item.stock, item.price, category.id 
                                from item left join category on item.catID = category.ID where item.name like ?
                            """, (inpID,))
                getData = cur.fetchone()
                if getData == None:
                    print("\n[i] Tidak ada barang yang bernama " + inpID)
                    return updateItem()
                else:
                    inpID = getData[0]
                    print("\n[i] ID Barang yang anda pilih adalah " + str(getData[0]))
                    
            inpName = input("[=] Barang yang Bernama '" + getData[1] + "' Akan diganti Ke : ")
            print("\n[i] Barang ini Berkategori : " + getData[2])
            print("\n[=] Apakah anda ingin mengubah kategori barang ini?")
            yesnt = input("[=] Y/N : ")
            if(yesnt == "y" or yesnt == "Y"):
                showCat()
                getCat()
            elif(yesnt == "n" or yesnt == "N"):
                item.catid = getData[5]
            inpStock = input("[=] Stok dari Barang ini adalah '" + str(getData[3]) + "' Akan diganti Ke : ")
            inpPrice = input("[=] Harga dari Barang ini adalah '" + str(getData[4]) + "' Akan diganti Ke : ")
            if(inpName == ""):
                inpName = getData[1]
            if(inpStock == ""):
                inpStock = getData[3]
            elif(not inpStock.isdigit()):
                print("\n[!] Ada kesalahan ketika menginput data!")
                return createItem()
            if(inpPrice == ""):
                inpPrice = getData[4]
            elif(not inpPrice.isdigit()):
                print("\n[!] Ada kesalahan ketika menginput data!")
                return createItem()
            cur.execute("update item set name=?, catID=?, stock=?, price=?  where id=?", 
                        (inpName, item.catid, inpStock, inpPrice, inpID),)
            conn.commit()
            print("\n[i] Data berhasil dirubah.")
                
        def deleteItem():
            showItem()
            print("[i] Masukkan ID atau Nama barang untuk menghapus.")
            print("[i] Masukkan 0 atau Exit untuk kembali ke Menu Pilihan.")
            inpID = input("[=] Masukkan ID atau Nama barang : ")
            if(inpID == ""):
                return deleteItem()
            elif(inpID == "0" or inpID == "exit" or inpID == "Exit" or inpID == "EXIT"):
                return
            elif(inpID.isdigit()):
                cur.execute("select * from item where ID=?", (inpID,))
                getData = cur.fetchone()
                if getData == None:
                    print("\n[i] Tidak ada barang yang ber-ID " + inpID)
                    return deleteItem()
                else:
                    print("\n[i] Barang yang anda pilih adalah " + getData[1])
            else:
                cur.execute("select * from item where name like ?", (inpID,))
                getData = cur.fetchone()
                if getData == None:
                    print("\n[i] Tidak ada barang yang bernama " + inpID)
                    return deleteItem()
                else:
                    print("\n[i] ID Barang yang anda pilih adalah " + str(getData[0]))

            print("[i] Apakah anda yakin ingin menghapus data ini?")
            inpUsure = input("[=] Y/N : ")
            if(inpUsure == "y" or inpUsure == "Y"):
                cur.execute("delete from item where id=?", (getData[0], ))
                conn.commit()
                print("\n[i] Data berhasil dihapus!")
            elif(inpUsure == "n" or inpUsure == "N"):
                return deleteItem()
            else:
                return deleteItem()
            
        def inputan():
            print('\n========================================')
            print('[i] Select Command')
            print('========================================')
            showMenu()
            
            inpSelect = input("\n[=] Pilih Menu : ")
            checkTable()

            if(inpSelect == '1'):
                showItem()
                return inputan()
            elif(inpSelect == '2'):
                createItem()
                return inputan()
            elif(inpSelect == '3'):
                if(item.ct == 0):
                    print("\n[i] Tabel Data masih kosong!")
                else:
                    updateItem()
                return inputan()
            elif(inpSelect == '4'):
                if(item.ct == 0):
                    print("\n[i] Tabel Data masih kosong!")
                else:
                    print("\n[i] Anda akan mengubah beberapa atribut barang.")
                    deleteItem()
                return inputan()                
            elif(inpSelect == '5'):
                return
            else:
                print("\n[!] Input Salah")
                return inputan()
        
        inputan()
        
    def cat():
        cat.ct = 0
        cat_menu = ["[1] LIHAT DATA KATEGORI", 
                     "[2] TAMBAH DATA KATEGORI", 
                     "[3] EDIT DATA KATEGORI",
                     "[4] HAPUS DATA KATEGORI",
                     "[5] KELUAR DARI MENU KATEGORI"]
        
        def showMenu():
            for i in cat_menu:
                print(i)

        def checkTable():
            cur.execute("select count(*) as count from category")
            for r in cur.fetchall():
                cat.ct = r[0]
        
        def createCat():
            print("\n[i] Anda akan mendaftarkan kategori baru ke server.")
            print("[i] Masukkan 0 atau Exit untuk kembali ke Menu Pilihan.")
            inpName = input("[=] Masukkan Nama Kategori : ")
            if(inpName == ""):
                return createCat()
            elif(inpName == "0" or inpName == "exit" or inpName == "Exit" or inpName == "EXIT"):
                return
            else:
                cur.execute("insert into category (name) values(?)", (inpName,))
                conn.commit()
                print("\n[i] Data berhasil ditambahkan.")
        
        def updateCat():
            showCat()
            print("\n[i] Masukkan ID atau Nama kategori untuk mengganti nama barang.")
            print("[i] Masukkan 0 atau Exit untuk kembali ke Menu Pilihan.")
            inpID = input("[=] Masukkan ID atau Nama kategori : ")
            
            if(inpID == ""):
                return updateCat()
            elif(inpID == "0" or inpID == "exit" or inpID == "Exit" or inpID == "EXIT"):
                return
            elif(inpID.isdigit()):
                cur.execute("select * from category where id=?", (inpID,))           
                getData = cur.fetchone()
                if getData == None:
                    print("\n[i] Tidak ada kategori yang ber-ID " + inpID)
                    return updateCat()
                else:
                    inpID = getData[0]
                    print("\n[i] Kategori yang anda pilih adalah " + getData[1])
            else:
                cur.execute("select * from category where name like ?", (inpID,))  
                getData = cur.fetchone()
                if getData == None:
                    print("\n[i] Tidak ada kategori yang bernama " + inpID)
                    return updateCat()
                else:
                    inpID = getData[0]
                    print("\n[i] ID Kategori yang anda pilih adalah " + str(getData[0]))
                    
            inpName = input("[=] Kategori yang Bernama '" + getData[1] + "' Akan diganti Ke : ")
            cur.execute("update category set name=? where id=?", (inpName, inpID),)
            conn.commit()
            print("\n[i] Data berhasil dirubah.")
                
        def deleteCat():
            showCat()
            print("[i] Masukkan ID atau Nama kategori untuk menghapus.")
            print("[i] Masukkan 0 atau Exit untuk kembali ke Menu Pilihan.")
            inpID = input("[=] Masukkan ID atau Nama kategori : ")
            if(inpID == ""):
                return deleteCat()
            elif(inpID == "0" or inpID == "exit" or inpID == "Exit" or inpID == "EXIT"):
                return
            elif(inpID.isdigit()):
                cur.execute("select * from category where ID=?", (inpID,))
                row = cur.fetchone()
                if row == None:
                    print("\n[i] Tidak ada kategori yang ber-ID " + inpID)
                    return deleteCat()
                else:
                    print("\n[i] Barang yang anda pilih adalah " + row[1])
            else:
                cur.execute("select * from category where name like ?", (inpID,))
                row = cur.fetchone()
                if row == None:
                    print("\n[i] Tidak ada kategori yang bernama " + inpID)
                    return deleteCat()
                else:
                    print("\n[i] ID Kategori yang anda pilih adalah " + str(row[0]))

            print("[i] Apakah anda yakin ingin menghapus data ini?")
            inpUsure = input("[=] Y/N : ")
            if(inpUsure == "y" or inpUsure == "Y"):
                cur.execute("delete from category where id=?", (row[0],))
                conn.commit()
                print("[i] Data berhasil dihapus!")
            elif(inpUsure == "n" or inpUsure == "N"):
                return deleteCat()
            else:
                return deleteCat()
            
        def inputan():
            print('\n========================================')
            print('[i] Select Command')
            print('========================================')
            showMenu()
            
            inpSelect = input("\n[=] Pilih Menu : ")
            checkTable()

            if(inpSelect == '1'):
                showCat()
                return inputan()
            elif(inpSelect == '2'):
                createCat()
                return inputan()
            elif(inpSelect == '3'):
                if(cat.ct == 0):
                    print("\n[i] Tabel Data masih kosong!")
                else:
                    updateCat()
                return inputan()
            elif(inpSelect == '4'):
                if(cat.ct == 0):
                    print("\n[i] Tabel Data masih kosong!")
                else:
                    print("\n[i] Anda akan mengubah beberapa atribut barang.")
                    deleteCat()
                return inputan()                
            elif(inpSelect == '5'):
                return
            else:
                print("\n[!] Input Salah")
                return inputan()
        
        inputan()

    def showMenu():
        for i in main_menu:
            print(i)

    def selector():
        print('\n========================================')
        print('[i] Select Menu')
        print('========================================')
        showMenu()
        
        inpSelect = input("\n[=] Pilih Menu : ")

        if(inpSelect == '1'):
            item()
            return selector()
        elif(inpSelect == '2'):
            cat()
            return selector()
        elif(inpSelect == '3'):              
            print("\n[i] Good Bye")
        else:
            print("\n[!] Input Salah")
            return selector()

    squek()
    selector()

sumberjaya()
conn.close