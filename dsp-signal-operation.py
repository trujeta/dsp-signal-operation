import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Genera una señal senoidal con parámetros definidos
def generate_signal(length=20, amp=1, freq=1, phase=0):
    t = np.arange(length)# Vector de tiempo
    signal = amp * np.sin(2 * np.pi * freq * t / length + phase)# Señal 
    return t, signal

# Aplica transformaciones a la señal
def process_signal(t, signal, time_shift=0, time_scale=1, amp_shift=0, amp_scale=1, mirror=False):
    t_new = (t - time_shift) * time_scale # Aplicación de desplazamiento y escalado temporal
    signal_new = (signal + amp_shift) * amp_scale  # Aplicación de desplazamiento y escalado de amplitud
    if mirror:
        t_new = -t_new[::-1] # Invierte el eje del tiempo si se selecciona "mirror"
        signal_new = signal_new[::-1] # Invierte la señal
    return t_new, signal_new

# Calcula la correlación normalizada entre dos señales
def correlation(sig1, sig2):
    return np.correlate(sig1 - np.mean(sig1), sig2 - np.mean(sig2), mode='full') / (np.std(sig1) * np.std(sig2) * len(sig1))

# Función para calcular la convolución de dos señales
def convolution():
    global ax3
    
    # Procesa ambas señales aplicando las transformaciones definidas en la interfaz
    _, sig1_proc = process_signal(*generate_signal(), int(vars_dict['Time Shift 1'].get()), float(vars_dict['Time Scale 1'].get()), float(vars_dict['Amplitude Shift 1'].get()), float(vars_dict['Amplitude Scale 1'].get()), vars_dict['Mirror 1'].get())
    _, sig2_proc = process_signal(*generate_signal(), int(vars_dict['Time Shift 2'].get()), float(vars_dict['Time Scale 2'].get()), float(vars_dict['Amplitude Shift 2'].get()), float(vars_dict['Amplitude Scale 2'].get()), vars_dict['Mirror 2'].get())
    
      # Calcula la convolución entre ambas señales
    conv_result = np.convolve(sig1_proc, sig2_proc, mode='full')
    
    # Limpia y actualiza el gráfico
    ax3.clear()
    ax3.stem(conv_result, linefmt='g-', markerfmt='go', basefmt='g-', label='Convolution', use_line_collection=True)
    ax3.legend()
    ax3.set_title('Convolution')
    canvas.draw()

    # Función para calcular la autocorrelación de la señal 1
def autocorrelation1():
    global ax3
    
     # Procesa la señal 1 aplicando las transformaciones
    _, sig1_proc = process_signal(*generate_signal(), int(vars_dict['Time Shift 1'].get()), float(vars_dict['Time Scale 1'].get()), float(vars_dict['Amplitude Shift 1'].get()), float(vars_dict['Amplitude Scale 1'].get()), vars_dict['Mirror 1'].get())
    
    # Calcula la autocorrelación y la normaliza
    auto_corr = np.correlate(sig1_proc, sig1_proc, mode='full')
    auto_corr /= np.max(np.abs(auto_corr)) # Normalización
    
     # Limpia y actualiza el gráfico
    ax3.clear()
    ax3.stem(auto_corr, linefmt='m-', markerfmt='mo', basefmt='m-', label='Autocorrelation 1', use_line_collection=True)
    ax3.legend()
    ax3.set_title('Autocorrelation Signal 1')
    canvas.draw()

    # Función para calcular la autocorrelación de la señal 2
def autocorrelation2():
    global ax3
    
    # Procesa la señal 2 aplicando las transformaciones
    _, sig2_proc = process_signal(*generate_signal(), int(vars_dict['Time Shift 2'].get()), float(vars_dict['Time Scale 2'].get()), float(vars_dict['Amplitude Shift 2'].get()), float(vars_dict['Amplitude Scale 2'].get()), vars_dict['Mirror 2'].get())
    
     # Calcula la autocorrelación y la normaliza
    auto_corr = np.correlate(sig2_proc, sig2_proc, mode='full')
    auto_corr /= np.max(np.abs(auto_corr))
    
    # Limpia y actualiza el gráfico
    ax3.clear()
    ax3.stem(auto_corr, linefmt='c-', markerfmt='co', basefmt='c-', label='Autocorrelation 2', use_line_collection=True)
    ax3.legend()
    ax3.set_title('Autocorrelation Signal 2')
    canvas.draw()

    # Función para calcular la correlación cruzada entre dos señales
