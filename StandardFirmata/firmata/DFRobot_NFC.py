import abc
import time

PN532_PREAMBLE                      = 0x00
PN532_STARTCODE1                    = 0x00
PN532_STARTCODE2                    = 0xFF
PN532_POSTAMBLE                     = 0x00
PN532_HOSTTOPN532                   = 0xD4
PN532_PN532TOHOST                   = 0xD5

# PN532 Commands
PN532_COMMAND_DIAGNOSE              = 0x00
PN532_COMMAND_GETFIRMWAREVERSION    = 0x02
PN532_COMMAND_GETGENERALSTATUS      = 0x04
PN532_COMMAND_READREGISTER          = 0x06
PN532_COMMAND_WRITEREGISTER         = 0x08
PN532_COMMAND_READGPIO              = 0x0C
PN532_COMMAND_WRITEGPIO             = 0x0E
PN532_COMMAND_SETSERIALBAUDRATE     = 0x10
PN532_COMMAND_SETPARAMETERS         = 0x12
PN532_COMMAND_SAMCONFIGURATION      = 0x14
PN532_COMMAND_POWERDOWN             = 0x16
PN532_COMMAND_RFCONFIGURATION       = 0x32
PN532_COMMAND_RFREGULATIONTEST      = 0x58
PN532_COMMAND_INJUMPFORDEP          = 0x56
PN532_COMMAND_INJUMPFORPSL          = 0x46
PN532_COMMAND_INLISTPASSIVETARGET   = 0x4A
PN532_COMMAND_INATR                 = 0x50
PN532_COMMAND_INPSL                 = 0x4E
PN532_COMMAND_INDATAEXCHANGE        = 0x40
PN532_COMMAND_INCOMMUNICATETHRU     = 0x42
PN532_COMMAND_INDESELECT            = 0x44
PN532_COMMAND_INRELEASE             = 0x52
PN532_COMMAND_INSELECT              = 0x54
PN532_COMMAND_INAUTOPOLL            = 0x60
PN532_COMMAND_TGINITASTARGET        = 0x8C
PN532_COMMAND_TGSETGENERALBYTES     = 0x92
PN532_COMMAND_TGGETDATA             = 0x86
PN532_COMMAND_TGSETDATA             = 0x8E
PN532_COMMAND_TGSETMETADATA         = 0x94
PN532_COMMAND_TGGETINITIATORCOMMAND = 0x88
PN532_COMMAND_TGRESPONSETOINITIATOR = 0x90
PN532_COMMAND_TGGETTARGETSTATUS     = 0x8A

PN532_RESPONSE_INDATAEXCHANGE       = 0x41
PN532_RESPONSE_INLISTPASSIVETARGET  = 0x4B

PN532_WAKEUP                        = 0x55

PN532_SPI_STATREAD                  = 0x02
PN532_SPI_DATAWRITE                 = 0x01
PN532_SPI_DATAREAD                  = 0x03
PN532_SPI_READY                     = 0x01

PN532_I2C_ADDRESS                   = 0x48 >> 1
PN532_I2C_READBIT                   = 0x01
PN532_I2C_BUSY                      = 0x00
PN532_I2C_READY                     = 0x01
PN532_I2C_READYTIMEOUT              = 20

PN532_MIFARE_ISO14443A              = 0x00

# Mifare Commands
MIFARE_CMD_AUTH_A                   = 0x60
MIFARE_CMD_AUTH_B                   = 0x61
MIFARE_CMD_READ                     = 0x30
MIFARE_CMD_WRITE                    = 0xA0
MIFARE_CMD_TRANSFER                 = 0xB0
MIFARE_CMD_DECREMENT                = 0xC0
MIFARE_CMD_INCREMENT                = 0xC1
MIFARE_CMD_STORE                    = 0xC2
MIFARE_ULTRALIGHT_CMD_WRITE         = 0xA2

