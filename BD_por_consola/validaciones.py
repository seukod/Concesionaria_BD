"""
Módulo de validaciones comunes para la aplicación de concesionaria.
Contiene funciones de validación reutilizables para diferentes tipos de datos.
"""

import re
from datetime import datetime

def validar_patente(patente):
    """
    Valida el formato de una patente chilena.
    
    Args:
        patente (str): Patente a validar
    
    Returns:
        tuple: (es_valida, mensaje_error)
    """
    if not patente:
        return False, "La patente no puede estar vacía"
    
    patente = patente.strip().upper()
    
    if len(patente) != 6:
        return False, "La patente debe tener exactamente 6 caracteres"
    
    # Formato tradicional: 4 letras + 2 números (ej: ABCD12)
    # Formato nuevo: 2 letras + 4 números (ej: AB1234)
    patron_tradicional = re.match(r'^[A-Z]{4}[0-9]{2}$', patente)
    patron_nuevo = re.match(r'^[A-Z]{2}[0-9]{4}$', patente)
    
    if not (patron_tradicional or patron_nuevo):
        return False, "Formato de patente inválido. Debe ser AAAA99 o AA9999"
    
    return True, ""

def validar_rut(rut):
    """
    Valida un RUT chileno (sin puntos ni guión).
    
    Args:
        rut (str o int): RUT a validar
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    try:
        # Convertir a string si es número
        rut_str = str(rut).strip()
        
        # Verificar que solo contenga dígitos
        if not rut_str.isdigit():
            return False, "El RUT debe contener solo números"
        
        # Verificar longitud
        if len(rut_str) < 7 or len(rut_str) > 8:
            return False, "El RUT debe tener entre 7 y 8 dígitos"
        
        return True, ""
        
    except Exception:
        return False, "RUT inválido"

def validar_precio(precio):
    """
    Valida un precio.
    
    Args:
        precio (str o float): Precio a validar
    
    Returns:
        tuple: (es_valido, precio_float, mensaje_error)
    """
    try:
        precio_float = float(precio)
        
        if precio_float <= 0:
            return False, 0, "El precio debe ser mayor a 0"
        
        if precio_float > 999999999:  # Límite razonable
            return False, 0, "El precio es demasiado alto"
        
        return True, precio_float, ""
        
    except ValueError:
        return False, 0, "El precio debe ser un número válido"

def validar_kilometraje(kilometraje):
    """
    Valida el kilometraje de un vehículo.
    
    Args:
        kilometraje (str o int): Kilometraje a validar
    
    Returns:
        tuple: (es_valido, kilometraje_int, mensaje_error)
    """
    try:
        km_int = int(kilometraje)
        
        if km_int < 0:
            return False, 0, "El kilometraje no puede ser negativo"
        
        if km_int > 1000000:  # Límite razonable
            return False, 0, "El kilometraje es demasiado alto"
        
        return True, km_int, ""
        
    except ValueError:
        return False, 0, "El kilometraje debe ser un número entero válido"

def validar_fecha(fecha_str, formato="%Y-%m-%d"):
    """
    Valida una fecha en formato específico.
    
    Args:
        fecha_str (str): Fecha en formato string
        formato (str): Formato esperado de la fecha
    
    Returns:
        tuple: (es_valida, fecha_datetime, mensaje_error)
    """
    try:
        fecha_obj = datetime.strptime(fecha_str.strip(), formato)
        
        # Verificar que la fecha no sea futura (para fechas de llegada)
        if fecha_obj > datetime.now():
            return False, None, "La fecha no puede ser futura"
        
        # Verificar que la fecha no sea demasiado antigua (más de 50 años)
        fecha_minima = datetime.now().replace(year=datetime.now().year - 50)
        if fecha_obj < fecha_minima:
            return False, None, "La fecha es demasiado antigua"
        
        return True, fecha_obj, ""
        
    except ValueError:
        return False, None, f"Formato de fecha inválido. Use {formato}"

def validar_fecha_hora(fecha_hora_str, formato="%Y-%m-%d %H:%M:%S"):
    """
    Valida una fecha y hora en formato específico.
    
    Args:
        fecha_hora_str (str): Fecha y hora en formato string
        formato (str): Formato esperado
    
    Returns:
        tuple: (es_valida, fecha_datetime, mensaje_error)
    """
    return validar_fecha(fecha_hora_str, formato)

def validar_boolean_input(input_str):
    """
    Valida y convierte un input string a boolean.
    
    Args:
        input_str (str): String a convertir
    
    Returns:
        tuple: (es_valido, valor_boolean, mensaje_error)
    """
    input_clean = input_str.strip().lower()
    
    valores_true = ['true', '1', 'si', 's', 'yes', 'y', 'verdadero']
    valores_false = ['false', '0', 'no', 'n', 'falso']
    
    if input_clean in valores_true:
        return True, True, ""
    elif input_clean in valores_false:
        return True, False, ""
    else:
        return False, False, "Valor inválido. Use: true/false, si/no, 1/0"

def validar_id_positivo(id_str, nombre_campo="ID"):
    """
    Valida que un ID sea un número entero positivo.
    
    Args:
        id_str (str): ID a validar
        nombre_campo (str): Nombre del campo para mensajes de error
    
    Returns:
        tuple: (es_valido, id_int, mensaje_error)
    """
    try:
        id_int = int(id_str)
        
        if id_int <= 0:
            return False, 0, f"El {nombre_campo} debe ser mayor a 0"
        
        return True, id_int, ""
        
    except ValueError:
        return False, 0, f"El {nombre_campo} debe ser un número entero válido"

def limpiar_y_validar_texto(texto, longitud_maxima=None, permitir_vacio=False):
    """
    Limpia y valida un texto.
    
    Args:
        texto (str): Texto a validar
        longitud_maxima (int, optional): Longitud máxima permitida
        permitir_vacio (bool): Si se permite texto vacío
    
    Returns:
        tuple: (es_valido, texto_limpio, mensaje_error)
    """
    texto_limpio = texto.strip()
    
    if not permitir_vacio and not texto_limpio:
        return False, "", "El texto no puede estar vacío"
    
    if longitud_maxima and len(texto_limpio) > longitud_maxima:
        return False, "", f"El texto no puede superar {longitud_maxima} caracteres"
    
    return True, texto_limpio, ""

def confirmar_accion(mensaje="¿Está seguro?"):
    """
    Solicita confirmación del usuario para una acción.
    
    Args:
        mensaje (str): Mensaje de confirmación
    
    Returns:
        bool: True si el usuario confirma, False en caso contrario
    """
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta in ['s', 'si', 'y', 'yes']
