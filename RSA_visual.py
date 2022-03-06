import tkinter as tk
import threading as th
import multiprocessing as mp
import random
import time
from math import gcd


def spec_calculate(x, modulas):
    return ((x % modulas) * (x % modulas)) % modulas


def fast_modular_calculation(n, m, modulas):
    m = str(bin(m))  # convert decimal to binomial
    li = list()

    for i in range(2, len(m)):
        li.append(int(m[i]))

    li.reverse()

    temp = n % modulas
    res = 1

    for i in li:  # 定理2
        if i == 1:
            res *= temp
        temp = spec_calculate(n, modulas)
        n = temp

    return res % modulas


class RSA:
    def __init__(self, master):

        pqlow = 10 ** 16
        pqhigh = 10 ** 17
        elow = 10 ** 8
        ehigh = 10 ** 9

        que = mp.Queue()
        process1 = mp.Process(target=self.generateP, args=(que, pqlow, pqhigh))
        process2 = mp.Process(target=self.generateQ, args=(que, pqlow, pqhigh))

        process1.start()
        process2.start()

        process1.join()
        process2.join()

        P = que.get()
        Q = que.get()

        n = P * Q
        Euler = (P - 1) * (Q - 1)

        e = self.generateE(Euler, elow, ehigh)
        x = self.ext_euclid(e, Euler)
        d = self.fixD(x, Euler)

        e, d = d, e

        del Euler, P, Q

        encode_frame(master, n, e, d)

    def is_prime_num(self, num):
        if num % 2 == 0:
            return False
        for i in range(2, int(num ** 0.5 + 1), 2):
            if num % (i + 1) == 0:
                return False

        return True

    def generateP(self, que, pqlow, pqhigh):  # Generate prime number p
        random.seed(time.time())
        p = random.randint(pqlow, pqhigh)  # size of P

        while True:
            if self.is_prime_num(p):
                break
            p += 1

        que.put(p)

    def generateQ(self, que, pqlow, pqhigh):  # Generate prime number q
        random.seed(time.time())
        q = random.randint(pqlow, pqhigh)  # size of Q

        while True:
            if self.is_prime_num(q):
                break
            q -= 1

        que.put(q)

    def generateE(self, Euler, elow, ehigh):
        random.seed(time.time())
        e = random.randint(elow, ehigh)

        while True:
            if gcd(e, Euler) == 1:
                return e
            e += 1

    def ext_euclid(self, a, b):  # i don't know why but it is correct
        old_s, s = 1, 0
        old_t, t = 0, 1
        old_r, r = a, b
        if b == 0:
            return 1, 0, a
        else:
            while(r != 0):
                q = old_r // r
                old_r, r = r, old_r - q * r
                old_s, s = s, old_s - q * s
                old_t, t = t, old_t - q * t

        return old_s

    def fixD(self, d, Euler):
        while True:
            if d < 0:
                d += Euler
            else:
                return d


class base_window:
    def __init__(self, master):
        self.master = master
        self.master.config(background="#afdfff")
        self.master.title("RSA algorithm")
        self.master.geometry("560x560")
        self.master.resizable(False, False)

        init_interface(self.master)


class init_interface:
    def __init__(self, master):

        self.master = master

        self.openning = tk.Label(
            text="\n\n\nThis is RSA encoding system\n\nPlease choose a mode",
            background="#afdfff",
            font=("Microsoft YaHei Light", 20)
        )
        self.openning.place(x=65, y=10)

        self.Encode = tk.Button(
            text="Encode",
            command=self.encode,
            width=15,
            height=3,
            font=16,
            background="#afdfff",
            activebackground="#90c0e0",
            relief="solid",
            borderwidth=1
        )
        self.Encode.place(x=50, y=380)

        self.Decode = tk.Button(
            text="Decode",
            command=self.decode,
            width=15,
            height=3,
            font=16,
            background="#afdfff",
            activebackground="#90c0e0",
            relief="solid",
            borderwidth=1
        )
        self.Decode.place(x=305, y=380)

        self.Encode.bind("<Enter>", self.enter_encode_button)
        self.Encode.bind("<Leave>", self.leave_encode_button)
        self.Decode.bind("<Enter>", self.enter_decode_button)
        self.Decode.bind("<Leave>", self.leave_decode_button)

    def encode(self):
        self.Encode.destroy()
        self.Decode.destroy()
        self.openning.destroy()

        global running_loading
        running_loading = th.Event()
        running_loading.set()

        thread1 = th.Thread(target=loading_frame)
        thread2 = th.Thread(target=RSA, args=(self.master,))

        thread1.start()
        thread2.start()

    def decode(self):
        self.Encode.destroy()
        self.Decode.destroy()
        self.openning.destroy()
        decode_frame(self.master)

    def enter_encode_button(self, event):
        self.Encode.config(background="#d8efff")

    def leave_encode_button(self, event):
        self.Encode.config(background="#afdfff")

    def enter_decode_button(self, event):
        self.Decode.config(background="#d8efff")

    def leave_decode_button(self, event):
        self.Decode.config(background="#afdfff")


