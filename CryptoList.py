from DTO.Crypto import CryptoDTO


class CryptoList:
    __crypto_list = []

    def add_crypto(self, name: str):
        self.__crypto_list.append(CryptoDTO(name=name))

    def get_list(self):
        return self.__crypto_list
