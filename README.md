# Section Properties Calculator

## Overview
This Python script is designed to assist structural engineers and students in evaluating the structural properties of steel I-beams with additional plate enhancements. It utilises the `sectionproperties` library to calculate key section properties, essential for the analysis and design of steel structural members.

## Features
- Imports structural section properties from the Excel file `UC Bluebook`. I have pre-processed the data from the "Steel for Life Bluebook" to facilitate extraction.
- Calculates the area of an additional plate and integrates it with a standard I-beam section.
- Generates a finite element mesh for the combined section.
- Determines centroidal axis, second moment of area, and plastic modulus.
- Computes the plastic neutral axis (PNA) and bending resistance, key for plastic design methodology.

## Dependencies
- `pandas`: For data manipulation and extraction from Excel files.
- `shapely`: For performing geometric operations.
- `sectionproperties`: For conducting finite element analysis and section property calculations.
- `sympy`: For solving algebraic equations to determine the PNA.

## Usage
Define the dimensions of the additional plate and specify the standard section designation. The script performs operations including filtering the section from the dataset, defining dimensions, calculating offsets for alignment, creating geometric objects, assembling the composite geometry, and calculating structural properties.

## Output
The script outputs the following calculated properties to the console:
- Centroidal distances from the top and bottom of the section.
- Maximum centroidal distance (y_max).
- Second moment of area about the x-axis (Ixx).
- Elastic modulus about the y-axis (Wel,y).
- Plastic neutral axis position (PNAtop and PNAbot).
- Plastic modulus about the y-axis (Wpl,y).
- Bending resistance (Mpl_rd).

A plot of the finite element mesh is also displayed to visualise the strengthened section's geometry.

## Assumptions
- The steel grade/material is consistent throughout the section.
- The script ignores the contribution of the root radius

## Future Development Ideas
- Integration of an interface for user input and interactive design changes.
- Expansion of the material library to include a variety of steel grades and composite materials.
- Incorporation of I-section libraries to improve accuracy.

## Acknowledgements
This project utilises the `section properties` library, developed by Robbie van Leeuwen, for the section property calculations. Appreciation is expressed to Robbie van Leeuwen and contributors for their work in developing this invaluable tool for the structural engineering community.

## How to Run
Ensure all dependencies are installed, set the `standard_section_designation` variable to the desired section size, and run the script in a Python environment. For detailed guidance, visit the official documentation of the `sectionproperties` library.

## License
This project is open-source and available under the MIT License.
