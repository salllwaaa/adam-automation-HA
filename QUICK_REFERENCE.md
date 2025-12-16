# Quick Reference Guide - Hassan Allam Inventory Automation

## 🚀 Quick Start (3 Steps)

1. **Place your files** in the project folder:
   - `New Availability.xlsx`
   - `The Current inv.xlsx`

2. **Run the script**:
   ```bash
   python main.py
   ```

3. **Check output** in `output/` folder

---

## 📋 Command Reference

### Run Main Script
```bash
cd "D:\Metrics\Adam\Automate Updating HA"
python main.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### View Logs
```bash
# Open latest log file in logs/ directory
notepad logs\processing_[latest].log
```

---

## 🔍 Project Identification

| Unit Code Pattern | Project Name |
|-------------------|--------------|
| PC1-... | Park Central - Mostakbal City |
| VAL-... / VALL-... | VAL: The Valleys |
| SLW-... | SLW: SwanLake West |

---

## 🎨 Finishing Rules Quick Reference

### Park Central & The Valleys
```
ALL → Fully Finished
```

### SLW (SwanLake West)
```
0100-0900 → Core and shell and near delivery
1000-1999 → Serviced Apartments
2000-2999 → Fully Finished
3000-7000 → Core and shell, 4 years delivery
8000+     → Fully Finished
```

---

## 📊 Column Mapping Cheat Sheet

| From | To | Example |
|------|-----|---------|
| UNIT CODE | default_code | PC1-A3-06-LA-21 |
| GROSS AREA | unit_area | 155.5 |
| SECOND | floor | 2nd |
| FIRST | floor | 1st |
| GROUND | floor | Ground |
| Three Bedrooms | number_of_rooms | 3 |
| Two Bedrooms | number_of_rooms | 2 |
| Price 10,000,000 | list_price | 10000000 |
| Price × 0.10 | maintenance_fee | 1000000 |

---

## 📁 File Locations

```
Project Root/
├── main.py              ← Run this
├── New Availability.xlsx ← Your input
├── The Current inv.xlsx  ← Your current data
├── output/              ← Generated files here
│   ├── Park_Central_New_Units_YYYYMMDD.xlsx
│   ├── The_Valleys_New_Units_YYYYMMDD.xlsx
│   └── SLW_New_Units_YYYYMMDD.xlsx
└── logs/                ← Processing logs here
    └── processing_YYYYMMDD_HHMMSS.log
```

---

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `config.py` | All mappings and rules |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |

---

## 🛠️ Troubleshooting

### Problem: No new units found
**Solution**: This is normal if all units already exist in current inventory

### Problem: Column not found
**Solution**: Check if Excel file has expected structure with "UNIT CODE" column

### Problem: Script won't run
**Solution**: 
```bash
# Install dependencies first
pip install pandas openpyxl
```

### Problem: Unicode errors
**Solution**: Already fixed - system uses ASCII characters only

---

## 📝 Output Columns (in order)

1. default_code
2. unit_area
3. finishing
4. floor
5. list_price
6. unit_npv
7. maintenance_fee
8. number_of_rooms
9. project
10. name

---

## 🔢 Examples

### Floor Conversion
```
GROUND → Ground
FIRST → 1st
SECOND → 2nd
THIRD → 3rd
FOURTH → 4th
```

### Bedroom Extraction
```
"APARTMENT-Three Bedrooms" → 3
"PENTHOUSE-Two Bedrooms" → 2
"DUPLEX-Four Bedrooms" → 4
```

### Name Generation
```
Input: 3BR Apartment, PC1-A3-06
Output: 3B Apartment in Park Central - Mostakbal City by Hassan Allam
```

### Finishing (SLW Examples)
```
Unit Code: SLW-0500-... → Core and shell and near delivery
Unit Code: SLW-1234-... → Serviced Apartments
Unit Code: SLW-2100-... → Fully Finished
Unit Code: SLW-5000-... → Core and shell, 4 years delivery
Unit Code: SLW-8200-... → Fully Finished
```

---

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Review `IMPLEMENTATION_SUMMARY.md` for technical details
3. Look at `SYSTEM_FLOW.md` for architecture diagrams
4. Check log files in `logs/` directory

---

## ✅ Pre-Flight Checklist

Before running:
- [ ] Both Excel files are in the project folder
- [ ] Files are closed (not open in Excel)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Python 3.8+ is installed

After running:
- [ ] Check console for success message
- [ ] Look in `output/` for generated files
- [ ] Review log file if any issues
- [ ] Import generated files to your system

---

## 🎯 Common Tasks

### Update Finishing Rules
Edit `utils/column_mapper.py` → `determine_finishing()` function

### Change Output Columns
Edit `config.py` → `OUTPUT_COLUMNS` list

### Modify Floor Mapping
Edit `config.py` → `FLOOR_MAPPING` dictionary

### Update Project Patterns
Edit `config.py` → `PROJECT_PATTERNS` dictionary

---

## 💡 Tips

1. **Always close Excel files** before running the script
2. **Check logs** if something seems wrong
3. **Backup your data** before running in production
4. **Test with sample data** first
5. **Keep file names consistent** (New Availability.xlsx, The Current inv.xlsx)

---

## 📈 Performance

- Processes ~120 units in ~5 seconds
- Handles multiple sheets automatically
- Skips empty/invalid rows gracefully
- Memory efficient for large files

---

## 🔐 Data Safety

- **No data modification**: Original files are never changed
- **Read-only access**: Only reads input files
- **New files only**: Creates new output files
- **Full logging**: Complete audit trail in logs

---

**Version**: 1.0  
**Last Updated**: December 16, 2025  
**Status**: Production Ready ✅

