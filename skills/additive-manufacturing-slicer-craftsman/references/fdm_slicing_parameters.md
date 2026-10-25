# Référence des Paramètres de Tranchage FDM (ISO/ASTM 52910)

## 1. Températures & Vitesses Standards par Matériau

| Matériau | T° Buse (°C) | T° Plateau (°C) | Vitesse Périmètre (mm/s) | Remplissage Recommandé |
| :--- | :--- | :--- | :--- | :--- |
| **PLA** | 205 - 220 | 50 - 60 | 60 - 200 | 15-20% Gyroid |
| **PETG** | 230 - 250 | 70 - 85 | 40 - 100 | 20-30% Gyroid / Cubic |
| **ABS / ASA** | 240 - 260 | 95 - 110 | 40 - 80 (Enceinte fermée) | 25-40% Cubic |
| **TPU (Flexible)** | 220 - 240 | 40 - 50 | 20 - 40 (Direct drive) | 10-15% Gyroid |

## 2. Débit Volumétrique Maximal (Max Volumetric Speed)
Le débit volumétrique maximal $Q_{\max}$ d'une buse est défini par :
$$Q = v \times h \times w \le Q_{\max}$$
avec :
- $v$ : Vitesse linéaire de la buse ($\text{mm/s}$)
- $h$ : Hauteur de couche ($\text{mm}$)
- $w$ : Largeur d'extrusion ($\text{mm}$)

Pour un hotend standard (type V6), $Q_{\max} \approx 12 - 15\text{ mm}^3/\text{s}$. Pour un hotend High-Flow (type Volcano / Bambu), $Q_{\max} \approx 25 - 32\text{ mm}^3/\text{s}$.
