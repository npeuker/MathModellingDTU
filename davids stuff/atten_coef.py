import matplotlib.pyplot as plt


C, H, O = [], [], []
photon_energy = []

def make_plot(y, el, x=photon_energy):
    d = {"Carbon": 6, "Hydrogen": 1, "Oxygen": 8, "Wood": None}
    plt.plot(x, y)
    plt.grid()
    plt.xlabel("Photon Energy, MeV")
    plt.ylabel("\u03BC \ \u03C1")
    plt.yscale('log')
    plt.xscale('log')
    plt.title(f"z = {d[el]}, {el}")
    plt.show()

# files from https://physics.nist.gov/PhysRefData/XrayMassCoef/tab3.html

filenames = ["carbon.txt", "hydrogen.txt", "oxygen.txt"]

for name in filenames:
    f = open(name, "r")
    for line in f:
        x = list(map(float,line.split()))
        if name=="carbon.txt":
            photon_energy.append(x[0])
            C.append(x[1])
        elif name=="hydrogen.txt":
            H.append(x[1])
        else:
            O.append(x[1])
f.close()

# make_plot(C, "Carbon")
# make_plot(H, "Hydrogen")
# make_plot(O, "Oxygen")

# Combining attenuation coefficients to calc ac for wood

C_prop = 0.458
H_prop =  0.00458
O_prop = 0.537

WOOD = [C_prop*i+O_prop*j+H_prop*k for (i,j,k) in zip(C, O, H)]
make_plot(WOOD, "Wood")

Fe_prop = 0.97
C_prop = 0.03


filenames = ["carbon.txt","iron.txt"]
Fe_energy = []
C_energy = []

Fe_val = []
C_val = []

f = open("carbon.txt","r")
for line in f:
    x = list(map(float,line.split()))
    C_energy.append(x[0])
    C_val.append(x[1])
f.close()

f = open("iron.txt","r")
for line in f:
    x = list(map(float,line.split()))
    if x[0] in C_energy:
        Fe_energy.append(x[0])
        Fe_val.append(x[1])
f.close()





