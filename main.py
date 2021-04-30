import qrcode
import numpy
from mcrcon import MCRcon
import PIL                      # needed for screenshot of qr-code


class Player:
    def __init__(self, connection, name):
        self.connection = connection
        self.name = name
        # join server

    def get_screen(self):
        # returns screenshot of qr-code
        img = 'qr.png'
        MCDatabase(img)
        pass


    def tp(self, qr_coords):
        # gets qr_position and calculates where to tp from there on
        # tp itself to those calculated coords
        pass


class MCDatabase:
    def __init__(self):
        self.tables_table_pos = (0, 80, 0)
        self.server = Server()

    def get_qr_data(self, img):
        # Get Date of Picture
        self.decoded = qrcode.Decoder()
        if self.decoded.decode(img):
            print('result: ' + self.decoded.result)
        else:
            print('error: ' + self.decoded.error)
        pass


class Server:
    def __init__(self, ip, pw):
        self.rcon_ip = ip
        self.rcon_pw = pw
        self.max_qr_size = 49
        self.qr_border = 2

    def open(self):
        # create rcon connection and store in self.connection
        self.connection = MCRcon(self.rcon_ip, self.rcon_pw).open()
        self.player = Player(self.connection)

    def read_table(self, table_start_pos):
        self.player.tp(table_start_pos)

        while True:
            screen = self.player.get_screen()
            data = self.get_qr_data(screen)
            yield data
            x, y, z = table_start_pos
            qr_pos = x, y, z - 20
            self.player.tp(qr_pos)

    def build_qr_code(self, input, pos, table, built):
        # Create QR Matrix
        qr_matrix = create_qr_matrix(input)
        print(qr_matrix)
        # Create Required QR-Codes
        if qr_matrix is not None:

            # Build QR-Code
            if len(qr_matrix) > self.max_qr_size:
                print(f"QR-Code too big ({len(qr_matrix)} x {len(qr_matrix[0])})")
                built = "0"
                return None

            if table != "0" and built != "0":
                # mark connection qr as built
                table == "0"
                # Build Main Connection QR
                print("")
                Cords = str(pos[0]) + "/" + str(pos[1]) + "/" + str(pos[2])
                data = Cords + " : " + str(table)
                server.build_table_connection_qr(data)

                try:
                    x, y, z = pos
                    with MCRcon(self.rcon_ip, self.rcon_pw) as mcr:
                        mcr.command(
                            f"fill {x} {y} {z} {x} {y - self.max_qr_size - 2 * self.qr_border + 1} {z + self.max_qr_size + 2 * self.qr_border - 1} minecraft:white_concrete")
                        for i in range(len(qr_matrix)):
                            for j in range(len(qr_matrix[i])):
                                tmp_x = x + j + self.qr_border
                                tmp_y = y - i - self.qr_border
                                tmp_z = z
                                if qr_matrix[i][j] == 0:
                                    command = f"/setblock {tmp_x} {tmp_y} {tmp_z} minecraft:black_concrete"
                                    resp = mcr.command(command)
                                    print(resp)
                        built = "0"
                        print(mcr.command(
                            f"say generated QR Code ({len(qr_matrix)} x {len(qr_matrix[0])}) at {x} {y} {z}"))
                except:
                    print("Connection to server failed")

    def build_table_connection_qr(self, Data):
        print(Data)
        qr_code = create_qr_matrix(Data)
        # Connection QR Code Coordinates
        self.max_qr_size = 56
        pos = (60, 60, 50)
        server.build_qr_code(Data, pos, table, built="0")


def create_qr_matrix(data):
    # QR-Code Static Configs
    qr_config = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=1,
        border=0,
    )

    qr_config.add_data(data)
    image = qr_config.make_image(fill_color="black", back_color="white")
    matrix = numpy.array(image, dtype=numpy.uint8)
    return matrix


# Main function
if __name__ == '__main__':
    text = ""
    while text != "exit":
        # User Input
        print("---------------- QR Code Creator ----------------")
        text = input("Enter Text-> ")
        # Input User from Website
        table = "InputWebsite"
        # Create QR Code Matrix
        pos = (100, 100, 50)
        server = Server("46.126.69.5", "password123")
        # Build Qr Code
        server.build_qr_code(text, pos, table, built="1")
