from flask import Flask, request, render_template_string
import csv
import os
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# HTML sablon: forma + prikaz
# -----------------------------
HTML_FORM = r"""
<!DOCTYPE html>
<html lang="sr">
<head>
  <meta charset="UTF-8">
  <title>Izveštaj - Railway Demo</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f2f5f9;
      margin: 0; padding: 0;
      color: #333;
    }
    .container {
      max-width: 600px; 
      margin: 50px auto; 
      padding: 20px; 
      background: #fff; 
      border-radius: 4px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    h1 { text-align: center; }
    label { display: block; margin-top: 10px; font-weight: bold; }
    input[type=text], input[type=date], textarea {
      width: 100%; 
      padding: 8px; 
      margin-top: 5px; 
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }
    textarea { resize: vertical; }
    button {
      margin-top: 15px;
      background-color: #7da2cc;
      color: #fff;
      border: none; 
      padding: 10px 16px;
      border-radius: 4px;
      cursor: pointer;
    }
    button:hover {
      background-color: #6b91b8;
    }
    .report {
      margin-top: 20px;
      padding: 15px;
      background: #eef2f6;
      border: 1px dashed #aaa;
    }
    .field { margin: 6px 0; }
    .field strong { margin-right: 4px; }
  </style>
</head>
<body>
<div class="container">
  <h1>Railway Flask - Izveštaj</h1>
  <form action="/" method="POST">
    <label>Ime i prezime:</label>
    <input type="text" name="ime" required/>

    <label>Grad/Mesto:</label>
    <input type="text" name="grad"/>

    <label>Datum rođenja:</label>
    <input type="date" name="datum_rodj"/>

    <label>Telefon:</label>
    <input type="text" name="telefon"/>

    <label>Anamneza:</label>
    <textarea name="anamneza" rows="3"></textarea>

    <label>Objektivni nalaz:</label>
    <textarea name="nalaz" rows="3"></textarea>

    <label>Dijagnoza (F-šifra):</label>
    <input type="text" name="dijagnoza" placeholder="npr: F20.0: Paranoidna šizofrenija"/>

    <label>Terapija (lekovi):</label>
    <input type="text" name="lekovi" placeholder="npr: Haloperidol 5 mg"/>

    <label>Zaključak:</label>
    <input type="text" name="zakljucak"/>

    <label>Datum pregleda:</label>
    <input type="date" name="datum_pregleda"/>

    <button type="submit">Sačuvaj izveštaj</button>
  </form>

  {% if show_report %}
  <div class="report">
    <h3>Sačuvano u izvestaji.csv:</h3>
    <div class="field"><strong>Ime:</strong> {{ ime }}</div>
    <div class="field"><strong>Grad:</strong> {{ grad }}</div>
    <div class="field"><strong>Datum rođenja:</strong> {{ datum_rodj }}</div>
    <div class="field"><strong>Telefon:</strong> {{ telefon }}</div>
    <div class="field"><strong>Anamneza:</strong> {{ anamneza }}</div>
    <div class="field"><strong>Nalaz:</strong> {{ nalaz }}</div>
    <div class="field"><strong>Dijagnoza:</strong> {{ dijagnoza }}</div>
    <div class="field"><strong>Lekovi:</strong> {{ lekovi }}</div>
    <div class="field"><strong>Zaključak:</strong> {{ zakljucak }}</div>
    <div class="field"><strong>Datum pregleda:</strong> {{ datum_pregleda }}</div>
  </div>
  {% endif %}
</div>
</body>
</html>
"""

CSV_FILENAME = "izvestaji.csv"

# Ako ne postoji csv fajl, kreiramo ga sa headerom
if not os.path.exists(CSV_FILENAME):
    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ime", "grad", "datum_rodj", "telefon", 
            "anamneza", "nalaz", "dijagnoza", "lekovi", 
            "zakljucak", "datum_pregleda", "vreme_unosa"
        ])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Preuzimamo podatke iz forme
        ime = request.form.get("ime","")
        grad = request.form.get("grad","")
        datum_rodj = request.form.get("datum_rodj","")
        telefon = request.form.get("telefon","")
        anamneza = request.form.get("anamneza","")
        nalaz = request.form.get("nalaz","")
        dijagnoza = request.form.get("dijagnoza","")
        lekovi = request.form.get("lekovi","")
        zakljucak = request.form.get("zakljucak","")
        datum_pregleda = request.form.get("datum_pregleda","")

        # Upisujemo red u CSV
        vreme_sada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CSV_FILENAME, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                ime, grad, datum_rodj, telefon, 
                anamneza, nalaz, dijagnoza, lekovi, 
                zakljucak, datum_pregleda, vreme_sada
            ])

        # Vraćamo formu + prikaz upravo snimljenog unosa
        return render_template_string(
            HTML_FORM,
            show_report=True,
            ime=ime,
            grad=grad,
            datum_rodj=datum_rodj,
            telefon=telefon,
            anamneza=anamneza,
            nalaz=nalaz,
            dijagnoza=dijagnoza,
            lekovi=lekovi,
            zakljucak=zakljucak,
            datum_pregleda=datum_pregleda
        )
    else:
        # GET metod -> samo prikaži praznu formu
        return render_template_string(HTML_FORM, show_report=False)

# Railway obično čita PORT iz env var
# U loc. testu: python izvestaj.py => app.run(debug=True, port=5000)
# U Railway: oni automatski postave PORT
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