# Prefixes for NDEF Records (to identify record type)
NDEF_URIPREFIX_NONE                 = 0x00
NDEF_URIPREFIX_HTTP_WWWDOT          = 0x01
NDEF_URIPREFIX_HTTPS_WWWDOT         = 0x02
NDEF_URIPREFIX_HTTP                 = 0x03
NDEF_URIPREFIX_HTTPS                = 0x04
NDEF_URIPREFIX_TEL                  = 0x05
NDEF_URIPREFIX_MAILTO               = 0x06
NDEF_URIPREFIX_FTP_ANONAT           = 0x07
NDEF_URIPREFIX_FTP_FTPDOT           = 0x08
NDEF_URIPREFIX_FTPS                 = 0x09
NDEF_URIPREFIX_SFTP                 = 0x0A
NDEF_URIPREFIX_SMB                  = 0x0B
NDEF_URIPREFIX_NFS                  = 0x0C
NDEF_URIPREFIX_FTP                  = 0x0D
NDEF_URIPREFIX_DAV                  = 0x0E
NDEF_URIPREFIX_NEWS                 = 0x0F
NDEF_URIPREFIX_TELNET               = 0x10
NDEF_URIPREFIX_IMAP                 = 0x11
NDEF_URIPREFIX_RTSP                 = 0x12
NDEF_URIPREFIX_URN                  = 0x13
NDEF_URIPREFIX_POP                  = 0x14
NDEF_URIPREFIX_SIP                  = 0x15
NDEF_URIPREFIX_SIPS                 = 0x16
NDEF_URIPREFIX_TFTP                 = 0x17
NDEF_URIPREFIX_BTSPP                = 0x18
NDEF_URIPREFIX_BTL2CAP              = 0x19
NDEF_URIPREFIX_BTGOEP               = 0x1A
NDEF_URIPREFIX_TCPOBEX              = 0x1B
NDEF_URIPREFIX_IRDAOBEX             = 0x1C
NDEF_URIPREFIX_FILE                 = 0x1D
NDEF_URIPREFIX_URN_EPC_ID           = 0x1E
NDEF_URIPREFIX_URN_EPC_TAG          = 0x1F
NDEF_URIPREFIX_URN_EPC_PAT          = 0x20
NDEF_URIPREFIX_URN_EPC_RAW          = 0x21
NDEF_URIPREFIX_URN_EPC              = 0x22
NDEF_URIPREFIX_URN_NFC              = 0x23

PN532_GPIO_VALIDATIONBIT            = 0x80
PN532_GPIO_P30                      = 0
PN532_GPIO_P31                      = 1
PN532_GPIO_P32                      = 2
PN532_GPIO_P33                      = 3
PN532_GPIO_P34                      = 4
PN532_GPIO_P35                      = 5

