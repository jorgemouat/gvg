from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from .jumpseller_utils import get_all_products, disable_products, notify_slack
from .settings import MAGIC_WORD

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def form_view():
    return """
    <html>
        <head>
            <title>GVG Disable Script</title>
            <meta name='viewport' content='width=device-width, initial-scale=1'>
            <style>
                html, body {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }
                body {
                    font-family: sans-serif;
                    background: #f7f7fa;
                    text-align: center;
                    margin-top: 8vw;
                }
                h1 {
                    font-size: 6vw;
                    margin-bottom: 5vw;
                }
                form, .modal-content {
                    width: 90vw;
                    max-width: 350px;
                    margin: 0 auto;
                }
                input[name='magic_word'] {
                    padding: 3vw;
                    font-size: 1.2em;
                    width: 80%;
                    max-width: 250px;
                    margin-bottom: 3vw;
                }
                button[type='submit'], button[onclick] {
                    padding: 3vw;
                    font-size: 1.1em;
                    border-radius: 8px;
                    border: none;
                    margin-top: 2vw;
                    margin-bottom: 2vw;
                    background: #ffe066;
                    cursor: pointer;
                    width: 90%;
                    max-width: 320px;
                }
                .loader {
                    display: inline-block;
                    animation: spin 1s linear infinite;
                    font-size: 2em;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg);}
                    100% { transform: rotate(360deg);}
                }
                /* Modal styles */
                .modal {
                    display: none;
                    position: fixed;
                    z-index: 999;
                    left: 0;
                    top: 0;
                    width: 100vw;
                    height: 100vh;
                    overflow: auto;
                    background-color: rgba(0,0,0,0.4);
                }
                .modal-content {
                    background-color: #fff;
                    margin: 30vh auto 0 auto;
                    padding: 7vw 5vw;
                    border: 1px solid #888;
                    border-radius: 12px;
                    text-align: center;
                    font-size: 1.5em;
                }
                .close {
                    color: #aaa;
                    float: right;
                    font-size: 28px;
                    font-weight: bold;
                    cursor: pointer;
                }
                .close:hover { color: #000; }
                @media (min-width: 600px) {
                    h1 { font-size: 2.2em; }
                    form, .modal-content { width: 350px; }
                }
            </style>
            <script>
                function showLoading() {
                    document.getElementById('loading').style.display = 'block';
                }
                function showModal() {
                    document.getElementById('myModal').style.display = 'block';
                }
                function closeModal() {
                    document.getElementById('myModal').style.display = 'none';
                }
            </script>
        </head>
        <body>
            <h1>🪄 Bienvenido José, Pichula Chica, Mayo! 🪄</h1>
            <form method=\"post\" onsubmit=\"showLoading()\">
                <p style='font-size:1.1em;'>Pon la <b>clave secreta</b> pa correr la wea:</p>
                <input name=\"magic_word\" type=\"text\" autofocus>
                <button type=\"submit\">✨ Haz click aquí po perroooo! ✨</button>
            </form>
            <div id=\"loading\" style=\"display:none; margin-top:30px; font-size:1.3em; color:#444;\">
                <span class=\"loader\">🌀</span>
                <span style=\"margin-left:10px;\">Ten paciencia ql, ya cargará...</span>
            </div>
            <br><br>
            <button onclick=\"showModal()\">👀 Cacha esta wea</button>
            <div id=\"myModal\" class=\"modal\">
                <div class=\"modal-content\">
                    <span class=\"close\" onclick=\"closeModal()\">&times;</span>
                    <p>pico pal que lee</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/", response_class=HTMLResponse)
async def run_script_post(magic_word: str = Form(...)):
    if magic_word.strip().lower() == MAGIC_WORD:
        products = get_all_products()
        result = "disable_products(products)"
        notify_slack()
        return f"""
        <html>
            <head>
                <meta name='viewport' content='width=device-width, initial-scale=1'>
                <style>
                    html, body {{
                        box-sizing: border-box;
                        margin: 0;
                        padding: 0;
                    }}
                    body {{
                        font-family: sans-serif;
                        background: #eaffea;
                        text-align: center;
                        margin-top: 8vw;
                    }}
                    h2 {{
                        font-size: 6vw;
                        margin-bottom: 5vw;
                        color: #1a7f37;
                    }}
                    p {{
                        font-size: 1.3em;
                        margin-bottom: 2vw;
                    }}
                    pre {{
                        text-align: left;
                        display: inline-block;
                        background: #fff;
                        padding: 16px;
                        border-radius: 8px;
                        font-size: 1em;
                        max-width: 90vw;
                        overflow-x: auto;
                        margin-bottom: 2vw;
                    }}
                    a {{
                        display: inline-block;
                        margin-top: 2vw;
                        padding: 2vw 5vw;
                        background: #ffe066;
                        color: #222;
                        border-radius: 8px;
                        text-decoration: none;
                        font-size: 1.1em;
                        font-weight: bold;
                    }}
                    @media (min-width: 600px) {{
                        h2 {{ font-size: 2.2em; }}
                        p {{ font-size: 1.2em; }}
                        pre {{ max-width: 500px; }}
                        a {{ font-size: 1.1em; }}
                    }}
                </style>
            </head>
            <body>
                <h2>🎉 No se porque funcionó, pero bacan! 🎉</h2>
                <p>Desactivados: <b>{len(products)}</b></p>
                <pre>{chr(10).join(result)}</pre>
                <br><a href="/">🔙 Correlo again</a>
            </body>
        </html>
        """
    else:
        return """
        <html>
            <head>
                <meta name='viewport' content='width=device-width, initial-scale=1'>
                <style>
                    html, body {
                        box-sizing: border-box;
                        margin: 0;
                        padding: 0;
                    }
                    body {
                        font-family: sans-serif;
                        background: #fff3f3;
                        text-align: center;
                        margin-top: 8vw;
                    }
                    h2 {
                        font-size: 6vw;
                        margin-bottom: 5vw;
                        color: #c00;
                    }
                    p {
                        font-size: 1.3em;
                        margin-bottom: 2vw;
                    }
                    img {
                        margin: 2vw 0;
                        max-width: 90vw;
                        border-radius: 12px;
                    }
                    a {
                        display: inline-block;
                        margin-top: 2vw;
                        padding: 2vw 5vw;
                        background: #ffe066;
                        color: #222;
                        border-radius: 8px;
                        text-decoration: none;
                        font-size: 1.1em;
                        font-weight: bold;
                    }
                    @media (min-width: 600px) {
                        h2 { font-size: 2.2em; }
                        p { font-size: 1.2em; }
                        img { max-width: 350px; }
                        a { font-size: 1.1em; }
                    }
                </style>
            </head>
            <body>
                <h2>🧙‍♂️ Uuuuu malo culiao achuntale! 🧙‍♂️</h2>
                <p>Trata de nuevo carepico...</p>
                <img src=\"https://media.giphy.com/media/3o7TKtnuHOHHUjR38Y/giphy.gif\" width=\"300\"/>
                <br><a href=\"/\">🔙 Back</a>
            </body>
        </html>
        """
