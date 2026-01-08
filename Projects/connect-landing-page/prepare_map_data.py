import xml.etree.ElementTree as ET
import sys

def process_map():
    tree = ET.parse('world_map_source.svg')
    root = tree.getroot()
    
    # Namespace handling
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Get viewBox
    viewbox = root.get('viewBox')
    print(f"Original ViewBox: {viewbox}")
    
    # Collect all path data
    all_d = []
    
    # Find all paths (handling namespace)
    for path in root.findall('.//svg:path', ns):
        d = path.get('d')
        if d:
            all_d.append(d)
            
    # Also look for paths without namespace if parse fails (sometimes ElementTree is strict/loose)
    if not all_d:
        for path in root.findall('.//path'):
            d = path.get('d')
            if d:
                all_d.append(d)
                
    # Join into one single string
    combined_d = " ".join(all_d)
    
    # Write to a file used for simple reading later
    with open('final_map_path.txt', 'w') as f:
        f.write(combined_d)
        
    print(f"Extracted {len(all_d)} paths.")
    print(f"Combined length: {len(combined_d)}")

if __name__ == "__main__":
    process_map()
