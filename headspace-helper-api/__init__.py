import os
import logging

root_dir = os.path.dirname(os.path.abspath(__file__))


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(root_dir + '/headspace-helper-api.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


# The specified cells are referenced to sheet "solvent 1" and need to be programmatically added to every solvent sheet.
cells_with_reference = [
    "I5", "I6", "I7", "I8", "I9", "I10", "I11", "I12", "M21",  # Only for sheet "Analytical report"
    "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16",  # 0. Project information
    "A22", "B22", "C22", "D22",  # 1. Diluent
    "A38", "B38", "C38", "D38",  # 4. Diluted stock solution
    "A43", "A44", "A45", "A46", "A47", "A48", "A49", "A50", "A51", "A52", "A53", "A54",  # 5. Blanks
    "A62", "A63", "A64", "A65", "A66", "A67", "A68", "A69", "A70", "A71", "A72", "A73",
    # 6. Calibration curve - Standard name
    "B62", "B63", "B64", "B65", "B66", "B67", "B68", "B69", "B70", "B71", "B72", "B73",  # 6. Calibration curve - V (uL)
    "C62", "C63", "C64", "C65", "C66", "C67", "C68", "C69", "C70", "C71", "C72", "C73",
    # 6. Calibration curve - From Stock
    "D62", "D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73",
    # 6. Calibration curve - V added (mL)
    "B78",  # Noise
    "A84", "B84", "C84", "D84",  # Repeatability and control
    "A95", "A96", "A97", "A98", "A99",  # Bracketing control - Control name
    "B95", "B96", "B97", "B98", "B99",  # Bracketing control - Bracket
    "C95", "C96", "C97", "C98", "C99",  # Bracketing control - V (uL)
    "D95", "D96", "D97", "D98", "D99",  # Bracketing control - From Stock
    "E95", "E96", "E97", "E98", "E99",  # Bracketing control - V added (mL)
    "A104", "A105", "A111", "A117", "A123", "A129",  # 9. Sample(s) - Sample name
    "B105", "B111", "B117", "B123", "B129",  # 9. Sample(s) - Bracket
    "C105", "C106", "C107", "C108", "C109", "C110", "C111", "C112", "C113", "C114", "C115", "C116", "C117",
    "C118", "C119", "C120", "C121", "C122", "C123", "C124", "C125", "C126", "C127", "C128", "C129", "C130",
    "C131", "C132", "C133", "C134",  # 9. Sample(s) - Tag
    "D105", "D106", "D107", "D108", "D109", "D110", "D111", "D112", "D113", "D114", "D115", "D116", "D117",
    "D118", "D119", "D120", "D121", "D122", "D123", "D124", "D125", "D126", "D127", "D128", "D129", "D130",
    "D131", "D132", "D133", "D134",  # 9. Sample(s) - Weight (mg)
    "E105", "E108", "E109", "E110", "E111", "E114", "E115", "E116", "E117", "E120", "E121", "E122", "E123",
    "E126", "E127", "E128", "E129", "E132", "E133", "E134",  # 9. Sample(s) - V pip (uL)
    "F105", "F108", "F109", "F110", "F111", "F114", "F115", "F116", "F117", "F120", "F121", "F122", "F123",
    "F126", "F127", "F128", "F129", "F132", "F133", "F134",  # 9. Sample(s) - From (Stock)
    "G105", "G106", "G107", "G108", "G109", "G110", "G111", "G112", "G113", "G114", "G115", "G116", "G117",
    "G118", "G119", "G120", "G121", "G122", "G123", "G124", "G125", "G126", "G127", "G128", "G129", "G130",
    "G131", "G132", "G133", "G134",  # 9. Sample(s) - V diluent (mL)
    "H105", "H106", "H107", "H108", "H109", "H110", "H111", "H112", "H113", "H114", "H115", "H116", "H117",
    "H118", "H119", "H120", "H121", "H122", "H123", "H124", "H125", "H126", "H127", "H128", "H129", "H130",
    "H131", "H132", "H133", "H134",  # 9. Sample(s) - Sample Conc. (mg/mL)
    "M108", "M109", "M110", "M114", "M115", "M116", "M120", "M121", "M122", "M126", "M127", "M128", "M132",
    "M133", "M134",  # 9. Sample(s) - Nom Spiked Conc (ug/mL)
    "K105", "K111", "K117", "K123", "K129",
    "L105", "L111", "L117", "L123", "L129",
    "M105", "M111", "M117", "M123", "M129",
    "N105", "N111", "N117", "N123", "N129",
    "O105", "O111", "O117", "O123", "O129",
    "P108", "P114", "P120", "P126", "P132",
    "Q108", "Q114", "Q120", "Q126", "Q132",
    "R108", "R114", "R120", "R126", "R132",
    "S108", "S114", "S120", "S126", "S132",
    "U108", "U114", "U120", "U126", "U132",
]
