from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import urllib.request
import json

# ==== НАСТРОЙКИ ТВОЕГО БОТА ====
TELEGRAM_TOKEN = "8577326327:AAHPP8B1upqNmXSI8N3nPc_S2jJ5ROslw-c"
TELEGRAM_CHAT_ID = "5587705234"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# ==== HTML ====
HTML = """
<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<title>Інтернет-магазин</title>
<style>
body {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, #f8f9fb, #e8ecf3);
  margin: 0;
  color: #333;
}
.sidebar {
  width: 230px;
  background: #1e1f2e;
  color: white;
  height: 100vh;
  position: fixed;
  top: 0; left: 0;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0,0,0,0.25);
}
.sidebar h2 {
  text-align: center;
  margin: 25px 0;
  font-size: 22px;
  font-weight: 600;
}
.sidebar button {
  background: none;
  border: none;
  color: white;
  text-align: left;
  padding: 15px 25px;
  font-size: 16px;
  cursor: pointer;
  transition: 0.2s;
}
.sidebar button:hover {
  background: rgba(255,255,255,0.1);
}
.main {
  margin-left: 250px;
  padding: 40px;
}
h1 {
  font-size: 30px;
  margin-bottom: 25px;
}
.products {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px;
}
.product {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}
.product:hover {
  transform: translateY(-5px);
}
.product img {
  width: 100%;
  border-radius: 10px;
  height: 180px;
  object-fit: cover;
}
button.buy {
  background: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  transition: 0.2s;
}
button.buy:hover { background: #218838; }

.cart-item {
  background: white;
  margin: 10px 0;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
button.remove {
  background: #dc3545;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
}
button.remove:hover { background: #c82333; }
.total {
  font-weight: bold;
  font-size: 18px;
  margin-top: 20px;
}
button.data {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  margin-top: 15px;
  cursor: pointer;
  font-size: 16px;
}
button.data:hover { background: #0069d9; }

/* Модальне вікно */
.modal {
  display: none;
  position: fixed;
  z-index: 10;
  left: 0; top: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.5);
}
.modal-content {
  background: white;
  padding: 25px;
  border-radius: 10px;
  width: 320px;
  margin: 10% auto;
  text-align: center;
  box-shadow: 0 3px 10px rgba(0,0,0,0.3);
}
input {
  width: 90%;
  padding: 10px;
  margin: 7px 0;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}
button.send {
  background: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  margin-top: 10px;
  cursor: pointer;
}
button.send:hover { background: #218838; }

/* Вкладка Інформація */
.info {
  background: white;
  border-radius: 12px;
  padding: 25px;
  max-width: 500px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  line-height: 1.7;
}
.info a {
  color: #007bff;
  text-decoration: none;
}
.info a:hover {
  text-decoration: underline;
}
</style>
</head>
<body>
<div class="sidebar">
  <h2>🛒 Меню</h2>
  <button onclick="showTab('products')">Товари</button>
  <button onclick="showTab('cart')">Корзина</button>
  <button onclick="showTab('info')">Інформація</button>
</div>

<div class="main">
  <div id="products" class="tab">
    <h1>Наші товари</h1>
    <div class="products">
      <div class="product">
        <img src="https://cdn.tgdd.vn/Products/Images/7327/223886/microwave-1-600x600.jpg" alt="Мікрохвильовка">
        <h3>Мікрохвильовка</h3>
        <p>Ціна: 200 грн</p>
        <button class="buy" onclick="addToCart('Мікрохвильовка', 200)">Додати</button>
      </div>
      <div class="product">
        <img src="https://cdn.tgdd.vn/Products/Images/1942/222758/tu-lanh-1-600x600.jpg" alt="Холодильник">
        <h3>Холодильник</h3>
        <p>Ціна: 500 грн</p>
        <button class="buy" onclick="addToCart('Холодильник', 500)">Додати</button>
      </div>
      <div class="product">
        <img src="https://cdn.tgdd.vn/Products/Images/7328/211464/iron-1-600x600.jpg" alt="Праска">
        <h3>Праска</h3>
        <p>Ціна: 150 грн</p>
        <button class="buy" onclick="addToCart('Праска', 150)">Додати</button>
      </div>
      <div class="product">
        <img src="https://cdn.tgdd.vn/Products/Images/1949/222814/toaster-1-600x600.jpg" alt="Тостер">
        <h3>Тостер</h3>
        <p>Ціна: 250 грн</p>
        <button class="buy" onclick="addToCart('Тостер', 250)">Додати</button>
      </div>
    </div>
  </div>

  <div id="cart" class="tab" style="display:none;">
    <h1>Корзина</h1>
    <div id="cartList"></div>
    <div class="total" id="total"></div>
    <button class="data" onclick="openModal()">Ввести дані</button>
  </div>

  <div id="info" class="tab" style="display:none;">
    <h1>Інформація</h1>
    <div class="info">
      <p><b>📞 Телефон:</b> +380 99 123 45 67</p>
      <p><b>📍 Адреса:</b> м. Київ, вул. Незалежності, 12</p>
      <p><b>💬 Telegram:</b> <a href="https://t.me/yourshop" target="_blank">@yourshop</a></p>
    </div>
  </div>
</div>

<!-- Модальне вікно -->
<div id="modal" class="modal">
  <div class="modal-content">
    <h3>Введіть ваші дані</h3>
    <input id="phone" type="text" placeholder="Номер телефону"><br>
    <input id="email" type="email" placeholder="Ел. пошта"><br>
    <input id="address" type="text" placeholder="Адреса проживання"><br>
    <button class="send" onclick="sendOrder()">Відправити</button>
  </div>
</div>

<script>
let cart = [];

function showTab(tab) {
  document.getElementById('products').style.display = (tab === 'products') ? 'block' : 'none';
  document.getElementById('cart').style.display = (tab === 'cart') ? 'block' : 'none';
  document.getElementById('info').style.display = (tab === 'info') ? 'block' : 'none';
}

function addToCart(name, price) {
  cart.push({name, price});
  updateCart();
  alert('✅ Товар додано до корзини!');
}

function removeFromCart(index) {
  cart.splice(index, 1);
  updateCart();
}

function updateCart() {
  const list = document.getElementById('cartList');
  list.innerHTML = '';
  let total = 0;
  cart.forEach((item, i) => {
    total += item.price;
    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = item.name + ' — ' + item.price + ' грн' +
      ' <button class="remove" onclick="removeFromCart(' + i + ')">Видалити</button>';
    list.appendChild(div);
  });
  document.getElementById('total').textContent = total > 0 ? 'Загалом: ' + total + ' грн' : '';
}

function openModal() {
  if (cart.length === 0) {
    alert('Корзина порожня!');
    return;
  }
  document.getElementById('modal').style.display = 'block';
}

function sendOrder() {
  const phone = document.getElementById('phone').value.trim();
  const email = document.getElementById('email').value.trim();
  const address = document.getElementById('address').value.trim();

  if (!phone || !email || !address) {
    alert('Будь ласка, заповніть всі поля!');
    return;
  }

  let total = 0;
  let productList = '';
  cart.forEach(item => {
    total += item.price;
    productList += ` - ${item.name} — ${item.price} грн\\n`;
  });

  const message =
    `📞 Номер телефону: ${phone}\\n` +
    `📧 Пошта: ${email}\\n` +
    `🏠 Адреса: ${address}\\n` +
    `💰 Загальна сума: ${total} грн\\n` +
    `🛒 Товари:\\n${productList}`;

  fetch('/order', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'message=' + encodeURIComponent(message)
  });

  alert('✅ Замовлення відправлено!');
  cart = [];
  updateCart();
  document.getElementById('modal').style.display = 'none';
}
</script>
</body>
</html>
"""

# ==== СЕРВЕР ====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def do_POST(self):
        if self.path == "/order":
            length = int(self.headers.get("Content-Length", 0))
            data = urllib.parse.parse_qs(self.rfile.read(length).decode())
            message = data.get("message", [""])[0]
            send_telegram(message)
            self.send_response(200)
            self.end_headers()

def send_telegram(text):
    try:
        data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": text}).encode()
        req = urllib.request.Request(API_URL, data=data)
        urllib.request.urlopen(req)
    except Exception as e:
        print("❌ Помилка Telegram:", e)

def run():
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("✅ Сайт запущено: http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    run()
