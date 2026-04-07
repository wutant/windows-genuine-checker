# Windows Genuine Checker

โปรแกรม GUI ขนาดเล็กสำหรับตรวจสถานะการ Activate ของ Windows แบบไม่ต้องเปิด `Run as administrator`

ตัวโปรแกรมใช้คำสั่งของระบบ Windows เพื่อสรุปผลเบื้องต้นว่าเครื่องอยู่ในสถานะใด เช่น

- `มีแนวโน้มว่าเป็น Windows แท้`
- `น่าสงสัยหรือเป็น KMS`
- `ไม่ activated`
- `สรุปไม่ชัดเจน`

## หลักการตรวจ

โปรแกรมจะเรียกคำสั่งต่อไปนี้

- `slmgr /xpr` เพื่อตรวจว่า activation เป็นแบบถาวรหรือมีวันหมดอายุ
- `slmgr /dli` เพื่อดูข้อมูล license เช่น `Retail`, `OEM`, `KMS`

จากนั้นจึงวิเคราะห์และแสดงผลสรุปในหน้าต่างโปรแกรม

## ไฟล์สำคัญในโปรเจกต์

- `windows_genuine_checker.py` ตัวโปรแกรมหลัก
- `build_exe_pyinstaller.bat` สคริปต์ build `.exe` บน Windows
- `.github/workflows/build-exe.yml` GitHub Actions สำหรับ build `.exe` อัตโนมัติ

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
python -m PyInstaller --onefile --windowed --name WindowsGenuineChecker windows_genuine_checker.py
```

ไฟล์ที่ได้จะอยู่ที่

```text
dist\WindowsGenuineChecker.exe
```

## วิธี build ด้วย GitHub Actions

repo นี้มี workflow สำหรับ build `.exe` อัตโนมัติเมื่อมี `push`

ไฟล์ workflow:

```text
.github/workflows/build-exe.yml
```

ขั้นตอนใช้งาน:

1. push โค้ดขึ้น GitHub
2. รอ workflow `Build EXE` ทำงานบน `windows-latest`
3. เปิดหน้า workflow run
4. ดาวน์โหลด artifact ชื่อ `exe`
5. ภายใน artifact จะมีไฟล์ `WindowsGenuineChecker.exe`

## ข้อจำกัดที่ควรรู้

- โปรแกรมนี้เป็นการวิเคราะห์เบื้องต้นจากผลลัพธ์ของ `slmgr`
- ไม่สามารถยืนยันความแท้ได้ 100% จากผลลัพธ์เพียง 2 คำสั่ง
- ถ้าเครื่องอยู่ในองค์กร การใช้ `KMS` อาจเป็นเรื่องปกติและถูกต้องตามสิทธิ์
- ถ้าเครื่องถูกบล็อกการเรียก `slmgr` โดยนโยบายองค์กร ผลลัพธ์อาจไม่ครบ
- โปรแกรมนี้ออกแบบมาให้ใช้บน Windows เท่านั้น

## หมายเหตุ

ถ้าต้องการแจกจ่ายให้ผู้ใช้งานทั่วไป แนะนำให้ใช้ไฟล์ `.exe` ที่ build จาก GitHub Actions หรือจากเครื่อง Windows จริง เพราะการสร้าง executable ของ Windows ต้อง build บนสภาพแวดล้อม Windows
