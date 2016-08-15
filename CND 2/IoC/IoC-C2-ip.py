"""
Description: Build a STIX Indicator document containing an indicator for
c2 ip address producer.
"""

from stix.core import STIXPackage
from stix.indicator import Indicator
from stix.ttp import TTP
from cybox.core import Observable
from cybox.objects.address_object import Address


def main():
    stix_package = STIXPackage()
    ttp = TTP(title="C2 Behavior")

    indicator = Indicator(title="IP Address for known C2 Channel")
    indicator.add_indicator_type("IP Watchlist")
    # For VM provided
    # addr = Address(address_value="192.168.1.3", category=Address.CAT_IPV4)
    # For Our VM with internet access
    addr = Address(address_value="128.164.219.56", category=Address.CAT_IPV4)
    addr.condition = "Equals"
    indicator.add_observable(addr)
    indicator.add_indicated_ttp(TTP(idref=ttp.id_))

    stix_package.add_indicator(indicator)
    stix_package.add_ttp(ttp)

    print stix_package.to_xml()

if __name__ == '__main__':
    main()
