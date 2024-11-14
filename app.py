from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/api/quotation', methods=['POST'])
def quotation():
    data = request.get_json()
    rubro = data.get('rubro')
    colaboradores = data.get('colaboradores')
    centros = data.get('centros')
    solucion = data.get('solucion')
    modulos = data.get('modulos', [])

    # Cálculo del valor base por empresa
    E_base = 2.39 * math.pow(colaboradores, 0.376)
    E = E_base

    # Aplicar ponderador si el rubro es EXPLOTACION DE MINAS Y CANTERAS
    if rubro == "C - EXPLOTACION DE MINAS Y CANTERAS":
        E *= 1.254

    # Aplicar modificador según la solución seleccionada
    modularizado_excedido = None
    if solucion == "PLAN AVANZADO":
        E *= 1.3
    elif solucion == "MODULARIZADO":
        # Sumar los porcentajes de los módulos seleccionados
        porcentaje_total = sum([
            0.804 if modulo == "PROGRAMA PERSONALIZADO" else
            0.432 if modulo == "PROGRAMA INDUCCIONES" else
            0.317 if modulo == "PROGRAMA CHARLAS CAPACITACIONES" else
            0.432 if modulo == "PROGRAMA GESTION HALLAZGOS" else
            0.65 if modulo == "PROGRAMA INSPECCIONES" else
            0.65 if modulo == "PROGRAMA INSUMO MAQUINARIA" else
            0.24 if modulo == "PROGRAMA INVESTIGACION ACCIDENTES" else
            0.317 if modulo == "PROGRAMA ART AST CHARLA DIARIA" else
            0.804 if modulo == "PROGRAMA PEC" else
            0.432 if modulo == "PROGRAMA EPP" else
            0.432 if modulo == "PROGRAMA CONTRATISTAS" else 0
            for modulo in modulos
        ])
        if porcentaje_total > 1:
            modularizado_excedido = E * porcentaje_total
            porcentaje_total = 1  # Limitar el porcentaje total a 1 si excede
        E *= porcentaje_total

    # Calcular el valor por centro de trabajo
    valor_por_centro = E / centros

    # Calcular el valor si fuera Plan Comercial sin ponderador de mina
    valor_plan_comercial = E_base

    # Calcular el valor si fuera Plan Avanzado
    valor_plan_avanzado = E_base * 1.3

    return jsonify({
        'valor_total': E,
        'valor_por_centro': valor_por_centro,
        'modularizado_excedido': modularizado_excedido,
        'valor_plan_comercial': valor_plan_comercial,
        'valor_plan_avanzado': valor_plan_avanzado
    })

if __name__ == '__main__':
    app.run(debug=True)