class DFRobot_PN532(object):

    def __init__(self):
        self.receive_ACK = bytearray(35)
        self.password = bytearray(6)
        self.uid = bytearray(4)
        self.block_data = bytearray(16)
        self.enable = True
        self.text_error = ["no card", "read error", "unknown error",
                           "read timeout", "wake up error"]

    def read_data(self, page, index=None):
        if not self.enable:
            return "wake up error"
        if not self.scan():
            return "no card"
        if not passWordCheck(page, self.uid, self.password):
            return "read error"
        cmdRead = [0x00, 0x00, 0xff, 0x05, 0xfb, 0xD4, 0x40, 0x01, 0x30, 0x07, 0xB4, 0x00]
        sum = 0
        cmdRead[9] = page
        for i in range(10):
            sum += cmdRead[i]
        cmdRead[10] = 0xff - sum & 0xff
        if not self.clear():
            return "unknown error"
        self.write_cmd(cmdRead, 12)
        time.sleep(0.1)
        if not self.read_Ack(32):
            return "read timeout"
        dataSrt = "0x"
        if self.check_DCS(32) == 1 and self.receive_ACK[12] == 0x41 and self.receive_ACK[13] == 0x00:
            for i in range(16):
                self.block_data[i] = self.receive_ACK[i + 14]
                dataSrt += hex(self.receive_ACK[i + 14])[2:].rjust(2, '0')
                # if self.receive_ACK[i + 14] <= 0x0f:
                #     dataSrt += "0"
                #     dataSrt += hex(self.receive_ACK[i + 14])[2:]
                # else:
                #     dataSrt += hex(receive_ACK[i + 14])[2:]
                if i < 15:
                    dataSrt += " 0x"
        if index:
            return self.block_data[index - 1]
        return dataSrt

    def write_data(self, block, data, index=None):
        if not self.enable:
            return
        if index and isinstance(data, int):
            index = max(min(index, 16), 1)
            self.read_data(block)
            self.block_data[index - 1] = data
            data = self.block_data
        if not self.scan():
            return
        if not self.password_check(block, self.uid, self.password):
            return
        cmdWrite = [
            0x00, 0x00, 0xff, 0x15, 0xEB, 0xD4, 0x40, 0x01, 0xA0,
            0x06, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
            0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0xCD, 0x00
        ]
        sum = 0
        cmdWrite[9] = block
        for i in range(10, 26):
            cmdWrite[i] = data[i - 10]  # data wait for write in
        for i in range(26):
            sum += cmdWrite[i]
        cmdWrite[26] = 0xff - sum & 0xff  # calculate DCS
        if not self.clear():
            return
        self.write_cmd(cmdWrite, 28)
        self.read_Ack(16)

    def scan(self, uid_str=None):
        if not self.enable:
            return False
        cmdUID = [0x00, 0x00, 0xFF, 0x04, 0xFC, 0xD4, 0x4A, 0x01, 0x00, 0xE1, 0x00]
        repeat = 1
        if not self.clear():
            return False
        self.write_cmd(cmdUID, 11)
        time.sleep(0.05)
        if not self.read_ACK(25):
            repeat -= 1
        if repeat == 0:
            return False
        for i in range(4):
            self.uid[i] = self.receive_ACK[i + 19]
        if self.uid[0] == 0xFF and self.uid[1] == 0xFF and self.uid[2] == 0xFF and self.uid[3] == 0xFF:
            return False
        if self.uid[0] == 0x80 and self.uid[1] == 0x80 and self.uid[2] == 0x80 and self.uid[3] == 0x80:
            return False
        if uid_str:
            temp = ""
            for i in range(4):
                temp += hex(self.uid[i])[2:].rjust(2, '0')
            if uid_str != temp:
                return False
        return True

    def read_uid(self):
        if not self.enable:
            return False
        if not self.scan():
            return "no card"
        uid_str = ''
        for i in range(0, 4):
            uid_str += hex(self.uid[i])[2:].rjust(2, '0')
            # if self.uid[i] <= 0x0f:
            #     uid_str += "0"
            #     uid_str += hex(self.uid[i])[2:]
            # else:
            #     uid_str += hex(self.uid[i])[2:]
        return uid_str

    @abc.abstractmethod
    def wake_up(self):
        pass

    @abc.abstractmethod
    def write_cmd(self, cmd_data, byte):
        pass

    @abc.abstractmethod
    def read_ACK(self, x, timeout=1000):
        pass

    def password_check(self, block_num, uid, pwd):
        if not self.enable:
            return False
        cmdPassWord = [
            0x00, 0x00, 0xFF, 0x0F, 0xF1, 0xD4, 0x40, 0x01, 0x60, 0x07, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xD1, 0xAA, 0x40, 0xEA, 0xC2, 0x00
        ]
        sum = 0
        cmdPassWord[9] = block_num
        for i in range(10, 16):
            cmdPassWord[i] = pwd[i - 10]  # password
        for i in range(16, 20):
            cmdPassWord[i] = uid[i - 16]  # uid
        for i in range(20):
            sum += cmdPassWord[i]
        cmdPassWord[20] = 0xff - sum & 0xff
        if not self.clear():
            return 'unknown error'
        self.write_cmd(cmdPassWord, 22)
        if not self.read_ACK(16):
            return False
        res = self.check_DCS(16)
        if res == 1 and self.receive_ACK[12] == 0x41 and self.receive_ACK[13] == 0x00:
            return True
        return False

    def check_DCS(self, x):
        # NFC S50卡 DCS校验检测子函数
        if not self.enable:
            return 0
        sum = 0
        for i in range(6, x-2):
            sum += self.receive_ACK[i]
        dcs = 0xff - sum & 0xff
        if dcs == self.receive_ACK[x - 2]:
            return 1
        return 0

    @abc.abstractmethod
    def clear(self):
        pass


