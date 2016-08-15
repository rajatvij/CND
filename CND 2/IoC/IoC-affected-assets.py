"""
Description: Build a STIX Indicator document regarding affected assets.
"""

from stix.core import STIXPackage
from stix.incident import (Incident, RelatedObservables, AffectedAsset, PropertyAffected)
from stix.common.related import (RelatedObservable)
from cybox.core import Observable
from cybox.common import Hash
from cybox.objects.file_object import File

def main():
    pkg = STIXPackage()
    affected_asset = AffectedAsset()
    affected_asset.description = "Hosts Mounted Devices and Drives"
    affected_asset.type_ = "Peripheral Devices"
    affected_asset.type_.count_affected = 1
    affected_asset.business_function_or_role = "Input and Output to the system"
    affected_asset.ownership_class = "Internally-Owned"
    affected_asset.management_class = "Internally-Managed"
    affected_asset.location_class = "Internally-Located"

    property_affected = PropertyAffected()
    property_affected.property_ = "Confidentiality"
    property_affected.description_of_effect = "Information regarding connected peripheral/mounted devices was exfiltrated"
    property_affected.non_public_data_compromised = "Yes"
    property_affected.non_public_data_compromised.data_encrypted = False

    affected_asset.nature_of_security_effect = property_affected
    incident = Incident(title="Exfiltration of Information on Connected mounted devices to the host/target system.")
    incident.affected_assets = affected_asset

    pkg.add_incident(incident)

    print pkg.to_xml()

if __name__ == '__main__':
    main()
