#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
backend.py - Nisa'ya Özür Sitesi (Render.com uyumlu)
Render'da çalıştırmak için: gunicorn backend:app
"""

from flask import Flask, render_template_string, request, jsonify
import os
import socket

app = Flask(__name__)

# ======================================================
# HTML KODU (index1.html'in tamamen aynısı)
# ======================================================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Nisa'ya Özür 🌸</title>
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            background: linear-gradient(145deg, #ffdde1 0%, #f9c9e7 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            margin: 0;
            position: relative;
            overflow-x: hidden;
            animation: bgPastel 12s infinite alternate ease-in-out;
        }

        @keyframes bgPastel {
            0% { background: linear-gradient(145deg, #ffe4ec, #fad0e6); }
            50% { background: linear-gradient(145deg, #ffe9f4, #fbc1d9); }
            100% { background: linear-gradient(145deg, #ffdeeb, #feb1d0); }
        }

        /* Kalp yağmuru arka plan */
        .hearts-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .heart-rain {
            position: absolute;
            font-size: 20px;
            color: rgba(255, 120, 160, 0.25);
            animation: floatHeart 8s linear infinite;
            user-select: none;
        }

        @keyframes floatHeart {
            0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
            10% { opacity: 0.8; }
            100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
        }

        /* Ana kart */
        .card {
            position: relative;
            z-index: 10;
            max-width: 500px;
            width: 100%;
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 60px 60px 80px 80px;
            box-shadow: 0 40px 60px rgba(255, 105, 135, 0.3), 0 20px 30px rgba(0, 0, 0, 0.1), inset 0 2px 5px rgba(255,255,255,0.8);
            padding: 35px 25px 40px 25px;
            border: 2px solid rgba(255, 220, 240, 0.9);
            transition: all 0.4s;
            animation: cardGlow 3s infinite alternate;
        }

        @keyframes cardGlow {
            0% { box-shadow: 0 35px 55px rgba(255, 120, 160, 0.3), 0 15px 25px rgba(0, 0, 0, 0.1); border-color: #ffb3c6; }
            100% { box-shadow: 0 45px 70px #ff9eb5, 0 20px 35px rgba(255, 80, 120, 0.4); border-color: #ff98b9; }
        }

        /* Başlık - Nisa özel */
        .nisa-title {
            text-align: center;
            margin-bottom: 25px;
            position: relative;
        }

        .name-glow {
            font-size: 5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #ff4d6d, #ff8fa3, #ffb3c6, #ff4d6d);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            letter-spacing: 8px;
            filter: drop-shadow(0 5px 10px #ffb6c1);
            animation: nameFlow 5s infinite, floatName 3s infinite ease-in-out;
            display: inline-block;
            text-shadow: 0 0 15px #fff5f7;
        }

        @keyframes nameFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes floatName {
            0% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
            100% { transform: translateY(0); }
        }

        .sub-heart {
            font-size: 2rem;
            color: #ff4d6d;
            animation: heartbeat 1.3s infinite;
            display: inline-block;
            margin: 0 5px;
        }

        @keyframes heartbeat {
            0% { transform: scale(1); }
            25% { transform: scale(1.2); color: #ff1e4d; }
            35% { transform: scale(1); }
            45% { transform: scale(1.1); }
            55% { transform: scale(1); }
            100% { transform: scale(1); }
        }

        /* Not kutusu (sevgilinin yazdığı not) */
        .message-box {
            background: rgba(255, 245, 250, 0.8);
            border-radius: 60px 60px 60px 10px;
            padding: 30px 25px;
            margin: 20px 0 25px;
            border: 3px dashed #ffa5c3;
            box-shadow: inset 0 0 30px #ffe2f0, 0 15px 20px rgba(255, 140, 170, 0.2);
            transform-origin: center;
            animation: messagePop 1.2s ease-out, borderGlow 2.2s infinite alternate;
        }

        @keyframes messagePop {
            0% { transform: scale(0.9) rotate(-1deg); opacity: 0; }
            70% { transform: scale(1.02) rotate(0.5deg); }
            100% { transform: scale(1) rotate(0); opacity: 1; }
        }

        @keyframes borderGlow {
            from { border-color: #ffa5c3; box-shadow: 0 0 15px #ffb6c1; }
            to { border-color: #ff4d6d; box-shadow: 0 0 35px #ff7a9e; }
        }

        .message-text {
            font-size: 1.15rem;
            line-height: 1.75;
            color: #3a2a2f;
            text-align: left;
            word-break: break-word;
            white-space: pre-wrap;
            font-weight: 500;
        }

        .message-text i {
            color: #ff4d6d;
            margin: 0 3px;
        }

        .message-text p {
            margin-bottom: 15px;
        }

        .highlight {
            background: linear-gradient(120deg, #ffe6ed 0%, #ffe6ed 40%);
            padding: 3px 8px;
            border-radius: 30px;
            font-weight: 700;
            color: #c1224b;
            display: inline-block;
            animation: softBlink 3s infinite;
        }

        @keyframes softBlink {
            0%,100% { background: #ffe6ed; }
            50% { background: #ffd9e6; }
        }

        /* Elcikler / gözler için ikon animasyon */
        .icon-line {
            display: flex;
            justify-content: center;
            gap: 25px;
            margin: 30px 0 15px;
        }

        .icon-item {
            font-size: 2.2rem;
            background: white;
            width: 70px;
            height: 70px;
            border-radius: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 20px #ffb8c9;
            color: #ff3b5c;
            transition: 0.3s;
            animation: iconDance 4s infinite;
            border: 2px solid white;
        }

        .icon-item:nth-child(1) { animation-delay: 0s; background: #ffeef2; }
        .icon-item:nth-child(2) { animation-delay: 0.5s; background: #fff0f5; }
        .icon-item:nth-child(3) { animation-delay: 1s; background: #ffe1ea; }

        @keyframes iconDance {
            0%,100% { transform: translateY(0) rotate(0deg); }
            25% { transform: translateY(-10px) rotate(5deg); }
            50% { transform: translateY(5px) rotate(-3deg); }
            75% { transform: translateY(-5px) rotate(2deg); }
        }

        /* affettim biliyorum - yeni soru kısmı */
        .forgiveness-box {
            background: rgba(255, 255, 255, 0.5);
            border-radius: 60px;
            padding: 20px 20px 30px;
            margin: 25px 0 15px;
            backdrop-filter: blur(5px);
            border: 2px solid white;
            text-align: center;
        }

        .question-text {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(145deg, #ff4d6d, #b34164);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 20px;
            line-height: 1.3;
        }

        .buttons {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }

        .btn {
            border: none;
            padding: 18px 40px;
            border-radius: 60px;
            font-size: 2rem;
            font-weight: bold;
            min-width: 150px;
            cursor: pointer;
            box-shadow: 0 10px 0 #b34164, 0 5px 20px rgba(255,0,100,0.4);
            transition: 0.1s ease;
            border: 2px solid white;
            letter-spacing: 2px;
        }

        .btn-evet {
            background: #77dd77;
            color: #1e5f1e;
            box-shadow: 0 10px 0 #2e7d32, 0 5px 20px #88d498;
        }

        .btn-evet:active {
            transform: translateY(7px);
            box-shadow: 0 3px 0 #2e7d32, 0 5px 20px #88d498;
        }

        .btn-hayir {
            background: #ffb4b4;
            color: #9b2c2c;
            box-shadow: 0 10px 0 #b24b4b, 0 5px 20px #ff9e9e;
            transition: all 0.2s;
        }

        .btn-hayir:active {
            transform: translateY(7px);
            box-shadow: 0 3px 0 #b24b4b;
        }

        /* hayır kaçış animu */
        .hayir-kaciyor {
            position: relative;
            transition: all 0.15s ease-out;
        }

        /* EVET sonrası gösterilecek script mesajı */
        .affetme-mesaji {
            background: rgba(255,255,240,0.9);
            border-radius: 50px;
            padding: 25px;
            margin: 20px 0 10px;
            border: 4px solid #ff99aa;
            font-size: 1.7rem;
            color: #c1224b;
            animation: fadeSlide 0.5s, heartbeat 1.8s infinite;
            text-align: center;
            box-shadow: 0 0 30px #ffa5c3;
            backdrop-filter: blur(10px);
        }

        @keyframes fadeSlide {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .footer-note {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-size: 1rem;
            color: #a14a62;
            margin-top: 25px;
            font-style: italic;
            background: rgba(255,220,235,0.7);
            padding: 12px 20px;
            border-radius: 50px;
            border: 1px solid white;
            animation: slideUp 1.4s;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .footer-note i {
            font-size: 1.6rem;
            color: #ff4d6d;
            animation: rotateLove 3s infinite;
        }

        @keyframes rotateLove {
            0% { transform: rotate(0deg); }
            25% { transform: rotate(10deg); }
            75% { transform: rotate(-10deg); }
            100% { transform: rotate(0deg); }
        }

        /* tekrar buton (saklı) */
        .reset-link {
            text-align: center;
            margin-top: 10px;
        }
        .reset-link a {
            color: #9f4d6a;
            font-size: 0.9rem;
            background: rgba(255,255,255,0.7);
            padding: 5px 15px;
            border-radius: 40px;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <!-- arkaplan uçuşan kalpler -->
    <div class="hearts-bg" id="heart-bg"></div>

    <!-- ana kart -->
    <div class="card" id="mainCard">
        <div class="nisa-title">
            <span class="sub-heart"><i class="fas fa-heart"></i></span>
            <span class="name-glow">NİSA</span>
            <span class="sub-heart"><i class="fas fa-heart"></i></span>
        </div>

        <!-- gözler, elcikler ikonları -->
        <div class="icon-line">
            <div class="icon-item"><i class="fas fa-eye"></i></div>
            <div class="icon-item"><i class="fas fa-sparkles"></i></div>
            <div class="icon-item"><i class="fas fa-hand-peace"></i></div>
        </div>

        <!-- AŞKIN YAZDIĞI NOT (birebir aynı) -->
        <div class="message-box">
            <div class="message-text">
                <p><i class="fas fa-heart" style="color:#ff4d6d;"></i> <span class="highlight">Benim güzeller güzeli allahım</span> ben senin kölenim çok özür dilerim kalbini kırdıysam gözlerindeki parıltıdan tut elciklerine kadar asığım o gözlerden akan tek damla yaş için ömrümü veririm haklı olmak istemiyorum ben seni istiyorum affettin biliyorum ama içimden geldi bu site bilgisayar yok çok detay olmamıs olabilir normalde daha iyilerini yaparım ama mobilden bu geldi elimden askım</p>
                <p style="text-align: right; font-size: 1.4rem; margin-bottom: 0;">💖</p>
            </div>
        </div>

        <!-- SORU: beni affettin mi ömrim?  + butonlar -->
        <div class="forgiveness-box" id="soruBolumu">
            <div class="question-text">beni affettin mi ömrim? 💭</div>
            <div class="buttons">
                <button class="btn btn-evet" id="evetBtn">EVET 💞</button>
                <button class="btn btn-hayir" id="hayirBtn">HAYIR 😥</button>
            </div>
        </div>

        <!-- mesaj buraya gelecek (evet tıklanınca) -->
        <div id="mesajAlani" style="min-height: 20px;"></div>

        <!-- mobil samimiyeti -->
        <div class="footer-note">
            <i class="fas fa-mobile-alt"></i>
            <span>mobilden ellerimden öptü, bilgisayar yoktu ama &nbsp;💖</span>
            <i class="fas fa-heart"></i>
        </div>

        <!-- tekrar göstermek için minik link -->
        <div class="reset-link">
            <a href="#" onclick="resetPage(event)">🔁 tekrar dene canım</a>
        </div>
    </div>

    <script>
        // kalp yağmuru
        function createHearts() {
            const bg = document.getElementById('heart-bg');
            const heartCount = 24;
            for (let i = 0; i < heartCount; i++) {
                let heart = document.createElement('div');
                heart.className = 'heart-rain';
                heart.innerHTML = '❤️';
                heart.style.left = Math.random() * 100 + '%';
                heart.style.animationDuration = (Math.random() * 6 + 6) + 's';
                heart.style.fontSize = (Math.random() * 25 + 15) + 'px';
                heart.style.animationDelay = (Math.random() * -10) + 's';
                heart.style.opacity = Math.random() * 0.4 + 0.2;
                bg.appendChild(heart);
            }
        }

        // hayır butonuna kaçış özelliği
        const hayirBtn = document.getElementById('hayirBtn');
        if (hayirBtn) {
            hayirBtn.addEventListener('mouseover', function(e) {
                const container = document.querySelector('.buttons');
                if (!container) return;
                const maxX = container.clientWidth - this.clientWidth - 20;
                const maxY = container.clientHeight - this.clientHeight - 10;
                let x = Math.random() * maxX;
                let y = Math.random() * maxY;
                x = Math.max(5, Math.min(x, maxX));
                y = Math.max(5, Math.min(y, maxY));
                this.style.position = 'relative';
                this.style.left = x + 'px';
                this.style.top = y + 'px';
                this.style.transform = 'scale(0.95)';
            });

            hayirBtn.addEventListener('touchstart', function(e) {
                e.preventDefault();
                const container = document.querySelector('.buttons');
                if (!container) return;
                const maxX = container.clientWidth - this.clientWidth - 20;
                const maxY = container.clientHeight - this.clientHeight - 10;
                let x = Math.random() * maxX;
                let y = Math.random() * maxY;
                x = Math.max(5, Math.min(x, maxX));
                y = Math.max(5, Math.min(y, maxY));
                this.style.position = 'relative';
                this.style.left = x + 'px';
                this.style.top = y + 'px';
                this.style.transform = 'scale(0.95)';
            });
        }

        document.getElementById('evetBtn').addEventListener('click', function() {
            const mesajAlani = document.getElementById('mesajAlani');
            mesajAlani.innerHTML = '';

            const affetDiv = document.createElement('div');
            affetDiv.className = 'affetme-mesaji';
            affetDiv.innerHTML = '❤️ Seni çok seviyorum bebeğim, iyi ki varsın Nisa ❤️';
            mesajAlani.appendChild(affetDiv);

            document.getElementById('soruBolumu').style.display = 'none';

            for (let i=0; i<8; i++) {
                setTimeout(() => {
                    let emoji = document.createElement('div');
                    emoji.style.position = 'fixed';
                    emoji.style.left = Math.random()*100 + '%';
                    emoji.style.top = '-20px';
                    emoji.style.fontSize = (30+Math.random()*20)+'px';
                    emoji.style.zIndex = '9999';
                    emoji.style.pointerEvents = 'none';
                    emoji.innerText = '💖🌸✨';
                    document.body.appendChild(emoji);
                    let fall = setInterval(() => {
                        let top = parseInt(emoji.style.top);
                        if (top > window.innerHeight) {
                            clearInterval(fall);
                            emoji.remove();
                        } else {
                            emoji.style.top = (top + 5) + 'px';
                        }
                    }, 30);
                }, i*100);
            }
        });

        window.resetPage = function(e) {
            e.preventDefault();
            document.getElementById('soruBolumu').style.display = 'block';
            document.getElementById('mesajAlani').innerHTML = '';
            const hayir = document.getElementById('hayirBtn');
            hayir.style.position = 'static';
            hayir.style.left = 'auto';
            hayir.style.top = 'auto';
            hayir.style.transform = 'none';
        };

        window.onload = function() {
            createHearts();
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Ana sayfayı göster"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health', methods=['GET'])
def health_check():
    """Render'ın sağlık kontrolü için"""
    return jsonify({"status": "healthy", "message": "Nisa'nın kalbi atıyor ❤️"})

@app.route('/api/affet', methods=['POST'])
def affet_api():
    """Butona tıklanınca backend'e kayıt düşer"""
    data = request.get_json()
    if data and data.get('cevap') == 'evet':
        print("💞 Nisa affetti! (backend kaydı)")
        return jsonify({"durum": "başarılı", "mesaj": "kaydedildi"})
    return jsonify({"durum": "bekleniyor"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print("🌸 NİSA'YA ÖZÜR SİTESİ BAŞLATILDI 🌸")
    print("=" * 50)
    print(f"🚀 Sunucu port {port} üzerinde çalışıyor...")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
