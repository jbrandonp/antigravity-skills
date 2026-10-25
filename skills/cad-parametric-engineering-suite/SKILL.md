---
name: cad-parametric-engineering-suite
description: "Unified CAD/CAM and Parametric Engineering Master Suite for Autodesk Fusion and Dassault Systèmes SOLIDWORKS. Covers parametric feature modeling, timeline inspection, BOM/mass properties reports, CAM toolpaths, COM / Python API automation, and batch export (STEP, STL, DXF, PDF). Use ONLY for proprietary commercial CAD suites Autodesk Fusion and Dassault Systèmes SOLIDWORKS via Windows COM / desktop APIs. Do NOT use for Python CAD-as-Code (use build123d-ecip-cad-engineer instead) or 2D sketch constraint solving (use planegcs-sketch-solver instead)."
category: cad
risk: safe
tags: ["cad", "fusion-360", "solidworks", "parametric", "cam", "step", "com", "python-api"]
---

# Unified CAD & Parametric Engineering Master Suite

The definitive engineering playbook for parametric CAD modeling, timeline rebuilds, CAM toolpath verification, and batch file exports across **Autodesk Fusion** and **Dassault Systèmes SOLIDWORKS**.

---

## 🏛️ Architecture & Platform Matrix

| Platform | Automation Engine | Primary Workflows | Key Formats |
| :--- | :--- | :--- | :--- |
| **Autodesk Fusion** | In-process Python (`adsk.core`, `adsk.fusion`, `adsk.cam`) | Parametric timelines, user parameters, cloud hub sync, CAM toolpath review | `.step`, `.stp`, `.stl`, `.f3d` |
| **SOLIDWORKS** | Windows COM (`SldWorks.Application`), VBA macros, Document Manager | Rebuild diagnostics (Ctrl+Q), assembly mates, configurations, drawing exports | `.step`, `.sldprt`, `.sldasm`, `.dxf`, `.pdf` |

---

## 📐 Section 1: Autodesk Fusion Automation

### Engine Architecture
Autodesk Fusion runs in-process Python 3.x. Claude/Antigravity acts as CAD/CAM automation specialist:
1. **User Parameters**: Always drive dimensions via `design.userParameters` — never hardcode magic values.
2. **Export Pipeline**: `exportManager.createSTEPExportOptions` / STL with deterministic `meshRefinement`.
3. **Timeline Diagnostics**: Review red compute warnings and repair broken sketch projections before reordering features.
4. **CAM Verification**: Validate stock, tool diameter, minimum cutting radius, and simulate G-code post (`.cps`).

```python
import adsk.core, adsk.fusion

def run(context):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if not design:
        raise RuntimeError("Active product is not a Fusion design")
    export_mgr = design.exportManager
    file = adsk.core.FileDialog.create()
    file.filter = "STEP (*.stp)"
    if file.showSave() == adsk.core.DialogResults.DialogOK:
        opts = export_mgr.createSTEPExportOptions(file.filename)
        opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
        export_mgr.execute(opts)
```

---

## ⚙️ Section 2: Dassault Systèmes SOLIDWORKS Automation

### COM Architecture & Directives
1. **COM Lifecycle**: `win32com.client.Dispatch("SldWorks.Application")`. Set `Visible = False` in batch pipelines.
2. **Rebuild Truth**: Always invoke **Ctrl+Q** full rebuild (`model.ForceRebuild3(True)`), not Ctrl+B.
3. **Export Integrity**: Always read `errors` and `warnings` byref VARIANTs from `SaveAs3` / `ExportToFile2`.
4. **Units**: SOLIDWORKS API defaults to meters for mass properties — convert to mm/kg for reports.

```python
import win32com.client
from win32com.client import VARIANT
import pythoncom

def export_solidworks_step(path: str) -> None:
    pythoncom.CoInitialize()
    sw = win32com.client.Dispatch("SldWorks.Application")
    model = sw.ActiveDoc
    if model is None:
        raise RuntimeError("No active document in SOLIDWORKS")
    ext = model.Extension
    errors = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    warnings = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    ok = ext.SaveAs3(path, 0, 2, None, None, errors, warnings)
    if not ok or errors.value != 0:
        raise RuntimeError(f"SOLIDWORKS SaveAs failed: err={errors.value} warn={warnings.value}")
```

---

## 🛠️ Verification & Deterministic Tooling

```bash
# Validate exported CAD STEP geometry integrity
python scripts/validate_cad_step.py --file part_export.step
```