def cross_correlation():
    global ax3
    
    # Procesa ambas señales aplicando las transformaciones
    _, sig1_proc = process_signal(*generate_signal(), int(vars_dict['Time Shift 1'].get()), float(vars_dict['Time Scale 1'].get()), float(vars_dict['Amplitude Shift 1'].get()), float(vars_dict['Amplitude Scale 1'].get()), vars_dict['Mirror 1'].get())
    _, sig2_proc = process_signal(*generate_signal(), int(vars_dict['Time Shift 2'].get()), float(vars_dict['Time Scale 2'].get()), float(vars_dict['Amplitude Shift 2'].get()), float(vars_dict['Amplitude Scale 2'].get()), vars_dict['Mirror 2'].get())
    
     # Calcula la correlación cruzada y la normaliza
    cross_corr = np.correlate(sig1_proc, sig2_proc, mode='full')
    cross_corr /= np.max(np.abs(cross_corr))
    
    # Limpia y actualiza el gráfico
    ax3.clear()
    ax3.stem(cross_corr, linefmt='y-', markerfmt='yo', basefmt='y-', label='Cross-correlation 1 & 2', use_line_collection=True)
    ax3.legend()
    ax3.set_title('Cross-correlation')
    canvas.draw()

    
    # Actualiza las gráficas de las señales
def update_plot():
    try:
        t1, sig1 = generate_signal()
        t2, sig2 = generate_signal()
        
        global t1_proc, sig1_proc, t2_proc, sig2_proc
        t1_proc, sig1_proc = process_signal(t1, sig1, int(vars_dict['Time Shift 1'].get()), float(vars_dict['Time Scale 1'].get()), float(vars_dict['Amplitude Shift 1'].get()), float(vars_dict['Amplitude Scale 1'].get()), vars_dict['Mirror 1'].get())
        t2_proc, sig2_proc = process_signal(t2, sig2, int(vars_dict['Time Shift 2'].get()), float(vars_dict['Time Scale 2'].get()), float(vars_dict['Amplitude Shift 2'].get()), float(vars_dict['Amplitude Scale 2'].get()), vars_dict['Mirror 2'].get())
        
        ax1.clear()
        ax2.clear()
        
        ax1.stem(t1, sig1, linefmt='b-', markerfmt='bo', basefmt='b-', label='Original Signal 1', use_line_collection=True)
        ax1.stem(t1_proc, sig1_proc, linefmt='r--', markerfmt='ro', basefmt='r-', label='Processed Signal 1', use_line_collection=True)
        ax1.legend()
        ax1.set_title('Signal 1')
        
        ax2.stem(t2, sig2, linefmt='b-', markerfmt='bo', basefmt='b-', label='Original Signal 2', use_line_collection=True)
        ax2.stem(t2_proc, sig2_proc, linefmt='r--', markerfmt='ro', basefmt='r-', label='Processed Signal 2', use_line_collection=True)
        ax2.legend()
        ax2.set_title('Signal 2')
        
        canvas.draw()
    except ValueError:
        pass

root = tk.Tk()
root.title("Signal Processing App")

frame = ttk.Frame(root)
frame.pack(side=tk.LEFT, padx=20, pady=20)

params = [('Time Shift 1', '0'), ('Time Scale 1', '1'), ('Amplitude Shift 1', '0'), ('Amplitude Scale 1', '1'), ('Mirror 1', False),
          ('Time Shift 2', '0'), ('Time Scale 2', '1'), ('Amplitude Shift 2', '0'), ('Amplitude Scale 2', '1'), ('Mirror 2', False)]
vars_dict = {}

for text, default in params:
    ttk.Label(frame, text=text).pack()
    if isinstance(default, bool):
        vars_dict[text] = tk.BooleanVar(value=default)
        ttk.Checkbutton(frame, variable=vars_dict[text], command=update_plot).pack()
    else:
        vars_dict[text] = tk.StringVar(value=default)
        ttk.Entry(frame, textvariable=vars_dict[text]).pack()

buttons = [("Update", update_plot), ("Convolution", convolution), ("Autocorrelation 1", autocorrelation1),
           ("Autocorrelation 2", autocorrelation2), ("Cross-correlation", cross_correlation)]

for text, command in buttons:
    ttk.Button(frame, text=text, command=command).pack()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 9))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

update_plot()
root.mainloop()