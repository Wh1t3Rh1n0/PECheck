# PECheck

A tool to verify and create PE Checksums for Portable Executable (PE) files.

It's a good idea to run this on any EXE malware payloads (or any other EXE files) you create, since the lack of a valid PE checksum increases the likelihood that defensive products will classify the file as malware.


## Installation

```
pip3 install -r requirements.txt
```


## Usage

```
python3 ./PECheck.py <Target PE (EXE) File> [Optional -y to skip prompts]
```


## Example

Using [Bginfo.exe](https://live.sysinternals.com/Bginfo.exe) from Microsoft's SysInternals suite as an example...

Here I first verify that the file, in its original state, has a valid PE checksum:

```
$ ./PECheck.py Bginfo.exe
Checking the PE checksum of Bginfo.exe
GOOD CHECKSUM DETECTED on Bginfo.exe!
```

Next, I'll do a quick and simple "obfuscation" of the file by appending roughly 100 MB of random data to the end of the file. While this will change the file's (overall) checksum and frustrate scanning by some AV/EDR products, it also breaks the file's PE checksum.

```
$ dd if=/dev/urandom bs=1024 count=102400 >> Bginfo.exe
102400+0 records in
102400+0 records out
104857600 bytes (105 MB, 100 MiB) copied, 19.3398 s, 5.4 MB/s
```

Now I'll run `PECheck.py` on the file again. This time, PECheck will:
1. Identify that the file's PE checksum is invalid,
2. Prompt the user to generate a new PE checksum for the file,
3. Write the new PE checksum to the file,
4. Check the PE checksum again to confirm that it was written to the file successfully.

```
$ ./PECheck.py Bginfo.exe
Checking the PE checksum of Bginfo.exe
ERROR: Checksum is missing or invalid!

Write new checksum to Bginfo.exe (y/n)? y
Writing new checksum to Bginfo.exe...
Done writing new checksum!

Verifying that PE checksum was successfully written...
SUCCESS! New PE checksum written to Bginfo.exe and verified!
```


## References

- GitHub issue for PyInstaller that initially brought my attention to the PE header and its effects on AV scores in VirusTotal: https://github.com/pyinstaller/pyinstaller/issues/5579