import ctypes
from ctypes import windll, Structure, c_ulong
import tkinter as tk


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


def get_pixel_color(x, y):
    hdc = windll.user32.GetDC(0)
    pixel = windll.gdi32.GetPixel(hdc, x, y)
    windll.user32.ReleaseDC(0, hdc)
    return (pixel & 0xff, (pixel >> 8) & 0xff, (pixel >> 16) & 0xff)


def average_color(colors):
    num_colors = len(colors)
    avg_r = sum(color[0] for color in colors) // num_colors
    avg_g = sum(color[1] for color in colors) // num_colors
    avg_b = sum(color[2] for color in colors) // num_colors
    return (avg_r, avg_g, avg_b)


def update_color():
    colors = []
    for offset in range(-2, 2):
        x_color = get_pixel_color(center_x + offset, center_y)  # Yatay eksen
        y_color = get_pixel_color(center_x, center_y + offset)  # Dikey eksen
        colors.append(x_color)
        colors.append(y_color)
    avg_color = average_color(colors)
    print(f"The average color at the center region is RGB{avg_color}")
    color_str = f"#{avg_color[0]:02x}{avg_color[1]:02x}{avg_color[2]:02x}"
    color_box.configure(bg=color_str)
    root.after(1000, update_color)  # 1 saniye sonra tekrar çalıştır


if __name__ == "__main__":
    # Ekran çözünürlüğünü all
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    # Ekranın ortasındaki koordinatları hesapla
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Tkinter arayüzünü başlatt
    root = tk.Tk()
    root.title("Renk Kutusu")

    # Renk kutusunu oluştur
    color_box = tk.Label(root, text="Renk Kutusu", width=40, height=20, bg="white")
    color_box.pack(padx=20, pady=20)

    # İlk güncellemeyi başlat
    update_color()

    # Tkinter ana döngüsünü çalıştır
    root.mainloop()
