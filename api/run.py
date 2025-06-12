from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from api.jumpseller_utils import get_all_products, disable_products, notify_slack
from api.settings import MAGIC_WORD

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def form_view():
    return """
    <html>
        <head>
            <title>Desactivador de Productos GVG</title>
            <meta name='viewport' content='width=device-width, initial-scale=1'>
            <style>
                html, body {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: #f4f6fb;
                    text-align: center;
                    margin-top: 8vw;
                }
                h1 {
                    font-size: 2.2em;
                    margin-bottom: 2vw;
                    color: #222;
                    font-weight: 600;
                }
                form, .modal-content {
                    width: 90vw;
                    max-width: 350px;
                    margin: 0 auto;
                    background: #fff;
                    border-radius: 12px;
                    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
                    padding: 2.5em 1.5em 2em 1.5em;
                }
                input[name='magic_word'] {
                    padding: 0.9em;
                    font-size: 1.1em;
                    width: 80%;
                    max-width: 250px;
                    margin-bottom: 1.5em;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    outline: none;
                    transition: border 0.2s;
                }
                input[name='magic_word']:focus {
                    border: 1.5px solid #4f8cff;
                }
                button[type='submit'] {
                    padding: 0.9em;
                    font-size: 1.1em;
                    border-radius: 8px;
                    border: none;
                    margin-top: 0.5em;
                    background: #4f8cff;
                    color: #fff;
                    cursor: pointer;
                    width: 90%;
                    max-width: 320px;
                    font-weight: 500;
                    transition: background 0.2s;
                }
                button[type='submit']:hover {
                    background: #2563eb;
                }
                #loading {
                    display: none;
                    margin-top: 30px;
                    font-size: 1.1em;
                    color: #444;
                }
                @media (min-width: 600px) {
                    h1 { font-size: 2.2em; }
                    form, .modal-content { width: 350px; }
                }
            </style>
            <script>
                function showLoading() {
                    document.getElementById('loading').style.display = 'block';
                    var bar = document.getElementById('progress-bar');
                    var width = 0;
                    bar.style.width = '0%';
                    var interval = setInterval(function() {
                        if (width >= 100) {
                            clearInterval(interval);
                        } else {
                            width += Math.random() * 7 + 2; // random progress
                            if (width > 100) width = 100;
                            bar.style.width = width + '%';
                        }
                    }, 250);
                }
            </script>
        </head>
        <body>
            <h1>Desactivador de Productos GVG</h1>
            <form method="post" onsubmit="showLoading()">
                <p style='font-size:1.1em; color:#555;'>Ingresa la clave de acceso para continuar:</p>
                <input name="magic_word" type="password" autofocus required>
                <button type="submit">Desactivar productos</button>
            </form>
            <div id="loading" style="display:none; margin-top:30px; font-size:1.1em; color:#444;">
                <div style="width: 100%; max-width: 320px; margin: 0 auto;">
                    <div id="progress-bar-container" style="background: #e0e0e0; border-radius: 8px; height: 18px; width: 100%; overflow: hidden;">
                        <div id="progress-bar" style="height: 100%; width: 0%; background: linear-gradient(90deg, #4f8cff 60%, #2563eb 100%); transition: width 0.3s;"></div>
                    </div>
                </div>
                <span style="display:block; margin-top:10px;">Procesando...</span>
            </div>
        </body>
    </html>
    """

@app.post("/", response_class=HTMLResponse)
async def run_script_post(magic_word: str = Form(...)):
    if magic_word.strip().lower() == MAGIC_WORD:
        products = get_all_products()
        result = disable_products(products)
        # notify_slack()
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
                        font-family: 'Segoe UI', Arial, sans-serif;
                        background: #f4f6fb;
                        text-align: center;
                        margin-top: 8vw;
                    }}
                    h2 {{
                        font-size: 2em;
                        margin-bottom: 1.5vw;
                        color: #2563eb;
                        font-weight: 600;
                    }}
                    p {{
                        font-size: 1.1em;
                        margin-bottom: 1.5vw;
                        color: #333;
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
                        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                    }}
                    a {{
                        display: inline-block;
                        margin-top: 2vw;
                        padding: 0.7em 2em;
                        background: #4f8cff;
                        color: #fff;
                        border-radius: 8px;
                        text-decoration: none;
                        font-size: 1.1em;
                        font-weight: 500;
                        transition: background 0.2s;
                    }}
                    a:hover {{ background: #2563eb; }}
                    @media (min-width: 600px) {{
                        h2 {{ font-size: 2.2em; }}
                        p {{ font-size: 1.2em; }}
                        pre {{ max-width: 500px; }}
                        a {{ font-size: 1.1em; }}
                    }}
                </style>
            </head>
            <body>
                <h2>Productos desactivados correctamente</h2>
                <p>Total desactivados: <b>{len(products)}</b></p>
                <pre>{chr(10).join(result)}</pre>
                <a href=\"/\">Volver al inicio</a>
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
                        font-family: 'Segoe UI', Arial, sans-serif;
                        background: #fff3f3;
                        text-align: center;
                        margin-top: 8vw;
                    }
                    h2 {
                        font-size: 2em;
                        margin-bottom: 1.5vw;
                        color: #c00;
                        font-weight: 600;
                    }
                    p {
                        font-size: 1.1em;
                        margin-bottom: 1.5vw;
                        color: #333;
                    }
                    a {
                        display: inline-block;
                        margin-top: 2vw;
                        padding: 0.7em 2em;
                        background: #4f8cff;
                        color: #fff;
                        border-radius: 8px;
                        text-decoration: none;
                        font-size: 1.1em;
                        font-weight: 500;
                        transition: background 0.2s;
                    }
                    a:hover { background: #2563eb; }
                    @media (min-width: 600px) {
                        h2 { font-size: 2.2em; }
                        p { font-size: 1.2em; }
                        a { font-size: 1.1em; }
                    }
                </style>
            </head>
            <body>
                <h2>Acceso denegado</h2>
                <p>La clave de acceso ingresada es incorrecta. Inténtalo nuevamente.</p>
                <a href=\"/\">Volver al inicio</a>
            </body>
        </html>
        """
