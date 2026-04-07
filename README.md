# Windows Genuine Checker

โปรแกรม GUI ขนาดเล็กสำหรับตรวจสถานะการ Activate ของ Windows แบบไม่ต้องเปิด `Run as administrator`

ตัวโปรแกรมใช้คำสั่งของระบบ Windows เพื่อสรุปผลเบื้องต้นว่าเครื่องอยู่ในสถานะใด เช่น

- `มีแนวโน้มว่าเป็น Windows แท้`
- `น่าสงสัยหรือเป็น KMS`
- `ไม่ activated`
- `สรุปไม่ชัดเจน`

ฟอนต์ที่ใช้ในแอปคือ `Sarabun` และถูก bundle ไว้ในโปรเจกต์แล้ว เพื่อให้ใช้งานภาษาไทยแบบ offline ได้แม้เครื่องปลายทางไม่มีฟอนต์นี้ติดตั้ง

## หลักการตรวจ

โปรแกรมจะเรียกคำสั่งต่อไปนี้

- `slmgr /xpr` เพื่อตรวจว่า activation เป็นแบบถาวรหรือมีวันหมดอายุ
- `slmgr /dli` เพื่อดูข้อมูล license เช่น `Retail`, `OEM`, `KMS`

จากนั้นจึงวิเคราะห์และแสดงผลสรุปในหน้าต่างโปรแกรม

## ไฟล์สำคัญในโปรเจกต์

- `windows_genuine_checker.py` ตัวโปรแกรมหลัก
- `build_exe_pyinstaller.bat` สคริปต์ build `.exe` บน Windows
- `.github/workflows/build-exe.yml` GitHub Actions สำหรับ build และ release `.exe`
- `.releaserc.json` config ของ `semantic-release`
- `assets/fonts/` ฟอนต์ Sarabun ที่ bundle มากับแอป

## วิธีรันจาก Python

เหมาะสำหรับทดสอบหรือใช้งานจาก source code โดยตรง

1. ติดตั้ง Python 3.11 หรือใหม่กว่า บน Windows
2. เปิด Command Prompt หรือ PowerShell ในโฟลเดอร์โปรเจกต์
3. รันคำสั่งนี้

```bash
python windows_genuine_checker.py
```

## วิธี build เป็น EXE บนเครื่อง Windows

มี 2 วิธี

### วิธีที่ 1: ใช้ไฟล์ batch

1. เปิดไฟล์ `build_exe_pyinstaller.bat`
2. รอให้ระบบติดตั้ง `pyinstaller` และ build เสร็จ
3. ไฟล์ที่ได้จะอยู่ที่

```text
dist\WindowsGenuineChecker.exe
```

### วิธีที่ 2: ใช้คำสั่งตรง

```bash
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name WindowsGenuineChecker --add-data "assets/fonts/Sarabun-Regular.ttf;assets/fonts" --add-data "assets/fonts/Sarabun-Bold.ttf;assets/fonts" windows_genuine_checker.py
```

ไฟล์ที่ได้จะอยู่ที่

```text
dist\WindowsGenuineChecker.exe
```

หมายเหตุ:

- ตัว `.exe` จะ bundle ฟอนต์ `Sarabun` ไปด้วย
- ไม่ต้องดาวน์โหลดฟอนต์เพิ่มตอนใช้งาน

## วิธี build และ release ด้วย GitHub Actions

repo นี้มี workflow ที่ทำ 2 อย่างในรอบเดียวกันเมื่อมี `push` เข้า `main`

- build `WindowsGenuineChecker.exe`
- ให้ `semantic-release` สร้าง GitHub Release และแนบไฟล์ `.exe` เข้า release นั้น

ไฟล์ workflow:

```text
.github/workflows/build-exe.yml
```

ขั้นตอนใช้งาน:

1. push โค้ดขึ้น branch `main`
2. workflow จะ build ไฟล์ `WindowsGenuineChecker.exe`
3. artifact ชื่อ `exe` จะถูกเก็บไว้ใน workflow run
4. ถ้า commit message เข้ากฎของ `semantic-release` ระบบจะสร้าง GitHub Release ใหม่
5. ไฟล์ `WindowsGenuineChecker.exe` จะถูกแนบเข้า release ที่เพิ่งถูกสร้าง

## รูปแบบ commit ที่ทำให้เกิด release

`semantic-release` จะออก release จากข้อความ commit เป็นหลัก ดังนั้นควรใช้ Conventional Commits

ตัวอย่างที่จะทำให้เกิด release:

- `feat: add activation details panel`
- `fix: handle empty slmgr output`
- `feat!: change verdict logic`

แนวทางโดยย่อ:

- `fix:` จะออก patch release
- `feat:` จะออก minor release
- `!` หรือ `BREAKING CHANGE:` จะออก major release

ถ้าเป็น commit แบบทั่วไปที่ไม่เข้า pattern นี้ เช่น `update readme` หรือ `misc changes` ระบบจะไม่สร้าง release ใหม่

## ข้อจำกัดที่ควรรู้

- โปรแกรมนี้เป็นการวิเคราะห์เบื้องต้นจากผลลัพธ์ของ `slmgr`
- ไม่สามารถยืนยันความแท้ได้ 100% จากผลลัพธ์เพียง 2 คำสั่ง
- ถ้าเครื่องอยู่ในองค์กร การใช้ `KMS` อาจเป็นเรื่องปกติและถูกต้องตามสิทธิ์
- ถ้าเครื่องถูกบล็อกการเรียก `slmgr` โดยนโยบายองค์กร ผลลัพธ์อาจไม่ครบ
- โปรแกรมนี้ออกแบบมาให้ใช้บน Windows เท่านั้น

## หมายเหตุ

ถ้าต้องการแจกจ่ายให้ผู้ใช้งานทั่วไป แนะนำให้ใช้ไฟล์ `.exe` ที่ build จาก GitHub Actions หรือจากเครื่อง Windows จริง เพราะการสร้าง executable ของ Windows ต้อง build บนสภาพแวดล้อม Windows
