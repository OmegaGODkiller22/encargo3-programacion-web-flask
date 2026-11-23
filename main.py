from flask import Flask, render_template, request, abort

app = Flask(__name__)


def calcular_estado_academico(n1: float, n2: float, n3: float, asistencia: float):
    promedio = round((n1 + n2 + n3) / 3, 1)
    if promedio >= 40 and asistencia >= 75:
        estado = "APROBADO"
    else:
        estado = "REPROBADO"
    return promedio, estado


def obtener_nombre_mas_largo(n1: str, n2: str, n3: str):
    nombres = [n1.strip(), n2.strip(), n3.strip()]
    mayor = max(nombres, key=len)
    return mayor, len(mayor)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    promedio = None
    estado = None
    error = None
    nota1 = nota2 = nota3 = asistencia = None

    if request.method == "POST":
        try:
            nota1 = float(request.form.get("nota1", ""))
            nota2 = float(request.form.get("nota2", ""))
            nota3 = float(request.form.get("nota3", ""))
            asistencia = float(request.form.get("asistencia", ""))

            if not (10 <= nota1 <= 70 and 10 <= nota2 <= 70 and 10 <= nota3 <= 70):
                error = "Las notas deben estar entre 10 y 70."
            elif not (0 <= asistencia <= 100):
                error = "La asistencia debe estar entre 0 y 100."
            else:
                promedio, estado = calcular_estado_academico(nota1, nota2, nota3, asistencia)
        except ValueError:
            error = "Ingrese valores numéricos válidos."
        except Exception:
            abort(400)

    return render_template(
        "ejercicio1.html",
        promedio=promedio,
        estado=estado,
        error=error,
        nota1=nota1,
        nota2=nota2,
        nota3=nota3,
        asistencia=asistencia,
    )


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    nombre_mayor = None
    cantidad_caracteres = None
    error = None
    nombre1 = nombre2 = nombre3 = None

    if request.method == "POST":
        nombre1 = request.form.get("nombre1", "").strip()
        nombre2 = request.form.get("nombre2", "").strip()
        nombre3 = request.form.get("nombre3", "").strip()

        if not nombre1 or not nombre2 or not nombre3:
            error = "Debe completar los 3 nombres."
        elif len({nombre1.lower(), nombre2.lower(), nombre3.lower()}) < 3:
            error = "Debe ingresar 3 nombres diferentes."
        else:
            nombre_mayor, cantidad_caracteres = obtener_nombre_mas_largo(nombre1, nombre2, nombre3)

    return render_template(
        "ejercicio2.html",
        nombre_mayor=nombre_mayor,
        cantidad_caracteres=cantidad_caracteres,
        error=error,
        nombre1=nombre1,
        nombre2=nombre2,
        nombre3=nombre3,
    )


if __name__ == "__main__":
    app.run(debug=True)
