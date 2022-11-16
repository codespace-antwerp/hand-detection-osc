import argparse
from pythonosc import dispatcher
from pythonosc import osc_server


def print_number_of_hands(_, args):
    print("Number of hands: ", args)


def print_hand_details(_, *args):
    print("Hand : ", *args)


def sniff(osc_ip, osc_port):
    router = dispatcher.Dispatcher()
    router.map("/number_of_hands", print_number_of_hands)
    router.map("/hand", print_hand_details)
    server = osc_server.ThreadingOSCUDPServer((osc_ip, osc_port), router)
    print("Listening on {}".format(server.server_address))
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument(
        "--port", type=int, default=5005, help="The port the OSC server is listening on"
    )
    args = parser.parse_args()
    sniff(args.ip, args.port)
