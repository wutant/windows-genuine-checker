import ctypes
from pathlib import Path
import subprocess
import sys
import platform
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


APP_TITLE = "Windows Genuine Checker"
WINDOWS_PRIVATE_FONT = 0x10
FONT_CANDIDATES = (
    ("assets", "fonts", "Sarabun-Regular.ttf"),
    ("assets", "fonts", "Sarabun-Bold.ttf"),
)
ICON_ICO_PATH = ("assets", "icons", "app-icon.ico")
ICON_PNG_PATH = ("assets", "icons", "app-icon.png")


def resource_path(*parts):
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_dir.joinpath(*parts)


def register_private_font(font_path):
    if platform.system().lower() != "windows":
        return False

    try:
        added_count = ctypes.windll.gdi32.AddFontResourceExW(
            str(font_path),
            WINDOWS_PRIVATE_FONT,
            0
        )
        return added_count > 0
    except Exception:
        return False


def unregister_private_font(font_path):
    if platform.system().lower() != "windows":
        return

    try:
        ctypes.windll.gdi32.RemoveFontResourceExW(
            str(font_path),
            WINDOWS_PRIVATE_FONT,
            0
        )
    except Exception:
        pass


def register_bundled_fonts():
    registered = []
    for parts in FONT_CANDIDATES:
        font_path = resource_path(*parts)
        if font_path.exists() and register_private_font(font_path):
            registered.append(font_path)
    return registered


def run_command(cmd):
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            encoding="utf-8",
            errors="replace"
        )
        output = (completed.stdout or "") + ("\n" + completed.stderr if completed.stderr else "")
        return completed.returncode, output.strip()
    except Exception as e:
        return 1, str(e)


