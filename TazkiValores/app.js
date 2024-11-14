const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

app.post('/api/quotation', (req, res) => {
    const { rubro, colaboradores, centros, solucion, modulos = [] } = req.body;

    // Cálculo del valor base por empresa
    let E_base = 2.39 * Math.pow(colaboradores, 0.376);
    let E = E_base;

    // Aplicar ponderador si el rubro es EXPLOTACION DE MINAS Y CANTERAS
    if (rubro === "C - EXPLOTACION DE MINAS Y CANTERAS") {
        E *= 1.254;
    }

    // Aplicar modificador según la solución seleccionada
    let modularizado_excedido = null;
    if (solucion === "PLAN AVANZADO") {
        E *= 1.3;
    } else if (solucion === "MODULARIZADO") {
        // Sumar los porcentajes de los módulos seleccionados
        let porcentaje_total = modulos.reduce((sum, modulo) => {
            return sum + (
                modulo === "PROGRAMA PERSONALIZADO" ? 0.804 :
                modulo === "PROGRAMA INDUCCIONES" ? 0.432 :
                modulo === "PROGRAMA CHARLAS CAPACITACIONES" ? 0.317 :
                modulo === "PROGRAMA GESTION HALLAZGOS" ? 0.432 :
                modulo === "PROGRAMA INSPECCIONES" ? 0.65 :
                modulo === "PROGRAMA INSUMO MAQUINARIA" ? 0.65 :
                modulo === "PROGRAMA INVESTIGACION ACCIDENTES" ? 0.24 :
                modulo === "PROGRAMA ART AST CHARLA DIARIA" ? 0.317 :
                modulo === "PROGRAMA PEC" ? 0.804 :
                modulo === "PROGRAMA EPP" ? 0.432 :
                modulo === "PROGRAMA CONTRATISTAS" ? 0.432 : 0
            );
        }, 0);

        if (porcentaje_total > 1) {
            modularizado_excedido = E * porcentaje_total;
            porcentaje_total = 1;
        }
        E *= porcentaje_total;
    }

    // Calcular el valor por centro de trabajo
    const valor_por_centro = E / centros;

    // Calcular el valor si fuera Plan Comercial sin ponderador de mina
    const valor_plan_comercial = E_base;

    // Calcular el valor si fuera Plan Avanzado
    const valor_plan_avanzado = E_base * 1.3;

    res.json({
        valor_total: E,
        valor_por_centro,
        modularizado_excedido,
        valor_plan_comercial,
        valor_plan_avanzado
    });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
