import sys, os
sys.path.insert(0, os.path.abspath(".."))
import cv2
from arduino.arduino import Arduino
from ai.finite_state_machine import FiniteStateMachine
from ai.state_find_button import state_find_button
from ai.state_wait_until_start import state_wait_until_start
from ai.state_move_to_button import state_move_to_button
from ai.state_celebrate import state_celebrate
from ai.state_find_door import state_find_door
from ai.state_climb_through_door import state_climb_trough_door
from ai.state_straighten_up import state_straighten_up
from calc.kalman import create_default_kalman
import config
from time import sleep

cap = cv2.VideoCapture(config.capture_device)

mega = Arduino(config.mega_usb)
nano = Arduino(config.nano_usb)
sleep(1)

mega.send("servo", 80)

kalman = create_default_kalman()
kalman2 = create_default_kalman()

fsm = FiniteStateMachine()

fsm.push_state(state_celebrate(mega))
fsm.push_state(state_climb_trough_door(mega, nano))
#fsm.push_state(state_straighten_up(mega, reverse=0))
fsm.push_state(state_find_door(mega))
fsm.push_state(state_move_to_button(kalman2, mega, nano, dist_to_btn=300))
#fsm.push_state(state_find_button(kalman2, mega))
#fsm.push_state(state_straighten_up(mega, reverse=10))
#fsm.push_state(state_move_to_button(kalman, mega, nano, dist_to_btn=400))
fsm.push_state(state_find_button(kalman, mega))
fsm.push_state(state_wait_until_start(mega))

while True:

    keyboard = cv2.waitKey(1) & 0xFF
    ret, frame = cap.read()

    mega.update()
    nano.update()
    fsm.update(frame)

    cv2.imshow('frame', frame)

    if keyboard == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()