import qrcode
import numpy
from mcrcon import MCRcon

class Server:
    def __init__(self):
        self.rcon_ip = "46.126.69.5"
        self.rcon_pw = "password123"
        self.max_qr_size = 49
        self.qr_border = 2

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
                        mcr.command(f"fill {x} {y} {z} {x} {y - self.max_qr_size - 2 * self.qr_border + 1} {z + self.max_qr_size + 2 * self.qr_border - 1} minecraft:white_concrete")
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
                        print(mcr.command(f"say generated QR Code ({len(qr_matrix)} x {len(qr_matrix[0])}) at {x} {y} {z}"))
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
        server = Server()
        # Build Qr Code
        server.build_qr_code(text, pos, table, built = "1")
