# Tugas Praktikum 2: Sistem Pakar Diagnosis Awal Saluran Pernapasan

Repositori ini berisi penjelasan alur logika dan implementasi kode untuk **Sistem Pakar Berbasis Aturan (Rule-Based Expert System)**. Sistem ini mendiagnosis penyakit saluran pernapasan umum (Flu, Bronkitis, dan COVID-19) berdasarkan input gejala pengguna menggunakan pustaka **Experta** dengan metode **Forward Chaining**.

---

## 🧠 Alur Logika Sistem (Inference Logic)

Sistem ini bekerja melalui beberapa tahapan logis berikut:

### 1. Representasi Pengetahuan (Knowledge Representation)
Pengetahuan medis dasar diubah menjadi kode menggunakan turunan kelas `Fact` dari Experta. Kelas `GejalaPasien` bertindak sebagai *template* kerangka data untuk menampung seluruh variabel gejala (seperti demam, batuk, sesak napas) yang diinputkan oleh pengguna.

### 2. Pengumpulan Fakta (Data Gathering)
Program berjalan secara interaktif di terminal dengan menanyakan 9 (sembilan) gejala spesifik kepada pengguna. Jawaban "y" (Ya) atau "n" (Tidak) kemudian dideklarasikan (`engine.declare()`) dan dimasukkan ke dalam memori kerja (*Working Memory*) mesin inferensi.

### 3. Mesin Inferensi & Forward Chaining
Sistem menggunakan pendekatan **Forward Chaining** (Data-Driven). Mesin akan mengambil fakta-fakta yang ada di *Working Memory* dan menyusuri basis aturan (Rule Base) dari atas ke bawah untuk mencari kesimpulan. Pencocokan aturan menggunakan logika **Strict AND** (`AND(...)`), yang berarti sebuah penyakit hanya akan terdiagnosis jika seluruh gejala khas wajibnya terpenuhi oleh input pengguna.

### 4. Resolusi Konflik (Conflict Resolution)
Untuk menghindari mesin mencetak lebih dari satu penyakit secara bersamaan (ketika pengguna menjawab "Ya" pada banyak gejala), sistem ini menerapkan teknik tingkat lanjut:
*   **Salience (Prioritas Pembobotan):** Aturan diberi tingkat prioritas. `COVID-19` diberikan salience tertinggi (30) karena sifatnya yang kritis/darurat, diikuti `Bronkitis` (20), `Flu` (10), dan terakhir *Fallback/Unknown* (0).
*   **Halt Execution:** Jika sebuah aturan dengan prioritas tinggi terpenuhi, perintah `self.halt()` akan dipanggil. Ini menghentikan mesin untuk mencari penyakit lain yang lebih ringan di bawahnya, memastikan sistem memberikan diagnosis yang paling darurat/relevan.

---

## 📋 Basis Aturan (Rule Base)

*   **IF** (Demam=y **AND** Batuk Kering=y **AND** Hilang Penciuman=y **AND** Sesak Napas=y)  
    👉 **THEN Diagnosis = COVID-19** *(Salience: 30)*
*   **IF** (Batuk Dahak=y **AND** Sakit Dada=y **AND** Lelah=y)  
    👉 **THEN Diagnosis = Bronkitis** *(Salience: 20)*
*   **IF** (Demam=y **AND** Hidung Tersumbat=y **AND** Bersin=y)  
    👉 **THEN Diagnosis = Flu Biasa** *(Salience: 10)*
*   **IF** (Tidak memenuhi kombinasi lengkap dari ketiga di atas)  
    👉 **THEN Diagnosis = Gejala Tidak Spesifik** *(Salience: 0)*

---

## 🛠️ Prasyarat & Cara Menjalankan

1. Pastikan Anda telah menginstal pustaka `experta` di lingkungan Python Anda:
   ```bash
   pip install experta