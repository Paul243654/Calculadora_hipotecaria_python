# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['inicio.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
a.datas += [
            ("./formulario_hipoteca_acceso.ui", "formulario_hipoteca_acceso.ui", "DATA"),
            ("./formulario_hipoteca_calculo.ui", "formulario_hipoteca_calculo.ui", "DATA"),
            ("./formulario_hipoteca_ingresoDatos.ui", "formulario_hipoteca_ingresoDatos.ui", "DATA"),
            ("./formulario_hipoteca_tablas.ui", "formulario_hipoteca_tablas.ui", "DATA"),
            ("./formulario_hipoteca_datosgraficofijo.ui", "formulario_hipoteca_datosgraficofijo.ui", "DATA"),
            ("./formulario_hipoteca_datosgraficovariable.ui", "formulario_hipoteca_datosgraficovariable.ui", "DATA"),
            ("./Base_datos_IH.db", "Base_datos_IH.db", "DATA"),
            ("./calculo_interes.py", "calculo_interes.py", "DATA"),
            ("./Ficher_datos.py", "Ficher_datos.py", "DATA"),
            ("./tablas_historico.py", "tablas_historico.py", "DATA"),
            ("./df_graph_fijo.py", "df_graph_fijo.py", "DATA"),
            ("./df_graph_variable.py", "df_graph_variable.py", "DATA"), 
            ("./GUIA DE IMPORTACION.pdf", "GUIA DE IMPORTACION.pdf", "DATA"),
            ("./GUIA DE USO.pdf", "GUIA DE USO.pdf", "DATA"),
            ("./calc-hip.ico", "calc-hip.ico", "DATA")
            ]
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='inicio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='calc-hip.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='inicio',
)
