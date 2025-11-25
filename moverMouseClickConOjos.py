import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time # <-- 1. IMPORTAMOS TIME

# --- Configuración de Sensibilidad ---
SENSITIVITY_RADIUS_X = 0.04
SENSITIVITY_RADIUS_Y = 0.04
# ----------------------------------------

# --- 2. NUEVA CONFIGURACIÓN DE CLICK ---
# "Cerrado" = menos del 50% de la distancia normal (abierto)
EAR_CLOSED_MULTIPLIER = 0.5 
BLINK_DURATION = 0.5      # 0.5 segundos
CLICK_COOLDOWN = 1.0      # 1 segundo de espera entre clicks
# ----------------------------------------

pyautogui.FAILSAFE = False

# Inicialización
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

# Variables de estado
alpha = 0.4
is_calibrated = False
center_nose_x, center_nose_y = 0.5, 0.5 
prev_x, prev_y = screen_w // 2, screen_h // 2

# --- 3. NUEVAS VARIABLES DE ESTADO ---
last_click_time = 0
both_eyes_closed_start_time = None
# Guardarán las distancias "normales" (en reposo)
calibrated_left_ear_open = 0.03    # Default
calibrated_right_ear_open = 0.03   # Default
# -----------------------------------

# --- CAMBIO EN INSTRUCCIÓN ---
print("Coloca tu cara en reposo (ojos abiertos).")
print("Presiona '<' para calibrar.")
print("Presiona '|' o 'Esc' para salir.")
print("Cierra AMBOS ojos (0.5s) para clickear.")
# ---------------------------


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # No usamos espejo (como pediste)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    h, w, _ = frame.shape

    current_nose_x_ratio = None
    current_nose_y_ratio = None
    current_left_ear_dist = 0
    current_right_ear_dist = 0

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        
        nose_tip = landmarks[1]
        current_nose_x_ratio = nose_tip.x
        current_nose_y_ratio = nose_tip.y
        
        # --- 4. LÓGICA DE CLICK (CÁLCULO) ---
        # Puntos OJO IZQUIERDO (Párpado)
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]
        current_left_ear_dist = abs(left_eye_top.y - left_eye_bottom.y)
        
        # Puntos OJO DERECHO (Párpado)
        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]
        current_right_ear_dist = abs(right_eye_top.y - right_eye_bottom.y)
        # ----------------------------------

        # Si estamos calibrados, mover el mouse
        if is_calibrated:
            
            # --- LÓGICA DE MOVIMIENTO (Sin cambios) ---
            BOX_X_MIN_RATIO = center_nose_x - SENSITIVITY_RADIUS_X
            BOX_X_MAX_RATIO = center_nose_x + SENSITIVITY_RADIUS_X
            BOX_Y_MIN_RATIO = center_nose_y - SENSITIVITY_RADIUS_Y
            BOX_Y_MAX_RATIO = center_nose_y + SENSITIVITY_RADIUS_Y
            
            BOX_WIDTH = (SENSITIVITY_RADIUS_X * 2)
            BOX_HEIGHT = (SENSITIVITY_RADIUS_Y * 2)

            relative_x = (current_nose_x_ratio - BOX_X_MIN_RATIO) / BOX_WIDTH
            relative_y = (current_nose_y_ratio - BOX_Y_MIN_RATIO) / BOX_HEIGHT
            
            screen_x_ratio = np.clip(1.0 - relative_x, 0.0, 1.0)
            screen_y_ratio = np.clip(relative_y, 0.0, 1.0)

            mouse_x = screen_x_ratio * screen_w
            mouse_y = screen_y_ratio * screen_h
            
            smooth_x = prev_x * (1 - alpha) + mouse_x * alpha
            smooth_y = prev_y * (1 - alpha) + mouse_y * alpha
            
            pyautogui.moveTo(smooth_x, smooth_y)
            prev_x, prev_y = smooth_x, smooth_y
            # --- FIN LÓGICA DE MOVIMIENTO ---

            
            # --- 5. NUEVA LÓGICA DE CLICK (GATILLO) ---
            
            # Comparamos la distancia actual con la CALIBRADA
            is_left_closed = current_left_ear_dist < (calibrated_left_ear_open * EAR_CLOSED_MULTIPLIER)
            is_right_closed = current_right_ear_dist < (calibrated_right_ear_open * EAR_CLOSED_MULTIPLIER)
            is_both_eyes_closed = is_left_closed and is_right_closed

            current_time = time.time()
            can_click_again = (current_time - last_click_time) > CLICK_COOLDOWN

            if is_both_eyes_closed:
                if both_eyes_closed_start_time is None:
                    both_eyes_closed_start_time = current_time
                else:
                    duration = current_time - both_eyes_closed_start_time
                    if duration > BLINK_DURATION and can_click_again:
                        pyautogui.click()
                        print("¡CLICK (Ambos ojos)!")
                        last_click_time = current_time 
                        both_eyes_closed_start_time = None 
            else:
                # Si se abre CUALQUIER ojo, se resetea
                both_eyes_closed_start_time = None
            
            # Feedback visual
            if both_eyes_closed_start_time is not None:
                cv2.circle(frame, (int(left_eye_top.x * w), int(left_eye_top.y * h)), 3, (0, 255, 0), -1)
                cv2.circle(frame, (int(right_eye_top.x * w), int(right_eye_top.y * h)), 3, (0, 255, 0), -1)
            # --- FIN LÓGICA DE CLICK ---


            # Dibujar la caja dinámica
            box_x_min_px = int(BOX_X_MIN_RATIO * w)
            box_x_max_px = int(BOX_X_MAX_RATIO * w)
            box_y_min_px = int(BOX_Y_MIN_RATIO * h)
            box_y_max_px = int(BOX_Y_MAX_RATIO * h)
            cv2.rectangle(frame, (box_x_min_px, box_y_min_px), (box_x_max_px, box_y_max_px), (0, 255, 0), 2)
        
        # Dibujar punto de la nariz
        cx, cy = int(current_nose_x_ratio * w), int(current_nose_y_ratio * h)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # --- Instrucciones en pantalla ---
    if not is_calibrated:
        cv2.putText(frame, "Presiona '<' para centrar", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    cv2.putText(frame, "Presiona '|' o ESC para salir", (20, 90), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Head Tracking Mouse", frame)
    
    # --- Manejo de Teclas ---
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('|'):
        break
    elif key == ord('<'): # <-- 6. LÓGICA DE CALIBRACIÓN ACTUALIZADA
        if current_nose_x_ratio is not None:
            # ¡Calibrar!
            center_nose_x = current_nose_x_ratio
            center_nose_y = current_nose_y_ratio
            is_calibrated = True
            
            prev_x, prev_y = screen_w // 2, screen_h // 2
            
            # --- Guardamos las distancias de los ojos EN REPOSO ---
            calibrated_left_ear_open = current_left_ear_dist
            calibrated_right_ear_open = current_right_ear_dist
            
            print(f"¡Calibrado! Centro fijado en: ({center_nose_x:.2f}, {center_nose_y:.2f})")
            print(f"Distancia Ojo Izq (Abierto): {calibrated_left_ear_open:.4f}")
            print(f"Distancia Ojo Der (Abierto): {calibrated_right_ear_open:.4f}")
            # --------------------------------------------
        else:
            print("No se detecta rostro para calibrar.")

cap.release()
cv2.destroyAllWindows()