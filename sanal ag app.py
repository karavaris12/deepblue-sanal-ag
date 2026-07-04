import streamlit as st
import requests

# 1. Sayfa Ayarları ve Sinematik Tasarım
st.set_page_config(page_title="DeepBlue - Canlı Sanal Evren", page_icon="🌊", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(10, 20, 35, 0.7), rgba(5, 10, 20, 0.8)), 
                    url('https://unsplash.com');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f1f5f9;
    }
    .glass-box {
        background: rgba(15, 32, 67, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .pay-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Ücretsiz Yapay Zeka Motoru Bağlantısı
HF_TOKEN = "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"
API_URL = "https://huggingface.co"

def bot_cevap_uret(sistem_talimati, mesajlar):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    full_prompt = f"<|system|>\n{sistem_talimati}\n"
    for m in mesajlar[-6:]:
        rol = "user" if m["role"] == "user" else "assistant"
        full_prompt += f"<|{rol}|>\n{m['text']}\n"
    full_prompt += "<|assistant|>\n"
    
    payload = {
        "inputs": full_prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    try:
        r = requests.post(API_URL, headers=headers, json=payload)
        sonuc = r.json()
        if isinstance(sonuc, list) and len(sonuc) > 0:
            ham_cevap = sonuc[0].get('generated_text', '')
            return ham_cevap.split("<|assistant|>\n")[-1].strip()
        return "Dalgaların sesine daldım, ne demiştin? 🌊"
    except:
        return "Küçük bir siber fırtına koptu, tekrar yazar mısın?"

# 3. Oturum Veri Yapıları (Hafıza)
if "giris_ok" not in st.session_state:
    st.session_state.giris_ok = False
if "mesaj_hakki" not in st.session_state:
    st.session_state.mesaj_hakki = 15
if "sohbet_gecmisi" not in st.session_state:
    st.session_state.sohbet_gecmisi = [{"role": "bot", "text": "Selam... Ben Deniz. İskelede oturmuş ufku seyrediyordum. Senin hikayen ne?"}]

# ================= DURUM 1: GİRİŞ EKRANI =================
if not st.session_state.giris_ok:
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🌊 DEEPBLUE SANAL DÜNYASI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color:#94a3b8;'>Canlı karakter odaları ve kuantum bilincine ilk adım.</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔐 Giriş Yap", "📝 Kayıt Ol"])
        with t1:
            eposta = st.text_input("E-posta Adresiniz", placeholder="isim@domain.com")
            sifre = st.text_input("Şifreniz", type="password", placeholder="••••••••")
            if st.button("Dünyayı Aktif Et", use_container_width=True):
                if eposta and sifre:
                    st.session_state.giris_ok = True
                    st.session_state.user_name = eposta.split("@")[0]
                    st.rerun()
                else:
                    st.error("Lütfen alanları doldurun.")
        with t2:
            st.text_input("Kullanıcı Adı Seç", placeholder="ornek_kullanici")
            st.text_input("E-posta", placeholder="kayit@domain.com")
            st.text_input("Şifre", type="password")
            if st.button("Kimlik Oluştur", use_container_width=True):
                st.success("Kayıt başarılı! Giriş Yap sekmesine geçebilirsin.")
        st.markdown("</div>", unsafe_allow_html=True)

# ================= DURUM 2: ANA SOSYAL PANEL =================
else:
    # Sol Menü Kontrolleri
    st.sidebar.markdown(f"### 👋 Selam @{st.session_state.user_name}")
    
    if st.session_state.mesaj_hakki > 0:
        st.sidebar.info(f"⚡ Kalan Güç: {st.session_state.mesaj_hakki} Kredi")
    else:
        st.sidebar.error("🚨 Bağlantı Koptu: 0 Kredi!")
        
    menu = st.sidebar.radio("📍 Sektör Seçin:", ["🌅 Deniz Odası", "💳 VIP Abonelik Al"])
    
    if st.sidebar.button("🔌 Çıkış Yap", use_container_width=True):
        st.session_state.giris_ok = False
        st.rerun()

    # --- SEKTÖR 1: SOHBET ODASI ---
    if menu == "🌅 Deniz Odası":
        st.markdown("# 🌅 Canlı Karakter Odası: 'Deniz'")
        
        col_img, col_chat = st.columns([1, 1.8])
        with col_img:
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.image("https://unsplash.com", use_column_width=True)
            st.markdown("<h3 style='text-align:center;'>Deniz (Ufka Bakan)</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_chat:
            st.markdown("<div class='glass-box' style='height: 350px; overflow-y: auto;'>", unsafe_allow_html=True)
            for m in st.session_state.sohbet_gecmisi:
                if m["role"] == "bot":
                    st.markdown(f"**🤖 Deniz:** {m['text']}\n")
                else:
                    st.markdown(f"**👤 Siz:** {m['text']}\n")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Kredi Kontrolü
            if st.session_state.mesaj_hakki > 0:
                if girdi := st.chat_input("Deniz ile konuş..."):
                    st.session_state.sohbet_gecmisi.append({"role": "user", "text": girdi})
                    st.session_state.mesaj_hakki -= 1
                    
                    # Talimat (Prompt)
                    deniz_prompt = "Sen 'Deniz' adında, iskelede denize bakarak felsefi ve sakin cümleler kuran gizemli bir karaktersin. Türkçe cevap ver."
                    bot_reply = bot_cevap_uret(deniz_prompt, st.session_state.sohbet_gecmisi)
                    
                    st.session_state.sohbet_gecmisi.append({"role": "bot", "text": bot_reply})
                    st.rerun()
            else:
                st.markdown("""
                    <div class='pay-card'>
                        <h3>⚠️ ÜCRETSİZ ERİŞİM BİTTİ (15/15)</h3>
                        <p>Deneme limitiniz doldu. Konuşmaya devam etmek için yan menüden VIP paketine geçin.</p>
                    </div>
                """, unsafe_allow_html=True)

    # --- SEKTÖR 2: KASA DAİRESİ (PARA KAZANMA) ---
    elif menu == "💳 VIP Abonelik Al":
        st.markdown("# 💳 VIP Kulübüne Katıl")
        st.markdown("""
            <div class='pay-card'>
                <h2>🏆 DEEPBLUE VIP RESIDENCE</h2>
                <p>15 Mesajlık yapay zeka sınırını tamamen ortadan kaldırın.</p>
                <h3 style='color:#10b981;'>99.00 TRY / Aylık</h3>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 iyzico ile Güvenli Satın Al (Simüle)", use_container_width=True):
            st.balloons()
            st.session_state.mesaj_hakki = 999999
            st.success("💳 Ödeme Onaylandı! 15 Mesajlık Sınır Kalıcı Olarak Kaldırıldı.")
