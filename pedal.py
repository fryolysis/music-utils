import mido, mouse, time

def sus_pedal():
   PORT_NAME = 'Midi Through Port-0'
   MSG_PEDAL_ON = mido.Message('control_change', control=64, value=127)
   MSG_PEDAL_OFF = mido.Message('control_change', control=64, value=0)

   def pressed():
      port.send(MSG_PEDAL_ON)
   def released():
      port.send(MSG_PEDAL_OFF)

   port = mido.open_output(PORT_NAME)
   mouse.on_button(pressed, buttons=mouse.LEFT, types=mouse.DOWN)
   mouse.on_button(released, buttons=mouse.LEFT, types=mouse.UP)
   while True:
      time.sleep(1000)