class DFRobot_PN532_IIC(DFRobot_PN532):

    def __init__(self, i2c):
        self.i2c = i2c
        super().__init__()

    def begin(self):
        return self.wake_up()

    def wake_up(self):
        self.password[0] = self.password[1] = self.password[2] = 0xff
        self.password[3] = self.password[4] = self.password[5] = 0xff
        pn532PacketBuffer = [0] * 4
        pn532PacketBuffer[0] = PN532_COMMAND_SAMCONFIGURATION
        pn532PacketBuffer[1] = 0x01  # normal mode;
        pn532PacketBuffer[2] = 0x14  # timeout 50ms * 20 = 1 second
        pn532PacketBuffer[3] = 0x01  # use IRQ pin!
        self.enable = True
        cmd_len = 5
        # time.sleep(0.02)
        checksum = PN532_PREAMBLE + PN532_PREAMBLE + PN532_STARTCODE2
        data = []
        data.extend(
            [PN532_PREAMBLE, PN532_PREAMBLE, PN532_STARTCODE2, cmd_len, ~cmd_len+1, PN532_HOSTTOPN532]
        )
        checksum += PN532_HOSTTOPN532
        for i in range(4):
            data.append(pn532PacketBuffer[i])
            checksum += pn532PacketBuffer[i]
        data.append(255-((checksum%255)-1))
        data.append(PN532_POSTAMBLE)
        print("from wake_up: ", PN532_I2C_ADDRESS, data)
        self.i2c.i2c_write_request(PN532_I2C_ADDRESS, data)
        self.i2c.sleep(0.2)
        val = self.read_ACK(14)
        if val != 1:
            return 0
        return (self.receive_ACK[12] == 0x15)

    def write_cmd(self, cmd, cmd_len):
        self.i2c.i2c_write_request(PN532_I2C_ADDRESS, cmd)
        self.i2c.sleep(0.2)

    def clear(self):
        return 1

    def read_ACK(self, x, timeout=1000):
        pn532ack = [0x00, 0x00, 0xFF, 0x00, 0xFF, 0x00]
        # time.sleep(0.002)
        self.i2c.i2c_read_request(PN532_I2C_ADDRESS, 8, 8)
        self.i2c.sleep(0.1)
        data = self.i2c.i2c_read_data(PN532_I2C_ADDRESS)[1:-1]
        # print("from DFRobot_PN532_IIC read_ACK: ", data)
        for i in range(6):
            # time.sleep(0.001)
            self.receive_ACK[i] = data[i]
        # self.i2c.sleep(0.5)
        self.i2c.i2c_read_request(PN532_I2C_ADDRESS, x-4, 8)
        self.i2c.sleep(0.1)
        data = self.i2c.i2c_read_data(PN532_I2C_ADDRESS)[1:-1]
        # print("from DFRobot_PN532_IIC read_ACK: ", data)
        for i in range(x - 6):
            # time.sleep(0.001)
            self.receive_ACK[i + 6] = data[i]
        # print(list(self.receive_ACK[19:25]))
        if pn532ack != list(self.receive_ACK[:6]):
            return 0
        return 1
