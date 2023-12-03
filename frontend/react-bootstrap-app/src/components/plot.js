import React, { useRef, useState} from 'react';
import Plot from 'react-plotly.js';
const Scatter3D  = ({ data }) => {

    const hardcodedData = [
        { x: 1, y: 2, z: 3, c: 1, t: 'Punto 1' },
        { x: 2, y: 3, z: 4, c: 2, t: 'Punto 2' },
        { x: 3, y: 4, z: 5, c: 1, t: 'Punto 3' },
        { x: 4, y: 5, z: 6, c: 2, t: 'Punto 4' },];

    // Extraer las columnas x, y, z, c, t del conjunto de datos
    const xData = hardcodedData.map(entry => entry.x);
    const yData = hardcodedData.map(entry => entry.y);
    const zData = hardcodedData.map(entry => entry.z);
    const cData = hardcodedData.map(entry => entry.c);
    const tData = hardcodedData.map(entry => entry.t);

    // Crear un objeto de rastreo para el gráfico 3D
    const trace = {
        x: xData,
        y: yData,
        z: zData,
        mode: 'markers',
        type: 'scatter3d',
        marker: {
            size: 8,
            color: cData,
            colorscale: 'Viridis',
            opacity: 0.8,
            colorbar: {
                title: 'Cluster ID',
            },
        },
        text: tData.map(String),
    };

    // Configuración del diseño del gráfico
    const layout = {
        margin: { l: 0, r: 0, b: 0, t: 0 },
        scene: {
            xaxis: { title: 'X' },
            yaxis: { title: 'Y' },
            zaxis: { title: 'Z' },
        },
    };

    return <Plot data={[trace]} layout={layout} />;
};

export default Scatter3D ;