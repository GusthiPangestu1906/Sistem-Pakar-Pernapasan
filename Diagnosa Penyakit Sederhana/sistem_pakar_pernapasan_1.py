"""
Sistem Pakar Diagnosis Awal Penyakit Saluran Pernapasan
Topik: Flu, Bronkitis, COVID-19
Metode: Forward Chaining dengan Pembobotan (Scoring Threshold > 50%)
Pustaka: Experta
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
    """Template untuk menyimpan fakta gejala yang dialami pasien"""
    pass

# ==========================================
# 2. INFERENCE ENGINE (MESIN INFERENSI SCORING)
# ==========================================
class DiagnosisPernapasan(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        # Inisialisasi variabel untuk menampung skor persentase
        self.skor_covid = 0
        self.skor_bronkitis = 0
        self.skor_flu = 0

    # --- ATURAN BOBOT COVID-19 ---
    @Rule(GejalaPasien(hilang_penciuman='y'))
    def bobot_covid_1(self): self.skor_covid += 40
    
    @Rule(GejalaPasien(sesak_napas='y'))
    def bobot_covid_2(self): self.skor_covid += 20
    
    @Rule(GejalaPasien(batuk_kering='y'))
    def bobot_covid_3(self): self.skor_covid += 20

    # --- ATURAN BOBOT BRONKITIS ---
    @Rule(GejalaPasien(batuk_berdahak='y'))
    def bobot_bronkitis_1(self): self.skor_bronkitis += 40
    
    @Rule(GejalaPasien(sakit_dada='y'))
    def bobot_bronkitis_2(self): self.skor_bronkitis += 30
    
    @Rule(GejalaPasien(lelah='y'))
    def bobot_bronkitis_3(self): self.skor_bronkitis += 30

    # --- ATURAN BOBOT FLU BIASA ---
    @Rule(GejalaPasien(hidung_tersumbat='y'))
    def bobot_flu_1(self): self.skor_flu += 40
    
    @Rule(GejalaPasien(bersin='y'))
    def bobot_flu_2(self): self.skor_flu += 30

    # --- ATURAN GEJALA BERIRISAN (Dimiliki >1 Penyakit) ---
    @Rule(GejalaPasien(demam='y'))
    def bobot_gejala_irisan(self): 
        self.skor_covid += 20
        self.skor_flu += 30

    # --- EVALUASI AKHIR (Resolusi Konflik) ---
    # salience=-100 memastikan fungsi ini dieksekusi paling TERAKHIR setelah semua bobot dihitung
    @Rule(salience=-100) 
    def evaluasi_diagnosis(self):
        print("\n" + "="*60)
        print(" HASIL DIAGNOSIS (Berdasarkan Ambang Batas > 50%)")
        print("="*60)
        
        diagnosis_ditemukan = False
        
        # Mengecek apakah COVID-19 melebihi ambang batas
        if self.skor_covid > 50:
            print(f"[!] PERINGATAN: Indikasi COVID-19 (Tingkat Kecocokan: {self.skor_covid}%)")
            print("    Saran: Lakukan isolasi mandiri segera, jadwalkan tes Swab/PCR.\n")
            diagnosis_ditemukan = True
            
        # Mengecek apakah Bronkitis melebihi ambang batas
        if self.skor_bronkitis > 50:
            print(f"[*] Indikasi BRONKITIS (Tingkat Kecocokan: {self.skor_bronkitis}%)")
            print("    Saran: Hindari asap rokok/polusi, gunakan pelembap udara (humidifier).\n")
            diagnosis_ditemukan = True
            
        # Mengecek apakah Flu Biasa melebihi ambang batas
        if self.skor_flu > 50:
            print(f"[*] Indikasi FLU BIASA (Tingkat Kecocokan: {self.skor_flu}%)")
            print("    Saran: Istirahat cukup, minum air hangat, konsumsi vitamin C.\n")
            diagnosis_ditemukan = True
            
        # Jika tidak ada yang mencapai 50%
        if not diagnosis_ditemukan:
            print("[-] Gejala Tidak Spesifik.")
            print("    Skor tertinggi tidak mencapai ambang batas diagnosis (>50%).")
            print("    Saran: Jaga kondisi tubuh. Jika keluhan mengganggu, periksakan ke dokter.")
        print("="*60 + "\n")


# ==========================================
# 3. INTERFACE PENGGUNA (INTERAKTIVITAS)
# ==========================================
def mulai_konsultasi():
    print("Selamat datang di Sistem Pakar Diagnosis Awal Saluran Pernapasan")
    print("Silakan jawab pertanyaan berikut sesuai kondisi Anda saat ini.")
    print("Ketik 'y' untuk Ya, atau 'n' untuk Tidak.\n")
    
    # Input User
    g_demam = input("Apakah Anda mengalami demam (suhu tubuh naik)? (y/n): ").strip().lower()
    g_tersumbat = input("Apakah hidung Anda tersumbat atau beringus? (y/n): ").strip().lower()
    g_bersin = input("Apakah Anda sering bersin-bersin? (y/n): ").strip().lower()
    g_batuk_dahak = input("Apakah Anda mengalami batuk berdahak berkepanjangan? (y/n): ").strip().lower()
    g_dada = input("Apakah dada terasa sakit/nyeri saat bernapas atau batuk? (y/n): ").strip().lower()
    g_lelah = input("Apakah Anda merasa sangat kelelahan secara fisik? (y/n): ").strip().lower()
    g_batuk_kering = input("Apakah Anda mengalami batuk kering (tanpa dahak)? (y/n): ").strip().lower()
    g_anosmia = input("Apakah Anda kehilangan indera penciuman (anosmia)? (y/n): ").strip().lower()
    g_sesak = input("Apakah Anda mengalami sesak napas? (y/n): ").strip().lower()
    
    # Menjalankan Experta
    engine = DiagnosisPernapasan()
    engine.reset() 
    
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
    
    engine.run()

if __name__ == "__main__":
    mulai_konsultasi()