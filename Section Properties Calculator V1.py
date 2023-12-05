import pandas as pd
from shapely.geometry import Polygon
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
from sectionproperties.analysis import Section
from sympy import symbols, Eq, solve

# Importing necessary libraries

# Load the Excel file containing section properties
df = pd.read_excel(r'C:\Users\joshu\Desktop\Section Properties Calculator\UC Bluebook.xlsx')

# Initialize basic plate dimensions and area
bp = 250  # Plate width in mm
tp = 10   # Plate thickness in mm
Ap = bp * tp  # Plate area in mm^2

standard_section_designation = '203 x 203 x 86'

fy = 355 # Steel grade in N/mm2

def get_section_properties_with_plate(standard_section_designation):
    # Function to calculate section properties with additional plate
    
    # Selecting the standard section from the DataFrame
    section_property = df[df['Section designation'] == standard_section_designation].iloc[0]
    
    # Defining dimensions of the standard section in mm
    h =  section_property['Depth of section h (mm)']
    bbot = section_property['Width of section b (mm)']
    btop = section_property['Width of section b (mm)']
    tfbot = section_property['Flange Thickness tf (mm)']
    tftop = section_property['Flange Thickness tf (mm)']
    tw = section_property['Web Thickness tw (mm)']
    hw = h - tfbot - tftop  # Web height

    # Calculating individual areas
    Aw = tw * hw
    Afbot = bbot * tfbot
    Aftop = btop * tftop
    A = Aftop + Afbot + Aw
    Atotal = A + Ap

    # Calculating offsets for the plate alignment
    offset_bot = (bbot - bp) / 2
    offset_top = (bbot - btop) / 2

    # Defining the shapes of section parts
    additional_plate = Polygon([
        (offset_bot, 0), (offset_bot + bp, 0), (offset_bot + bp, tp), (offset_bot, tp)])  
    bot_flange = Polygon([
        (0, tp), (bbot, tp), (bbot, tp + tfbot), (0, tp + tfbot)]) 
    web = Polygon([
        (bbot/2 - tw/2, tfbot + tp), (bbot/2 + tw/2, tfbot + tp),
        (bbot/2 + tw/2, tfbot + tp + hw), (bbot/2 - tw/2, tfbot + tp + hw)])  
    top_flange = Polygon([
        (offset_top, h - tftop), (offset_top + btop, h - tftop), 
        (offset_top + btop, h), (offset_top, h)])

    # Creating geometry objects
    geom_additional_plate = Geometry(geom=additional_plate)
    geom_bot_flange = Geometry(geom=bot_flange)
    geom_web = Geometry(geom=web)
    geom_top_flange = Geometry(geom=top_flange)


    # Assembling and meshing the compound geometry
    compound_geom = CompoundGeometry([geom_additional_plate, geom_bot_flange, geom_web, geom_top_flange])
    compound_geom.create_mesh(mesh_sizes=100)
    compound_geom.plot_geometry()

    # Creating the section and displaying mesh info
    section = Section(compound_geom)
    section.display_mesh_info()
    
    # Plotting the mesh
    section.plot_mesh(materials = False, title = f" FE Mesh - UC with additional {bp} x {tp}mm plate")

    # Calculating centroids and elastic neutral axis distances using first moment of area principles
    y_plate = tp / 2
    y_bot_flange = tp + tfbot / 2
    y_web = tp + tfbot + hw / 2
    y_top_flange = h - tftop / 2
    ybot = (Ap * y_plate + Afbot * y_bot_flange + Aw * y_web + Aftop * y_top_flange) / Atotal
    ytop = h - ybot
    y_max = max(ybot, ytop)

    # Calculating the second moment of area using parallel axis theorum and elastic modulus
    Ixx_plate_centre = (bp * tp**3) / 12
    Ixx_plate_body = Ixx_plate_centre + Ap * (ybot - tp/2)**2
    Ixx_bot_flange = (bbot * tfbot**3) / 12
    Ixx_bot_flange_body = Ixx_bot_flange + Afbot * (ybot - tp - tfbot/2)**2
    Ixx_web_centre = (tw * hw**3) / 12
    Ixx_web_body = Ixx_web_centre + Aw * (hw/2 + tftop - ytop)**2
    Ixx_top_flange = (btop * tftop**3) / 12
    Ixx_top_flange_body = Ixx_top_flange + Aftop * (ytop - tftop/2)**2
    Ixx_total_body = Ixx_plate_body + Ixx_bot_flange_body + Ixx_web_body + Ixx_top_flange_body 
    Wel_y = Ixx_total_body / y_max
    
    # Calculating the plastic neutral axis (PNA) by equating the tensile and compressive area (At = Ac)
    PNAtop = symbols('PNAtop')
    equation = Eq(Aftop + tw*(PNAtop - tftop), (Afbot + Ap) + tw *(h - PNAtop - tfbot - tp))
    solution = solve(equation, PNAtop)
    PNAtop_value = float(solution[0])
    PNAbot_value = h - PNAtop_value
    
    # Calculate the plastic modulus by taking moments about the plastic neutral axis
    Wpl_y = Aftop * (PNAtop_value - tftop/2) + tw * (PNAtop_value - tftop) * (PNAtop_value - tftop)/2 + (Afbot + Ap) * (PNAbot_value - (tfbot + tp)/2)+ (tw * (PNAbot_value - (tfbot + tp)) )* (PNAbot_value - (tfbot + tp))/2
    
    # Calculate the bending resistance of the section
    Mpl_rd = (Wpl_y * fy)/(1000000)
    
    # Printing results
    print(f"ybot = {ybot:.2f} mm")
    print(f"ytop = {ytop:.2f} mm")
    print(f"ymax = {y_max:.2f} mm")
    print(f"Second Moment of Area Ixx = {Ixx_total_body:.2f} mm4")
    print(f"Elastic Modulus Wel,y = {Wel_y:.2f} mm3")
    print(f"PNAtop = {PNAtop_value:.2f} mm")
    print(f"PNAbot = {PNAbot_value:.2f} mm")
    print(f"Plastic Modulus Wpl,y = {Wpl_y:.2f} mm3")
    print(f"Bending Resistance = {Mpl_rd:.2f} kNm")

get_section_properties_with_plate(standard_section_designation)