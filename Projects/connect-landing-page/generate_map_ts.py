
def generate_ts():
    with open('final_map_path.txt', 'r') as f:
        path_data = f.read().strip()
    
    content = f'export const WORLD_MAP_PATH = "{path_data}";\n'
    
    with open('app/data/worldMapPath.ts', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    generate_ts()
