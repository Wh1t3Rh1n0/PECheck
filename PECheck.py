#!/usr/bin/env python3

import pefile
import sys


def valid_pe_checksum(filename):
    """Return True if the given PE (EXE) file has a valid PE checksum."""

    pe = pefile.PE(filename)
    return pe.verify_checksum()


def add_pe_checksum(filename):
    """Generate a new PE checksum for a PE file, and write it to the file."""
    pe = pefile.PE(filename)

    pe.OPTIONAL_HEADER.CheckSum = pe.generate_checksum()
    pe.close()
    pe.write(filename)



# Print usage, if appropriate.
if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
    print(f'''
PECheck // 2023-05-09 by Wh1t3Rh1n0
=======    ------------------------

Checks the Portable Executable (PE) checksum of a given EXE file.

If the PE checksum is not valid, this tool will optionally generate a valid
PE checksum, write it to the file, and then check the file again to confirm
that a valid PE checksum is now present.

Usage: {sys.argv[0]} <TARGET PE (EXE) FILE>
    ''')
    exit()


# Check the checksum of the given file.
filename = sys.argv[1]

print(f"Checking the PE checksum of {filename}")
checksum_is_valid = valid_pe_checksum(filename)


# If the checksum is not valid/not present, prompt to add one.
if checksum_is_valid:
    print(f"GOOD CHECKSUM DETECTED on {filename}!")
    exit()
else:
    print(f"ERROR: Checksum is missing or invalid!")

write_new_checksum = input(f"\nWrite new checksum to {filename} (y/n)? ")

if write_new_checksum.lower() != 'y':
    print("Operation canceled by user. Quitting...")
    exit()
else:
    print(f"Writing new checksum to {filename}...")
    add_pe_checksum(filename)
    print(f"Done writing new checksum!")


# Check the checksum of the file again to verify that it was written
# successfully.
print("\nVerifying that PE checksum was successfully written...")

new_checksum_is_valid = valid_pe_checksum(filename)

if not new_checksum_is_valid:
    print("\nERROR: The new checksum was not written to the file for some reason.")
    exit()
elif new_checksum_is_valid:
    print(f"SUCCESS! New PE checksum written to {filename} and verified!")
    exit()


print("ERROR: Something weird happened and I don't know what.")
print("The program was never supposed to reach this point. :(")
