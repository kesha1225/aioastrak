from astrak.types import Event, NewMessage


a = Event(type="dss", event={})

a.event = {1: "dsd"}

print(a)