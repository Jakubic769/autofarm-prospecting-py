import pyautogui
import pydirectinput as pdi
import keyboard
import threading
import time

# --- USTAWIENIA --- Dla kolegi (każdy musi sobie zmienić dla siebie !!!)
COUNTDOWN_S = 3.0
INIT_LPM_HOLD = 0.8      # początkowe trzymanie LPM
LOOP_LPM_HOLD = 0.8    # w pętli: trzymanie LPM
LOOP_LPM_PAUSE = 1  # w pętli: przerwa po puszczeniu
LOOP_LPM_REPS = 5     # liczba powtórzeń w pętli

DELAY_BEFORE_D = 1.0
HOLD_D = 0.6             # trzymanie D
CLICK_GAP_AFTER_D = 0.5

LONG_LPM_HOLD = 18
DELAY_BEFORE_A = 0.25
HOLD_A = 0.6             # trzymanie A

running = False
pyautogui.PAUSE = 0


def sleep_checked(duration: float, step: float = 0.01):
    """Usypia z możliwością szybkiego przerwania F2."""
    end = time.time() + duration
    while running and time.time() < end:
        time.sleep(min(step, end - time.time()))


def hold_mouse_left(duration: float):
    if not running:
        return
    pyautogui.mouseDown()
    sleep_checked(duration)
    pyautogui.mouseUp()


def hold_key(key: str, duration: float):
    """Trzymanie klawisza przez czas (pydirectinput działa stabilniej w grach)."""
    if not running:
        return
    pdi.keyDown(key)
    sleep_checked(duration)
    pdi.keyUp(key)


def script():
    global running

    # odliczanie
    for i in range(int(COUNTDOWN_S), 0, -1):
        if not running:
            return
        print(f"Start za {i}...")
        time.sleep(1)

    if not running:
        return

    # 1) Początkowe LPM 0.4 s
    hold_mouse_left(INIT_LPM_HOLD)

    while running:
        # 2) 15x LPM 0.43 s + pauza 0.43 s
        for _ in range(LOOP_LPM_REPS):
            if not running:
                break
            hold_mouse_left(LOOP_LPM_HOLD)
            sleep_checked(LOOP_LPM_PAUSE)

        if not running:
            break

        # 3) D trzymane 0.6 s
        sleep_checked(DELAY_BEFORE_D)
        hold_key("d", HOLD_D)

        # 4) klik LPM + pauza 0.5 s
        pyautogui.click()
        sleep_checked(CLICK_GAP_AFTER_D)

        # 5) LPM trzymane 8 s
        hold_mouse_left(LONG_LPM_HOLD)

        # 6) A trzymane 0.6 s po 0.25 s
        sleep_checked(DELAY_BEFORE_A)
        hold_key("a", HOLD_A)


def start_script():
    global running
    if not running:
        running = True
        threading.Thread(target=script, daemon=True).start()
        print("Skrypt uruchomiony (odliczanie 3 sekundy)")


def stop_script():
    global running
    if running:
        running = False
        print("Skrypt zatrzymany")


keyboard.add_hotkey("F1", start_script)
keyboard.add_hotkey("F2", stop_script)

print("Naciśnij F1 aby uruchomić skrypt, F2 aby zatrzymać. ESC aby zakończyć program.")
keyboard.wait("esc")