class encode_frame:
    def __init__(self, master, n, e, d):

        running_loading.clear()
        time.sleep(0.5)

        self.master = master

        self.n = n
        self.e = e
        self.d = d

        self.description = tk.Label(
            text="\nPlease input data\n",
            background="#afdfff",
            font=("Microsoft YaHei Light", 30)
        )
        self.description.pack()

        self.entry_encode = tk.Entry(
            width=40, font=("Microsoft YaHei Light", 12))
        self.entry_encode.pack()

        self.space = tk.Label(text="\n\n", background="#afdfff")
        self.space.pack()

        self.OK = tk.Button(
            text="OK",
            command=self.start_encode,
            width=12,
            height=3,
            font=12,
            background="#afdfff",
            activebackground="#90c0e0",
            relief="solid",
            borderwidth=1
        )
        self.OK.place(x=200, y=400)

        self.OK.bind("<Enter>", self.enter_OK_button)
        self.OK.bind("<Leave>", self.leave_OK_button)

    def enter_OK_button(self, event):
        self.OK.config(background="#d8efff")

    def leave_OK_button(self, event):
        self.OK.config(background="#afdfff")

    def start_encode(self):
        code = self.entry_encode.get()

        if code == "":
            self.description.destroy()
            self.space.destroy()
            self.entry_encode.destroy()
            self.OK.destroy()
            error_frame(self.master)
        else:
            self.stri = str()
            for i in code:
                ch = ord(i)
                res = fast_modular_calculation(ch, self.e, self.n)
                self.stri += hex(res)
                self.stri += "\n"

            self.description.config(
                text="Result after encode:\n", font=("Microsoft YaHei Light", 22))
            self.space.destroy()
            self.entry_encode.destroy()
            self.OK.destroy()

            self.result_after_en = tk.Label(
                text=self.stri, background="#afdfff")
            self.result_after_en.pack()

            self.private_key_des = tk.Label(
                text="Private Key:",
                background="#afdfff",
                font=("Microsoft YaHei Light", 18)
            )
            self.private_key_des.pack()

            self.pv_key = str(hex(self.n)) + str(hex(self.d))

            self.private_key = tk.Label(
                text=self.pv_key,
                background="#afdfff"
            )
            self.private_key.pack()

            self.write_button = tk.Button(
                text="Write into\nnotepad",
                command=self.store_data,
                width=13,
                height=3,
                font=12,
                background="#afdfff",
                activebackground="#90c0e0",
                relief="solid",
                borderwidth=1
            )
            self.write_button.place(x=65, y=450)

            self.back_button = tk.Button(
                text="Back to menu",
                command=self.back_menu,
                width=13,
                height=3,
                font=12,
                background="#afdfff",
                activebackground="#90c0e0",
                relief="solid",
                borderwidth=1
            )
            self.back_button.place(x=320, y=450)
            self.back_button.bind("<Enter>", self.enter_b_btn)
            self.back_button.bind("<Leave>", self.leave_b_btn)
            self.write_button.bind("<Enter>", self.enter_write_btn)
            self.write_button.bind("<Leave>", self.leave_write_btn)

    def enter_b_btn(self, event):
        self.back_button.config(background="#d8efff")

    def leave_b_btn(self, event):
        self.back_button.config(background="#afdfff")

    def enter_write_btn(self, event):
        self.write_button.config(background="#d8efff")

    def leave_write_btn(self, event):
        self.write_button.config(background="#afdfff")

    def store_data(self):
        self.write_button.destroy()
        with open("RSA_code.txt", "a") as txt:
            txt.write("Result after encode:\n\n")
            txt.write(self.stri)
            txt.write("\n")
            txt.write("Private key:\n\n")
            txt.write(self.pv_key)
            txt.write("\n\n")

        self.hint = tk.Label(
            text="Done.\nIt has been stored under\nthe same file of this program",
            background="#afdfff",
            font=("Microsoft YaHei", 10)
        )
        self.hint.place(x=40, y=450)

    def back_menu(self):
        self.description.destroy()
        self.result_after_en.destroy()
        self.back_button.destroy()
        self.private_key_des.destroy()
        self.private_key.destroy()
        try:
            self.write_button.destroy()
        except:
            pass
        try:
            self.hint.destroy()
        except:
            pass

        init_interface(self.master)


