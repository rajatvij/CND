"""
Description: Build a STIX Indicator document containing an indicator for
list of c2 ip addresses in network traffic.
"""

from stix.common.vocabs import VocabString
from stix.core import STIXPackage
from stix.indicator import Indicator
from stix.ttp import TTP
from stix.ttp.infrastructure import Infrastructure
from stix.ttp.resource import Resource
from cybox.core import Observables, Observable, Object
from cybox.objects.address_object import Address

def main():
    stix_package = STIXPackage()
    # For VM provided
    addr1 = Observable(Address(address_value="192.168.1.3", category=Address.CAT_IPV4))
    addr2 = Observable(Address(address_value="192.168.1.50", category=Address.CAT_IPV4))
    addr3 = Observable(Address(address_value="169.254.127.100", category=Address.CAT_IPV4))
    addr4 = Observable(Address(address_value="169.254.183.168", category=Address.CAT_IPV4))
    addr5 = Observable(Address(address_value="169.254.229.163", category=Address.CAT_IPV4))
    addr6 = Observable(Address(address_value="169.254.99.82", category=Address.CAT_IPV4))
    addr7 = Observable(Address(address_value="192.168.1.2", category=Address.CAT_IPV4))

    # For Our VM with internet Access
    addr8 = Observable(Address(address_value="173.194.208.98", category=Address.CAT_IPV4))
    addr9 = Observable(Address(address_value="104.16.25.190", category=Address.CAT_IPV4))
    addr10 = Observable(Address(address_value="216.58.195.142", category=Address.CAT_IPV4))
    addr11 = Observable(Address(address_value="216.58.217.174", category=Address.CAT_IPV4))
    addr12 = Observable(Address(address_value="209.85.282.188", category=Address.CAT_IPV4))
    
    stix_package.add_observable(addr1)
    stix_package.add_observable(addr2)
    stix_package.add_observable(addr3)
    stix_package.add_observable(addr4)
    stix_package.add_observable(addr5)
    stix_package.add_observable(addr6)
    stix_package.add_observable(addr7)
    stix_package.add_observable(addr8)
    stix_package.add_observable(addr9)
    stix_package.add_observable(addr10)
    stix_package.add_observable(addr11)
    stix_package.add_observable(addr12)
    
    obs_addr1 = Observable()
    obs_addr2 = Observable()
    obs_addr3 = Observable()
    obs_addr4 = Observable()
    obs_addr5 = Observable()
    obs_addr6 = Observable()
    obs_addr7 = Observable()
    obs_addr8 = Observable()
    obs_addr9 = Observable()
    obs_addr10 = Observable()
    obs_addr11 = Observable()
    obs_addr12 = Observable()

    obs_addr1.id_ = None
    obs_addr2.id_ = None
    obs_addr3.id_ = None
    obs_addr4.id_ = None
    obs_addr5.id_ = None
    obs_addr6.id_ = None
    obs_addr7.id_ = None
    obs_addr8.id_ = None
    obs_addr9.id_ = None
    obs_addr10.id_ = None
    obs_addr11.id_ = None
    obs_addr12.id_ = None
    
    obs_addr1.idref = addr1.id_
    obs_addr2.idref = addr2.id_
    obs_addr3.idref = addr3.id_
    obs_addr4.idref = addr4.id_
    obs_addr5.idref = addr5.id_
    obs_addr6.idref = addr6.id_
    obs_addr7.idref = addr7.id_
    obs_addr8.idref = addr8.id_
    obs_addr9.idref = addr9.id_
    obs_addr10.idref = addr10.id_
    obs_addr11.idref = addr11.id_
    obs_addr12.idref = addr12.id_
    
    vocab_string = VocabString(value='Malware C2')

    infrastructure = Infrastructure()
    infrastructure.observable_characterization = Observables([obs_addr1, obs_addr2, obs_addr3, obs_addr4, obs_addr5, obs_addr6, obs_addr7, obs_addr8, obs_addr9, obs_addr10, obs_addr11, obs_addr12])
    infrastructure.add_type(vocab_string)
    
    resource = Resource()
    resource.infrastructure = infrastructure
    
    ttp = TTP(title="Malware C2 Channel")
    ttp.resources = resource
    
    stix_package.add_ttp(ttp)
    print stix_package.to_xml()
    
if __name__ == '__main__':
    main()
