import qrcode
import numpy
from mcrcon import MCRcon


class Server:
    def __init__(self):
        self.rcon_ip = "46.126.69.5"
        self.rcon_pw = "password123"
        self.max_qr_size = 49
        self.qr_border = 2

    def build_qr_code(self, matrix, pos):
        if len(matrix) > self.max_qr_size:
            print(f"QR-Code too big ({len(matrix)} x {len(matrix[0])})")
            return None
        try:
            x, y, z = pos
            with MCRcon(self.rcon_ip, self.rcon_pw) as mcr:
                mcr.command(f"fill {x} {y} {z} {x} {y - self.max_qr_size - 2 * self.qr_border + 1} {z + self.max_qr_size + 2 * self.qr_border - 1} minecraft:white_concrete")
                for i in range(len(matrix)):
                    for j in range(len(matrix[i])):
                        tmp_x = x + j + self.qr_border
                        tmp_y = y - i - self.qr_border
                        tmp_z = z
                        if matrix[i][j] == 0:
                            command = f"/setblock {tmp_x} {tmp_y} {tmp_z} minecraft:black_concrete"
                            resp = mcr.command(command)
                            print(resp)
                print(mcr.command(f"say generated QR Code ({len(matrix)} x {len(matrix[0])}) at {x} {y} {z}"))
        except:
            print("Connection to server failed")

    def build_table_connection_qr(self, pos, table):
        Data = (pos, table)
        print(Data)
        qr_code = create_qr_matrix(Data)
        pos = (60, 60, 50)
        server.build_qr_code(qr_code, pos)


qr_config = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
    box_size=1,
    border=0,
)


def create_qr_matrix(data):
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
        table = "InputWebseite"
        # Create QR Code
        pos = (100, 100, 50)
        qr_matrix = create_qr_matrix(text)
        print(qr_matrix)
        server = Server()
        if qr_matrix is not None:
            if len(qr_matrix) < server.max_qr_size:
                server.build_table_connection_qr(pos, table)
            server.build_qr_code(qr_matrix, pos)
