import os


def main() -> None:

    to_populate = []
    
    current_path = os.path.dirname(os.path.abspath(__file__))
    if not current_path.endswith("backend"):
        print("Please run this script from the backend directory")
        return
    
    subdirectories = [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]

    for subdirectory in subdirectories:
        if "fixtures" in os.listdir(os.path.join(current_path, subdirectory)):
            for file in os.listdir(os.path.join(current_path, subdirectory, "fixtures")):
                if file.endswith(".json") and file != "__init__.py":
                    to_populate.append(f"{file[:-5]}")

    command = f"python ./manage.py loaddata {' '.join(to_populate)}"                
    os.system(command)
            
if __name__ == "__main__":
    main()