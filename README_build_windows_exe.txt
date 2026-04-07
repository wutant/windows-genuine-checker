Windows Genuine Checker - วิธีสร้าง EXE บน Windows

ไฟล์ในชุดนี้:
- windows_genuine_checker.py
- build_exe_pyinstaller.bat

วิธีใช้:
1) ติดตั้ง Python บน Windows
2) วาง 2 ไฟล์นี้ไว้โฟลเดอร์เดียวกัน
3) ดับเบิลคลิก build_exe_pyinstaller.bat
4) รอจนจบ
5) ไฟล์ EXE จะอยู่ที่ dist\WindowsGenuineChecker.exe

หมายเหตุ:
- ตอนนี้ผมสร้างไฟล์ EXE ให้ตรงนี้ไม่ได้ เพราะสภาพแวดล้อมที่กำลังใช้ไม่ใช่ Windows
- แต่สคริปต์ build ที่ให้ไป สามารถนำไปรันบนเครื่อง Windows เพื่อสร้าง .exe ได้ทันที
- โปรแกรมถูกออกแบบให้ตรวจโดยไม่ต้อง Run as administrator
