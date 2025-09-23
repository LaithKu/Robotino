import requests
import json
import time
from opcua import Client, ua
import threading

ROBOTINOIP = "172.21.12.1"
PARAMS = {'sid': 'rest-api'}
PLCIP = "172.21.0.250"

########################################################################################################################

# OPC UA Read/Write
def read_input_value(client, node_id):
    client_node = client.get_node(node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
    # print("Value of : " + str(client_node) + ' : ' + str(client_node_value))

    return client_node_value


def write_int16(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_int32(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int32))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_int_array(client, node_id, int_array):
    client_node = client.get_node(node_id)  # get node
    client_node_value = int_array
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16, is_array=True))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_real(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Float))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_real_array(client, node_id, real_array):
    client_node = client.get_node(node_id)  # get node
    client_node_value = real_array
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Float, is_array=True))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_string(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.String))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_string_array(client, node_id, string_array):
    client_node = client.get_node(node_id)  # get node
    client_node_value = string_array
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.String, is_array=True))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_bool(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_bool_array(client, node_id, bool_array):
    client_node = client.get_node(node_id)  # get node
    client_node_value = bool_array
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean, is_array=True))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


########################################################################################################################


# REST API for Robotino
class RobotinoAPI:
    def __init__(self, ip_address, params=None):
        self.base_url = f"http://{ip_address}"
        self.session = requests.Session()
        self.params = params

    def _get(self, endpoint, port=80):
        url = f"{self.base_url}:{port}{endpoint}"
        response = self.session.get(url, params=self.params)

        if response.status_code == requests.codes.ok:
            if not response.text.strip():
                return None
            try:
                return response.json()
            except json.JSONDecodeError:
                return None
        else:
            raise RuntimeError(
                f"Error: GET from {url} failed "
                f"(Status code: {response.status_code})"
            )

    # === GET ===

    def get_cam0(self):
        return 0

    def get_powermanagement(self):
        try:
            data = self._get("/data/powermanagement")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_charger0(self):
        try:
            data = self._get("/data/charger0")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_controllerinfo(self):
        try:
            data = self._get("/data/controllerinfo")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_services(self):
        try:
            data = self._get("/data/services")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_servicestatus(self, service="SmartFestoFleetCom_master"):
        try:
            data = self._get(f"/data/servicestatus/{service}")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_analoginputarray(self):
        try:
            data = self._get("/data/analoginputarray")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_digitalinputarray(self):
        try:
            data = self._get("/data/digitalinputarray")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_digitaloutputstatus(self):
        try:
            data = self._get("/data/digitaloutputstatus")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_relaystatus(self):  # noch nicht ganz sauber aber tut was es soll (robotino interner Fehler)
        try:
            data = self._get("/data/relaystatus")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_bumper(self):
        try:
            data = self._get("/data/bumper")
            return data["value"]
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_distancesensorarray(self):
        try:
            data = self._get("/data/distancesensorarray")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain a valid 'value' field")

    def get_scan0(self):
        try:
            data = self._get("/data/scan0")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_odometry(self):
        try:
            data = self._get("/data/odometry")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_imageversion(self):
        try:
            data = self._get("/data/imageversion")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    def get_outputcurrentmotor4(self):
        try:
            data = self._get("/data/poweroutputcurrent")
            return data
        except (KeyError, TypeError):
            raise ValueError("Response did not contain valid values")

    # === PUT ===

    def put_omnidrive(self, payload):  # vx, vy, omega):
        # payload = [vx, vy, omega]
        url = self.base_url + "/data/omnidrive"
        response = self.session.put(url=url, params=PARAMS, data=json.dumps(payload))
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                f"Error: PUT to {url} failed "
                f"(Status code: {response.status_code})")

    def put_digitaloutputX(self, num, val):
        payload = {"num": num, "val": val}
        url = self.base_url + ":80/data/digitaloutput"
        response = self.session.put(url=url, params=PARAMS, data=json.dumps(payload))
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                f"Error: PUT to {url} failed "
                f"(Status code: {response.status_code})")

    def put_digitaloutputarray(self, payload):  # val0, val1, val2, val3, val4, val5, val6, val7):
        # payload = [val0, val1, val2, val3, val4, val5, val6, val7]
        url = self.base_url + "/data/digitaloutputarray"
        response = self.session.put(url=url, params=PARAMS, data=json.dumps(payload))
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                f"Error: PUT to {url} failed "
                f"(Status code: {response.status_code})")

    def put_relayX(self, num, val):
        payload = {"num": num, "val": val}
        url = self.base_url + ":80/data/relay"
        response = self.session.put(url=url, params=PARAMS, data=json.dumps(payload))
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                f"Error: PUT to {url} failed "
                f"(Status code: {response.status_code})")

    def put_relayarray(self, payload):  # val0, val1):
        # payload = [val0, val1]
        url = self.base_url + "/data/relayarray"
        response = self.session.put(url=url, params=PARAMS, data=json.dumps(payload))
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                f"Error: PUT to {url} failed "
                f"(Status code: {response.status_code})")

    def put_outputmotor4(self, val):
        payload = {"value": val}
        url = self.base_url + ":80/data/poweroutput"
        response = self.session.put(url=url, params=PARAMS, data=json.dumps(payload))
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                f"Error: PUT to {url} failed "
                f"(Status code: {response.status_code})")

    def put_startstopprogram(self, name):
        payload = {"action": "", "name": name, "suffix": "rvwx"}
        url = self.base_url + ":80/data/startStopProgram"
        response = self.session.put(url=url, params=PARAMS, data=json.dumps(payload))
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                f"Error: PUT to {url} failed "
                f"(Status code: {response.status_code})")

    # === Movement ===
    def navigation(self, plcclient, robotinoclient, robotinoId=1):  # designed to be used in a loop
        pos_id = read_input_value(plcclient, 'ns=3;s="ROBOTINO".Position_ID')
        start_goto = read_input_value(plcclient, 'ns=3;s="ROBOTINO".Start_GoToPos')
        start_dockto = read_input_value(plcclient, 'ns=3;s="ROBOTINO".Start_DockTo')
        stop_dockto = read_input_value(plcclient, 'ns=3;s="ROBOTINO".Stop_DockTo')

        factory_started = read_input_value(robotinoclient, 'ns=1;s=out1')
        factory_idle = read_input_value(robotinoclient, 'ns=1;s=out2')
        factory_busy = read_input_value(robotinoclient, 'ns=1;s=out3')
        factory_error = read_input_value(robotinoclient, 'ns=1;s=out4')
        write_bool_array(plcclient, 'ns=3;s="ROBOTINO".Factory_Status', [factory_idle, factory_busy, factory_error,
                                                                         factory_started])

        goto_completed = read_input_value(plcclient, 'ns=3;s="ROBOTINO"."GoToPos_Completed"')
        dockto_completed = read_input_value(plcclient, 'ns=3;s="ROBOTINO"."DockTo_Completed"')
        write_int32(robotinoclient, 'ns=1;s=in6', goto_completed)
        write_int32(robotinoclient, 'ns=1;s=in8', start_goto)
        write_int32(robotinoclient, 'ns=1;s=in4', dockto_completed)
        write_int32(robotinoclient, 'ns=1;s=in3', start_dockto)
        write_int32(robotinoclient, 'ns=1;s=in5', stop_dockto)
        write_int32(robotinoclient, 'ns=1;s=in1', pos_id)
        write_int32(robotinoclient, 'ns=1;s=in7', robotinoId)
        time.sleep(0.5)
        write_int32(robotinoclient, 'ns=1;s=in2', start_goto)