class decode_frame:
    def __init__(self, master):

        self.master = master

        self.space = tk.Label(text="\n\n", background="#afdfff")
        self.space.grid(row=0, column=1)

        self.input_code = tk.Label(
            text="  input code:",
            background="#afdfff",
            font=("Microsoft YaHei Light", 15)
        )
        self.input_code.grid(row=1, column=1)

        self.input_key = tk.Label(
            text="  input key:",
            background="#afdfff",
            font=("Microsoft YaHei Light", 15)
        )
        self.input_key.grid(row=2, column=1)

        self.entry_code = tk.Entry(
            font=("Microsoft YaHei Light", 12), width=35)
        self.entry_code.grid(row=1, column=2)

        self.entry_key = tk.Entry(font=("Microsoft YaHei Light", 12), width=35)
        self.entry_key.grid(row=2, column=2)

        self.OK2 = tk.Button(
            text="OK",
            command=self.start_decode,
            width=12,
            height=3,
            font=12,
            background="#afdfff",
            activebackground="#90c0e0",
            relief="solid",
            borderwidth=1
        )
        self.OK2.place(x=200, y=400)

        self.OK2.bind("<Enter>", self.enter_OK2_button)
        self.OK2.bind("<Leave>", self.leave_OK2_button)

    def enter_OK2_button(self, event):
        self.OK2.config(background="#d8efff")

    def leave_OK2_button(self, event):
        self.OK2.config(background="#afdfff")

    def start_decode(self):

        encoded_t = self.entry_code.get()
        key_t = self.entry_key.get()

        self.space.destroy()
        self.input_code.destroy()
        self.input_key.destroy()
        self.entry_code.destroy()
        self.entry_key.destroy()
        self.OK2.destroy()

        encoded_t = encoded_t.split("0x")
        key_t = key_t.split("0x")

        try:
            temp = key_t[1].strip("\n")
            n = int(temp, 16)
            temp = key_t[2].strip("\n")
            d = int(temp, 16)

            result = str()

            for i in encoded_t[1:]:
                temp = i.strip("\n")
                temp = int(temp, 16)
                temp = fast_modular_calculation(temp, d, n)
                result += chr(temp)
                if len(result) % 15 == 0:
                    result += "\n"

            self.result_descrip = tk.Label(
                text="Result:\n",
                background="#afdfff",
                font=("Microsoft YaHei Light", 30)
            )
            self.result_descrip.pack()

            self.result_decode = tk.Label(
                text=result,
                background="white",
                font=("Microsoft YaHei Light", 18)
            )
            self.result_decode.pack()

            self.deco_ba_to_menu = tk.Button(
                text="Back to menu",
                command=self.decode_back_to_menu,
                width=13,
                height=3,
                font=12,
                background="#afdfff",
                activebackground="#90c0e0",
                relief="solid",
                borderwidth=1
            )
            self.deco_ba_to_menu.place(x=200, y=450)

            self.deco_ba_to_menu.bind("<Enter>", self.enter_butn)
            self.deco_ba_to_menu.bind("<Leave>", self.leave_butn)
        except (IndexError, OverflowError):
            error_frame(self.master)

    def enter_butn(self, event):
        self.deco_ba_to_menu.config(background="#d8efff")

    def leave_butn(self, event):
        self.deco_ba_to_menu.config(background="#afdfff")

    def decode_back_to_menu(self):
        self.result_descrip.destroy()
        self.result_decode.destroy()
        self.deco_ba_to_menu.destroy()

        init_interface(self.master)


class loading_frame:
    def __init__(self):

        self.load = tk.Label(
            background="#afdfff",
            font=("Microsoft YaHei Light", 26)
        )
        self.load.pack()

        self.pls_wait = tk.Label(
            text="\nPlease Wait",
            background="#afdfff",
            font=("Microsoft YaHei Light", 18)
        )
        self.pls_wait.pack()

        self.loading1(running_loading)

    def loading1(self, running_loading):
        if running_loading.is_set():
            self.load.config(text="\nloading.")
            window.after(500, self.loading2, running_loading)
        else:
            self.load.destroy()
            self.pls_wait.destroy()

    def loading2(self, running_loading):
        if running_loading.is_set():
            self.load.config(text="\nloading..")
            window.after(500, self.loading3, running_loading)
        else:
            self.load.destroy()
            self.pls_wait.destroy()

    def loading3(self, running_loading):
        if running_loading.is_set():
            self.load.config(text="\nloading...")
            window.after(500, self.loading1, running_loading)
        else:
            self.load.destroy()
            self.pls_wait.destroy()


class error_frame:
    def __init__(self, master):

        self.master = master

        self.err_lab = tk.Label(
            text="\nValue error",
            background="#afdfff",
            font=("Microsoft YaHei Light", 40)
        )
        self.err_lab.pack()

        self.sp = tk.Label(text="\n\n\n\n\n", background="#afdfff")
        self.sp.pack()

        self.err_b_btn = tk.Button(
            text="Back to menu",
            command=self.bt_menu,
            width=13,
            height=3,
            font=12,
            background="#afdfff",
            activebackground="#90c0e0",
            relief="solid",
            borderwidth=1
        )
        self.err_b_btn.pack()
        self.err_b_btn.bind("<Enter>", self.enter_err_b_btn)
        self.err_b_btn.bind("<Leave>", self.leave_err_b_btn)

    def enter_err_b_btn(self, event):
        self.err_b_btn.config(background="#d8efff")

    def leave_err_b_btn(self, event):
        self.err_b_btn.config(background="#afdfff")

    def bt_menu(self):
        self.err_lab.destroy()
        self.sp.destroy()
        self.err_b_btn.destroy()

        init_interface(self.master)


if __name__ == "__main__":

    window = tk.Tk()
    base_window(window)
    window.mainloop()
