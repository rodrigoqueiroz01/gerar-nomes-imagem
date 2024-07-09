import zipfile
import os
import shutil
import webbrowser

def zipar_imagem(image_path):
    base_dir, file_name = os.path.split(image_path)
    file_name_base = os.path.splitext(file_name)[0]
    zip_file_path = os.path.join(base_dir, f"{file_name_base}.zip")

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(image_path, file_name)

    return zip_file_path

def abrir_pasta_downloads():
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    webbrowser.open(downloads_dir)

if __name__ == "__main__":
    image_path = "../utils/images/output/intercessão.jpg"
    zip_file_path = zipar_imagem(image_path)
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    shutil.move(zip_file_path, downloads_dir)
    abrir_pasta_downloads()