def int_to_bytes32(input: int) -> str:
    return f"0x{input.to_bytes(32, byteorder='big').hex()}"