class App(tk.Tk):
    def __init__(self):
        self._registered_fonts = register_bundled_fonts()
        super().__init__()
        self._icon_image = None
        self.title(APP_TITLE)
        self.geometry("940x720")
        self.minsize(840, 620)

        self._configure_fonts()
        self._configure_window_icon()
        self.status_var = tk.StringVar(value="พร้อมตรวจสอบ")
        self.summary_var = tk.StringVar(value="กดปุ่ม 'ตรวจสอบ' เพื่อเริ่ม")

        self._build_ui()

    def _configure_fonts(self):
        self.ui_font_family = self._resolve_font_family(
            "TH Sarabun New",
            "Sarabun",
            "Leelawadee UI",
            "Segoe UI"
        )

        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family=self.ui_font_family, size=14)
        tkfont.nametofont("TkTextFont").configure(family=self.ui_font_family, size=14)
        tkfont.nametofont("TkMenuFont").configure(family=self.ui_font_family, size=13)
        tkfont.nametofont("TkHeadingFont").configure(family=self.ui_font_family, size=14, weight="bold")
        tkfont.nametofont("TkFixedFont").configure(family=self.ui_font_family, size=13)

        self.title_font = tkfont.Font(family=self.ui_font_family, size=24, weight="bold")
        self.subtitle_font = tkfont.Font(family=self.ui_font_family, size=15)
        self.summary_font = tkfont.Font(family=self.ui_font_family, size=17, weight="bold")
        self.output_font = tkfont.Font(family=self.ui_font_family, size=14)

        style = ttk.Style(self)
        style.configure(".", font=default_font)
        style.configure("TLabelframe.Label", font=(self.ui_font_family, 14, "bold"))
        style.configure("TButton", padding=(14, 8))

    def _resolve_font_family(self, *candidates):
        available_families = {name.casefold(): name for name in tkfont.families(self)}
        for candidate in candidates:
            match = available_families.get(candidate.casefold())
            if match:
                return match
        return tkfont.nametofont("TkDefaultFont").actual("family")

    def _configure_window_icon(self):
        ico_path = resource_path(*ICON_ICO_PATH)
        png_path = resource_path(*ICON_PNG_PATH)

        if ico_path.exists():
            try:
                self.iconbitmap(str(ico_path))
                return
            except Exception:
                pass

        if png_path.exists():
            try:
                self._icon_image = tk.PhotoImage(file=str(png_path))
                self.iconphoto(True, self._icon_image)
            except Exception:
                self._icon_image = None

    def _build_ui(self):
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text=APP_TITLE, font=self.title_font)
        title.pack(anchor="w")

        subtitle = ttk.Label(
            frame,
            text="ตรวจสถานะ Activation ของ Windows โดยไม่ต้อง Run as administrator",
            font=self.subtitle_font
        )
        subtitle.pack(anchor="w", pady=(4, 14))

        info = ttk.Label(
            frame,
            text=(
                "หลักการตรวจ:\n"
                "1) ใช้ slmgr /xpr เพื่อตรวจว่า Permanent หรือมีวันหมดอายุ\n"
                "2) ใช้ slmgr /dli เพื่อดูประเภทไลเซนส์ เช่น Retail, OEM, KMS\n"
                "3) สรุปผลเบื้องต้นว่าแท้ / น่าสงสัย / ยังไม่ activated"
            ),
            justify="left",
            wraplength=820
        )
        info.pack(anchor="w", pady=(0, 14))

        btn_row = ttk.Frame(frame)
        btn_row.pack(fill="x", pady=(0, 12))

        ttk.Button(btn_row, text="ตรวจสอบ", command=self.check_windows).pack(side="left")
        ttk.Button(btn_row, text="คัดลอกผลลัพธ์", command=self.copy_output).pack(side="left", padx=8)
        ttk.Button(btn_row, text="ล้างผลลัพธ์", command=self.clear_output).pack(side="left")

        summary_box = ttk.LabelFrame(frame, text="สรุปผล", padding=12)
        summary_box.pack(fill="x", pady=(0, 12))

        ttk.Label(
            summary_box,
            textvariable=self.summary_var,
            font=self.summary_font,
            justify="left",
            wraplength=780
        ).pack(anchor="w")
        ttk.Label(summary_box, textvariable=self.status_var, justify="left", wraplength=780).pack(anchor="w", pady=(6, 0))

        output_box = ttk.LabelFrame(frame, text="รายละเอียด", padding=8)
        output_box.pack(fill="both", expand=True)

        self.output = ScrolledText(output_box, wrap="word", font=self.output_font)
        self.output.pack(fill="both", expand=True)

        self._write_intro()

    def _write_intro(self):
        self.output.delete("1.0", "end")
        self.output.insert("end", "ระบบพร้อมใช้งาน\n")
        self.output.insert("end", f"Python: {sys.version.split()[0]}\n")
        self.output.insert("end", f"OS: {platform.platform()}\n\n")
        self.output.insert("end", "หมายเหตุ:\n")
        self.output.insert("end", "- โปรแกรมนี้พยายามอ่านข้อมูลแบบไม่ใช้สิทธิ์ admin\n")
        self.output.insert("end", "- ถ้าเครื่องถูกบล็อกคำสั่ง slmgr โดยนโยบายองค์กร ผลลัพธ์อาจไม่ครบ\n")
        self.output.insert("end", "- KMS ขององค์กรจริงอาจเป็นของถูกต้องตามสิทธิ์องค์กรได้\n")

    def clear_output(self):
        self.summary_var.set("กดปุ่ม 'ตรวจสอบ' เพื่อเริ่ม")
        self.status_var.set("พร้อมตรวจสอบ")
        self._write_intro()

    def copy_output(self):
        text = self.output.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo(APP_TITLE, "ไม่มีข้อมูลให้คัดลอก")
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo(APP_TITLE, "คัดลอกผลลัพธ์แล้ว")

    def check_windows(self):
        if platform.system().lower() != "windows":
            self.summary_var.set("โปรแกรมนี้ใช้ตรวจบน Windows เท่านั้น")
            self.status_var.set("ระบบปัจจุบันไม่ใช่ Windows")
            return

        self.output.delete("1.0", "end")
        self.output.insert("end", "กำลังตรวจสอบ...\n\n")
        self.update_idletasks()

        commands = {
            "Activation Expiry": r'cscript //nologo %windir%\system32\slmgr.vbs /xpr',
            "License Info": r'cscript //nologo %windir%\system32\slmgr.vbs /dli',
        }

        results = {}
        for name, cmd in commands.items():
            code, out = run_command(cmd)
            results[name] = {"code": code, "output": out}
            self.output.insert("end", f"===== {name} =====\n")
            self.output.insert("end", out + "\n\n")

        verdict, detail = self._analyze(results)
        self.summary_var.set(verdict)
        self.status_var.set(detail)

        self.output.insert("end", "===== วิเคราะห์ =====\n")
        self.output.insert("end", verdict + "\n")
        self.output.insert("end", detail + "\n")

    def _analyze(self, results):
        xpr = results.get("Activation Expiry", {}).get("output", "").lower()
        dli = results.get("License Info", {}).get("output", "").lower()

        if not xpr and not dli:
            return "อ่านข้อมูลไม่ได้", "คำสั่งระบบไม่ตอบกลับ หรือถูกบล็อกโดยนโยบายของเครื่อง"

        is_permanent = "permanent" in xpr or "permanently activated" in xpr
        has_expiry = "expire" in xpr or "expires" in xpr or "will expire" in xpr
        is_kms = "kms" in dli or "volume_kmsclient" in dli
        is_retail = "retail" in dli
        is_oem = "oem" in dli
        is_not_activated = "notification" in dli or "unlicensed" in dli or "not activated" in xpr

        if is_not_activated:
            return "ไม่ activated", "สถานะนี้ถือว่ายังไม่พร้อมใช้งานแบบลิขสิทธิ์สมบูรณ์"

        if is_permanent and (is_retail or is_oem) and not is_kms:
            return "มีแนวโน้มว่าเป็น Windows แท้", "พบ Permanent activation และประเภทไลเซนส์เป็น Retail/OEM"

        if is_kms and has_expiry:
            return "น่าสงสัยหรือเป็น KMS", "ถ้าเป็นเครื่ององค์กรอาจปกติ แต่ถ้าเป็นเครื่องส่วนตัวควรตรวจสอบเพิ่ม"

        if is_kms and is_permanent:
            return "เป็น KMS หรือระบบองค์กร", "อาจถูกต้องตามสิทธิ์องค์กร แต่ไม่ใช่รูปแบบ Retail/OEM ทั่วไป"

        if is_permanent:
            return "Activated แบบถาวร", "แต่ยังระบุความแท้ 100% ไม่ได้ ควรดูที่แหล่งที่มาของไลเซนส์ร่วมด้วย"

        if has_expiry:
            return "Activation มีวันหมดอายุ", "มักเป็น Volume/KMS และควรตรวจสอบสิทธิ์การใช้งานเพิ่มเติม"

        return "สรุปไม่ชัดเจน", "ควรตรวจผลลัพธ์ดิบด้านล่าง หรือส่งผลลัพธ์ให้ผมช่วยแปลได้"

    def destroy(self):
        for font_path in self._registered_fonts:
            unregister_private_font(font_path)
        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