########################################################################################################################


def main():
    client1 = Client(f"opc.tcp://{PLCIP}:4840")
    client1.session_timeout = 30000

    robotino1 = RobotinoAPI(ROBOTINOIP, params=PARAMS)
    client2 = Client(f"opc.tcp://{ROBOTINOIP}:8225")

    def outputmotor4_worker():
        while True:
            try:
                robotino1.put_outputmotor4(read_input_value(client1, 'ns=3;s="ROBOTINO".Motor4'))
                time.sleep(0.01)
            except Exception as e:
                print("Thread error", e)

    try:
        client1.connect()
        client2.connect()

        root1 = client1.get_root_node()
        print("Objects root node is: ", root1)

        root2 = client2.get_root_node()
        print("Objects root node is: ", root2)

        # robotino1.put_startstopprogram("GoToPos2")

        motor4_thread = threading.Thread(target=outputmotor4_worker, daemon=True)
        motor4_thread.start()

        while 1:
            try:
                robotino1.navigation(client1, client2)

                # Write Data from Robotino to PLC
                write_bool(client1, 'ns=3;s="ROBOTINO"."Bumper"', robotino1.get_bumper())
                write_real_array(client1, 'ns=3;s="ROBOTINO"."Distance_Sensors"', robotino1.get_distancesensorarray())
                write_bool_array(client1, 'ns=3;s="ROBOTINO"."Digital_Inputs"', robotino1.get_digitalinputarray())
                write_real_array(client1, 'ns=3;s="ROBOTINO"."Analog_Inputs"', robotino1.get_analoginputarray())
                write_real(client1, 'ns=3;s="ROBOTINO"."Motor4_Current"',
                           robotino1.get_outputcurrentmotor4().get("current"))
                write_bool_array(client1, 'ns=3;s="ROBOTINO"."Digital_Outputs_Status"',
                                 robotino1.get_digitaloutputstatus())

                # macht noch Probleme
                # write_bool_array(client, 'ns=3;s="ROBOTINO"."Relay_Status"', robotino1.get_relaystatus())
                write_real_array(client1, 'ns=3;s="ROBOTINO"."Odometry"', robotino1.get_odometry())
                write_real(client1, 'ns=3;s="ROBOTINO"."Bat_Voltage"', robotino1.get_powermanagement().get("voltage"))
                write_string(client1, 'ns=3;s="ROBOTINO"."Charging_State"', robotino1.get_charger0().get("state"))
                write_real(client1, 'ns=3;s="ROBOTINO"."Charging_Current"',
                           robotino1.get_charger0().get("chargingCurrent"))
                write_string(client1, 'ns=3;s="ROBOTINO"."Controller_Info"[0]',
                             robotino1.get_controllerinfo().get("payload").get("hardware"))
                write_string(client1, 'ns=3;s="ROBOTINO"."Controller_Info"[1]',
                             robotino1.get_controllerinfo().get("payload").get("software"))
                write_string(client1, 'ns=3;s="ROBOTINO".Image_Version',
                             robotino1.get_imageversion().get("version").rstrip("\n"))

                # Write Data from PLC to Robotino
                # robotino1.put_outputmotor4(read_input_value(client1, 'ns=3;s="ROBOTINO".Motor4'))
                robotino1.put_digitaloutputarray(read_input_value(client1, 'ns=3;s="ROBOTINO".Digital_Outputs'))
                robotino1.put_relayarray(read_input_value(client1, 'ns=3;s="ROBOTINO".Relay'))
                robotino1.put_omnidrive(read_input_value(client1, 'ns=3;s="ROBOTINO".Omnidrive'))

                print(read_input_value(client1, 'ns=3;s="ROBOTINO".Omnidrive'))

                last_motor4_value = read_input_value(client1, 'ns=3;s="ROBOTINO".Motor4')

                time.sleep(0.1)

            except Exception as e:
                print(e)
                continue

    finally:
        client1.disconnect()
        client2.disconnect()

    return 0


if __name__ == "__main__":
    main()

