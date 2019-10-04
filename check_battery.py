# -- coding: utf-8 --
from __future__ import unicode_literals
import os
from time import sleep


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


status_path = '/sys/class/power_supply/battery/status'
capacity_path = '/sys/class/power_supply/battery/capacity'
volt_path = '/sys/class/power_supply/battery/voltage_now'
current_path = '/sys/class/power_supply//battery/current_now'
technology_path = '/sys/class/power_supply//battery/technology'
temp_path = '/sys/class/power_supply//battery/temp'
present_path = '/sys/class/power_supply//battery/present'
health_path = '/sys/class/power_supply//battery/health'


def get_capacity():
    """
    What:		/sys/class/power_supply/<supply_name>/capacity
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
		    Fine grain representation of battery capacity.
		    Access: Read
		    Valid values: 0 - 100 (percent)
    """
    response = 0
    if os.path.exists(capacity_path):
        with open(capacity_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_volt():
    """
    What:		/sys/class/power_supply/<supply_name>/voltage_now,
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
		    Reports an instant, single VBAT voltage reading for the battery.
		    This value is not averaged/smoothed.

		    Access: Read
		    Valid values: Represented in microvolts
    """
    response = 0
    if os.path.exists(volt_path):
        with open(volt_path, 'r') as f:
          response = f.readline().rstrip()
          response = float(response) / 1000000.0
    return response


def get_current():
    """
    What:		/sys/class/power_supply/<supply_name>/current_now
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
		    Reports an instant, single IBAT current reading for the battery.
		    This value is not averaged/smoothed.

		    Access: Read
		    Valid values: Represented in microamps
    """
    response = 0
    if os.path.exists(current_path):
        with open(current_path, 'r') as f:
            response = f.readline().rstrip()
            response = float(response) / 1000.0
    return response


def get_status():
    """
    What:		/sys/class/power_supply/<supply_name>/status
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
		    Represents the charging status of the battery. Normally this
		    is read-only reporting although for some supplies this can be
		    used to enable/disable charging to the battery.

		    Access: Read, Write
		    Valid values: "Unknown", "Charging", "Discharging",
			          "Not charging", "Full"
    """
    with open(status_path) as f:
        response = f.readline().rstrip()
    return response


def get_technology():
    """
    What:		/sys/class/power_supply/<supply_name>/technology
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
		    Describes the battery technology supported by the supply.

		    Access: Read
		    Valid values: "Unknown", "NiMH", "Li-ion", "Li-poly", "LiFe",
			          "NiCd", "LiMn"
    """
    response = 0
    if os.path.exists(technology_path):
        with open(technology_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_temp():
    """
    What:		/sys/class/power_supply/<supply_name>/temp
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
		    Reports the current TBAT battery temperature reading.

		    Access: Read
		    Valid values: Represented in 1/10 Degrees Celsius
    """
    response = 0
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as f:
            response = f.readline().rstrip()
            response = float(response) / 10.0
    return response


def get_present():
    """
    What:		/sys/class/power_supply/<supply_name>/present
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
		    Reports whether a battery is present or not in the system.

		    Access: Read
		    Valid values:
			    0: Absent
			    1: Present
    """
    response = 0
    if os.path.exists(present_path):
        with open(present_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_health():
    """
    What:		/sys/class/power_supply/<supply_name>/health
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
		    Reports the health of the battery or battery side of charger
		    functionality.

		    Access: Read
		    Valid values: "Unknown", "Good", "Overheat", "Dead",
			          "Over voltage", "Unspecified failure", "Cold",
			          "Watchdog timer expire", "Safety timer expire"
    """
    response = 0
    if os.path.exists(health_path):
        with open(health_path, 'r') as f:
            response = f.readline().rstrip()
    return response


if __name__ == '__main__':
    while True:
        print(get_volt())
        print(get_capacity())
        print(get_current())
        print(get_status())
        print(get_technology())
        print(get_temp())
        print(get_present())
        print(get_health())
        sleep(15)

