"""
Sistem Pakar Diagnosis Awal Penyakit Saluran Pernapasan
Topik: Flu, Bronkitis, COVID-19
Metode: Forward Chaining menggunakan pustaka Experta
Dibuat oleh: Gusthi Pangestu
"""

import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.Iterable = collections.abc.Iterable
collections.MutableMapping = collections.abc.MutableMapping
collections.Callable = collections.abc.Callable

from experta import *

# ==========================================
# 1. REPRESENTASI PENGETAHUAN (MODELING)
# ==========================================
class GejalaPasien(Fact):
    """
    Fact ini bertindak sebagai template untuk menyimpan 
    fakta-fakta (gejala) yang dialami oleh pasien.
    """
    pass

# ==========================================
# 2. INFERENCE ENGINE (MESIN INFERENSI)
# ==========================================
class DiagnosisPernapasan(KnowledgeEngine):
    
    # --- RULE 1: COVID-19 (PRIORITAS TERTINGGI: 30) ---
    @Rule(AND(GejalaPasien(demam='y'),
              GejalaPasien(batuk_kering='y'),
              GejalaPasien(hilang_penciuman='y'),
              GejalaPasien(sesak_napas='y')), salience=30)
    def diagnosis_covid(self):
        print("\n" + "="*50)
        print("HASIL DIAGNOSIS SEMENTARA")
        print("="*50)
        print("Diagnosis : PERINGATAN! Gejala Anda sangat mengarah pada infeksi COVID-19.")
        print("Saran     : Lakukan isolasi mandiri segera, jadwalkan tes Swab/PCR, dan hubungi fasilitas kesehatan terdekat.")
        self.halt() # Hentikan mesin agar tidak mengeksekusi penyakit lain

    # --- RULE 2: BRONKITIS (PRIORITAS MENENGAH: 20) ---
    @Rule(AND(GejalaPasien(batuk_berdahak='y'),
              GejalaPasien(sakit_dada='y'),
              GejalaPasien(lelah='y')), salience=20)
    def diagnosis_bronkitis(self):
        print("\n" + "="*50)
        print("HASIL DIAGNOSIS SEMENTARA")
        print("="*50)
        print("Diagnosis : Kemungkinan besar Anda mengalami Bronkitis (Peradangan saluran pernapasan).")
        print("Saran     : Hindari asap rokok/polusi, gunakan pelembap udara (humidifier), dan segera konsultasi ke dokter jika batuk berdarah.")
        self.halt()

    # --- RULE 3: FLU BIASA (PRIORITAS RENDAH: 10) ---
    @Rule(AND(GejalaPasien(demam='y'),
              GejalaPasien(hidung_tersumbat='y'),
              GejalaPasien(bersin='y')), salience=10)
    def diagnosis_flu(self):
        print("\n" + "="*50)
        print("HASIL DIAGNOSIS SEMENTARA")
        print("="*50)
        print("Diagnosis : Kemungkinan besar Anda terkena Flu Biasa (Influenza).")
        print("Saran     : Istirahat cukup, minum air hangat, konsumsi vitamin C, dan makan makanan bergizi.")
        self.halt()

    # --- RULE 4: GEJALA TIDAK SPESIFIK (PRIORITAS TERENDAH: 0) ---
    @Rule(NOT(OR(
        AND(GejalaPasien(demam='y'), GejalaPasien(batuk_kering='y'), GejalaPasien(hilang_penciuman='y'), GejalaPasien(sesak_napas='y')),
        AND(GejalaPasien(batuk_berdahak='y'), GejalaPasien(sakit_dada='y'), GejalaPasien(lelah='y')),
        AND(GejalaPasien(demam='y'), GejalaPasien(hidung_tersumbat='y'), GejalaPasien(bersin='y'))
    )), salience=0)
    def diagnosis_tidak_diketahui(self):
        print("\n" + "="*50)
        print("HASIL DIAGNOSIS SEMENTARA")
        print("="*50)
        print("Diagnosis : Gejala tidak cukup spesifik untuk merujuk pada Flu, Bronkitis, atau COVID-19 secara pasti.")
        print("Saran     : Jaga kondisi tubuh. Jika keluhan dirasa mengganggu aktivitas, periksakan diri ke dokter umum.")


# ==========================================
# 3. INTERFACE PENGGUNA (INTERAKTIVITAS)
# ==========================================
def mulai_konsultasi():
    print("Selamat datang di Sistem Pakar Diagnosis Awal Saluran Pernapasan")
    print("Silakan jawab pertanyaan berikut sesuai kondisi Anda saat ini.")
    print("Ketik 'y' untuk Ya, atau 'n' untuk Tidak.\n")
    
    # Kumpulan input user
    g_demam = input("Apakah Anda mengalami demam (suhu tubuh naik)? (y/n): ").strip().lower()
    g_tersumbat = input("Apakah hidung Anda tersumbat atau beringus? (y/n): ").strip().lower()
    g_bersin = input("Apakah Anda sering bersin-bersin? (y/n): ").strip().lower()
    
    g_batuk_dahak = input("Apakah Anda mengalami batuk berdahak yang berkepanjangan? (y/n): ").strip().lower()
    g_dada = input("Apakah dada Anda terasa sakit atau nyeri saat bernapas/batuk? (y/n): ").strip().lower()
    g_lelah = input("Apakah Anda merasa sangat kelelahan secara fisik? (y/n): ").strip().lower()
    
    g_batuk_kering = input("Apakah Anda mengalami batuk kering (tanpa dahak)? (y/n): ").strip().lower()
    g_anosmia = input("Apakah Anda kehilangan indera penciuman atau perasa (makanan terasa hambar)? (y/n): ").strip().lower()
    g_sesak = input("Apakah Anda mengalami sesak napas yang cukup parah? (y/n): ").strip().lower()
    
    # Inisialisasi dan jalankan Experta
    engine = DiagnosisPernapasan()
    engine.reset()  # Sangat penting! Mengosongkan working memory sebelum proses dimulai
    
    # Mendeklarasikan fakta-fakta yang diinputkan user ke dalam sistem
    engine.declare(GejalaPasien(
        demam=g_demam,
        hidung_tersumbat=g_tersumbat,
        bersin=g_bersin,
        batuk_berdahak=g_batuk_dahak,
        sakit_dada=g_dada,
        lelah=g_lelah,
        batuk_kering=g_batuk_kering,
        hilang_penciuman=g_anosmia,
        sesak_napas=g_sesak
    ))
    
    # Memulai pencocokan aturan (Forward Chaining)
    engine.run()

# Mengeksekusi program
if __name__ == "__main__":
    mulai_konsultasi()