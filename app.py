import os
import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_from_directory
)

from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "gelistirme-anahtari")


# ==========================================
# AYARLAR
# ==========================================

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "uploads",
    "raporlar"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# VERİTABANI
# ==========================================

def veritabani_baglantisi():

    conn = sqlite3.connect("portfolio.db")

    conn.row_factory = sqlite3.Row

    return conn


def veritabani_olustur():

    conn = veritabani_baglantisi()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS raporlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT NOT NULL,
            aciklama TEXT NOT NULL,
            dosya TEXT NOT NULL
        )
    """)

    conn.commit()

    conn.close()


veritabani_olustur()


# ==========================================
# ANA SAYFA
# ==========================================

@app.route("/")
def ana_sayfa():

    conn = veritabani_baglantisi()

    raporlar = conn.execute(
        "SELECT * FROM raporlar ORDER BY id DESC LIMIT 3"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        raporlar=raporlar
    )


# ==========================================
# YÖNETİCİ GİRİŞİ
# ==========================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    hata = None

    if request.method == "POST":

        kullanici_adi = request.form["kullanici_adi"]
        sifre = request.form["sifre"]

        if kullanici_adi == "dmlsu" and sifre == "2016":

            session["admin"] = True

            return redirect("/panel")

        else:

            hata = "Kullanıcı adı veya şifre yanlış."

    return render_template(
        "admin-login.html",
        hata=hata
    )


# ==========================================
# YÖNETİM PANELİ
# ==========================================

@app.route("/panel")
def panel():

    if not session.get("admin"):

        return redirect("/admin")

    return render_template("admin.html")


# ==========================================
# RAPOR YÖNETİMİ
# ==========================================

@app.route("/rapor-yonet")
def rapor_yonet():

    if not session.get("admin"):

        return redirect("/admin")

    conn = veritabani_baglantisi()

    raporlar = conn.execute(
        "SELECT * FROM raporlar ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "rapor-yonet.html",
        raporlar=raporlar
    )


# ==========================================
# RAPOR YÜKLE
# ==========================================

@app.route("/rapor-yukle", methods=["POST"])
def rapor_yukle():

    if not session.get("admin"):

        return redirect("/admin")

    baslik = request.form["baslik"]

    aciklama = request.form["aciklama"]

    dosya = request.files["dosya"]


    if dosya.filename == "":

        return redirect("/rapor-yonet")


    dosya_adi = secure_filename(dosya.filename)


    if not dosya_adi.lower().endswith(".pdf"):

        return "Sadece PDF dosyası yükleyebilirsiniz."


    dosya.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            dosya_adi
        )
    )


    conn = veritabani_baglantisi()

    conn.execute(
        """
        INSERT INTO raporlar
        (baslik, aciklama, dosya)

        VALUES (?, ?, ?)
        """,

        (
            baslik,
            aciklama,
            dosya_adi
        )
    )

    conn.commit()

    conn.close()


    return redirect("/rapor-yonet")


# ==========================================
# RAPOR SİL
# ==========================================

@app.route("/rapor-sil/<int:id>")
def rapor_sil(id):

    if not session.get("admin"):

        return redirect("/admin")


    conn = veritabani_baglantisi()


    rapor = conn.execute(
        "SELECT * FROM raporlar WHERE id = ?",
        (id,)
    ).fetchone()


    if rapor:

        dosya_yolu = os.path.join(
            app.config["UPLOAD_FOLDER"],
            rapor["dosya"]
        )


        if os.path.exists(dosya_yolu):

            os.remove(dosya_yolu)


        conn.execute(
            "DELETE FROM raporlar WHERE id = ?",
            (id,)
        )

        conn.commit()


    conn.close()


    return redirect("/rapor-yonet")


# ==========================================
# ZİYARETÇİ RAPOR SAYFASI
# ==========================================

@app.route("/raporlar")
def raporlar():

    conn = veritabani_baglantisi()

    raporlar = conn.execute(
        "SELECT * FROM raporlar ORDER BY id DESC"
    ).fetchall()

    conn.close()


    return render_template(
        "raporlar.html",
        raporlar=raporlar
    )


# ==========================================
# PDF DOSYALARINI AÇ
# ==========================================

@app.route("/uploads/raporlar/<filename>")
def rapor_dosyasi(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ==========================================
# ÇIKIŞ
# ==========================================

@app.route("/cikis")
def cikis():

    session.pop("admin", None)

    return redirect("/admin")


# ==========================================
# ÇALIŞTIR
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)