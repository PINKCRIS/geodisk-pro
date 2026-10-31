<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laboratorio del Macizo Rocoso | Geomecánica Avanzada</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    },
                    colors: {
                        field: {
                            50: '#fbfcfc',
                            100: '#f4f6f5',
                            200: '#e3e9e6',
                            300: '#c5d1cb',
                            700: '#3c5248',
                            800: '#2c3d35',
                            900: '#1c2722',
                        },
                        amberField: {
                            500: '#d97706',
                            600: '#b45309',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #f5f7f5;
            color: #1f2937;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col font-sans">

    <!-- BARRA FIJA SUPERIOR (Resultados en Vivo) -->
    <header class="sticky top-0 z-50 bg-field-900 text-stone-100 shadow-lg border-b border-field-700">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center space-x-3">
                <div class="bg-amberField-500 text-white p-2 rounded-lg font-mono font-bold text-lg shadow">
                    GR
                </div>
                <div>
                    <h1 class="text-base sm:text-lg font-bold tracking-tight">Laboratorio del Macizo Rocoso</h1>
                    <p class="text-xs text-stone-400">Cuaderno Geomecánico Digital • Hoek-Brown & Clasificaciones Empíricas</p>
                </div>
            </div>

            <!-- Live Indicators Bar -->
            <div class="flex items-center space-x-3 sm:space-x-6 overflow-x-auto py-1">
                <!-- RQD Live -->
                <div class="bg-field-800 px-3 py-1.5 rounded-lg border border-field-700 flex items-center space-x-2">
                    <span class="text-xs text-stone-400 uppercase font-mono">RQD:</span>
                    <span id="live-rqd" class="font-mono font-bold text-amberField-500 text-sm">--</span>
                    <span id="live-rqd-desc" class="text-xs text-stone-300 hidden sm:inline">(--)</span>
                </div>
                <!-- RMR Live -->
                <div class="bg-field-800 px-3 py-1.5 rounded-lg border border-field-700 flex items-center space-x-2">
                    <span class="text-xs text-stone-400 uppercase font-mono">RMR₈₉:</span>
                    <span id="live-rmr" class="font-mono font-bold text-emerald-400 text-sm">--</span>
                    <span id="live-rmr-class" class="text-xs px-1.5 py-0.5 rounded font-bold bg-stone-700 text-stone-200">Clase --</span>
                </div>
                <!-- Q Barton Live -->
                <div class="bg-field-800 px-3 py-1.5 rounded-lg border border-field-700 flex items-center space-x-2">
                    <span class="text-xs text-stone-400 uppercase font-mono">Q Barton:</span>
                    <span id="live-q" class="font-mono font-bold text-cyan-400 text-sm">--</span>
                </div>
            </div>
        </div>
    </header>

    <!-- NAVEGACIÓN POR PESTAÑAS -->
    <nav class="bg-white border-b border-stone-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 flex space-x-1 sm:space-x-4 overflow-x-auto">
            <button onclick="switchTab('tab-rqd', this)" class="tab-btn px-4 py-3 text-sm font-semibold border-b-2 border-emerald-600 text-emerald-700 flex items-center space-x-2 whitespace-nowrap">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                <span>1. RQD (Designación)</span>
            </button>
            <button onclick="switchTab('tab-rmr', this)" class="tab-btn px-4 py-3 text-sm font-medium border-b-2 border-transparent text-stone-600 hover:text-stone-900 flex items-center space-x-2 whitespace-nowrap">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
                <span>2. RMR (Bieniawski)</span>
            </button>
            <button onclick="switchTab('tab-q', this)" class="tab-btn px-4 py-3 text-sm font-medium border-b-2 border-transparent text-stone-600 hover:text-stone-900 flex items-center space-x-2 whitespace-nowrap">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                <span>3. Q de Barton</span>
            </button>
            <button onclick="switchTab('tab-hb', this)" class="tab-btn px-4 py-3 text-sm font-medium border-b-2 border-transparent text-stone-600 hover:text-stone-900 flex items-center space-x-2 whitespace-nowrap">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                <span>4. Criterio Hoek-Brown</span>
            </button>
        </div>
    </nav>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 py-6">

        <!-- ================= MÓDULO 1: RQD ================= -->
        <div id="tab-rqd" class="tab-content active space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-stone-200 p-6">
                <h2 class="text-xl font-bold text-stone-800 mb-2">Cálculo de RQD (Rock Quality Designation)</h2>
                <p class="text-sm text-stone-600 mb-6">El RQD representa el porcentaje de recuperación de testigos de perforación mayores a 10 cm (4 pulgadas) sin fracturas mecánicas respecto a la longitud total del tramo.</p>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="space-y-4">
                        <div class="bg-field-50 p-4 rounded-lg border border-stone-200 space-y-3">
                            <label class="block text-sm font-semibold text-stone-700">Longitud total del sondeo / tramo ($L$) [cm]:</label>
                            <input type="number" id="rqd-total-len" value="100" min="1" class="w-full px-3 py-2 border rounded-lg font-mono text-sm focus:ring-2 focus:ring-emerald-500 outline-none" oninput="calculateRQD()">
                        </div>

                        <div class="bg-field-50 p-4 rounded-lg border border-stone-200 space-y-3">
                            <label class="block text-sm font-semibold text-stone-700">Suma de trozos $\ge 10\text{ cm}$ sin fracturas mecánicas [cm]:</label>
                            <input type="number" id="rqd-sum-len" value="78" min="0" class="w-full px-3 py-2 border rounded-lg font-mono text-sm focus:ring-2 focus:ring-emerald-500 outline-none" oninput="calculateRQD()">
                        </div>

                        <div class="text-xs text-stone-500 bg-amber-50 p-3 rounded border border-amber-200">
                            <strong>Fórmula de Deere (1967):</strong><br>
                            $$\text{RQD} = \frac{\sum (\text{Longitud de trozos } > 10\text{ cm})}{\text{Longitud total del tramo}} \times 100$$
                        </div>
                    </div>

                    <!-- Resultados RQD -->
                    <div class="bg-field-900 text-white p-6 rounded-xl flex flex-col justify-between shadow-inner">
                        <div>
                            <span class="text-xs uppercase tracking-widest text-stone-400 font-mono">Resultado RQD</span>
                            <div class="text-4xl sm:text-5xl font-extrabold font-mono text-amberField-500 mt-2" id="rqd-val">78.0%</div>
                            <div class="text-lg font-semibold text-stone-200 mt-1" id="rqd-quality">Calidad: Buena</div>
                        </div>
                        <div class="mt-6 pt-4 border-t border-field-700 text-xs text-stone-400 space-y-1">
                            <p>• <90%: Muy Pobre</p>
                            <p>• 50% - 75%: Regular</p>
                            <p>• 75% - 90%: Buena</p>
                            <p>• >90%: Excelente</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= MÓDULO 2: RMR (Bieniawski 1989) ================= -->
        <div id="tab-rmr" class="tab-content space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-stone-200 p-6">
                <h2 class="text-xl font-bold text-stone-800 mb-2">Clasificación Geomecánica RMR (Bieniawski, 1989)</h2>
                <p class="text-sm text-stone-600 mb-6">Seleccione los parámetros geológicos y geotécnicos correspondientes al macizo rocoso para obtener la puntuación total y su clasificación.</p>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <!-- Entradas RMR -->
                    <div class="lg:col-span-2 space-y-5">
                        <!-- 1. UCS -->
                        <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                            <label class="block text-sm font-bold text-stone-800 mb-1">1. Resistencia Compresiva Uniaxial (UCS) / Ensayo Carga Puntual</label>
                            <select id="rmr-ucs" class="w-full px-3 py-2 border rounded-lg text-sm bg-white font-mono" onchange="calculateRMR()">
                                <option value="15">> 250 MPa (> 10 MPa Carga Puntual) [Puntos: 15]</option>
                                <option value="12" selected>100 - 250 MPa (4 - 10 MPa) [Puntos: 12]</option>
                                <option value="7">50 - 100 MPa (2 - 4 MPa) [Puntos: 7]</option>
                                <option value="4">25 - 50 MPa (1 - 2 MPa) [Puntos: 4]</option>
                                <option value="2">5 - 25 MPa (Prueba de martillo) [Puntos: 2]</option>
                                <option value="1">1 - 5 MPa [Puntos: 1]</option>
                                <option value="0">< 1 MPa [Puntos: 0]</option>
                            </select>
                        </div>

                        <!-- 2. RQD -->
                        <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                            <label class="block text-sm font-bold text-stone-800 mb-1">2. Designación de Calidad de Roca (RQD)</label>
                            <select id="rmr-rqd" class="w-full px-3 py-2 border rounded-lg text-sm bg-white font-mono" onchange="calculateRMR()">
                                <option value="20">90% - 100% (Excelente) [Puntos: 20]</option>
                                <option value="17" selected>75% - 90% (Buena) [Puntos: 17]</option>
                                <option value="13">50% - 75% (Regular) [Puntos: 13]</option>
                                <option value="8">25% - 50% (Mala) [Puntos: 8]</option>
                                <option value="3">< 25% (Muy Mala) [Puntos: 3]</option>
                            </select>
                        </div>

                        <!-- 3. Espaciamiento de Discontinuidades -->
                        <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                            <label class="block text-sm font-bold text-stone-800 mb-1">3. Espaciamiento de las Discontinuidades</label>
                            <select id="rmr-spacing" class="w-full px-3 py-2 border rounded-lg text-sm bg-white font-mono" onchange="calculateRMR()">
                                <option value="30">> 2. m [Puntos: 30]</option>
                                <option value="25" selected>0.6 - 2.0 m [Puntos: 25]</option>
                                <option value="20">200 - 600 mm [Puntos: 20]</option>
                                <option value="10">60 - 200 mm [Puntos: 10]</option>
                                <option value="5">< 60 mm [Puntos: 5]</option>
                            </select>
                        </div>

                        <!-- 4. Condición de Discontinuidades -->
                        <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                            <label class="block text-sm font-bold text-stone-800 mb-1">4. Condición de las Discontinuidades (Persistencia, abertura, rugosidad, relleno, alteración)</label>
                            <select id="rmr-cond" class="w-full px-3 py-2 border rounded-lg text-sm bg-white font-mono" onchange="calculateRMR()">
                                <option value="30">Muy rugosas, sin continuidad, no separadas, paredes rocosas sin alteración [Puntos: 30]</option>
                                <option value="25" selected>Ligeramente rugosas, separación < 1 mm, paredes rocosas ligeramente alteradas [Puntos: 25]</option>
                                <option value="20">Ligeramente rugosas, separación 1-5 mm, relleno arcilloso < 5 mm [Puntos: 20]</option>
                                <option value="10">Espejos de falla o relleno arcilloso > 5 mm o separación 1-5 mm continuo [Puntos: 10]</option>
                                <option value="0">Relleno blando espeso continuo o muy abierto [Puntos: 0]</option>
                            </select>
                        </div>

                        <!-- 5. Agua Subterránea -->
                        <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                            <label class="block text-sm font-bold text-stone-800 mb-1">5. Aguas Subterráneas</label>
                            <select id="rmr-water" class="w-full px-3 py-2 border rounded-lg text-sm bg-white font-mono" onchange="calculateRMR()">
                                <option value="15" selected>Completamente seco [Puntos: 15]</option>
                                <option value="10">Húmedo [Puntos: 10]</option>
                                <option value="7">Goteo continuo [Puntos: 7]</option>
                                <option value="4">Flujo moderado [Puntos: 4]</option>
                                <option value="0">Flujo abundante / presión alta [Puntos: 0]</option>
                            </select>
                        </div>

                        <!-- 6. Ajuste por Orientación -->
                        <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                            <label class="block text-sm font-bold text-stone-800 mb-1">6. Ajuste por Orientación de Discontinuidades (Túneles/Cimentaciones/Taludes)</label>
                            <select id="rmr-adj" class="w-full px-3 py-2 border rounded-lg text-sm bg-white font-mono" onchange="calculateRMR()">
                                <option value="0">Muy favorable [Puntos: 0]</option>
                                <option value="-2" selected>Favorable [Puntos: -2]</option>
                                <option value="-5">Regular [Puntos: -5]</option>
                                <option value="-10">Desfavorable [Puntos: -10]</option>
                                <option value="-12">Muy desfavorable [Puntos: -12]</option>
                            </select>
                        </div>
                    </div>

                    <!-- Panel Lateral RMR Resultados -->
                    <div class="space-y-6">
                        <div class="bg-field-900 text-white p-6 rounded-xl shadow-inner sticky top-24">
                            <span class="text-xs uppercase tracking-widest text-stone-400 font-mono">Puntuación RMR₈₉</span>
                            <div class="text-5xl font-extrabold font-mono text-emerald-400 mt-2" id="rmr-total">72</div>
                            <div class="mt-3">
                                <div id="rmr-class-badge" class="inline-block px-3 py-1 rounded font-bold text-sm bg-emerald-700 text-white">Clase II: Buena Roca</div>
                            </div>

                            <div class="mt-6 pt-4 border-t border-field-700 space-y-3 text-xs text-stone-300">
                                <div class="flex justify-between"><span>Tiempo de Exposición (Vano 10m):</span> <strong id="rmr-time" class="text-white font-mono">6 meses por 1m vano</strong></div>
                                <div class="flex justify-between"><span>Cohesión estimada ($c$):</span> <strong id="rmr-coh" class="text-white font-mono">> 300 kPa</strong></div>
                                <div class="flex justify-between"><span>Ángulo de Fricción ($\phi$):</span> <strong id="rmr-phi" class="text-white font-mono">> 45°</strong></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= MÓDULO 3: Q DE BARTON ================= -->
        <div id="tab-q" class="tab-content space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-stone-200 p-6">
                <h2 class="text-xl font-bold text-stone-800 mb-2">Sistema Q de Barton (NGI, 1974)</h2>
                <p class="text-sm text-stone-600 mb-6">El índice Q evalúa la calidad del macizo rocoso para el diseño de sostenimiento en subterráneos mediante cocientes de parámetros de fracturación, rugosidad, alteración y condiciones de agua.</p>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <!-- Entradas Q -->
                    <div class="lg:col-span-2 space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">RQD</label>
                                <input type="number" id="q-rqd" value="75" min="1" max="100" class="w-full px-3 py-2 border rounded font-mono text-sm" oninput="calculateQ()">
                            </div>
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">Jn (Índice de familias de juntas)</label>
                                <select id="q-jn" class="w-full px-3 py-2 border rounded font-mono text-sm bg-white" onchange="calculateQ()">
                                    <option value="0.5">Masiva, sin o pocas juntas [0.5]</option>
                                    <option value="1">1 familia de juntas [1.0]</option>
                                    <option value="2">1 familia + juntas ocasionales [2.0]</option>
                                    <option value="2" selected>2 familias de juntas [4.0 -> select option]</option>
                                    <option value="6">3 familias de juntas [9.0]</option>
                                    <option value="12">4 o más familias, agrietada [12.0]</option>
                                    <option value="15">Roca triturada / brechada [15.0]</option>
                                </select>
                            </div>
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">Jr (Rugosidad de las juntas)</label>
                                <select id="q-jr" class="w-full px-3 py-2 border rounded font-mono text-sm bg-white" onchange="calculateQ()">
                                    <option value="3">Discontinuas [3.0]</option>
                                    <option value="1.5" selected>Rugosas u onduladas, escalonadas [1.5]</option>
                                    <option value="1">Lisas u onduladas [1.0]</option>
                                    <option value="0.5">Lisas, planas [0.5]</option>
                                </select>
                            </div>
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">Ja (Alteración de las juntas)</label>
                                <select id="q-ja" class="w-full px-3 py-2 border rounded font-mono text-sm bg-white" onchange="calculateQ()">
                                    <option value="0.75">Sanotas, sin relleno [0.75]</option>
                                    <option value="1" selected>Ligeramente alteradas, sin relleno arcilloso [1.0]</option>
                                    <option value="2">Relleno mineral arcilloso duro [2.0]</option>
                                    <option value="4">Relleno blando arcilloso [4.0]</option>
                                </select>
                            </div>
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">Jw (Reducción por agua)</label>
                                <select id="q-jw" class="w-full px-3 py-2 border rounded font-mono text-sm bg-white" onchange="calculateQ()">
                                    <option value="1" selected>Excavación seca o goteo menor [1.0]</option>
                                    <option value="0.66">Flujo medio o presión moderada [0.66]</option>
                                    <option value="0.33">Flujo abundante [0.33]</option>
                                </select>
                            </div>
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">SRF (Factor de reducción por esfuerzos)</label>
                                <select id="q-srf" class="w-full px-3 py-2 border rounded font-mono text-sm bg-white" onchange="calculateQ()">
                                    <option value="1" selected>Condiciones de esfuerzo favorables [1.0]</option>
                                    <option value="2.5">Esfuerzo medio en roca competente [2.5]</option>
                                    <option value="5">Roca blanda / fluencia [5.0]</option>
                                    <option value="10">Zona de falla a profundidad media [10.0]</option>
                                </select>
                            </div>
                        </div>

                        <div class="bg-amber-50 p-4 rounded-lg border border-amber-200 text-xs text-stone-700 space-y-1">
                            <strong>Ecuación de Barton:</strong>
                            $$Q = \left(\frac{\text{RQD}}{J_n}\right) \times \left(\frac{J_r}{J_a}\right) \times \left(\frac{J_w}{\text{SRF}}\right)$$
                        </div>
                    </div>

                    <!-- Panel Q Resultados -->
                    <div class="space-y-6">
                        <div class="bg-field-900 text-white p-6 rounded-xl shadow-inner sticky top-24">
                            <span class="text-xs uppercase tracking-widest text-stone-400 font-mono">Índice Q de Barton</span>
                            <div class="text-4xl sm:text-5xl font-extrabold font-mono text-cyan-400 mt-2" id="q-val">--</div>
                            <div class="mt-3" id="q-quality-badge">
                                <span class="px-3 py-1 rounded font-bold text-sm bg-cyan-700 text-white">Calidad: --</span>
                            </div>
                            <div class="mt-6 pt-4 border-t border-field-700 space-y-2 text-xs text-stone-300">
                                <p>• Longitud de excavación sin soporte ($De$): <span id="q-de" class="font-mono text-white font-bold">--</span> m</p>
                                <p>• Sostenimiento recomendado: <span id="q-support" class="font-mono text-white">Calculando...</span></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= MÓDULO 4: HOEK-BROWN ================= -->
        <div id="tab-hb" class="tab-content space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-stone-200 p-6">
                <h2 class="text-xl font-bold text-stone-800 mb-2">Criterio de Hoek-Brown (Generalized 2002)</h2>
                <p class="text-sm text-stone-600 mb-6">Determina la resistencia del macizo rocoso tridimensionalmente mediante los parámetros GSI, resistencia intacta ($\sigma_{ci}$) y constante petrográfica ($m_i$).</p>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <!-- Entradas Hoek-Brown -->
                    <div class="lg:col-span-2 space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">UCS Roca Intacta ($\sigma_{ci}$) [MPa]</label>
                                <input type="number" id="hb-sigci" value="100" min="1" class="w-full px-3 py-2 border rounded font-mono text-sm" oninput="calculateHB()">
                            </div>
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">GSI (Geological Strength Index)</label>
                                <input type="number" id="hb-gsi" value="65" min="10" max="100" class="w-full px-3 py-2 border rounded font-mono text-sm" oninput="calculateHB()">
                            </div>
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">Constante $m_i$ (Mineralogía)</label>
                                <input type="number" id="hb-mi" value="10" min="4" max="35" class="w-full px-3 py-2 border rounded font-mono text-sm" oninput="calculateHB()">
                            </div>
                            <div class="bg-stone-50 p-4 rounded-xl border border-stone-200">
                                <label class="block text-sm font-bold text-stone-800 mb-1">Factor de Disturbio ($D$)</label>
                                <select id="hb-d" class="w-full px-3 py-2 border rounded font-mono text-sm bg-white" onchange="calculateHB()">
                                    <option value="0">0.0 (Excavación cuidadosa con voladura / TBM)</option>
                                    <option value="0.7">0.7 (Voladura mediocre / estándar)</option>
                                    <option value="1.0">1.0 (Voladura de alta producción / daño severo)</option>
                                </select>
                            </div>
                        </div>

                        <div class="bg-emerald-50 p-4 rounded-lg border border-emerald-200 text-xs text-stone-700 space-y-1 font-mono">
                            <strong>Ecuación Generalizada:</strong><br>
                            $$\sigma_1' = \sigma_3' + \sigma_{ci} \left( m_b \frac{\sigma_3'}{\sigma_{ci}} + s \right)^a$$
                        </div>
                    </div>

                    <!-- Panel Hoek-Brown Resultados -->
                    <div class="space-y-6">
                        <div class="bg-field-900 text-white p-6 rounded-xl shadow-inner sticky top-24 space-y-4">
                            <span class="text-xs uppercase tracking-widest text-stone-400 font-mono">Parámetros Derivados H-B</span>
                            <div class="grid grid-cols-2 gap-4">
                                <div class="bg-field-800 p-3 rounded border border-field-700">
                                    <span class="text-xs text-stone-400 block font-mono">mb:</span>
                                    <span id="hb-res-mb" class="text-lg font-bold font-mono text-emerald-400">--</span>
                                </div>
                                <div class="bg-field-800 p-3 rounded border border-field-700">
                                    <span class="text-xs text-stone-400 block font-mono">s:</span>
                                    <span id="hb-res-s" class="text-lg font-bold font-mono text-emerald-400">--</span>
                                </div>
                                <div class="bg-field-800 p-3 rounded border border-field-700">
                                    <span class="text-xs text-stone-400 block font-mono">a:</span>
                                    <span id="hb-res-a" class="text-lg font-bold font-mono text-emerald-400">--</span>
                                </div>
                                <div class="bg-field-800 p-3 rounded border border-field-700">
                                    <span class="text-xs text-stone-400 block font-mono">Resistencia Macizo ($\sigma_{cm}$):</span>
                                    <span id="hb-res-sigcm" class="text-base font-bold font-mono text-amberField-500">--</span>
                                </div>
                            </div>
                            <div class="pt-2 border-t border-field-700 text-xs text-stone-300 space-y-1">
                                <p>• Módulo de deformación $Em$: <span id="hb-res-em" class="font-mono text-white">--</span> GPa</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- PIE DE PÁGINA -->
    <footer class="bg-white border-t border-stone-200 mt-12 py-6 text-center text-xs text-stone-500">
        <p>Laboratorio del Macizo Rocoso • Herramienta Interactiva Geomecánica basada en Bieniawski, Barton y Hoek & Brown.</p>
    </footer>

    <!-- JAVASCRIPT DE CÁLCULO EN VIVO -->
    <script>
        // Cambio de Pestañas
        function switchTab(tabId, btnElement) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');

            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('border-emerald-600', 'text-emerald-700', 'font-semibold');
                btn.classList.add('border-transparent', 'text-stone-600', 'font-medium');
            });
            btnElement.classList.add('border-emerald-600', 'text-emerald-700', 'font-semibold');
            btnElement.classList.remove('border-transparent', 'text-stone-600', 'font-medium');
        }

        // 1. Cálculo RQD
        function calculateRQD() {
            const total = parseFloat(document.getElementById('rqd-total-len').value) || 100;
            const sum = parseFloat(document.getElementById('rqd-sum-len').value) || 0;
            let rqd = (sum / total) * 100;
            if (rqd > 100) rqd = 100;
            if (rqd < 0) rqd = 0;

            let desc = "Muy Pobre";
            if (rqd >= 90) desc = "Excelente";
            else if (rqd >= 75) desc = "Buena";
            else if (rqd >= 50) desc = "Regular";
            else if (rqd >= 25) desc = "Mala";

            document.getElementById('rqd-val').innerText = rqd.toFixed(1) + "%";
            document.getElementById('rqd-quality').innerText = "Calidad: " + desc;

            // Actualizar barra viva
            document.getElementById('live-rqd').innerText = rqd.toFixed(1) + "%";
            document.getElementById('live-rqd-desc').innerText = "(" + desc + ")";

            return rqd;
        }

        // 2. Cálculo RMR
        function calculateRMR() {
            const ucs = parseFloat(document.getElementById('rmr-ucs').value);
            const rqd = parseFloat(document.getElementById('rmr-rqd').value);
            const spacing = parseFloat(document.getElementById('rmr-spacing').value);
            const cond = parseFloat(document.getElementById('rmr-cond').value);
            const water = parseFloat(document.getElementById('rmr-water').value);
            const adj = parseFloat(document.getElementById('rmr-adj').value);

            let total = ucs + rqd + spacing + cond + water + adj;

            let className = "Clase V: Muy Mala";
            let classBg = "bg-red-700";
            let time = "10 min por 5m vano";
            let coh = "< 100 kPa";
            let phi = "< 20°";

            if (total > 80) {
                className = "Clase I: Muy Buena"; classBg = "bg-emerald-800"; time = "20 años por 15m vano"; coh = "> 400 kPa"; phi = "> 45°";
            } else if (total >= 61) {
                className = "Clase II: Buena"; classBg = "bg-emerald-600"; time = "1 año por 10m vano"; coh = "300 - 400 kPa"; phi = "35° - 45°";
            } else if (total >= 41) {
                className = "Clase III: Regular"; classBg = "bg-amber-600"; time = "1 semana por 5m vano"; coh = "200 - 300 kPa"; phi = "25° - 35°";
            } else if (total >= 21) {
                className = "Clase IV: Mala"; classBg = "bg-orange-700"; time = "10 horas por 2.5m vano"; coh = "100 - 200 kPa"; phi = "20° - 25°";
            }

            document.getElementById('rmr-total').innerText = total;
            const badge = document.getElementById('rmr-class-badge');
            badge.className = "inline-block px-3 py-1 rounded font-bold text-sm text-white " + classBg;
            badge.innerText = className;

            document.getElementById('rmr-time').innerText = time;
            document.getElementById('rmr-coh').innerText = coh;
            document.getElementById('rmr-phi').innerText = phi;

            // Barra viva RMR
            document.getElementById('live-rmr').innerText = total;
            const liveClass = document.getElementById('live-rmr-class');
            liveClass.className = "text-xs px-1.5 py-0.5 rounded font-bold text-white " + classBg;
            liveClass.innerText = className.split(':')[0];

            return total;
        }

        // 3. Cálculo Q de Barton
        function calculateQ() {
            const rqd = parseFloat(document.getElementById('q-rqd').value) || 75;
            const jn = parseFloat(document.getElementById('q-jn').value) || 2;
            const jr = parseFloat(document.getElementById('q-jr').value) || 1.5;
            const ja = parseFloat(document.getElementById('q-ja').value) || 1;
            const jw = parseFloat(document.getElementById('q-jw').value) || 1;
            const srf = parseFloat(document.getElementById('q-srf').value) || 1;

            let q = (rqd / jn) * (jr / ja) * (jw / srf);

            let desc = "Pobre";
            if (q > 40) desc = "Muy Buena";
            else if (q > 10) desc = "Buena";
            else if (q > 4) desc = "Regular";
            else if (q > 1) desc = "Mala";

            document.getElementById('q-val').innerText = q.toFixed(2);
            document.getElementById('live-q').innerText = q.toFixed(2);

            // ESR (Equivalente span ratio por defecto 1.6 para túneles piloto)
            let esr = 1.6;
            let de = 5 / esr; // Asumiendo vano de 5m
            document.getElementById('q-de').innerText = de.toFixed(1);

            let support = "Pernos sistemáticos con hormigón proyectado (5-9 cm)";
            if (q > 40) support = "Sin sostenimiento o pernos ocasionales";
            else if (q < 1) support = "Sostenimiento pesado: Cimbras metálicas, concreto reforzado denso";

            document.getElementById('q-support').innerText = support;
        }
