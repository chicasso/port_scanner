import  threading
import  sys
import  socket

def scan_port(port_number, target):
    try:
        target_machine = socket.gethostbyname(target)

        # 0 in case of successful connection
        #                                IPv4 - socket   TCP based socket
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.settimeout(1) # Only wait till 1 second (avoid hanging)
        connection_success = not socket_instance.connect_ex((target_machine, port_number))
        socket_instance.close()

        # print("Connection Status", connection_success)

        if connection_success:
            print('{} is open'.format(port_number))

    except Exception as e:
        print("Connection Failed! {}".format(e))
        sys.exit(1)

def scan_port_from_range():
    if not sys.argv[2].isnumeric() or not sys.argv[3].isnumeric():
        print("Invalid input params")
        sys.exit(1)

    target = sys.argv[1]
    port_start = int(sys.argv[2])
    port_end = port_start + int(sys.argv[3])

    spawned_threads = []

    for i in range(port_start, port_end):
        t = threading.Thread(target = scan_port, args = (i, target))
        t.start()
        spawned_threads.append(t)

    for i in spawned_threads:
        i.join() # Waiting for all threads to finish executing

if __name__ == '__main__':
    message: str = "PORT Sniffer\nUsage: python main <dest> <port_start> <range>"

    if len(sys.argv) != 4:
        print(message)
        sys.exit(1)

    scan_port_from_range()
