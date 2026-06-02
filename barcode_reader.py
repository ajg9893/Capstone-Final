# barcode_reader.py
# Compatible with Netum NSL3 CCD USB scanner (and any USB HID barcode scanner)
# The scanner acts as a keyboard — it types the barcode value and presses Enter

def read_barcode():
    student_id = input("").strip()
    return student_id


if __name__ == "__main__":
    # Quick test to make sure it works
    result = read_barcode()
    print(f"\nScanned ID: {result}")