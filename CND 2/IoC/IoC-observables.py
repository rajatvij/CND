"""
Description: Build a STIX Indicator document showing observed
behavior of malware calling ipconfig.
"""

from cybox.core import Observable, Observables, ObservableComposition
from cybox.objects.file_object import File
from cybox.objects.process_object import Process
from cybox.utils import IDGenerator, set_id_method
set_id_method(IDGenerator.METHOD_INT)

observables = Observables()

proc = Process.from_dict(
    {"name": "cmd.exe",
    "image_info": {"command_line": "cmd.exe /c ipconfig"}})
proc.name.condition = "Equals"
proc.image_info.command_line.condition = "Contains"
oproc = Observable(proc)
observables.add(oproc)

oproc_ref = Observable()
oproc_ref.id_ = None
oproc_ref.idref = oproc.id_

o_comp = ObservableComposition(operator="OR")
o_comp.add(oproc_ref)
observables.add(Observable(o_comp))

print observables.to_xml(include_namespaces=False)
